# Language-neutral conformance harness protocol

This protocol is the portable execution contract for the behavioral vectors in
`tests/v0.2/vectors`. An implementation under test is an **adapter executable**;
the adapter does not import repository Python code and may be written in any
language.

## Invocation

The harness invokes the command supplied by `--adapter` once per case as:

```text
ADAPTER produce|consume|round-trip REQUEST.json
```

The current vectors use `consume` and `round-trip`; `produce` is reserved for
producer vectors and has the identical transport contract.  The working
directory is an empty per-case directory. `REQUEST.json` is UTF-8 JSON with:

```json
{
  "protocol_version": "1.0",
  "case_id": "CONSUMER-001",
  "operation": "consume",
  "fixture": "/absolute/read-only/input/path",
  "artifact_directory": "/absolute/writable/output/path",
  "parameters": {},
  "supported_profiles": ["core", "graph", "media", "action"]
}
```

`fixture` is generated or copied exactly as directed by the vector's
`fixture` object. Paths in requests are absolute; adapters MUST NOT assume the
repository is their current directory. The adapter may only write beneath
`artifact_directory`. A producer places its package at `artifacts/package`; a
round trip places its exported package there. Other evidence files may be
placed below `artifacts/evidence/` and referenced by relative path.

## Result and process behavior

The adapter writes exactly one UTF-8 JSON object to standard output and may
write human-readable progress to standard error. The result is:

```json
{
  "protocol_version": "1.0",
  "case_id": "CONSUMER-001",
  "outcome": "completed",
  "observed": {"status": "success"},
  "diagnostics": [
    {"severity": "warning", "code": "EXAMPLE", "message": "text", "object_id": "optional"}
  ],
  "artifacts": [{"media_type": "application/json", "path": "evidence/report.json"}]
}
```

`outcome` is `completed`, `unsupported`, or `error`. `observed` is always an
object and contains the vector-specific machine observations. Diagnostics are
an array (possibly empty), use severity `info`, `warning`, or `error`, and have
stable implementation-defined codes. Artifact paths are safe relative paths
beneath the requested artifact directory.

Exit 0 means a well-formed result was produced (including a normative rejection
or unsupported-profile result). Exit 2 means the request or protocol is not
supported. Any other nonzero exit is an adapter failure. On timeout, malformed
JSON, a mismatched case ID/version, unsafe artifact path, undeclared artifact,
or unexpected exit, the harness fails the case. Normative rejection is data in
`observed.status`, never communicated only through an exit code.

Expected objects are matched recursively: every member and array value in
`expected` must occur with the same JSON type and value in `observed`; adapters
may return additional observations. This lets implementations provide richer
evidence without weakening common assertions.

## Running the suite

```sh
python scripts/conformance_harness.py --adapter "my-adapter"
```

The harness owns fixture materialization, limits, isolation, expected-result
assertions, and the result report. The adapter owns implementation behavior.
No adapter API depends on `scripts/validate.py`.
