# Decision 9: Migration outcome reporting

- **Status:** deferred
- **Outcome:** Defer the machine-readable preserved/transformed/omitted/unsupported/failed report and cross-standard loss claims to the **Migration Specification**. Core 1.0 retains deterministic unsupported-profile reporting.

## Rationale and compatibility

A report vocabulary without defined transformations would make “lossless” claims incomparable. Core conformance can still require observable unsupported results and conditional preservation without claiming migration equivalence.

## Affected requirements and schemas

`REQ-CONF-001` through `REQ-CONF-003`, `REQ-EXT-002`; [SPEC §11](../../SPEC.md#11-profiles-and-conformance), [consumer vectors](../../tests/vectors/consumer.json), and [round-trip vectors](../../tests/vectors/round-trip.json). No report schema is added.

## Acceptance criteria and evidence

- **Satisfied for core scope:** [SPEC §11](../../SPEC.md#11-profiles-and-conformance) separates processing support, preservation claims, and round-trip roles; it makes no generic “imported” or cross-standard “lossless” claim.
- **Inapplicable by scope:** report version/profile metadata, per-object diagnostics, transformations, and fatality fields belong to the named future specification.
- **Inapplicable by scope:** lossy-conversion report fixtures belong to that specification. Unknown-extension, unsupported-profile, and unresolved-reference core behavior remains covered by [`extension-preservation`](../../tests/valid/extension-preservation), `CONSUMER-002`, and [`partial-external`](../../tests/valid/partial-external).
- **Satisfied:** `REQ-CONF-003` plus `CONSUMER-002` requires deterministic unsupported-profile reporting; [rationale](../rationale.md#current-state-history-and-migration-rationale) rejects broad losslessness advertising.

## Linked changes

Core evidence is [SPEC](../../SPEC.md), [conformance](../conformance.md), [traceability](../traceability.md), and the behavioral vectors above. A future report must use a separate versioned schema.
