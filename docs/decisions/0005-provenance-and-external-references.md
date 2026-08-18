# Decision 5: Provenance and external-reference semantics

- **Status:** deferred
- **Outcome:** Include only typed/scoped external references in core 1.0. Defer creator, source, import, derivation, authority, freshness, authenticity, signatures, and permission semantics to the **Data and Provenance Specification**.

## Rationale and compatibility

A target identity or locator does not prove who controls content or whether it is current. Core hashes provide integrity only, and `owner` is descriptive metadata. Stable IDs, links, hashes, owner metadata, and extensions preserve inputs for future provenance without acquiring trust semantics.

## Affected requirements and schemas

`REQ-REF-001`, `REQ-MEDIA-001`, `REQ-SEC-002`, and `REQ-SEC-003`; [SPEC §§7, 9, and 13](../../SPEC.md#13-security-and-privacy), [record](../../schemas/v0.1/record.schema.json), [attachment](../../schemas/v0.1/attachment.schema.json), and [manifest](../../schemas/v0.1/manifest.schema.json) schemas.

## Acceptance criteria and evidence

- **Satisfied:** [SPEC §13](../../SPEC.md#13-security-and-privacy) and [SECURITY.md](../../SECURITY.md) distinguish identity/location and integrity from authority, freshness, authenticity, and permission.
- **Inapplicable by scope:** core includes no provenance fields, so their cardinality, actor/source identifiers, timestamp rules, and fixtures belong to the named future specification.
- **Satisfied:** the security review states hashes do not authenticate and package possession does not authorize; `CONSUMER-007` in the [consumer vectors](../../tests/vectors/consumer.json) tests the latter.
- **Satisfied:** the [design-decision matrix](../design-decisions.md) identifies links, owner metadata, hashes, IDs, and extensions only as hooks.

## Linked changes

Evidence lives in [SPEC](../../SPEC.md), [SECURITY.md](../../SECURITY.md), the schemas above, [`attachment-hash-mismatch`](../../tests/invalid/attachment-hash-mismatch), and the [consumer vectors](../../tests/vectors/consumer.json).
