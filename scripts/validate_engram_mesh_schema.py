#!/usr/bin/env python3
"""Validate Engram Mesh schemas and schema-valid examples/positive fixtures."""
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas" / "v0.3"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    definitions = load(SCHEMAS / "definitions.schema.json")
    mesh_schema = load(SCHEMAS / "mesh.schema.json")
    Draft202012Validator.check_schema(definitions)
    Draft202012Validator.check_schema(mesh_schema)
    registry = Registry().with_resource(
        "definitions.schema.json", Resource.from_contents(definitions)
    )
    validator = Draft202012Validator(
        mesh_schema, registry=registry, format_checker=FormatChecker()
    )
    documents = sorted((ROOT / "tests/v0.3/valid").glob("*/engram-mesh.json"))
    documents += sorted((ROOT / "examples/v0.3").glob("*/engram-mesh.json"))
    for path in documents:
        errors = sorted(validator.iter_errors(load(path)), key=lambda error: list(error.path))
        if errors:
            location = "/".join(str(part) for part in errors[0].path)
            raise RuntimeError(f"{path}:{location}: {errors[0].message}")
        print(f"PASS {path.relative_to(ROOT)} (schema)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
