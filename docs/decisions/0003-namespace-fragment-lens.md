# Decision 3: Namespace, fragment, and lens scope

- **Status:** deferred
- **Outcome:** Defer namespace membership, cross-namespace policy, fragments, and lens/query evaluation together to the **Namespace and Selection Specification**.

## Rationale and compatibility

Core has no deterministic query grammar or authorization model. Partial packages already exchange selected objects without standardizing why they were selected. Stable IDs, scoped external links, tags, and reverse-DNS extensions are compatibility hooks only; they confer neither membership nor permission.

## Affected requirements and schemas

No new core requirement or schema member is introduced. The retained hooks are [SPEC §§5, 6.1, 7, and 10](../../SPEC.md#5-identifiers), the [manifest](../../schemas/v0.1/manifest.schema.json) and [record](../../schemas/v0.1/record.schema.json) schemas, and [`partial-external`](../../tests/valid/partial-external).

## Acceptance criteria and evidence

- **Satisfied:** [SPEC terminology and future work](../../SPEC.md#14-non-goals-and-future-work) give none of the four concepts normative core semantics.
- **Inapplicable by scope:** ordering, missing-value, traversal-limit, error, and grammar-version rules apply only if a query grammar is included; none is included.
- **Satisfied:** the hooks and their non-authoritative character are documented in the [design-decision matrix](../design-decisions.md) and [security rules](../../SPEC.md#13-security-and-privacy).

## Linked changes

Current evidence is [SPEC](../../SPEC.md), [design decisions](../design-decisions.md), [record schema](../../schemas/v0.1/record.schema.json), and [partial fixture](../../tests/valid/partial-external). Future semantics must be introduced only by the named specification.
