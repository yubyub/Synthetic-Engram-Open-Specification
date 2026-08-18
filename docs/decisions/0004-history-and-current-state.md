# Decision 4: History and current state

- **Status:** deferred
- **Outcome:** Core 1.0 exports current state. Defer revisions, deltas, tombstones, supersession, conflicts, ordering, and synchronization to the **History and Synchronization Specification**.

## Rationale and compatibility

Stable logical IDs are useful without imposing a revision system. `created_at` and `updated_at` describe the current object but never establish a total order. External or absent references do not become deletion markers. Future history objects may be preserved through profiles/extensions without changing core IDs.

## Affected requirements and schemas

`REQ-TIME-001`, `REQ-ID-003`, `REQ-ID-004`, `REQ-REF-001`; [SPEC §§6.2–7](../../SPEC.md#7-records), [record schema](../../schemas/v0.1/record.schema.json), and [round-trip vectors](../../tests/vectors/round-trip.json).

## Acceptance criteria and evidence

- **Satisfied:** current objects and unresolved targets are distinguishable; historical revision and deletion are explicitly not core states. Evidence: [SPEC §§6.2, 7, and 14](../../SPEC.md#14-non-goals-and-future-work) and [`partial-external`](../../tests/valid/partial-external).
- **Satisfied:** timestamp syntax and identity preservation are tested by [`invalid/malformed-timestamp`](../../tests/invalid/malformed-timestamp) and `ROUNDTRIP-001/002`; [rationale](../rationale.md#current-state-history-and-migration-rationale) disclaims timestamp ordering.
- **Inapplicable by scope:** deletion, resurrection, conflicts, ancestors, and compaction fixtures belong to the named future specification.
- **Satisfied:** revision, deletion, conflict-resolution, and synchronization semantics are disclaimed in [SPEC §14](../../SPEC.md#14-non-goals-and-future-work) and the [design decisions](../design-decisions.md).

## Linked changes

The decision is reflected in [SPEC](../../SPEC.md), [record schema](../../schemas/v0.1/record.schema.json), [fixtures](../../tests), and [rationale](../rationale.md). A future history schema must not reinterpret core timestamps or IDs.
