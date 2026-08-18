# Normative requirement traceability

This matrix maps every stable requirement in [`SPEC.md`](../SPEC.md) to its
schema constraint, validator assertion, fixture, vector, or review procedure.
[`requirements.json`](requirements.json) is the machine-readable catalog.
Schema validation below means the applicable file in `schemas/v0.2/`.

| Requirement(s) | Conformance evidence |
|---|---|
| REQ-ENC-001–003 | JSON/record decoders; `invalid/invalid-json-utf8`, `invalid/duplicate-json-key`, `invalid/duplicate-yaml-key`, `valid/unicode-content`; `ROUNDTRIP-004` |
| REQ-PATH-001–003 | `definitions.schema.json#/$defs/safePath`; validator `safe_path`; unsafe-path fixtures; `CONSUMER-005` |
| REQ-TIME-001 | `definitions.schema.json#/$defs/timestamp`; `invalid/malformed-timestamp` |
| REQ-ID-001–004 | `definitions.schema.json#/$defs/id`; package-wide collision check; `invalid/id-collision`; `ROUNDTRIP-001`, `ROUNDTRIP-002` |
| REQ-MAN-001 | Manifest schema validation and missing-manifest assertion |
| REQ-INV-001–006 | Manifest `objects` schema and cross-file inventory checks; broken-reference, object-ID-mismatch, ID-collision, missing-blob, and complete-omission fixtures; `CONSUMER-001`, `ROUNDTRIP-005` |
| REQ-SCOPE-001, REQ-SCOPE-003 | Manifest `partial` conditional schema constraints; partial and complete fixtures |
| REQ-SCOPE-002 | Producer review: selection metadata is not accepted as source-closure evidence |
| REQ-SCOPE-004 | `target_scope`, `parent_scope`, and `record_scope` enums/defaults in definitions, record, and graph schemas; schemas reject other members because objects are closed |
| REQ-CLOSE-001–005 | Complete-package durable-path and reference-closure assertions; `invalid/complete-omits-durable-object`; producer snapshot comparison review |
| REQ-REC-001–002 | Record parser and `record.schema.json`; all record fixtures |
| REQ-REC-003–009 | Record byte/YAML parser; malformed-delimiter, duplicate-key, YAML-tag, YAML-alias, YAML-flow, and scalar-typing fixtures |
| REQ-REC-010 | Renderer security review with unsafe Markdown/HTML input |
| REQ-REC-011 | Record schema action conditional; `valid/all-record-types` |
| REQ-REF-001 | Cross-file resolver; `invalid/broken-reference`, `invalid/complete-omits-durable-object`, `valid/partial-external` |
| REQ-REF-002 | Parent traversal; `invalid/hierarchy-cycle` |
| REQ-GRAPH-001–003 | Graph cross-file checks; duplicate-node, duplicate-edge, and unresolved-endpoint fixtures |
| REQ-MEDIA-001–002 | Attachment cross-file checks; missing payload/blob, size/hash mismatch, and zero-byte fixtures |
| REQ-MEDIA-003 | `CONSUMER-003` |
| REQ-MEDIA-004 | `CONSUMER-010` |
| REQ-EXT-001–002 | Extensions schema; invalid extension/core-field fixtures; `ROUNDTRIP-003` |
| REQ-PROF-001–002 | Manifest `profiles` schema and validator profile checks; `invalid/missing-profile` |
| REQ-CONF-001–002 | Conformance-result review and full repository valid/invalid suite |
| REQ-CONF-003–004 | `CONSUMER-002` |
| REQ-VERS-001–003 | `CONSUMER-004`, `CONSUMER-011`, `CONSUMER-012`, `ROUNDTRIP-006`, `ROUNDTRIP-007` |
| REQ-SEC-001–003 | Unsafe-path fixtures; `CONSUMER-005`, `CONSUMER-008`, `CONSUMER-009` |
| REQ-SEC-004 | `CONSUMER-006` |
| REQ-SEC-005 | `CONSUMER-007` |

A conformance result SHOULD be a JSON object with `spec_version`,
`implementation`, `role`, and a `results` array. Each result contains
`requirement`, `status` (`pass`, `fail`, `unsupported`, or `not-applicable`),
and optional `evidence`. The repository suite asserts catalog/spec equality,
traceability coverage, unique vector IDs, valid vector requirement references,
and an observable `expected` result for every vector.

## Explicit catalog coverage

The grouped ranges above expand to these catalog identifiers: `REQ-ENC-001`, `REQ-ENC-002`, `REQ-ENC-003`, `REQ-PATH-001`, `REQ-PATH-002`, `REQ-PATH-003`, `REQ-TIME-001`, `REQ-ID-001`, `REQ-ID-002`, `REQ-ID-003`, `REQ-ID-004`, `REQ-MAN-001`, `REQ-INV-001`, `REQ-INV-002`, `REQ-INV-003`, `REQ-INV-004`, `REQ-INV-005`, `REQ-INV-006`, `REQ-SCOPE-001`, `REQ-SCOPE-002`, `REQ-SCOPE-003`, `REQ-SCOPE-004`, `REQ-CLOSE-001`, `REQ-CLOSE-002`, `REQ-CLOSE-003`, `REQ-CLOSE-004`, `REQ-CLOSE-005`, `REQ-REC-001`, `REQ-REC-002`, `REQ-REC-003`, `REQ-REC-004`, `REQ-REC-005`, `REQ-REC-006`, `REQ-REC-007`, `REQ-REC-008`, `REQ-REC-009`, `REQ-REC-010`, `REQ-REC-011`, `REQ-REF-001`, `REQ-REF-002`, `REQ-GRAPH-001`, `REQ-GRAPH-002`, `REQ-GRAPH-003`, `REQ-MEDIA-001`, `REQ-MEDIA-002`, `REQ-MEDIA-003`, `REQ-MEDIA-004`, `REQ-EXT-001`, `REQ-EXT-002`, `REQ-PROF-001`, `REQ-PROF-002`, `REQ-CONF-001`, `REQ-CONF-002`, `REQ-CONF-003`, `REQ-CONF-004`, `REQ-VERS-001`, `REQ-VERS-002`, `REQ-VERS-003`, `REQ-SEC-001`, `REQ-SEC-002`, `REQ-SEC-003`, `REQ-SEC-004`, `REQ-SEC-005`.
