#!/usr/bin/env python3
"""Exercise the two prototype adapters against the canonical Engram Mesh fixture."""
import json, subprocess, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/v0.3/valid/basic-mesh"
ADAPTERS = [[sys.executable, str(ROOT / "implementations/python-engram-mesh/adapter.py")], ["node", str(ROOT / "implementations/node-engram-mesh/adapter.js")]]
with tempfile.TemporaryDirectory(prefix="engram-mesh-adapter-") as temp:
    for adapter in ADAPTERS:
        base = Path(temp) / Path(adapter[-1]).parent.name; base.mkdir(); artifacts = base / "artifacts"; artifacts.mkdir()
        request = {"protocol_version":"1.0","case_id":"TM-ROUNDTRIP-001","fixture":str(FIXTURE),"artifact_directory":str(artifacts)}
        request_path = base / "request.json"; request_path.write_text(json.dumps(request))
        result = subprocess.run(adapter + ["round-trip", str(request_path)], text=True, capture_output=True, timeout=20)
        if result.returncode: raise SystemExit(result.stderr)
        response = json.loads(result.stdout)
        if response["observed"].get("status") != "success" or not (artifacts / "engram-mesh.json").is_file(): raise SystemExit("adapter round trip failed")
        print(f"PASS {Path(adapter[-1]).parent.name}")
