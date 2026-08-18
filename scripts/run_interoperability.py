#!/usr/bin/env python3
"""Reproduce the 1.0 two-implementation exchange evidence."""
import hashlib, json, shutil, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; BASE=ROOT/'docs/interoperability/1.0/artifacts'
ADAPTERS={'python':[str(ROOT/'implementations/python-engram/engram_adapter.py')], 'node':[str(ROOT/'implementations/node-engram/engram-adapter.js')]}

def invoke(name, operation, source, output, case):
    output.mkdir(parents=True,exist_ok=True); request=output/'request.json'; artifact=output/'adapter-artifacts'; artifact.mkdir()
    request.write_text(json.dumps({'protocol_version':'1.0','case_id':case,'operation':operation,'fixture':str(source.resolve()),'artifact_directory':str(artifact.resolve()),'parameters':{'edits':[]},'supported_profiles':['core','graph','media','action']},indent=2)+'\n')
    result=subprocess.run(ADAPTERS[name]+[operation,str(request)],check=True,text=True,capture_output=True)
    parsed=json.loads(result.stdout); (output/'result.json').write_text(json.dumps(parsed,indent=2)+'\n'); return artifact/'package'

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def jsons(package): return {str(p.relative_to(package)):json.loads(p.read_text()) for p in package.rglob('*.json')}
def snapshot(package):
    manifest=json.loads((package/'engram.json').read_text()); graph=next((v for k,v in jsons(package).items() if k.startswith('graphs/')),None)
    markdown={str(p.relative_to(package)):digest(p) for p in package.rglob('*.md')}
    attachments={o['id']:{'descriptor':json.loads((package/o['path']).read_text()) if o['kind']=='attachment' else None,
              'payload_sha256':digest(package/o['path']) if o['kind']=='blob' else None} for o in manifest['objects'] if o['kind'] in ('attachment','blob')}
    all_json=jsons(package)
    def values(key,obj):
        found=[]
        if isinstance(obj,dict):
            for k,v in obj.items():
                if k==key: found.append(v)
                found.extend(values(key,v))
        elif isinstance(obj,list):
            for v in obj: found.extend(values(key,v))
        return found
    return {'engram_id':manifest.get('engram_id'),'package_id':manifest['id'],'object_id_kinds':[[o['id'],o['kind']] for o in manifest['objects']],
      'profiles':manifest['profiles'],'markdown_sha256':markdown,
      'graph_topology':{'nodes':[[n['id'],n.get('record')] for n in graph['nodes']], 'edges':[[e['id'],e['from'],e['to'],e['relation']] for e in graph['edges']]} if graph else None,
      'attachments':attachments,'extensions':values('extensions',all_json),'reference_scopes':values('scope',all_json)}

def compare(label,left,right):
    a,b=snapshot(left),snapshot(right); fields={k:a[k]==b[k] for k in a}; semantic=all(fields.values())
    byte_differences=[]
    for p in sorted(set(x.relative_to(left) for x in left.rglob('*') if x.is_file()) & set(x.relative_to(right) for x in right.rglob('*') if x.is_file())):
        if (left/p).read_bytes() != (right/p).read_bytes(): byte_differences.append(str(p))
    return {'exchange':label,'semantic_equal':semantic,'comparisons':fields,'intentional_serialization_differences':byte_differences,
            'semantic_or_normative_content_loss':[] if semantic else [k for k,v in fields.items() if not v]}

def main():
    if BASE.exists(): shutil.rmtree(BASE)
    for d in ('python','node','exchange'): (BASE/d).mkdir(parents=True)
    source=ROOT/'examples/basic-engram'
    py=invoke('python','produce',source,BASE/'python','PY-PRODUCE-BASIC'); node=invoke('node','produce',source,BASE/'node','NODE-PRODUCE-BASIC')
    node_from_py=invoke('node','round-trip',py,BASE/'exchange/node-import-python','NODE-IMPORT-PYTHON')
    py_from_node=invoke('python','round-trip',node,BASE/'exchange/python-import-node','PYTHON-IMPORT-NODE')
    report={'report_version':'1.0','source':'examples/basic-engram','comparisons':[compare('Python producer -> Node consumer/producer',py,node_from_py),compare('Node producer -> Python consumer/producer',node,py_from_node)]}
    (BASE/'exchange/comparison.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__': main()
