# Decision 6: Non-narrative and operational data

- **Status:** deferred
- **Outcome:** Defer native tabular/numeric data, units, precision, snapshots, authoritative-source descriptors, and freshness together to the **Data and Provenance Specification**.

## Rationale and compatibility

Defining only part of this model would invite incompatible assumptions about nulls, units, precision, and live data. Core media attachments can preserve bytes and extensions can preserve application metadata, but neither claims semantic understanding.

## Affected requirements and schemas

No native-data requirement is added. Compatibility hooks are `REQ-MEDIA-*` and `REQ-EXT-*`; [SPEC §§9–10 and 14](../../SPEC.md#9-attachments), [attachment schema](../../schemas/v0.1/attachment.schema.json), and [extension definitions](../../schemas/v0.1/definitions.schema.json).

## Acceptance criteria and evidence

- **Inapplicable by scope:** native schemas, canonical examples, media type, precision, units, null/missing, and source timestamps are requirements of the named future specification.
- **Inapplicable by scope:** core contains neither snapshot nor live-reference representations, so it cannot confuse or claim to distinguish them.
- **Satisfied:** [SPEC §§9, 11, and 14](../../SPEC.md#14-non-goals-and-future-work) bound attachments to byte preservation and profile support; the [design decisions](../design-decisions.md) explicitly deny native-data semantics.

## Linked changes

The retained preservation mechanisms are the [attachment schema](../../schemas/v0.1/attachment.schema.json), [`zero-byte-attachment`](../../tests/valid/zero-byte-attachment), extension fixture [`extension-preservation`](../../tests/valid/extension-preservation), and `ROUNDTRIP-003/005` in the [round-trip vectors](../../tests/vectors/round-trip.json).
