# Conformance

This document translates the normative rules in `SPEC.md` into a reviewable
checklist. In a conflict, `SPEC.md` wins.

Normative clauses have stable `REQ-*` identifiers. See the complete
[requirement-to-test matrix](traceability.md) and the
[machine-readable requirement catalog](requirements.json). The independent
[clean-room review](clean-room-review.md) records pseudocode and unresolved ambiguities.

## Package checks

- `engram.json` exists and validates against the v0.1 manifest schema.
- Every inventory path is safe, unique, and exists.
- Every normative object appears in the inventory.
- `id`, `engram_id`, and `export_id` identify the package instance, durable Engram, and export event.
- Partial packages supply selection metadata; complete packages close over every current durable source artifact.
- Object IDs are unique and agree with their inventory entries.
- Every included optional object type has its corresponding declared profile.

## Reference checks

- In a complete package, references scoped `synthetic_engram` resolve.
- A missing `synthetic_engram` target is external to a partial package; `outside_engram` means external to the Engram.
- Parent relationships are acyclic.
- Graph-node `record` references follow `record_scope`; complete-package `synthetic_engram` references resolve.
- Graph edge endpoints resolve to nodes in the same graph.

## Media checks

- Attachment metadata and payload both exist in the inventory.
- Payload byte size and SHA-256 digest match the metadata.
- Attachment URIs refer to attachment IDs rather than package paths.

## Repository fixtures

Run `python scripts/validate.py`. It validates the complete example and every
fixture in `tests/valid`, then asserts that every fixture in `tests/invalid` is
rejected. Invalid fixtures contain an `expected-error.txt` substring to ensure
they fail for the intended reason. The suite also checks catalog/traceability
coverage and the structure of the consumer and round-trip vectors in
`tests/vectors`. Unlike producer fixtures, vectors name an operation and an
observable `expected` result so implementations can report behavioral evidence.
