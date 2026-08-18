#!/usr/bin/env python3
"""Exercise a bidirectional exchange between the repository's 0.2 pilot processors."""
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTERS = {
    "python": [str(ROOT / "implementations/python-engram/engram_adapter.py")],
    "node": [str(ROOT / "implementations/node-engram/engram-adapter.js")],
}


def invoke(name: str, operation: str, source: Path, output: Path, case: str) -> Path:
    output.mkdir(parents=True)
    artifacts = output / "artifacts"
    artifacts.mkdir()
    request = output / "request.json"
    request.write_text(json.dumps({
        "protocol_version": "1.0",
        "case_id": case,
        "operation": operation,
        "fixture": str(source.resolve()),
        "artifact_directory": str(artifacts.resolve()),
        "parameters": {"edits": []},
        "supported_profiles": ["core", "graph", "media", "action"],
    }, indent=2) + "\n", encoding="utf-8")
    completed = subprocess.run(
        ADAPTERS[name] + [operation, str(request)],
        check=True,
        text=True,
        capture_output=True,
    )
    result = json.loads(completed.stdout)
    if result.get("outcome") != "completed":
        raise RuntimeError(f"{name} did not complete {case}")
    return artifacts / "package"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(package: Path):
    values = {}
    for item in sorted(path for path in package.rglob("*") if path.is_file()):
        relative = str(item.relative_to(package))
        values[relative] = (
            {"json": json.loads(item.read_text(encoding="utf-8"))}
            if item.suffix == ".json"
            else {"sha256": sha256(item)}
        )
    return values


def comparison(label: str, before: Path, after: Path):
    left = snapshot(before)
    right = snapshot(after)
    changed = sorted(path for path in set(left) | set(right) if left.get(path) != right.get(path))
    return {
        "exchange": label,
        "normative_content_equal": not changed,
        "changed_or_missing_paths": changed,
    }


def main() -> int:
    source = ROOT / "examples/v0.2/basic-engram"
    with tempfile.TemporaryDirectory(prefix="engram-interoperability-") as temporary:
        base = Path(temporary)
        python_export = invoke("python", "produce", source, base / "python", "PY-PRODUCE-BASIC")
        node_export = invoke("node", "produce", source, base / "node", "NODE-PRODUCE-BASIC")
        node_after_python = invoke(
            "node", "round-trip", python_export, base / "node-after-python", "NODE-IMPORT-PYTHON"
        )
        python_after_node = invoke(
            "python", "round-trip", node_export, base / "python-after-node", "PYTHON-IMPORT-NODE"
        )
        report = {
            "report_version": "0.2",
            "status": "repository-pilot-exercise",
            "independent_implementation_evidence": False,
            "source": "examples/v0.2/basic-engram",
            "comparisons": [
                comparison("Python export -> Node round trip", python_export, node_after_python),
                comparison("Node export -> Python round trip", node_export, python_after_node),
            ],
        }
    print(json.dumps(report, indent=2))
    return 0 if all(item["normative_content_equal"] for item in report["comparisons"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
