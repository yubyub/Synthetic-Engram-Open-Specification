# Decision 1: Core package and identifier contract

- **Status:** open
- **Outcome:** Include the ULID-prefixed identity, UTF-8 JSON/Markdown, YAML front matter, safe relative paths, timestamps, inventory, and directory package in core 1.0. Defer a canonical archive media type and deterministic archive serialization to the **Archive Binding Specification**.

## Rationale and compatibility

The existing directory model is inspectable and already has schemas and validator coverage. Freezing it avoids changing stable IDs or normative bytes. An archive is only a transport wrapper: core identities and paths remain valid when a future binding is introduced. Core 1.0 must not claim archive conformance; archive readers remain responsible for safe extraction.

## Affected requirements and schemas

`REQ-ENC-*`, `REQ-PATH-*`, `REQ-TIME-001`, `REQ-ID-*`, and `REQ-INV-*`; [SPEC §§4–6](../../SPEC.md#4-encoding-and-paths); [shared definitions](../../schemas/v0.1/definitions.schema.json), [manifest schema](../../schemas/v0.1/manifest.schema.json), and [record schema](../../schemas/v0.1/record.schema.json).

## Acceptance criteria and evidence

- **Satisfied:** identities and inventory are specified and schema constrained. Evidence: [SPEC §§5–6](../../SPEC.md#5-identifiers), the schemas above, and [`invalid/id-collision`](../../tests/invalid/id-collision).
- **Open:** add normative edge fixtures for all equivalent path/timestamp/YAML cases and document the coverage set; traversal and duplicate keys alone do not establish completeness. Existing evidence includes [`invalid/unsafe-path`](../../tests/invalid/unsafe-path), [`invalid/duplicate-json-key`](../../tests/invalid/duplicate-json-key), [`invalid/duplicate-yaml-key`](../../tests/invalid/duplicate-yaml-key), and [`invalid/malformed-timestamp`](../../tests/invalid/malformed-timestamp).
- **Open:** amend `SPEC.md` to name directory interchange as canonical and prohibit archive-specific conformance claims. `REQ-PATH-003` remains applicable security guidance, not an archive-format claim.
- **Open:** publish exchange evidence from two independent implementations using [`tests/valid/basic-engram`](../../tests/valid/basic-engram), with unchanged IDs and normative content.

## Linked changes required to close

Update [SPEC](../../SPEC.md), [schemas](../../schemas/README.md), [fixtures and vectors](../../tests), [traceability](../traceability.md), and the interoperability evidence required by [decision 11](0011-release-evidence.md). Do not change this status until all three open items link to merged evidence.
