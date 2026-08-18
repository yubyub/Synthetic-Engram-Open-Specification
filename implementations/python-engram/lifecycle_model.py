#!/usr/bin/env python3
"""Executable non-normative identity lifecycle model."""
import json, sys
from pathlib import Path

def evaluate(operation, data):
    if operation == "export-event":
        kind, previous, candidate = data["kind"], data.get("previous"), data["candidate"]
        if previous is None:
            return {"status":"valid", "engram_id_retained":False, "export_id_retained":False,
                    "package_id_changed":True, "object_ids_retained":True}
        retained = set(candidate["object_ids"]).issubset(set(previous["object_ids"])) if kind == "partial" else candidate["object_ids"] == previous["object_ids"]
        same_export = kind in ("retry", "repack")
        valid = candidate["engram_id"] == previous["engram_id"] and (candidate["export_id"] == previous["export_id"]) == same_export and candidate["package_id"] != previous["package_id"] and retained
        return {"status":"valid" if valid else "invalid", "engram_id_retained":candidate["engram_id"] == previous["engram_id"],
                "export_id_retained":candidate["export_id"] == previous["export_id"], "package_id_changed":candidate["package_id"] != previous["package_id"], "object_ids_retained":retained}
    if operation == "native-map":
        by_engram = {}
        for item in data["mappings"]: by_engram.setdefault(item["engram_id"], set()).add((item["namespace"], item["native_id"]))
        collision = next((key for key, values in by_engram.items() if len(values) > 1), None)
        return {"status":"collision", "engram_id":collision, "automatic_merge":False} if collision else {"status":"valid"}
    if operation == "reclassify":
        return {"status":"valid", "record_id":data["record_id"], "id_retained":True, "prefix_rewritten":False}
    if operation == "merge":
        return {"status":"loss-report-required", "survivor":data["survivor"], "retired":data["merged"], "ids_reassigned":False}
    if operation == "split":
        return {"status":"loss-report-required", "retained":[data["continuing"]] if data.get("continuing") else [], "new":data["created"], "old_id_reused_more_than_once":False}
    raise ValueError(operation)

if __name__ == "__main__":
    request=json.loads(Path(sys.argv[1]).read_text()); print(json.dumps(evaluate(request["operation"],request["input"]),separators=(",",":")))
