#!/usr/bin/env python3
"""Dependency-free structural and semantic validator for Engram Mesh 0.3."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r"^[a-z][a-z0-9-]{1,31}_[0-9A-HJKMNP-TV-Z]{26}$")
NAMESPACE = re.compile(r"^[a-z0-9]+(?:\.[a-z0-9-]+)+$")
CORE_CAPS = {"discover", "read", "create", "modify", "move", "delete"}
AUTHORITY = {"authoritative", "replica", "reference"}
BINDING_STATES = {"active", "superseded", "deleted", "unresolved"}
MAX_BYTES = 10 * 1024 * 1024

TOP_KEYS = {"format", "version", "mesh_id", "generated_at", "sources", "nodes", "bindings", "relationships", "slices", "lenses", "extensions"}
SOURCE_KEYS = {"id", "kind", "identity_domain", "display_name", "resolver", "capabilities", "extensions"}
NODE_KEYS = {"id", "type", "title", "description", "tags", "extensions"}
BINDING_KEYS = {"id", "node", "source", "external_id", "object_generation", "state", "authority", "successor", "capabilities", "freshness", "extensions"}
RELATIONSHIP_KEYS = {"id", "from", "to", "type", "extensions"}
SLICE_KEYS = {"id", "scope", "snapshot", "selection", "sources", "nodes", "bindings", "relationships", "boundary"}
LENS_KEYS = {"id", "mechanism", "version", "expression", "extensions"}


class ValidationError(ValueError):
    pass


def fail(path: Path, message: str) -> None:
    raise ValidationError(f"{path}: {message}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def load(path: Path, max_bytes: int = MAX_BYTES) -> dict[str, Any]:
    if path.stat().st_size > max_bytes:
        fail(path, f"document exceeds {max_bytes} bytes")
    try:
        value = json.loads(path.read_bytes().decode("utf-8"), object_pairs_hook=unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError, ValidationError) as exc:
        fail(path, f"invalid JSON: {exc}")
    if not isinstance(value, dict):
        fail(path, "document root must be an object")
    return value


def closed(path: Path, value: dict[str, Any], allowed: set[str], kind: str) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        fail(path, f"unknown {kind} field {unknown[0]!r}")


def text(path: Path, value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        fail(path, f"{label} must be a non-empty string")
    return value


def timestamp(path: Path, value: Any, label: str) -> None:
    raw = text(path, value, label)
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        fail(path, f"{label} must be an RFC 3339 timestamp")
    if parsed.tzinfo is None:
        fail(path, f"{label} must include a timezone")


def extensions(path: Path, value: Any) -> None:
    if value is None:
        return
    if not isinstance(value, dict):
        fail(path, "extensions must be an object")
    for key in value:
        if not NAMESPACE.fullmatch(key):
            fail(path, f"invalid extension namespace {key!r}")


def entity_ids(path: Path, values: Any, kind: str, allowed: set[str]) -> tuple[set[str], dict[str, dict[str, Any]]]:
    if not isinstance(values, list):
        fail(path, f"{kind}s must be an array")
    found: set[str] = set()
    indexed: dict[str, dict[str, Any]] = {}
    for value in values:
        if not isinstance(value, dict):
            fail(path, f"{kind} must be an object")
        closed(path, value, allowed, kind)
        value_id = value.get("id")
        if not isinstance(value_id, str) or not ID.fullmatch(value_id):
            fail(path, f"invalid {kind} ID")
        if value_id in found:
            fail(path, f"duplicate {kind} ID {value_id}")
        found.add(value_id)
        indexed[value_id] = value
        extensions(path, value.get("extensions"))
    return found, indexed


def capabilities(path: Path, value: Any, label: str) -> set[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        fail(path, f"{label} capabilities must be an array of strings")
    if len(value) != len(set(value)):
        fail(path, f"duplicate {label} capability")
    for capability in value:
        if capability not in CORE_CAPS:
            parts = capability.split(".")
            if len(parts) < 3 or not NAMESPACE.fullmatch(".".join(parts[:-1])) or not parts[-1]:
                fail(path, f"unnamespaced extension capability {capability!r}")
    return set(value)


def id_list(path: Path, value: Any, universe: set[str], label: str) -> set[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        fail(path, f"slice {label} must be an ID array")
    if len(value) != len(set(value)):
        fail(path, f"slice {label} contains duplicates")
    if not set(value) <= universe:
        fail(path, f"slice {label} includes an unknown ID")
    return set(value)


def validate(path: Path, max_bytes: int = MAX_BYTES) -> dict[str, Any]:
    mesh = load(path, max_bytes)
    closed(path, mesh, TOP_KEYS, "mesh")
    required = {"format", "version", "mesh_id", "sources", "nodes", "bindings", "relationships"}
    if not required <= mesh.keys():
        fail(path, "missing core mesh fields")
    if mesh["format"] != "engram-mesh" or mesh["version"] != "0.3":
        fail(path, "unsupported format or version")
    if not isinstance(mesh["mesh_id"], str) or not ID.fullmatch(mesh["mesh_id"]):
        fail(path, "invalid mesh ID")
    if "generated_at" in mesh:
        timestamp(path, mesh["generated_at"], "generated_at")
    extensions(path, mesh.get("extensions"))

    source_ids, sources = entity_ids(path, mesh["sources"], "source", SOURCE_KEYS)
    node_ids, _nodes = entity_ids(path, mesh["nodes"], "node", NODE_KEYS)
    binding_ids, bindings = entity_ids(path, mesh["bindings"], "binding", BINDING_KEYS)
    relationship_ids, relationships = entity_ids(path, mesh["relationships"], "relationship", RELATIONSHIP_KEYS)
    slice_ids, slices = entity_ids(path, mesh.get("slices", []), "slice", SLICE_KEYS)
    lens_ids, lenses = entity_ids(path, mesh.get("lenses", []), "lens", LENS_KEYS)

    all_ids = [mesh["mesh_id"], *source_ids, *node_ids, *binding_ids, *relationship_ids, *slice_ids, *lens_ids]
    if len(all_ids) != len(set(all_ids)):
        fail(path, "IDs must be globally unique within the document")

    source_caps: dict[str, set[str]] = {}
    identity_domains: set[str] = set()
    for source_id, source in sources.items():
        text(path, source.get("kind"), "source kind")
        identity_domain = text(path, source.get("identity_domain"), "source identity_domain")
        if identity_domain in identity_domains:
            fail(path, f"duplicate source identity_domain {identity_domain!r}")
        identity_domains.add(identity_domain)
        source_caps[source_id] = capabilities(path, source.get("capabilities"), "source")
        resolver = source.get("resolver")
        if resolver is not None:
            if not isinstance(resolver, dict) or set(resolver) != {"mechanism", "locator"}:
                fail(path, "resolver must contain exactly mechanism and locator")
            text(path, resolver["mechanism"], "resolver mechanism")
            locator = text(path, resolver["locator"], "resolver locator")
            if re.search(r"(?i)(password|passwd|access[_-]?token|api[_-]?key|secret)=|://[^/@:]+:[^/@]+@", locator):
                fail(path, "resolver locator appears to contain a credential")

    external_generations: set[tuple[str, str, str]] = set()
    active_external_ids: set[tuple[str, str]] = set()
    authoritative: dict[str, str] = {}
    for binding_id, binding in bindings.items():
        node_id, source_id = binding.get("node"), binding.get("source")
        if node_id not in node_ids or source_id not in source_ids:
            fail(path, "binding endpoint is unknown")
        external_id = text(path, binding.get("external_id"), "external_id")
        generation = text(path, binding.get("object_generation"), "object_generation")
        identity = (source_id, external_id, generation)
        if identity in external_generations:
            fail(path, "duplicate source/external ID/object generation")
        external_generations.add(identity)
        state, authority = binding.get("state"), binding.get("authority")
        if state not in BINDING_STATES or authority not in AUTHORITY:
            fail(path, "invalid binding state or authority")
        successor = binding.get("successor")
        if state == "superseded" and successor not in binding_ids:
            fail(path, "superseded binding requires an existing successor")
        if successor == binding_id:
            fail(path, "binding cannot succeed itself")
        if state in {"deleted", "unresolved"} and "capabilities" in binding:
            fail(path, "deleted or unresolved binding cannot advertise capabilities")
        if state == "active" and authority == "authoritative":
            if node_id in authoritative:
                fail(path, f"node has multiple active authoritative bindings: {node_id}")
            authoritative[node_id] = binding_id
        if state == "active":
            current_identity = (source_id, external_id)
            if current_identity in active_external_ids:
                fail(path, "external ID has multiple active object generations")
            active_external_ids.add(current_identity)
        if "capabilities" in binding:
            binding_caps = capabilities(path, binding["capabilities"], "binding")
            if not binding_caps <= source_caps[source_id]:
                fail(path, "binding capabilities must be a subset of source capabilities")
        freshness = binding.get("freshness")
        if freshness is not None:
            if not isinstance(freshness, dict) or set(freshness) - {"observed_at", "revision", "digest", "token"}:
                fail(path, "invalid freshness object")
            timestamp(path, freshness.get("observed_at"), "freshness observed_at")
            if not any(text_value for key in ("revision", "digest", "token") if isinstance((text_value := freshness.get(key)), str) and text_value):
                fail(path, "freshness requires revision, digest, or token evidence")

    for binding_id, binding in bindings.items():
        if binding["state"] != "superseded":
            continue
        successor = bindings[binding["successor"]]
        if successor["node"] != binding["node"]:
            fail(path, "successor binding must retain the same node")
        seen = {binding_id}
        current = successor
        while current["state"] == "superseded":
            current_id = current["id"]
            if current_id in seen:
                fail(path, "binding successor cycle")
            seen.add(current_id)
            current = bindings[current["successor"]]

    parents: dict[str, str] = {}
    for relationship in relationships.values():
        if relationship.get("from") not in node_ids or relationship.get("to") not in node_ids:
            fail(path, "relationship endpoint is unknown")
        relation_type = text(path, relationship.get("type"), "relationship type")
        if relation_type == "parent":
            child = relationship["from"]
            if child in parents:
                fail(path, f"node has multiple parents: {child}")
            parents[child] = relationship["to"]
    for node_id in parents:
        seen: set[str] = set()
        current = node_id
        while current in parents:
            if current in seen:
                fail(path, "parent relationship cycle")
            seen.add(current)
            current = parents[current]

    for slice_value in slices.values():
        if slice_value.get("scope") not in {"complete", "partial"}:
            fail(path, "slice scope must be complete or partial")
        if slice_value["scope"] == "complete" and not isinstance(slice_value.get("snapshot"), str):
            fail(path, "complete slice requires snapshot evidence")
        selection = slice_value.get("selection")
        if not isinstance(selection, dict) or set(selection) - {"mechanism", "version", "expression", "description"}:
            fail(path, "invalid slice selection")
        text(path, selection.get("mechanism"), "selection mechanism")
        text(path, selection.get("description"), "selection description")
        selected_sources = id_list(path, slice_value.get("sources"), source_ids, "sources")
        selected_nodes = id_list(path, slice_value.get("nodes"), node_ids, "nodes")
        selected_bindings = id_list(path, slice_value.get("bindings"), binding_ids, "bindings")
        selected_relationships = id_list(path, slice_value.get("relationships"), relationship_ids, "relationships")
        if slice_value["scope"] == "complete" and (
            selected_sources != source_ids
            or selected_nodes != node_ids
            or selected_bindings != binding_ids
            or selected_relationships != relationship_ids
        ):
            fail(path, "complete slice must include every mesh entity")
        for binding_id in selected_bindings:
            binding = bindings[binding_id]
            if binding["node"] not in selected_nodes or binding["source"] not in selected_sources:
                fail(path, "slice binding requires its node and source")
        for relationship_id in selected_relationships:
            relation = relationships[relationship_id]
            if relation["from"] not in selected_nodes or relation["to"] not in selected_nodes:
                fail(path, "slice relationship requires both endpoint nodes")
        boundary = slice_value.get("boundary")
        if not isinstance(boundary, list):
            fail(path, "slice boundary must be an array")
        for item in boundary:
            if not isinstance(item, dict) or set(item) - {"kind", "id", "disposition", "reason"}:
                fail(path, "invalid slice boundary entry")
            if item.get("kind") not in {"node", "relationship"} or item.get("disposition") not in {"omitted", "unresolved", "undisclosed"}:
                fail(path, "invalid slice boundary kind or disposition")
            if item["disposition"] == "undisclosed" and "id" in item:
                fail(path, "undisclosed boundary must not reveal an ID")
            if item["disposition"] != "undisclosed" and not isinstance(item.get("id"), str):
                fail(path, "identified boundary entry requires an ID")
            if item["disposition"] == "omitted":
                universe = node_ids if item["kind"] == "node" else relationship_ids
                selected = selected_nodes if item["kind"] == "node" else selected_relationships
                if item["id"] not in universe or item["id"] in selected:
                    fail(path, "omitted boundary ID must identify an unselected mesh entity")
        if slice_value["scope"] == "complete" and boundary:
            fail(path, "complete slice must have an empty boundary")

    for lens in lenses.values():
        for key in ("mechanism", "version", "expression"):
            text(path, lens.get(key), f"lens {key}")
        if not NAMESPACE.fullmatch(lens["mechanism"]):
            fail(path, "lens mechanism must use a namespaced identifier")

    return mesh


def repository_suite() -> None:
    for path in sorted((ROOT / "tests/v0.3/valid").glob("*/engram-mesh.json")):
        validate(path)
        print(f"PASS {path.relative_to(ROOT)}")
    for path in sorted((ROOT / "tests/v0.3/invalid").glob("*/engram-mesh.json")):
        expected_path = path.parent / "expected-error.txt"
        if not expected_path.is_file():
            fail(path, "invalid fixture lacks expected-error.txt")
        expected = expected_path.read_text(encoding="utf-8").strip()
        try:
            validate(path)
        except ValidationError as exc:
            if expected not in str(exc):
                fail(path, f"expected error {expected!r}, got {exc!r}")
            print(f"PASS {path.relative_to(ROOT)} (rejected)")
        else:
            fail(path, "invalid fixture accepted")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("document", nargs="?", type=Path)
    parser.add_argument("--max-bytes", type=int, default=MAX_BYTES)
    args = parser.parse_args()
    try:
        if args.document:
            validate(args.document, args.max_bytes)
            print(f"PASS {args.document}")
        else:
            repository_suite()
    except (OSError, ValidationError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
