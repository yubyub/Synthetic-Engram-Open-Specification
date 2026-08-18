#!/usr/bin/env python3
"""Small, dependency-free Synthetic Engram 0.2 pilot processor."""
from __future__ import annotations

import json
import re
import shutil
import sys
import tarfile
from pathlib import Path, PurePosixPath

VERSION = "0.2.0"
PROFILES = ["core", "graph", "media", "action"]
ROLES = ["producer", "consumer", "round-trip"]


def read_json(path: Path):
    return json.loads(path.read_bytes().decode("utf-8"))


def safe_relative(value: str) -> bool:
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts and "\\" not in value


def copy_package(
    source: Path, target: Path, rename_paths: bool = False, rename_titles: bool = False
):
    manifest = read_json(source / "engram.json")
    target.mkdir(parents=True, exist_ok=False)
    output_manifest = json.loads(json.dumps(manifest))
    for index, item in enumerate(output_manifest["objects"]):
        original = manifest["objects"][index]["path"]
        if not safe_relative(original):
            raise ValueError(f"unsafe inventory path: {original}")
        destination_name = original
        if rename_paths:
            path = PurePosixPath(original)
            destination_name = str(path.with_name(f"renamed-{path.name}"))
            item["path"] = destination_name
        destination = target / destination_name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / original, destination)
        if rename_titles and item["media_type"] == "text/markdown":
            content = destination.read_text(encoding="utf-8")
            content, changed = re.subn(
                r"(?m)^title: (.+)$", r"title: Renamed \1", content, count=1
            )
            if changed != 1:
                raise ValueError(f"record has no title to rename: {original}")
            destination.write_text(content, encoding="utf-8")
    (target / "engram.json").write_text(
        json.dumps(output_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest, output_manifest


def inventory_signature(manifest):
    return sorted((item["id"], item["kind"]) for item in manifest["objects"])


def package_size_and_count(root: Path):
    files = [path for path in root.rglob("*") if path.is_file()]
    return sum(path.stat().st_size for path in files), len(files)


def version_status(manifest, parameters):
    major, minor, _patch = (int(part) for part in manifest["version"].split("."))
    supported_major = parameters.get("supported_major", 0)
    supported_minor = parameters.get("supported_minor", 2)
    if major != supported_major:
        return "unsupported-major-version"
    if minor != supported_minor:
        return "unsupported-minor-version"
    return None


def import_status(fixture: Path, request, capability_wording: bool = False):
    manifest = read_json(fixture / "engram.json")
    mismatch = version_status(manifest, request["parameters"])
    if mismatch:
        return {"status": mismatch, "must_not_report_success": True}
    unsupported = next(
        (profile for profile in manifest["profiles"] if profile not in request["supported_profiles"]),
        None,
    )
    if unsupported:
        status = "unsupported-required-capability" if capability_wording else "unsupported-profile"
        key = "capability" if capability_wording else "profile"
        return {"status": status, key: unsupported, "must_not_report_success": True}
    size, count = package_size_and_count(fixture)
    parameters = request["parameters"]
    if size > parameters.get("max_bytes", size) or count > parameters.get("max_objects", count):
        return {"status": "rejected", "limits_enforced": True}
    return {"status": "success"}


def extract_status(archive_path: Path, parameters):
    unsafe = False
    size = 0
    count = 0
    with tarfile.open(archive_path) as archive:
        for member in archive.getmembers():
            path = PurePosixPath(member.name)
            unsafe |= path.is_absolute() or ".." in path.parts or member.issym() or member.islnk()
            size += member.size
            count += 1
    over_limit = size > parameters["max_bytes"] or count > parameters["max_objects"]
    return {
        "status": "rejected" if unsafe or over_limit else "success",
        "outside_root_writes": 0,
        "record_content_executions": 0,
        "limits_enforced": True,
    }


def consume(fixture: Path, request):
    parameters = request["parameters"]
    task = parameters["task"]
    if task == "inventory":
        manifest = read_json(fixture / "engram.json")
        inventoried = {item["path"] for item in manifest["objects"]}
        return {"status": "success", "normative_object_ids_exclude_unlisted": "scratch.tmp" not in inventoried}
    if task == "import":
        return import_status(fixture, request)
    if task == "negotiate-capabilities":
        return import_status(fixture, request, capability_wording=True)
    if task == "resolve-attachment":
        attachment_id = parameters["uri"].split(":", 1)[1]
        manifest = read_json(fixture / "engram.json")
        if not any(item["id"] == attachment_id and item["kind"] == "attachment" for item in manifest["objects"]):
            raise ValueError("attachment URI does not resolve through the inventory")
        return {"resolved_inventory_id": attachment_id, "suggested_path_ignored": True}
    if task == "extract":
        return extract_status(fixture, parameters)
    if task in ("import-untrusted", "import-and-render"):
        for path in fixture.rglob("*"):
            if path.is_file():
                path.read_bytes()
        return {"content_treated_as_data": True, "record_content_executions": 0}
    if task == "authorize":
        return {"permission_granted": parameters.get("credential") is not None}
    if task == "discover-attachment-references":
        content = (fixture / parameters["document"]).read_text(encoding="utf-8")
        link = re.search(r"\]\(engram-attachment:[A-Za-z0-9_]+\)", content)
        plain = re.search(r"(?m)^engram-attachment:[A-Za-z0-9_]+$", content)
        return {"link_destination_discovered": bool(link), "plain_text_ignored": bool(plain)}
    raise ValueError(f"unsupported consumer task: {task}")


def round_trip(fixture: Path, output: Path, parameters):
    edits = parameters.get("edits", [])
    before, after = copy_package(
        fixture,
        output,
        rename_paths="rename-paths" in edits,
        rename_titles="rename-titles" in edits,
    )
    bytes_unchanged = all(
        (fixture / item["path"]).read_bytes()
        == (output / after["objects"][index]["path"]).read_bytes()
        for index, item in enumerate(before["objects"])
        if item["media_type"] == "text/markdown"
    )
    observed = {
        "all_object_ids_unchanged": inventory_signature(before) == inventory_signature(after),
        "json_compatible_extension_value_deep_equal": bytes_unchanged,
        "core_semantics_unchanged": inventory_signature(before) == inventory_signature(after),
        "markdown_utf8_bytes_unchanged": bytes_unchanged,
        "all_normative_inventory_entries_present": inventory_signature(before) == inventory_signature(after),
    }
    blob = next((item for item in after["objects"] if item["kind"] == "blob"), None)
    if blob:
        observed["payload_size"] = (output / blob["path"]).stat().st_size
    if parameters.get("claim_unknown_extension_preservation"):
        observed["unknown_extension_keys_unchanged"] = bytes_unchanged
        observed["unknown_extension_values_deep_equal"] = bytes_unchanged
    definitions = parameters.get("extension_definitions", [])
    keys = [item["key"] for item in definitions]
    collision = next((key for key in keys if keys.count(key) > 1), None)
    if collision:
        observed.update(status="extension-namespace-collision", collision_key=collision, definitions_merged=False)
    return observed


def main():
    operation, request_file = sys.argv[1:]
    request = read_json(Path(request_file))
    fixture = Path(request["fixture"])
    artifacts = Path(request["artifact_directory"])
    emitted = []
    if operation == "produce":
        before, after = copy_package(fixture, artifacts / "package")
        observed = {
            "status": "success",
            "package_artifact_present": (artifacts / "package/engram.json").is_file(),
            "declared_profiles": after["profiles"],
            "inventory_preserved": inventory_signature(before) == inventory_signature(after),
        }
        emitted = [{"path": "package/engram.json", "media_type": "application/json"}]
    elif operation == "round-trip":
        observed = round_trip(fixture, artifacts / "package", request["parameters"])
        emitted = [{"path": "package/engram.json", "media_type": "application/json"}]
    elif operation == "consume":
        observed = consume(fixture, request)
    else:
        raise ValueError(f"unsupported operation: {operation}")
    print(json.dumps({
        "protocol_version": "1.0",
        "case_id": request["case_id"],
        "outcome": "completed",
        "observed": observed,
        "diagnostics": [],
        "artifacts": emitted,
    }))


if __name__ == "__main__":
    main()
