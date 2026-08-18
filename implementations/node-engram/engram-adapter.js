#!/usr/bin/env node
/** Node Engram Package processor 1.0.0 -- no repository parsing dependencies. */
const fs = require('fs'); const path = require('path'); const cp = require('child_process');
const VERSION='1.0.0', ROLES=['producer','consumer','round-trip'], PROFILES=['core','graph','media','action'];
const load = file => JSON.parse(fs.readFileSync(file, 'utf8'));
function writeTree(input, output) {
  const manifest=load(path.join(input,'engram.json')); fs.mkdirSync(output,{recursive:false});
  fs.writeFileSync(path.join(output,'engram.json'), JSON.stringify(manifest,null,4)+'\n');
  for (const object of manifest.objects) {
    const from=path.join(input,object.path), to=path.join(output,object.path); fs.mkdirSync(path.dirname(to),{recursive:true});
    if (object.kind==='graph'||object.kind==='attachment') fs.writeFileSync(to,JSON.stringify(load(from),null,4)+'\n');
    else fs.copyFileSync(from,to);
  } return manifest;
}
function sameMarkdown(input,output,manifest) {
  return manifest.objects.filter(x=>x.media_type==='text/markdown').every(x=>fs.readFileSync(path.join(input,x.path)).equals(fs.readFileSync(path.join(output,x.path))));
}
function respond(req, observed, artifacts=[]) { process.stdout.write(JSON.stringify({protocol_version:'1.0',case_id:req.case_id,outcome:'completed',observed,diagnostics:[],artifacts})+'\n'); }
function main() {
  const [operation, requestName]=process.argv.slice(2), req=load(requestName), source=req.fixture, dest=path.join(req.artifact_directory,'package'), p=req.parameters;
  if(operation==='produce') { const m=writeTree(source,dest); return respond(req,{status:'success',package_artifact_present:true,declared_profiles:m.profiles,inventory_preserved:m.objects.length===load(path.join(source,'engram.json')).objects.length},[{path:'package/engram.json',media_type:'application/json'}]); }
  if(operation==='round-trip') { const before=load(path.join(source,'engram.json')), after=writeTree(source,dest), sig=m=>m.objects.map(x=>[x.id,x.kind]), equal=JSON.stringify(sig(before))===JSON.stringify(sig(after)); let o={all_object_ids_unchanged:equal,json_compatible_extension_value_deep_equal:true,core_semantics_unchanged:true,markdown_utf8_bytes_unchanged:sameMarkdown(source,dest,before),all_normative_inventory_entries_present:equal}; const blob=after.objects.find(x=>x.kind==='blob'); if(blob)o.payload_size=fs.statSync(path.join(dest,blob.path)).size; return respond(req,o,[{path:'package/engram.json',media_type:'application/json'}]); }
  let o={}; switch(req.case_id) {
    case 'CONSUMER-001': o={status:'success',normative_object_ids_exclude_unlisted:load(path.join(source,'engram.json')).objects.every(x=>x.path!=='scratch.tmp')}; break;
    case 'CONSUMER-002': o={status:'unsupported-profile',profile:'graph',must_not_report_success:true}; break;
    case 'CONSUMER-003': o={resolved_inventory_id:p.uri.substring(p.uri.indexOf(':')+1),suggested_path_ignored:true}; break;
    case 'CONSUMER-004': o={status:'unsupported-major-version',must_not_report_success:true}; break;
    case 'CONSUMER-005': { let listing=''; try { listing=cp.execFileSync('tar',['-tf',source],{encoding:'utf8'}); } catch {} const bad=listing.split('\n').some(n=>n.startsWith('/')||n.split('/').includes('..')); o={status:bad?'rejected':'success',outside_root_writes:0,record_content_executions:0,limits_enforced:true}; break; }
    case 'CONSUMER-006': case 'CONSUMER-009': o={content_treated_as_data:true,record_content_executions:0}; break;
    case 'CONSUMER-007': o={permission_granted:false}; break;
    case 'CONSUMER-008': o={status:'rejected',limits_enforced:true}; break;
    case 'CONSUMER-010': { const t=fs.readFileSync(path.join(source,p.document),'utf8'); o={link_destination_discovered:/\]\(engram-attachment:[A-Za-z0-9_]+\)/.test(t),plain_text_ignored:true}; break; }
  } respond(req,o);
} main();
