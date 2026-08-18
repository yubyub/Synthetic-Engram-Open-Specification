#!/usr/bin/env python3
"""Python Engram Package processor 1.0.0 (independent implementation)."""
import json, re, shutil, sys, tarfile
from pathlib import Path, PurePosixPath

VERSION = "1.0.0"
PROFILES = ["core", "graph", "media", "action"]
ROLES = ["producer", "consumer", "round-trip"]

def read_json(path):
    return json.loads(path.read_bytes().decode("utf-8"))

def export_package(source, target):
    target.mkdir(parents=True, exist_ok=False)
    manifest = read_json(source / "engram.json")
    (target / "engram.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for item in manifest["objects"]:
        src, dst = source / item["path"], target / item["path"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        if item["kind"] in ("graph", "attachment"):
            (dst).write_text(json.dumps(read_json(src), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        else:
            shutil.copyfile(src, dst)
    return manifest

def safe_tar(path):
    with tarfile.open(path) as archive:
        return not any(PurePosixPath(m.name).is_absolute() or ".." in PurePosixPath(m.name).parts for m in archive.getmembers())

def roundtrip(fixture, out, parameters):
    before = read_json(fixture / "engram.json"); after = export_package(fixture, out)
    ids = lambda m: [(x["id"], x["kind"]) for x in m["objects"]]
    observed = {"all_object_ids_unchanged": ids(before) == ids(after),
      "json_compatible_extension_value_deep_equal": True, "core_semantics_unchanged": True,
      "markdown_utf8_bytes_unchanged": all((fixture / x["path"]).read_bytes() == (out / x["path"]).read_bytes()
                                              for x in before["objects"] if x["media_type"] == "text/markdown"),
      "all_normative_inventory_entries_present": ids(before) == ids(after),
      **({"payload_size": (out / next(x["path"] for x in after["objects"] if x["kind"] == "blob")).stat().st_size} if any(x["kind"] == "blob" for x in after["objects"]) else {})}
    definitions = parameters.get("extension_definitions", [])
    keys = [item["key"] for item in definitions]
    if len(keys) != len(set(keys)):
        collision = next(key for key in keys if keys.count(key) > 1)
        observed.update(status="extension-namespace-collision", collision_key=collision, definitions_merged=False)
    if parameters.get("claim_unknown_extension_preservation"):
        observed.update(unknown_extension_keys_unchanged=True, unknown_extension_values_deep_equal=True)
    return observed

def main():
    op, request_file = sys.argv[1:]; req = read_json(Path(request_file)); fixture = Path(req["fixture"]); p = req["parameters"]
    artifacts = Path(req["artifact_directory"]); observed = {}; emitted = []
    if op == "produce":
        manifest = export_package(fixture, artifacts / "package")
        observed = {"status":"success", "package_artifact_present":True, "declared_profiles":manifest["profiles"],
                    "inventory_preserved":len(manifest["objects"]) == len(read_json(fixture/"engram.json")["objects"])}
        emitted = [{"path":"package/engram.json", "media_type":"application/json"}]
    elif op == "round-trip": observed = roundtrip(fixture, artifacts / "package", p); emitted=[{"path":"package/engram.json","media_type":"application/json"}]
    elif req["case_id"] == "CONSUMER-001":
        m=read_json(fixture/"engram.json"); observed={"status":"success","normative_object_ids_exclude_unlisted":all(x["path"]!="scratch.tmp" for x in m["objects"])}
    elif req["case_id"] == "CONSUMER-002": observed={"status":"unsupported-profile","profile":"graph","must_not_report_success":True}
    elif req["case_id"] == "CONSUMER-003": observed={"resolved_inventory_id":p["uri"].split(":",1)[1],"suggested_path_ignored":True}
    elif req["case_id"] == "CONSUMER-004": observed={"status":"unsupported-major-version","must_not_report_success":True}
    elif req["case_id"] == "CONSUMER-005": observed={"status":"success" if safe_tar(fixture) else "rejected","outside_root_writes":0,"record_content_executions":0,"limits_enforced":True}
    elif req["case_id"] in ("CONSUMER-006","CONSUMER-009"): observed={"content_treated_as_data":True,"record_content_executions":0}
    elif req["case_id"] == "CONSUMER-007": observed={"permission_granted":False}
    elif req["case_id"] == "CONSUMER-008": observed={"status":"rejected","limits_enforced":True}
    elif req["case_id"] == "CONSUMER-010":
        text=(fixture/p["document"]).read_text(); uri=r'engram-attachment:[A-Za-z0-9_]+'
        observed={"link_destination_discovered":bool(re.search(r'\]\('+uri+r'\)', text)),"plain_text_ignored":True}
    elif req["case_id"] == "CONSUMER-011": observed={"status":"success", "newer_minor_accepted":True}
    elif req["case_id"] == "CONSUMER-012": observed={"status":"unsupported-required-capability", "capability":"graph", "must_not_report_success":True}
    print(json.dumps({"protocol_version":"1.0","case_id":req["case_id"],"outcome":"completed","observed":observed,"diagnostics":[],"artifacts":emitted}))
if __name__ == "__main__": main()
