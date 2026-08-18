#!/usr/bin/env python3
"""Validate Synthetic Engram v0.1 packages and repository fixtures."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path, PurePosixPath
from typing import Any

import yaml
from yaml import tokens as yaml_tokens
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = ROOT / "schemas"
OBJECT_SCHEMA = {
    "record": "record.schema.json",
    "graph": "graph.schema.json",
    "attachment": "attachment.schema.json",
}
PROFILE_FOR = {"graph": "graph", "attachment": "media"}


# PyYAML normally converts timestamps to datetime objects. The data model treats
# timestamps as RFC 3339 strings, so retain scalar text for schema validation.
class EngramLoader(yaml.SafeLoader):
    pass


EngramLoader.yaml_implicit_resolvers = {}
EngramLoader.add_implicit_resolver(
    "tag:yaml.org,2002:null", re.compile(r"^null$"), ["n"]
)
EngramLoader.add_implicit_resolver(
    "tag:yaml.org,2002:bool", re.compile(r"^(?:true|false)$"), ["t", "f"]
)
EngramLoader.add_implicit_resolver(
    "tag:yaml.org,2002:int", re.compile(r"^-?(?:0|[1-9][0-9]*)$"), list("-0123456789")
)
EngramLoader.add_implicit_resolver(
    "tag:yaml.org,2002:float",
    re.compile(
        r"^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+(?:[eE][+-]?[0-9]+)?|[eE][+-]?[0-9]+)$"
    ),
    list("-0123456789"),
)


def _unique_mapping(
    loader: EngramLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            fail("front matter mapping keys must be strings")
        if key == "<<":
            fail("YAML merge keys are not permitted")
        if key in result:
            fail(f"duplicate YAML key {key!r}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


EngramLoader.add_constructor("tag:yaml.org,2002:map", _unique_mapping)


class ValidationError(Exception):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def load_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object
        )
    except (OSError, UnicodeError, json.JSONDecodeError, ValidationError) as exc:
        fail(f"{path}: {exc}")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail(f"duplicate JSON key {key!r}")
        result[key] = value
    return result

def schema_registry(schema_dir: Path) -> Registry:

def schema_registry() -> Registry:
    registry = Registry()
    for path in schema_dir.glob("*.schema.json"):
        contents = load_json(path)
        registry = registry.with_resource(
            contents["$id"], Resource.from_contents(contents)
        )
    return registry

def validator(name: str, registry: Registry, schema_dir: Path) -> Draft202012Validator:
    schema = load_json(schema_dir / name)

def validator(name: str, registry: Registry) -> Draft202012Validator:
    schema = load_json(SCHEMA_DIR / name)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(
        schema, registry=registry, format_checker=FormatChecker()
    )


def check_schema(instance: Any, name: str, registry: Registry, schema_dir: Path, label: Path) -> None:
    errors = sorted(validator(name, registry, schema_dir).iter_errors(instance), key=lambda e: list(e.absolute_path))
def check_schema(instance: Any, name: str, registry: Registry, label: Path) -> None:
    errors = sorted(
        validator(name, registry).iter_errors(instance),
        key=lambda e: list(e.absolute_path),
    )
    if errors:
        err = errors[0]
        location = "/".join(str(part) for part in err.absolute_path) or "<root>"
        fail(f"{label}: schema error at {location}: {err.message}")


def read_record(path: Path) -> dict[str, Any]:
    try:
        text = path.read_bytes().decode("utf-8")
    except (OSError, UnicodeError) as exc:
        fail(f"{path}: {exc}")
    if text.startswith("\ufeff"):
        fail(f"{path}: UTF-8 byte-order mark is not permitted")
    if re.search(r"\r(?!\n)", text):
        fail(f"{path}: bare CR line ending is not permitted")
    lines = text.splitlines(keepends=True)
    if not lines or lines[0] not in ("---\n", "---\r\n"):
        fail(f"{path}: opening delimiter must be exactly '---' on the first line")
    closing = next(
        (
            index
            for index, line in enumerate(lines[1:], 1)
            if line.removesuffix("\n").removesuffix("\r") == "---"
        ),
        None,
    )
    if closing is None:
        fail(f"{path}: missing exact front matter closing delimiter")
    front_matter = "".join(lines[1:closing])
    try:
        for token in yaml.scan(front_matter, Loader=EngramLoader):
            if isinstance(
                token,
                (yaml_tokens.TagToken, yaml_tokens.AnchorToken, yaml_tokens.AliasToken),
            ):
                fail(f"{path}: YAML tags, anchors, and aliases are not permitted")
            if isinstance(
                token,
                (
                    yaml_tokens.DirectiveToken,
                    yaml_tokens.DocumentStartToken,
                    yaml_tokens.DocumentEndToken,
                ),
            ):
                fail(f"{path}: YAML directives and document markers are not permitted")
            if isinstance(
                token,
                (yaml_tokens.FlowMappingStartToken, yaml_tokens.FlowSequenceStartToken),
            ):
                fail(f"{path}: YAML flow collections are not permitted")
        value = yaml.load(front_matter, Loader=EngramLoader)
    except (yaml.YAMLError, ValidationError) as exc:
        if isinstance(exc, ValidationError):
            raise
        fail(f"{path}: invalid YAML: {exc}")
    if not isinstance(value, dict):
        fail(f"{path}: front matter must be a mapping")
    return value


def safe_path(root: Path, value: str) -> Path:
    pure = PurePosixPath(value)
    if pure.is_absolute() or any(part in ("", ".", "..") for part in pure.parts):
        fail(f"unsafe inventory path: {value}")
    path = root.joinpath(*pure.parts)
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        fail(f"inventory path escapes package: {value}")
    return path


def validate_package(root: Path) -> None:
    manifest_path = root / "engram.json"
    if not manifest_path.is_file():
        fail(f"{root}: missing engram.json")
    manifest = load_json(manifest_path)
    version = manifest.get("version", "")
    schema_version = "1.0" if version.startswith("1.0.") else "0.1"
    schema_dir = SCHEMA_ROOT / f"v{schema_version}"
    registry = schema_registry(schema_dir)
    check_schema(manifest, "manifest.schema.json", registry, schema_dir, manifest_path)

    paths: set[str] = set()
    entries_by_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    objects: dict[str, tuple[str, Any, Path]] = {}
    parent: dict[str, str] = {}

    for entry in manifest["objects"]:
        if entry["path"] in paths:
            fail(f"duplicate inventory path: {entry['path']}")
        paths.add(entry["path"])
        entries_by_id[entry["id"]].append(entry)
        path = safe_path(root, entry["path"])
        if not path.is_file():
            fail(f"missing inventory path: {entry['path']}")
        kind = entry["kind"]
        if kind == "blob":
            continue
        value = read_record(path) if kind == "record" else load_json(path)
        check_schema(value, OBJECT_SCHEMA[kind], registry, schema_dir, path)
        if value["id"] != entry["id"]:
            fail(f"{entry['path']}: object ID does not match inventory")
        if entry["id"] in objects:
            fail(f"duplicate object ID: {entry['id']}")
        objects[entry["id"]] = (kind, value, path)
        if kind == "record" and "parent" in value:
            parent[entry["id"]] = value["parent"]
        required_profile = PROFILE_FOR.get(kind)
        if required_profile and required_profile not in manifest["profiles"]:
            fail(f"{kind} object requires profile {required_profile}")
        if (
            kind == "record"
            and value["type"] == "action"
            and "action" not in manifest["profiles"]
        ):
            fail("action record requires profile action")

    # In a directory package, every file in a normative durable-artifact
    # directory is observable. A complete package cannot hide one by merely
    # leaving it out of the manifest.
    if manifest["completeness"] == "complete":
        durable_paths = {
            path.relative_to(root).as_posix()
            for directory in ("records", "graphs", "attachments")
            if (root / directory).is_dir()
            for path in (root / directory).rglob("*")
            if path.is_file()
        }
        omitted = sorted(durable_paths - paths)
        if omitted:
            fail(f"complete package has un-inventoried durable artifact: {omitted[0]}")

    for object_id, entries in entries_by_id.items():
        kinds = sorted(entry["kind"] for entry in entries)
        if len(entries) > 1 and kinds != ["attachment", "blob"]:
            fail(f"duplicate inventory ID: {object_id}")

    def resolve(target: str, target_scope: str, source: Path) -> None:
        if target_scope == "synthetic_engram" and target not in objects and manifest["completeness"] == "complete":
            fail(f"{source}: complete package omits Engram member {target}")

    for object_id, (kind, value, path) in objects.items():
        if kind == "record":
            if "parent" in value:
                resolve(value["parent"], value.get("parent_scope", "synthetic_engram"), path)
            for link in value.get("links", []):
                resolve(link["target"], link.get("target_scope", "synthetic_engram"), path)
        elif kind == "graph":
            node_ids = [node["id"] for node in value["nodes"]]
            edge_ids = [edge["id"] for edge in value["edges"]]
            if len(node_ids) != len(set(node_ids)):
                fail(f"{path}: duplicate graph node ID")
            if len(edge_ids) != len(set(edge_ids)):
                fail(f"{path}: duplicate graph edge ID")
            for node in value["nodes"]:
                reference = node.get("object_id", node.get("record"))
                if reference is not None:
                    resolve(reference, False, path)
                    if schema_version == "1.0" and node.get("object_kind") != objects[reference][0]:
                        fail(f"{path}: graph node object_kind does not match inventory")
                if "record" in node:
                    resolve(node["record"], node.get("record_scope", "synthetic_engram"), path)
            for edge in value["edges"]:
                if edge["from"] not in node_ids or edge["to"] not in node_ids:
                    fail(f"{path}: graph edge has unresolved endpoint")
                if schema_version == "1.0" and ":" in edge["relation"]:
                    prefix = edge["relation"].split(":", 1)[0]
                    if prefix != "core" and prefix not in value.get("relation_namespaces", {}):
                        fail(f"{path}: unsupported relation vocabulary {prefix}")
            if value["scope"] == "complete_records":
                represented = {
                    node["record"] for node in value["nodes"]
                    if "record" in node and not node.get("external", False)
                }
                records = {
                    candidate_id
                    for candidate_id, (candidate_kind, _, _) in objects.items()
                    if candidate_kind == "record"
                }
                missing = sorted(records - represented)
                if missing:
                    fail(f"{path}: complete_records graph omits inventoried record {missing[0]}")
        elif kind == "attachment":
            payload = safe_path(root, value["path"])
            blob_entries = [
                entry
                for entry in entries_by_id[object_id]
                if entry["kind"] == "blob" and entry["path"] == value["path"]
            ]
            if not blob_entries:
                fail(f"{path}: attachment payload is not inventoried as a blob")
            data = payload.read_bytes()
            if len(data) != value["size"]:
                fail(f"{path}: attachment size mismatch")
            if hashlib.sha256(data).hexdigest() != value["sha256"]:
                fail(f"{path}: attachment checksum mismatch")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(object_id: str) -> None:
        if object_id in visiting:
            fail(f"hierarchy cycle at {object_id}")
        if object_id in visited:
            return
        visiting.add(object_id)
        if object_id in parent:
            visit(parent[object_id])
        visiting.remove(object_id)
        visited.add(object_id)

    for object_id in parent:
        visit(object_id)


def repository_suite() -> None:
    check_local_markdown_links()
    targets = [
        ROOT / "examples" / "basic-engram",
        *sorted((ROOT / "tests" / "valid").iterdir()),
    ]
    for target in targets:
        validate_package(target)
        print(f"PASS {target.relative_to(ROOT)}")
    for target in sorted((ROOT / "tests" / "invalid").iterdir()):
        expected = (target / "expected-error.txt").read_text().strip()
        try:
            validate_package(target)
        except ValidationError as exc:
            if expected not in str(exc):
                fail(f"{target}: rejected for the wrong reason: {exc}")
            print(f"PASS {target.relative_to(ROOT)} (rejected: {expected})")
        else:
            fail(f"{target}: invalid fixture was accepted")


def check_local_markdown_links() -> None:
    link_pattern = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")
    for document in ROOT.rglob("*.md"):
        for target in link_pattern.findall(document.read_text(encoding="utf-8")):
            if target.startswith("#") or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
                continue
            target = target.split("#", 1)[0]
            if target and not (document.parent / target).exists():
                fail(f"{document}: broken local link {target}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", nargs="?", type=Path)
    args = parser.parse_args()
    try:
        validate_package(args.package.resolve()) if args.package else repository_suite()
    except ValidationError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
