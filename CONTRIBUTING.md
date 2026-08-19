# Contributing

Engram Mesh 0.3 is seeking design review and source-adapter evidence for stable
cross-source identity, bindings, authority, typed relationships, Mesh Slices,
Lenses, and OKF interoperability.

## Proposing an Engram Mesh change

1. Describe the cross-source interoperability problem and any implementation
   evidence.
2. State whether the change affects the abstract model, canonical serialization,
   an external-format mapping, or non-normative guidance.
3. For normative changes, update root `SPEC.md` and include compatibility,
   security, ownership, and disclosure analysis.
4. Reuse OKF or another existing standard where its semantics are sufficient;
   document mappings and losses instead of duplicating fields.
5. Keep database, search, authentication, deployment, and runtime-protocol
   choices outside the portable model unless independent implementations show
   a recurring interoperability requirement.
6. Update the schema, positive/negative fixtures, expected diagnostics,
   validator, and traceability for every testable normative change.
7. Update the changelog.

## Legacy Synthetic Engram 0.2 changes

The legacy `docs/legacy/synthetic-engram-0.2/SPEC.md`, `schemas/v0.2`,
`examples/v0.2`, and `tests/v0.2` form a
separate legacy contract. A change to that line must be identified explicitly
as a 0.2 correction, keep schemas and normative prose aligned, preserve tagged
artefacts, and run the legacy validation commands described by its tooling.

Do not rename 0.2 wire fields or schema identifiers to Engram Mesh. Do not
describe repository-local adapters or self-review as independent evidence.

One logical change per pull request is preferred. By contributing, you agree
that your contributions are available under the repository's [MIT License](LICENSE).
