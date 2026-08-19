#!/usr/bin/env python3
"""Dependency-free Engram Mesh 0.3 prototype adapter."""
import json, shutil, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_engram_mesh import validate
def main():
    operation, request_path = sys.argv[1:]
    request = json.loads(Path(request_path).read_text()); source = Path(request["fixture"])
    mesh = source / "engram-mesh.json"; validate(mesh)
    artifacts = []
    if operation in {"produce", "round-trip"}:
        out = Path(request["artifact_directory"]) / "engram-mesh.json"; shutil.copyfile(mesh, out); artifacts = [{"path":"engram-mesh.json", "media_type":"application/json"}]
    print(json.dumps({"protocol_version":"1.0","case_id":request["case_id"],"outcome":"completed","observed":{"status":"success","mesh_id":json.loads(mesh.read_text())["mesh_id"]},"diagnostics":[],"artifacts":artifacts}))
if __name__ == "__main__": main()
