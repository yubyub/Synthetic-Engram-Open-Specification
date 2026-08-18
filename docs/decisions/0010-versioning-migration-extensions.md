# Decision 10: Versioning, migration, and extension policy

- **Status:** accepted
- **Outcome:** Include Semantic Versioning, stable versioned schema identifiers, deterministic unsupported-major handling, and reverse-DNS extensions in core 1.0. A 0.x migration is required only if v1.0 claims to accept that repository format.

## Rationale and compatibility

Consumers need predictable rejection rather than best-effort reinterpretation. Extensions must remain preservable without changing core meaning; promotion into core cannot silently collide with existing extension ownership. Pre-1.0 formats are unstable and impose no migration burden unless the release explicitly claims them as accepted input.

## Affected requirements and schemas

`REQ-VERS-001`, `REQ-EXT-001`, `REQ-EXT-002`, `REQ-CONF-003`; [SPEC §§10–12](../../SPEC.md#12-versioning), [versioning policy](../versioning.md), all schemas under [`schemas/v0.1`](../../schemas/v0.1), and `CONSUMER-004`/`ROUNDTRIP-003` in the vectors.

## Acceptance criteria and evidence

- **Satisfied:** [versioning.md](../versioning.md) classifies schema, validation, semantic, profile, and serialization changes as patch, minor, or major.
- **Satisfied:** unsupported major versions and required capabilities have deterministic non-success outcomes through `REQ-VERS-001`, `REQ-CONF-003`, `CONSUMER-002`, and `CONSUMER-004`.
- **Satisfied:** reverse-DNS ownership, collision handling, unknown preservation, and extension-to-core promotion are normative and exercised by `ROUNDTRIP-006` and `ROUNDTRIP-007`.
- **Satisfied:** core v1.0 explicitly does not accept v0.1 input, so no migration fixture is applicable.

## Linked changes required to close

Implemented in [versioning](../versioning.md), [SPEC](../../SPEC.md), [schemas README](../../schemas/README.md), [fixtures/vectors](../../tests), [traceability](../traceability.md), and [CHANGELOG](../../CHANGELOG.md).
