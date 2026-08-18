# Release-decision index

These records control the eleven v1.0 release gates in
[`open-questions.md`](../open-questions.md). They distinguish the disposition of
a capability from gate closure: an outcome may be selected while the gate stays
`open` because evidence is missing.

## Status rules

- **open**: at least one acceptance criterion lacks evidence and has not been
  made inapplicable by the selected scope.
- **accepted**: included/rejected scope is approved and every applicable
  criterion has evidence.
- **deferred**: the named future specification owns the capability, core 1.0
  excludes its semantics, compatibility hooks are documented, and every
  remaining criterion is satisfied or explicitly inapplicable.

Only a merged record can close a gate. Changes to a decision must update its
evidence and the status table in `open-questions.md` in the same pull request.
The release manager must verify **11/11 closed** here before creating a v1.0
release-candidate tag or artifact.

## Decisions

| Gate | Record | Outcome | Status |
|---:|---|---|---|
| 1 | [Core package and identifiers](0001-core-package-and-identifiers.md) | Core directory format; deterministic archives deferred | accepted |
| 2 | [Profiles and partial consumption](0002-profiles-and-partial-consumption.md) | Core plus graph/media/action optional profiles | accepted |
| 3 | [Namespace, fragment, and lens](0003-namespace-fragment-lens.md) | Namespace and Selection Specification | deferred |
| 4 | [History and current state](0004-history-and-current-state.md) | Current state in core; History and Synchronization Specification | deferred |
| 5 | [Provenance and references](0005-provenance-and-external-references.md) | Minimal external links; Data and Provenance Specification | deferred |
| 6 | [Non-narrative data](0006-non-narrative-data.md) | Data and Provenance Specification | deferred |
| 7 | [Graph interoperability](0007-graph-interoperability.md) | Topology in graph profile; languages/derivation deferred | accepted |
| 8 | [Access and authority](0008-access-and-authority.md) | Access and Authority Specification | deferred |
| 9 | [Migration reporting](0009-migration-reporting.md) | Migration Specification | deferred |
| 10 | [Versioning and extensions](0010-versioning-migration-extensions.md) | SemVer policy in core | accepted |
| 11 | [Release evidence](0011-release-evidence.md) | Evidence bar in core; branding deferred | accepted |

**Closure count: 11/11. Release approved.**
