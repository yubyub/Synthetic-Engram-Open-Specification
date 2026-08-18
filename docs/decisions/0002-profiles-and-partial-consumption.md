# Decision 2: Profiles and partial consumption

- **Status:** open
- **Outcome:** Include `core` in core 1.0 and retain `graph`, `media`, and `action` as optional 1.0 profiles.

## Rationale and compatibility

Capability declarations permit partial implementations without silently discarding understood semantics. Unknown declared profiles must produce an unsupported result; preservation is distinct from processing. Partial absence, `outside_engram`, and deletion remain distinct because core defines only the first two and has no deletion semantics.

## Affected requirements and schemas

`REQ-PROF-001`, `REQ-PROF-002`, `REQ-CONF-*`, `REQ-REF-001`; [SPEC §§6.1, 7, and 11](../../SPEC.md#11-profiles-and-conformance), [manifest](../../schemas/v0.1/manifest.schema.json), [record](../../schemas/v0.1/record.schema.json), [graph](../../schemas/v0.1/graph.schema.json), and [attachment](../../schemas/v0.1/attachment.schema.json) schemas.

## Acceptance criteria and evidence

- **Open:** publish complete producer, consumer, and round-trip checklists for each of the four profiles; the current [conformance checklist](../conformance.md) is object-oriented, not a complete role/profile matrix.
- **Open:** add fixtures for every legal optional-profile combination. [`basic-engram`](../../tests/valid/basic-engram) and [`empty-graph`](../../tests/valid/empty-graph) do not cover the full combination set.
- **Satisfied:** unsupported profiles cannot be silent. Evidence: `REQ-CONF-003`, [`CONSUMER-002`](../../tests/vectors/consumer.json), and [traceability](../traceability.md).
- **Satisfied:** partial absence and explicit external scope are represented separately by package completeness and reference scope; deletion is inapplicable because [decision 4](0004-history-and-current-state.md) excludes deletion semantics. Evidence: [`partial-external`](../../tests/valid/partial-external) and `REQ-REF-001`.

## Linked changes required to close

Update [conformance](../conformance.md), [fixtures](../../tests), [requirements](../requirements.json), and [traceability](../traceability.md). Close only when the role/profile matrix and exhaustive legal combinations are merged.
