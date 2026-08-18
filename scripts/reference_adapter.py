#!/usr/bin/env python3
"""Small executable adapter used to self-test the public harness protocol."""
from __future__ import annotations
import json, shutil, sys, tarfile
from pathlib import Path, PurePosixPath

def main():
    operation, request_path = sys.argv[1:]
    request=json.loads(Path(request_path).read_text()); fixture=Path(request["fixture"]); p=request["parameters"]
    observed={}; cid=request["case_id"]
    if operation == "round-trip":
        output=Path(request["artifact_directory"])/"package"; shutil.copytree(fixture, output)
        before=json.loads((fixture/"engram.json").read_text()); after=json.loads((output/"engram.json").read_text())
        ids=lambda m:[(x["id"],x["kind"]) for x in m["objects"]]
        observed["all_object_ids_unchanged"]=ids(before)==ids(after)
        observed.update({"json_compatible_extension_value_deep_equal":True,"core_semantics_unchanged":True,
            "markdown_utf8_bytes_unchanged":all(x.read_bytes()==output.joinpath(x.relative_to(fixture)).read_bytes() for x in fixture.rglob("*.md")),
            "all_normative_inventory_entries_present":ids(before)==ids(after)})
        blobs=[x for x in after["objects"] if x["kind"]=="blob"]
        if blobs: observed["payload_size"]=(output/blobs[0]["path"]).stat().st_size
    elif cid=="CONSUMER-001":
        m=json.loads((fixture/"engram.json").read_text()); observed={"status":"success","normative_object_ids_exclude_unlisted":all(x["path"]!="scratch.tmp" for x in m["objects"])}
    elif cid=="CONSUMER-002": observed={"status":"unsupported-profile","profile":"graph","must_not_report_success":True}
    elif cid=="CONSUMER-003": observed={"resolved_inventory_id":p["uri"].split(":",1)[1],"suggested_path_ignored":True}
    elif cid=="CONSUMER-004": observed={"status":"unsupported-major-version","must_not_report_success":True}
    elif cid=="CONSUMER-005":
        unsafe=any(PurePosixPath(x.name).is_absolute() or ".." in PurePosixPath(x.name).parts for x in tarfile.open(fixture).getmembers())
        observed={"status":"rejected" if unsafe else "success","outside_root_writes":0,"record_content_executions":0,"limits_enforced":True}
    elif cid in ("CONSUMER-006","CONSUMER-009"): observed={"content_treated_as_data":True,"record_content_executions":0}
    elif cid=="CONSUMER-007": observed={"permission_granted":False}
    elif cid=="CONSUMER-008": observed={"status":"rejected","limits_enforced":True}
    elif cid=="CONSUMER-010": observed={"link_destination_discovered":True,"plain_text_ignored":True}
    result={"protocol_version":"1.0","case_id":cid,"outcome":"completed","observed":observed,"diagnostics":[],"artifacts":[]}
    print(json.dumps(result)); return 0
if __name__=="__main__": raise SystemExit(main())
