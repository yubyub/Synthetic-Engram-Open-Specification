#!/usr/bin/env python3
"""Run the shared front-matter corpus against Python and Node parsers."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PARSERS = {
    "python": [sys.executable, str(ROOT / "implementations/python-engram/frontmatter_parser.py")],
    "node": ["node", str(ROOT / "implementations/node-engram/frontmatter-parser.js")],
}


def generated_cases() -> list[dict[str, Any]]:
    plain_strings = ["yes", "Yes", "01", ".5", "1.", "NaN", "2026-08-18", "nullish", "TRUE"]
    cases = []
    for index, value in enumerate(plain_strings, 1):
        cases.append({
            "id": f"FM-PROPERTY-PLAIN-{index:03d}",
            "content": f"---\nvalue: {value}\n---\n",
            "expected": {"outcome": "accepted", "front_matter": {"value": value}},
        })
    for index, value in enumerate(range(-20, 21), 1):
        cases.append({
            "id": f"FM-PROPERTY-INT-{index:03d}",
            "content": f"---\nvalue: {value}\n---\n",
            "expected": {"outcome": "accepted", "front_matter": {"value": value}},
        })
    return cases


def invoke(command: list[str], case: dict[str, Any], base: Path) -> dict[str, Any]:
    record = base / f"{case['id']}.md"
    record.write_bytes(case["content"].encode("utf-8"))
    request = base / f"{case['id']}.request.json"
    request.write_text(json.dumps({
        "protocol_version": "1.0",
        "case_id": case["id"],
        "record": str(record.resolve()),
        "max_record_bytes": case.get("max_record_bytes", 1048576),
    }), encoding="utf-8")
    completed = subprocess.run(command + ["parse", str(request)], text=True, capture_output=True, timeout=10)
    if completed.returncode != 0:
        raise RuntimeError(f"{case['id']}: parser exit {completed.returncode}: {completed.stderr}")
    result = json.loads(completed.stdout)
    if result.get("protocol_version") != "1.0" or result.get("case_id") != case["id"]:
        raise RuntimeError(f"{case['id']}: parser result identity mismatch")
    return result


def observable(result: dict[str, Any]) -> dict[str, Any]:
    if result.get("outcome") == "accepted":
        return {"outcome": "accepted", "front_matter": result.get("front_matter")}
    return {"outcome": result.get("outcome"), "code": result.get("diagnostic", {}).get("code")}


def main() -> int:
    corpus = json.loads((ROOT / "tests/front-matter/cases.json").read_text(encoding="utf-8"))
    cases = corpus["cases"] + generated_cases()
    seen: set[str] = set()
    try:
        with tempfile.TemporaryDirectory(prefix="engram-frontmatter-") as tmp:
            base = Path(tmp)
            for case in cases:
                if case["id"] in seen:
                    raise RuntimeError(f"duplicate case ID {case['id']}")
                seen.add(case["id"])
                results = {name: observable(invoke(command, case, base)) for name, command in PARSERS.items()}
                if any(value != case["expected"] for value in results.values()):
                    raise RuntimeError(f"{case['id']}: expected {case['expected']!r}, got {results!r}")
                first = next(iter(results.values()))
                if any(value != first for value in results.values()):
                    raise RuntimeError(f"{case['id']}: differential mismatch {results!r}")
                print(f"PASS {case['id']}")
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    print(f"PASS {len(cases)} front-matter corpus and generated property cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
