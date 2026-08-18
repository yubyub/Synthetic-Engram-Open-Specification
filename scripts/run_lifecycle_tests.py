#!/usr/bin/env python3
"""Compare Python and Node against the non-normative lifecycle vectors."""
import json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MODELS={"python":[sys.executable,str(ROOT/'implementations/python-engram/lifecycle_model.py')],"node":["node",str(ROOT/'implementations/node-engram/lifecycle-model.js')]}
def main():
    cases=json.loads((ROOT/'tests/lifecycle/cases.json').read_text())["cases"]; seen=set()
    try:
        with tempfile.TemporaryDirectory(prefix='engram-lifecycle-') as tmp:
            for case in cases:
                if case['id'] in seen: raise RuntimeError(f"duplicate case ID {case['id']}")
                seen.add(case['id']); request=Path(tmp)/f"{case['id']}.json"; request.write_text(json.dumps({"operation":case['operation'],"input":case['input']}))
                results={name:json.loads(subprocess.run(cmd+[str(request)],check=True,text=True,capture_output=True,timeout=10).stdout) for name,cmd in MODELS.items()}
                if any(result!=case['expected'] for result in results.values()): raise RuntimeError(f"{case['id']}: expected {case['expected']!r}, got {results!r}")
                print(f"PASS {case['id']}")
        print(f"PASS {len(cases)} lifecycle cases")
    except (OSError,ValueError,RuntimeError,subprocess.SubprocessError) as exc:
        print(f"FAIL {exc}",file=sys.stderr);return 1
    return 0
if __name__=='__main__':raise SystemExit(main())
