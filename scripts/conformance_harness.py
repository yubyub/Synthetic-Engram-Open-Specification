#!/usr/bin/env python3
"""Language-neutral executor for producer, consumer, and round-trip vectors."""
from __future__ import annotations

import argparse, copy, json, os, shlex, shutil, subprocess, sys, tarfile, tempfile
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

def die(message: str) -> None:
    raise RuntimeError(message)

def materialize(spec: dict[str, Any], destination: Path) -> Path:
    kind = spec["kind"]
    if kind == "directory":
        shutil.copytree(ROOT / spec["source"], destination)
        for step in spec.get("steps", []):
            if step["action"] == "write-text":
                path = destination / step["path"]
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(step["content"], encoding="utf-8")
            elif step["action"] == "set-manifest-version":
                path = destination / "engram.json"
                value = json.loads(path.read_text())
                value["version"] = step["version"]
                path.write_text(json.dumps(value, indent=2) + "\n")
            else: die(f"unknown fixture step {step['action']}")
        return destination
    if kind == "generated-tar":
        destination.mkdir()
        archive = destination / "input.tar"
        with tarfile.open(archive, "w") as output:
            for entry in spec["entries"]:
                data = entry.get("content", "").encode()
                info = tarfile.TarInfo(entry["path"]); info.size = len(data)
                import io
                output.addfile(info, io.BytesIO(data))
        return archive
    die(f"unknown fixture kind {kind}")

def contains(expected: Any, actual: Any, at: str = "observed") -> None:
    if isinstance(expected, dict):
        if not isinstance(actual, dict): die(f"{at}: expected object")
        for key, value in expected.items():
            if key not in actual: die(f"{at}: missing {key}")
            contains(value, actual[key], f"{at}.{key}")
    elif expected != actual or type(expected) is not type(actual):
        die(f"{at}: expected {expected!r}, got {actual!r}")

def run(adapter: list[str], case: dict[str, Any], base: Path) -> dict[str, Any]:
    case_root = base / case["id"]; case_root.mkdir()
    fixture = materialize(case["fixture"], case_root / "fixture")
    artifacts = case_root / "artifacts"; artifacts.mkdir()
    request = {"protocol_version":"1.0", "case_id":case["id"],
        "operation":case["adapter_operation"], "fixture":str(fixture.resolve()),
        "artifact_directory":str(artifacts.resolve()),
        "parameters":case.get("parameters", {}),
        "supported_profiles":case.get("supported_profiles", ["core","graph","media","action"])}
    request_path = case_root / "request.json"
    request_path.write_text(json.dumps(request, indent=2)+"\n")
    completed = subprocess.run(adapter+[case["adapter_operation"], str(request_path)],
        cwd=case_root, text=True, capture_output=True, timeout=30)
    if completed.returncode != 0: die(f"{case['id']}: adapter exit {completed.returncode}: {completed.stderr}")
    try: result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc: die(f"{case['id']}: invalid result JSON: {exc}")
    if result.get("protocol_version") != "1.0" or result.get("case_id") != case["id"]: die(f"{case['id']}: result identity mismatch")
    if not isinstance(result.get("diagnostics"), list) or not isinstance(result.get("artifacts"), list): die(f"{case['id']}: diagnostics/artifacts must be arrays")
    for artifact in result["artifacts"]:
        path = PurePosixPath(artifact["path"])
        if path.is_absolute() or ".." in path.parts or not (artifacts/path).is_file(): die(f"{case['id']}: unsafe or missing artifact")
    contains(case["expected"], result.get("observed"))
    return result

def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--adapter", required=True); parser.add_argument("--report", type=Path)
    args=parser.parse_args(); cases=[]
    for path in (ROOT/"tests/vectors").glob("*.json"): cases += json.loads(path.read_text())["cases"]
    try:
        with tempfile.TemporaryDirectory(prefix="engram-harness-") as tmp:
            adapter = shlex.split(args.adapter)
            candidate = ROOT / adapter[0]
            if candidate.is_file():
                adapter[0] = str(candidate.resolve())
            results=[run(adapter, case, Path(tmp)) for case in cases]
        report={"protocol_version":"1.0","adapter":args.adapter,"passed":len(results),"results":results}
        if args.report: args.report.write_text(json.dumps(report,indent=2)+"\n")
        for case in cases: print(f"PASS {case['id']}")
    except (RuntimeError, subprocess.TimeoutExpired, OSError) as exc:
        print(f"FAIL {exc}", file=sys.stderr); return 1
    return 0
if __name__ == "__main__": raise SystemExit(main())
