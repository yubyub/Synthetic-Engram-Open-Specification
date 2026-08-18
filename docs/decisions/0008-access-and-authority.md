# Decision 8: Access descriptors and security claims

- **Status:** deferred
- **Outcome:** Defer portable access descriptors to the **Access and Authority Specification**. Authentication, runtime credentials, and secret material are rejected from the package format.

## Rationale and compatibility

Portable metadata cannot enforce access after export. Without subjects, resources, operations, delegation, expiry, revocation, audit, and a threat model, an access-looking field would create unsafe expectations. Partial packages and extensions are transport/preservation hooks only.

## Affected requirements and schemas

`REQ-SEC-001` through `REQ-SEC-005`, `REQ-EXT-002`; [SPEC §§6.2, 10, and 13](../../SPEC.md#13-security-and-privacy), [manifest schema](../../schemas/v0.1/manifest.schema.json), and [SECURITY.md](../../SECURITY.md).

## Acceptance criteria and evidence

- **Satisfied:** [SPEC §13](../../SPEC.md#13-security-and-privacy) prohibits permission inference; `CONSUMER-007` tests package possession and the [design decisions](../design-decisions.md) cover owner, fragments, and references.
- **Inapplicable by scope:** deny/unknown evaluation, canonical scope, revocation, and adversarial descriptor fixtures belong to the named future specification because no descriptor exists in core.
- **Satisfied:** [SPEC §6.2](../../SPEC.md#62-complete-export-closure) excludes credentials, access tokens, and sessions from normative packages.
- **Satisfied:** [architecture](../architecture.md) and [design decisions](../design-decisions.md) characterize partial packages/extensions as interchange hooks, not enforcement.

## Linked changes

Evidence is in [SPEC](../../SPEC.md), [SECURITY.md](../../SECURITY.md), [`CONSUMER-005/007`](../../tests/vectors/consumer.json), and [traceability](../traceability.md).
