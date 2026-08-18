#!/usr/bin/env node
/** Development parser for the language-neutral Engram front-matter corpus. */
const fs = require('fs');

class ParseError extends Error {
  constructor(code, message) { super(message); this.code = code; }
}

function stripComment(value) {
  let quote = null;
  for (let i = 0; i < value.length; i++) {
    const ch = value[i];
    if (quote === '"' && ch === '\\') { i++; continue; }
    if (quote && ch === quote) { quote = null; continue; }
    if (!quote && (ch === '"' || ch === "'")) { quote = ch; continue; }
    if (!quote && ch === '#' && (i === 0 || /\s/.test(value[i - 1]))) return value.slice(0, i).trimEnd();
  }
  return value.trimEnd();
}

function findColon(value) {
  let quote = null;
  for (let i = 0; i < value.length; i++) {
    const ch = value[i];
    if (quote === '"' && ch === '\\') { i++; continue; }
    if (quote && ch === quote) { quote = null; continue; }
    if (!quote && (ch === '"' || ch === "'")) { quote = ch; continue; }
    if (!quote && ch === ':' && (i + 1 === value.length || /\s/.test(value[i + 1]))) return i;
  }
  return -1;
}

function forbiddenFeature(front) {
  for (const original of front.split(/\r?\n/)) {
    const trimmed = original.trim();
    if (trimmed.startsWith('%') || trimmed === '...' || /^<<\s*:/.test(trimmed)) return true;
    let quote = null;
    for (let i = 0; i < original.length; i++) {
      const ch = original[i];
      if (quote === '"' && ch === '\\') { i++; continue; }
      if (quote && ch === quote) { quote = null; continue; }
      if (!quote && (ch === '"' || ch === "'")) { quote = ch; continue; }
      if (!quote && ch === '#') break;
      if (!quote && '[]{}'.includes(ch)) return true;
      if (!quote && '&*!'.includes(ch) && (i === 0 || /[\s:\-]/.test(original[i - 1]))) return true;
    }
  }
  return false;
}

function scalar(token) {
  const value = token.trim();
  if (value === '') return null;
  if (value.startsWith('"')) {
    if (!value.endsWith('"')) throw new ParseError('yaml-invalid', 'unterminated double-quoted scalar');
    try { return JSON.parse(value); } catch (error) { throw new ParseError('yaml-invalid', error.message); }
  }
  if (value.startsWith("'")) {
    if (!value.endsWith("'")) throw new ParseError('yaml-invalid', 'unterminated single-quoted scalar');
    return value.slice(1, -1).replace(/''/g, "'");
  }
  if (value === 'null') return null;
  if (value === 'true') return true;
  if (value === 'false') return false;
  if (/^-?(?:0|[1-9][0-9]*)$/.test(value)) return Number(value);
  if (/^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+(?:[eE][+-]?[0-9]+)?|[eE][+-]?[0-9]+)$/.test(value)) {
    const number = Number(value);
    if (!Number.isFinite(number)) throw new ParseError('yaml-invalid', 'number must be finite');
    return number;
  }
  return value;
}

function parseKey(token) {
  const value = scalar(token);
  if (typeof value !== 'string') throw new ParseError('yaml-non-string-key', 'front-matter mapping keys must be strings');
  if (value === '<<') throw new ParseError('yaml-forbidden-feature', 'YAML merge keys are not permitted');
  return value;
}

function parseBlock(lines, start, indent) {
  if (start >= lines.length || lines[start].indent !== indent) throw new ParseError('yaml-invalid', 'invalid indentation');
  return lines[start].content === '-' || lines[start].content.startsWith('- ')
    ? parseSequence(lines, start, indent)
    : parseMapping(lines, start, indent);
}

function parseMapping(lines, start, indent) {
  const result = {};
  let index = start;
  while (index < lines.length && lines[index].indent === indent && !(lines[index].content === '-' || lines[index].content.startsWith('- '))) {
    const entry = lines[index].content;
    const colon = findColon(entry);
    if (colon < 0) throw new ParseError('yaml-invalid', `mapping entry lacks colon: ${entry}`);
    const key = parseKey(entry.slice(0, colon).trim());
    if (Object.prototype.hasOwnProperty.call(result, key)) throw new ParseError('yaml-duplicate-key', `duplicate YAML key ${JSON.stringify(key)}`);
    const remainder = entry.slice(colon + 1).trim();
    index++;
    if (remainder !== '') {
      result[key] = scalar(remainder);
    } else if (index < lines.length && lines[index].indent > indent) {
      const parsed = parseBlock(lines, index, lines[index].indent);
      result[key] = parsed.value; index = parsed.next;
    } else {
      result[key] = '';
    }
    if (index < lines.length && lines[index].indent > indent) throw new ParseError('yaml-invalid', 'unexpected indentation');
  }
  return {value: result, next: index};
}

function parseSequence(lines, start, indent) {
  const result = [];
  let index = start;
  while (index < lines.length && lines[index].indent === indent && (lines[index].content === '-' || lines[index].content.startsWith('- '))) {
    const remainder = lines[index].content.slice(1).trim();
    index++;
    if (remainder === '') {
      if (index < lines.length && lines[index].indent > indent) {
        const parsed = parseBlock(lines, index, lines[index].indent);
        result.push(parsed.value); index = parsed.next;
      } else result.push(null);
    } else if (findColon(remainder) >= 0) {
      const childIndent = indent + 2;
      let end = index;
      while (end < lines.length && lines[end].indent > indent) end++;
      const synthetic = [{indent: childIndent, content: remainder}, ...lines.slice(index, end)];
      const parsed = parseMapping(synthetic, 0, childIndent);
      if (parsed.next !== synthetic.length) throw new ParseError('yaml-invalid', 'invalid sequence mapping indentation');
      result.push(parsed.value); index = end;
    } else {
      result.push(scalar(remainder));
      if (index < lines.length && lines[index].indent > indent) throw new ParseError('yaml-invalid', 'unexpected indentation after sequence scalar');
    }
  }
  return {value: result, next: index};
}

function parseRecord(file, maxRecordBytes) {
  const raw = fs.readFileSync(file);
  if (raw.length > maxRecordBytes) throw new ParseError('resource-limit', 'record exceeds max_record_bytes');
  if (raw.length >= 3 && raw[0] === 0xef && raw[1] === 0xbb && raw[2] === 0xbf) throw new ParseError('bom-not-allowed', 'UTF-8 byte-order mark is not permitted');
  let text;
  try { text = new TextDecoder('utf-8', {fatal: true}).decode(raw); }
  catch (error) { throw new ParseError('encoding-invalid', error.message); }
  if (/\r(?!\n)/.test(text)) throw new ParseError('line-ending-invalid', 'bare CR line ending is not permitted');
  const physical = text.split(/\r?\n/);
  if (physical[0] !== '---') throw new ParseError('delimiter-invalid', 'opening delimiter must be the first exact line');
  const closing = physical.indexOf('---', 1);
  if (closing < 0) throw new ParseError('delimiter-invalid', 'missing exact closing delimiter');
  const front = physical.slice(1, closing).join('\n');
  if (forbiddenFeature(front)) throw new ParseError('yaml-forbidden-feature', 'forbidden YAML feature');
  const lines = [];
  for (const original of front.split('\n')) {
    if (/^ *\t/.test(original)) throw new ParseError('yaml-invalid', 'tabs cannot be used for indentation');
    const content = stripComment(original.slice(original.match(/^ */)[0].length));
    if (content.trim() === '') continue;
    lines.push({indent: original.match(/^ */)[0].length, content});
  }
  if (lines.length === 0) throw new ParseError('front-matter-not-mapping', 'front matter must be a mapping');
  const parsed = parseBlock(lines, 0, lines[0].indent);
  if (parsed.next !== lines.length) throw new ParseError('yaml-invalid', 'unconsumed YAML content');
  if (Array.isArray(parsed.value) || parsed.value === null || typeof parsed.value !== 'object') throw new ParseError('front-matter-not-mapping', 'front matter must be a mapping');
  return parsed.value;
}

function main() {
  if (process.argv.length !== 4 || process.argv[2] !== 'parse') {
    process.stderr.write('usage: frontmatter-parser.js parse REQUEST.json\n'); process.exit(2);
  }
  const request = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
  const base = {protocol_version: '1.0', case_id: request.case_id};
  let result;
  try {
    result = {...base, outcome: 'accepted', front_matter: parseRecord(request.record, Number(request.max_record_bytes || 1048576))};
  } catch (error) {
    if (!(error instanceof ParseError)) throw error;
    result = {...base, outcome: 'rejected', diagnostic: {code: error.code, message: error.message}};
  }
  process.stdout.write(JSON.stringify(result) + '\n');
}

main();
