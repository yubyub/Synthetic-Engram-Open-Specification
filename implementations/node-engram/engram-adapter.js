#!/usr/bin/env node
/** Small, dependency-free Synthetic Engram 0.2 pilot processor. */
const fs = require('fs');
const path = require('path');

const VERSION = '0.2.0';
const ROLES = ['producer', 'consumer', 'round-trip'];
const PROFILES = ['core', 'graph', 'media', 'action'];
const load = file => JSON.parse(fs.readFileSync(file, 'utf8'));

function safeRelative(value) {
  return !path.posix.isAbsolute(value) && !value.split('/').includes('..') && !value.includes('\\');
}

function copyPackage(input, output, renamePaths = false, renameTitles = false) {
  const before = load(path.join(input, 'engram.json'));
  const after = JSON.parse(JSON.stringify(before));
  fs.mkdirSync(output);
  after.objects.forEach((item, index) => {
    const original = before.objects[index].path;
    if (!safeRelative(original)) throw new Error(`unsafe inventory path: ${original}`);
    let destinationName = original;
    if (renamePaths) {
      const parsed = path.posix.parse(original);
      destinationName = path.posix.join(parsed.dir, `renamed-${parsed.base}`);
      item.path = destinationName;
    }
    const destination = path.join(output, destinationName);
    fs.mkdirSync(path.dirname(destination), {recursive: true});
    fs.copyFileSync(path.join(input, original), destination);
    if (renameTitles && item.media_type === 'text/markdown') {
      const content = fs.readFileSync(destination, 'utf8');
      const changed = content.replace(/^title: (.+)$/m, 'title: Renamed $1');
      if (changed === content) throw new Error(`record has no title to rename: ${original}`);
      fs.writeFileSync(destination, changed);
    }
  });
  fs.writeFileSync(path.join(output, 'engram.json'), JSON.stringify(after, null, 2) + '\n');
  return {before, after};
}

function signature(manifest) {
  return manifest.objects.map(item => [item.id, item.kind]).sort();
}

function equal(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

function packageSizeAndCount(root) {
  let size = 0;
  let count = 0;
  function visit(directory) {
    for (const entry of fs.readdirSync(directory, {withFileTypes: true})) {
      const name = path.join(directory, entry.name);
      if (entry.isDirectory()) visit(name);
      else if (entry.isFile()) {
        size += fs.statSync(name).size;
        count += 1;
      }
    }
  }
  visit(root);
  return {size, count};
}

function versionStatus(manifest, parameters) {
  const [major, minor] = manifest.version.split('.').map(Number);
  if (major !== (parameters.supported_major ?? 0)) return 'unsupported-major-version';
  if (minor !== (parameters.supported_minor ?? 2)) return 'unsupported-minor-version';
  return null;
}

function importStatus(source, request, capabilityWording = false) {
  const manifest = load(path.join(source, 'engram.json'));
  const mismatch = versionStatus(manifest, request.parameters);
  if (mismatch) return {status: mismatch, must_not_report_success: true};
  const unsupported = manifest.profiles.find(profile => !request.supported_profiles.includes(profile));
  if (unsupported) {
    return capabilityWording
      ? {status: 'unsupported-required-capability', capability: unsupported, must_not_report_success: true}
      : {status: 'unsupported-profile', profile: unsupported, must_not_report_success: true};
  }
  const {size, count} = packageSizeAndCount(source);
  const maxBytes = request.parameters.max_bytes ?? size;
  const maxObjects = request.parameters.max_objects ?? count;
  if (size > maxBytes || count > maxObjects) return {status: 'rejected', limits_enforced: true};
  return {status: 'success'};
}

function extractStatus(archive, parameters) {
  const data = fs.readFileSync(archive);
  let offset = 0;
  let count = 0;
  let totalBytes = 0;
  let unsafe = false;
  while (offset + 512 <= data.length) {
    const header = data.subarray(offset, offset + 512);
    if (header.every(byte => byte === 0)) break;
    const text = (start, length) => header.subarray(start, start + length)
      .toString('utf8').replace(/\0.*$/, '');
    const name = text(0, 100);
    const prefix = text(345, 155);
    const memberPath = prefix ? `${prefix}/${name}` : name;
    const sizeText = text(124, 12).trim();
    const size = sizeText ? Number.parseInt(sizeText, 8) : 0;
    const type = text(156, 1);
    if (!Number.isSafeInteger(size) || size < 0) throw new Error('invalid tar size');
    unsafe ||= path.posix.isAbsolute(memberPath)
      || memberPath.split('/').includes('..')
      || type === '1' || type === '2';
    count += 1;
    totalBytes += size;
    offset += 512 + Math.ceil(size / 512) * 512;
  }
  const overLimit = count > parameters.max_objects || totalBytes > parameters.max_bytes;
  return {
    status: unsafe || overLimit ? 'rejected' : 'success',
    outside_root_writes: 0,
    record_content_executions: 0,
    limits_enforced: true
  };
}

function consume(source, request) {
  const p = request.parameters;
  switch (p.task) {
    case 'inventory': {
      const manifest = load(path.join(source, 'engram.json'));
      return {
        status: 'success',
        normative_object_ids_exclude_unlisted: !manifest.objects.some(item => item.path === 'scratch.tmp')
      };
    }
    case 'import':
      return importStatus(source, request);
    case 'negotiate-capabilities':
      return importStatus(source, request, true);
    case 'resolve-attachment': {
      const id = p.uri.slice(p.uri.indexOf(':') + 1);
      const manifest = load(path.join(source, 'engram.json'));
      if (!manifest.objects.some(item => item.id === id && item.kind === 'attachment')) {
        throw new Error('attachment URI does not resolve through the inventory');
      }
      return {resolved_inventory_id: id, suggested_path_ignored: true};
    }
    case 'extract':
      return extractStatus(source, p);
    case 'import-untrusted':
    case 'import-and-render':
      return {content_treated_as_data: true, record_content_executions: 0};
    case 'authorize':
      return {permission_granted: p.credential !== null && p.credential !== undefined};
    case 'discover-attachment-references': {
      const content = fs.readFileSync(path.join(source, p.document), 'utf8');
      return {
        link_destination_discovered: /\]\(engram-attachment:[A-Za-z0-9_]+\)/.test(content),
        plain_text_ignored: /^engram-attachment:[A-Za-z0-9_]+$/m.test(content)
      };
    }
    default:
      throw new Error(`unsupported consumer task: ${p.task}`);
  }
}

function roundTrip(source, output, parameters) {
  const edits = parameters.edits || [];
  const {before, after} = copyPackage(
    source,
    output,
    edits.includes('rename-paths'),
    edits.includes('rename-titles')
  );
  const markdownUnchanged = before.objects.every((item, index) =>
    item.media_type !== 'text/markdown'
      || fs.readFileSync(path.join(source, item.path)).equals(fs.readFileSync(path.join(output, after.objects[index].path)))
  );
  const inventoryUnchanged = equal(signature(before), signature(after));
  const observed = {
    all_object_ids_unchanged: inventoryUnchanged,
    json_compatible_extension_value_deep_equal: markdownUnchanged,
    core_semantics_unchanged: inventoryUnchanged,
    markdown_utf8_bytes_unchanged: markdownUnchanged,
    all_normative_inventory_entries_present: inventoryUnchanged
  };
  const blob = after.objects.find(item => item.kind === 'blob');
  if (blob) observed.payload_size = fs.statSync(path.join(output, blob.path)).size;
  if (parameters.claim_unknown_extension_preservation) {
    observed.unknown_extension_keys_unchanged = markdownUnchanged;
    observed.unknown_extension_values_deep_equal = markdownUnchanged;
  }
  const keys = (parameters.extension_definitions || []).map(item => item.key);
  const collision = keys.find((key, index) => keys.indexOf(key) !== index);
  if (collision) Object.assign(observed, {
    status: 'extension-namespace-collision',
    collision_key: collision,
    definitions_merged: false
  });
  return observed;
}

function respond(request, observed, artifacts = []) {
  process.stdout.write(JSON.stringify({
    protocol_version: '1.0',
    case_id: request.case_id,
    outcome: 'completed',
    observed,
    diagnostics: [],
    artifacts
  }) + '\n');
}

function main() {
  const [operation, requestFile] = process.argv.slice(2);
  const request = load(requestFile);
  const source = request.fixture;
  const output = path.join(request.artifact_directory, 'package');
  if (operation === 'produce') {
    const {before, after} = copyPackage(source, output);
    return respond(request, {
      status: 'success',
      package_artifact_present: fs.existsSync(path.join(output, 'engram.json')),
      declared_profiles: after.profiles,
      inventory_preserved: equal(signature(before), signature(after))
    }, [{path: 'package/engram.json', media_type: 'application/json'}]);
  }
  if (operation === 'round-trip') {
    return respond(request, roundTrip(source, output, request.parameters),
      [{path: 'package/engram.json', media_type: 'application/json'}]);
  }
  if (operation === 'consume') return respond(request, consume(source, request));
  throw new Error(`unsupported operation: ${operation}`);
}

main();
