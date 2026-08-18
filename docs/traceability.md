# Normative requirement traceability

This matrix is the authoritative mapping from stable requirement IDs in
[`SPEC.md`](../SPEC.md) to focused fixtures or observable behavioral vectors.
`docs/requirements.json` is the machine-readable requirement catalog. A
conformance result SHOULD be a JSON object with `spec_version`, `implementation`,
`role`, and a `results` array whose entries contain `requirement`, `status`
(`pass`, `fail`, `unsupported`, or `not-applicable`), and optional `evidence`.

| Requirement(s) | Fixture or automated assertion |
|---|---|
| REQ-ENC-001, REQ-ENC-003 | `invalid/invalid-json-utf8`; validator UTF-8 decode assertion; `valid/unicode-content`; `ROUNDTRIP-004` |
| REQ-ENC-002 | `invalid/duplicate-json-key` and `invalid/duplicate-yaml-key` |
| REQ-PATH-001, REQ-PATH-002 | `invalid/unsafe-path`, `invalid/unsafe-absolute-path`, `invalid/unsafe-backslash-path`; schema and `safe_path` assertions |
| REQ-PATH-003 | `CONSUMER-005` (zero outside-root writes) |
| REQ-TIME-001 | `invalid/malformed-timestamp` |
| REQ-ID-001 | JSON Schema assertion exercised by every fixture |
| REQ-ID-002 | `invalid/id-collision` |
| REQ-ID-003, REQ-ID-004 | `ROUNDTRIP-001` and `ROUNDTRIP-002` |
| REQ-MAN-001 | Missing-manifest automated assertion in `scripts/validate.py` |
| REQ-INV-001 | Manifest JSON Schema assertion |
| REQ-INV-002 | `invalid/broken-reference` |
| REQ-INV-003 | `invalid/object-id-mismatch` |
| REQ-INV-004 | `invalid/id-collision`; `valid/zero-byte-attachment` tests the blob exception |
| REQ-INV-005 | `ROUNDTRIP-005` |
| REQ-INV-006 | `CONSUMER-001` |
| REQ-REC-001, REQ-REC-002 | Record parser and JSON Schema assertions; all record fixtures |
| REQ-REC-003 | `valid/all-record-types`; schema conditional assertion |
| REQ-REF-001 | `invalid/broken-reference`; `valid/partial-external` |
| REQ-REF-002 | `invalid/hierarchy-cycle` |
| REQ-GRAPH-001 | `valid/partial-external` plus cross-file resolver assertion |
| REQ-GRAPH-002 | `invalid/duplicate-graph-ids`, `invalid/duplicate-graph-edge-ids`, and `invalid/unresolved-edge-endpoint` |
| REQ-MEDIA-001 | `invalid/missing-attachment-payload`, `invalid/attachment-size-mismatch`, `invalid/attachment-hash-mismatch`, and `valid/zero-byte-attachment` |
| REQ-MEDIA-002 | `invalid/missing-blob-inventory` |
| REQ-MEDIA-003 | `CONSUMER-003` |
| REQ-EXT-001 | `invalid/invalid-extension-name` |
| REQ-EXT-002 | `invalid/unknown-core-field`; `ROUNDTRIP-003` |
| REQ-PROF-001 | Manifest JSON Schema `contains` assertion |
| REQ-PROF-002 | `invalid/missing-profile` |
| REQ-CONF-001 | Machine-readable result shape documented above |
| REQ-CONF-002 | Repository valid/invalid suite assertion |
| REQ-CONF-003 | `CONSUMER-002` |
| REQ-VERS-001 | `CONSUMER-004` |
| REQ-SEC-001 | `invalid/unsafe-path`; `CONSUMER-005` |
| REQ-SEC-002 | `CONSUMER-006` |
| REQ-SEC-003 | `CONSUMER-007` |

The repository suite also asserts that every normative `MUST`/`MUST NOT` line
has an identifier, every catalog ID occurs in this matrix, vector IDs are
unique, vector requirements exist, and each vector defines an `expected`
observable result.
