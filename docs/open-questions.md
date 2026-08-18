# Decisions required before 1.0

This is a release-gate list, not a catalogue of possible features. A question
is closed only by a merged decision record or normative change that meets every
acceptance criterion below. Deferral is a valid decision when the core retains
an identified compatibility hook and the specification clearly excludes the
deferred semantics.

## Release-decision status

The linked records are the auditable source for scope, evidence, and remaining
work. `accepted` and `deferred` are closed states; `open` is not. A decision
record added by an unmerged change does not close its gate. **A v1.0 release
candidate MUST NOT be created until all 11 rows are closed and the index reports
11/11 closed.**

| Gate | Decision | Status |
|---:|---|---|
| 1 | [Core package and identifier contract](decisions/0001-core-package-and-identifiers.md) | open |
| 2 | [Profiles and partial consumption](decisions/0002-profiles-and-partial-consumption.md) | open |
| 3 | [Namespace, fragment, and lens scope](decisions/0003-namespace-fragment-lens.md) | deferred |
| 4 | [History and current state](decisions/0004-history-and-current-state.md) | deferred |
| 5 | [Provenance and external references](decisions/0005-provenance-and-external-references.md) | deferred |
| 6 | [Non-narrative and operational data](decisions/0006-non-narrative-data.md) | deferred |
| 7 | [Graph interoperability](decisions/0007-graph-interoperability.md) | accepted |
| 8 | [Access descriptors and security](decisions/0008-access-and-authority.md) | deferred |
| 9 | [Migration outcome reporting](decisions/0009-migration-reporting.md) | deferred |
| 10 | [Versioning, migration, and extensions](decisions/0010-versioning-migration-extensions.md) | open |
| 11 | [Evidence and release bar](decisions/0011-release-evidence.md) | open |

## 1. Freeze the core package and identifier contract

**Decision required:** confirm or replace the ULID-based ID syntax, directory
package layout, inventory rules, UTF-8 encodings, timestamps, and
Markdown/YAML-front-matter boundary. Decide whether 1.0 standardizes an archive
media type and deterministic archive serialization or only the directory form.

**Acceptance criteria**

- Every durable object and byte-bearing payload has an unambiguous identity and
  inventory rule in `SPEC.md` and the schemas.
- Equivalent path, timestamp, YAML, and archive edge cases have normative test
  fixtures, including traversal and duplicate-key failures.
- If archives are deferred, the 1.0 text names directory interchange as the
  canonical baseline and prohibits archive-specific conformance claims.
- At least two independent implementations can exchange the complete example
  without changing stable IDs or normative content.

## 2. Freeze profiles and partial-consumption behavior

**Decision required:** confirm the `core`, `graph`, `media`, and `action`
boundaries; decide required behavior for unknown profiles, unknown inventoried
objects, unknown extensions, and references outside partial packages.

**Acceptance criteria**

- Each profile has a complete producer, consumer, and round-trip checklist.
- A fixture exists for every legal combination of declared optional profiles.
- Unsupported data produces a testable report and is never silently reported
  as successfully processed.
- Partial-package absence, an explicitly external target, and a deleted target
  cannot be confused by any normative rule.

## 3. Set namespace, fragment, and lens scope

**Decision required:** either define namespace membership, cross-namespace
links, fragment metadata, and deterministic lens evaluation for 1.0, or defer
all four to the **Namespace and Selection Specification**.

**Acceptance criteria**

- Core 1.0 uses none of these terms normatively unless schemas and deterministic
  conformance fixtures define them.
- Any included query grammar specifies ordering, missing values, graph
  traversal limits, error behavior, and a versioning mechanism.
- On deferral, stable IDs, explicit external links, tags, and namespaced
  extensions are documented as hooks without implying authorization semantics.

## 4. Define the boundary for history and current state

**Decision required:** confirm that 1.0 records are current-state exports, or
define revision identity, snapshots/deltas, tombstones, supersession,
concurrent conflicts, and change ordering. Rich history can be deferred to the
**History and Synchronization Specification**.

**Acceptance criteria**

- Importers can determine whether each record represents current state, a
  historical revision, a deletion, or an unresolved external target.
- `created_at` and `updated_at` semantics are explicit and tested; timestamps
  alone never imply a total revision order.
- Any history model has fixtures for deletion, resurrection, concurrent edits,
  unknown ancestors, and compaction without identity loss.
- On deferral, the specification explicitly disclaims revision, deletion,
  conflict-resolution, and synchronization semantics.

## 5. Decide provenance and external-reference semantics

**Decision required:** define the minimum meaning of external links and decide
whether creator, source, import, derivation, authority, authenticity, and
signature metadata enter core or move to the **Data and Provenance
Specification**.

**Acceptance criteria**

- Core clearly distinguishes target identity from location, authority,
  freshness, integrity, authenticity, and permission.
- Included provenance fields define cardinality, timestamp rules, actor/source
  identifiers, and preservation behavior in schemas and fixtures.
- Security review demonstrates that hashes or ownership metadata cannot be
  mistaken for signatures, trust, copyright, or authorization.
- On deferral, typed links, owner metadata, content hashes, stable IDs, and
  extensions are documented only as compatibility hooks.

## 6. Decide non-narrative and operational-data scope

**Decision required:** either define deterministic tabular/numeric data,
units, precision, snapshots, authoritative-source descriptors, and freshness,
or defer them together to the **Data and Provenance Specification**.

**Acceptance criteria**

- Any native data form has a schema, canonical examples, media type, numeric
  precision rules, units policy, null/missing semantics, and source timestamps.
- Snapshot and live-reference representations are distinguishable by consumers.
- On deferral, attachments and extensions are identified as opaque preservation
  hooks and no 1.0 conformance claim implies semantic understanding.

## 7. Bound graph interoperability

**Decision required:** confirm that the 1.0 graph profile covers topology and
labels only; either define layout and graph-DSL extraction or defer them to the
**Graph Languages and Derivation Specification**.

**Acceptance criteria**

- Graph fixtures cover local IDs, Engram references, external references,
  directed edges, duplicate IDs, and broken endpoints.
- The specification explicitly states whether ordering, layout, styling,
  hyperedges, ports, groups, and subgraphs carry portable meaning.
- Any DSL mapping defines a versioned grammar, deterministic extraction,
  provenance, error handling, and round-trip-loss reporting.
- On deferral, extensions can preserve application data without changing core
  topology semantics.

## 8. Resolve access descriptors and security claims

**Decision required:** keep portable access descriptors outside 1.0 or define
subjects, resources, operations, delegation, expiry, revocation, and audit
meaning in an **Access and Authority Specification**. Authentication and secret
material remain outside the package format.

**Acceptance criteria**

- No manifest field, owner value, package possession, fragment, or external
  reference can be interpreted as a grant unless a normative authority model
  and threat model exist.
- Any descriptor has deny/unknown behavior, canonical scope evaluation,
  revocation semantics, and adversarial conformance fixtures.
- Runtime credentials are never required in a portable package.
- On deferral, partial packages and extensions are described as transport and
  preservation hooks, not enforcement mechanisms.

## 9. Standardize migration outcome reporting

**Decision required:** define a machine-readable report for preserved,
transformed, omitted, unsupported, and failed content, or defer it to the
**Migration Specification**.

**Acceptance criteria**

- Claims such as “imported,” “preserved,” “lossless,” and “round trip” have
  distinct testable definitions.
- Any report identifies input/output versions and profiles, object IDs,
  diagnostics, lossy transformations, and fatal versus non-fatal outcomes.
- Fixtures exercise unknown extensions, unsupported profiles, unresolved
  references, and an intentionally lossy conversion.
- On deferral, 1.0 still requires deterministic unsupported-profile reporting
  and does not advertise cross-standard losslessness.

## 10. Complete versioning, migration, and extension policy

**Decision required:** freeze Semantic Versioning effects, schema URI
stability, required-extension behavior, and the support window for older major
versions. Decide whether a 0.x-to-1.0 migration document is required.

**Acceptance criteria**

- A table classifies representative field, validation, profile, and semantic
  changes as patch, minor, or major.
- Consumers deterministically reject unsupported major versions and report
  unsupported required features without data loss claims.
- Reverse-DNS ownership, collision handling, preservation, and promotion of an
  extension into core are documented and tested.
- A migration fixture and notes exist for every repository format version that
  the 1.0 release claims to accept.

## 11. Establish the 1.0 evidence and release bar

**Decision required:** define the validator, fixtures, interoperability report,
security review, governance approvals, and licensing checks required to remove
the experimental label. Certification branding remains deferred to the
**Certification and Branding Program** unless separately approved.

**Acceptance criteria**

- Every normative MUST and MUST NOT maps to an automated test or a documented
  manual verification procedure.
- The validator passes all valid fixtures and rejects each invalid fixture for
  its intended reason on every supported runtime.
- Two independent implementations publish an interoperability report covering
  core and every optional profile proposed for 1.0.
- Security and privacy review covers archive extraction, resource exhaustion,
  content execution, link handling, extension data, and misleading trust or
  authority claims.
- Governance records approval of the normative text, schemas, licenses,
  changelog, and known limitations; no unclosed question above is silently
  converted into a requirement.
