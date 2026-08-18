# Adoption-feedback execution backlog

**Status:** active, non-normative source of truth

This backlog executes the [implementation plan](implementation-plan.md). A task
is complete only when its acceptance condition is met and its evidence is linked.
Documentation never counts as evidence for a wire-format capability.

## Workflow

Allowed statuses are `ready`, `active`, `blocked-external`, `blocked-decision`,
`deferred`, `complete`, and `rejected`. Work the next dependency-independent
`ready` task; do not assign dates to externally blocked work. Each pull request
implements one logical deliverable and updates this backlog and the
[feedback register](implementation-feedback.md) when its evidence changes a
feedback status.

### Backlog-entry template

```markdown
### TASK-NNN — Short outcome

- **Phase:** 0–7
- **Feedback:** FB-NNN, FB-NNN
- **Status:** ready
- **Depends on:** none
- **Owner:** unassigned
- **Deliverable:** Observable result.
- **Acceptance:** Reproducible condition for completion.
- **Evidence:** none
```

### Standards-proposal checklist

A normative proposal must identify the interoperability problem, affected
requirements and profiles, compatibility classification, security and privacy
impact, established vocabularies considered, schema and prose changes, examples,
valid and invalid fixtures, migration behavior, implementation evidence, and
every related `FB-*` and `TASK-*` identifier. It remains `blocked-decision` until
approved under [governance](../../GOVERNANCE.md).

## Phase 0 — Baseline and positioning

### TASK-001 — Establish the execution backlog

- **Phase:** 0
- **Feedback:** FB-003, FB-017
- **Status:** complete
- **Depends on:** none
- **Owner:** maintainers
- **Deliverable:** Machine-checked execution source of truth.
- **Acceptance:** Every task has valid metadata, dependencies, and evidence rules.
- **Evidence:** [`implementation-backlog.md`](implementation-backlog.md), [`scripts/validate.py`](../../scripts/validate.py)

### TASK-002 — Position the three intended roles consistently

- **Phase:** 0
- **Feedback:** FB-001, FB-002, FB-004, FB-006, FB-013, FB-014, FB-020
- **Status:** complete
- **Depends on:** TASK-001
- **Owner:** maintainers
- **Deliverable:** Knowledge management, interchange, and AI source-layer wording.
- **Acceptance:** README and implementation guides preserve the package, API, retrieval, and security boundaries.
- **Evidence:** [`README.md`](../../README.md), [`architecture.md`](../architecture.md), [`adoption-guide.md`](../adoption-guide.md), [`ai-integration.md`](../ai-integration.md)

### TASK-003 — Publish component maturity separately

- **Phase:** 0
- **Feedback:** FB-001, FB-017, FB-021
- **Status:** complete
- **Depends on:** TASK-002
- **Owner:** maintainers
- **Deliverable:** Component-by-component maturity matrix.
- **Acceptance:** Reference tools are not labelled production SDKs and repository implementations are not counted as external adoption.
- **Evidence:** [`status.md`](../status.md)

### TASK-004 — Add a five-minute evaluator exercise

- **Phase:** 0
- **Feedback:** FB-002, FB-003, FB-004, FB-006, FB-014
- **Status:** complete
- **Depends on:** TASK-002
- **Owner:** maintainers
- **Deliverable:** Evaluator questions and answer rubric.
- **Acceptance:** The rubric distinguishes package, live store, retrieval, interface, and authority boundaries.
- **Evidence:** [`evaluator-exercise.md`](evaluator-exercise.md)

### TASK-005 — Keep audience links checked in CI

- **Phase:** 0
- **Feedback:** FB-003
- **Status:** complete
- **Depends on:** TASK-001
- **Owner:** maintainers
- **Deliverable:** Repository-wide local Markdown-link validation.
- **Acceptance:** Broken local links fail the standard CI validation job.
- **Evidence:** [`scripts/validate.py`](../../scripts/validate.py), [validation workflow](../../.github/workflows/validate.yml)

## Phase 1 — Pilots and implementation ergonomics

### TASK-101 — Publish the independent-pilot report contract

- **Phase:** 1
- **Feedback:** FB-005, FB-019, FB-021
- **Status:** complete
- **Depends on:** TASK-001
- **Owner:** maintainers
- **Deliverable:** Common report template for all three pilot categories.
- **Acceptance:** Reports identify independence, mappings, loss, security, performance, and round-trip evidence.
- **Evidence:** [`pilot-report-template.md`](pilot-report-template.md)

### TASK-102 — Recruit and complete three independent pilots

- **Phase:** 1
- **Feedback:** FB-001, FB-005, FB-019, FB-021
- **Status:** blocked-external
- **Depends on:** TASK-101
- **Owner:** external adopters
- **Deliverable:** Note/project, AI-knowledge, and archive/migration pilot reports.
- **Acceptance:** Three public reports exist and at least one implementation is independently maintained.
- **Evidence:** none

### TASK-103 — Define production SDK release criteria

- **Phase:** 1
- **Feedback:** FB-005, FB-009, FB-017
- **Status:** complete
- **Depends on:** TASK-001
- **Owner:** maintainers
- **Deliverable:** Release and maintenance criteria for future SDKs.
- **Acceptance:** Criteria cover API stability, diagnostics, limits, preservation, compatibility, packaging, and security response.
- **Evidence:** [`sdk-release-criteria.md`](sdk-release-criteria.md)

### TASK-104 — Publish and differentially test front matter

- **Phase:** 1
- **Feedback:** FB-005, FB-009, FB-017
- **Status:** complete
- **Depends on:** TASK-103
- **Owner:** maintainers
- **Deliverable:** Grammar, parser contract, corpus, two parsers, and deterministic property tests.
- **Acceptance:** Python and Node return identical values or diagnostic categories for every test.
- **Evidence:** [`front-matter.md`](../front-matter.md), [`tests/front-matter`](../../tests/front-matter), [`scripts/run_frontmatter_tests.py`](../../scripts/run_frontmatter_tests.py)

### TASK-105 — Obtain independent parser evidence

- **Phase:** 1
- **Feedback:** FB-009, FB-021
- **Status:** blocked-external
- **Depends on:** TASK-104
- **Owner:** external implementer
- **Deliverable:** A third-party parser report using the shared corpus.
- **Acceptance:** An independently maintained runtime passes the corpus and publishes diagnostics for any divergence.
- **Evidence:** none

### TASK-106 — Assess JSON front matter

- **Phase:** 1
- **Feedback:** FB-009
- **Status:** complete
- **Depends on:** TASK-104
- **Owner:** maintainers
- **Deliverable:** Compatibility and ergonomics assessment.
- **Acceptance:** The assessment records why Core 1.0 remains unchanged and what evidence could reopen the question.
- **Evidence:** [`json-front-matter-assessment.md`](json-front-matter-assessment.md)

## Phase 2 — Identity and lifecycle

### TASK-201 — Publish identity and export lifecycle guidance

- **Phase:** 2
- **Feedback:** FB-010, FB-011
- **Status:** complete
- **Depends on:** TASK-104
- **Owner:** maintainers
- **Deliverable:** Native-ID mapping and lifecycle rules with executable vectors.
- **Acceptance:** Python and Node agree on first export, retry, repack, snapshot, partial, re-export, collision, reclassification, merge, and split cases.
- **Evidence:** [`identity-lifecycle.md`](../identity-lifecycle.md), [`tests/lifecycle`](../../tests/lifecycle), [`scripts/run_lifecycle_tests.py`](../../scripts/run_lifecycle_tests.py)

### TASK-202 — Validate lifecycle behavior independently

- **Phase:** 2
- **Feedback:** FB-010, FB-011, FB-021
- **Status:** blocked-external
- **Depends on:** TASK-201, TASK-102
- **Owner:** external implementer
- **Deliverable:** Independent lifecycle-vector result.
- **Acceptance:** A third implementation produces every expected identity decision.
- **Evidence:** none

### TASK-203 — Decide whether a global identifier is necessary

- **Phase:** 2
- **Feedback:** FB-010
- **Status:** deferred
- **Depends on:** TASK-202
- **Owner:** maintainers
- **Deliverable:** Evidence-based identity decision record.
- **Acceptance:** Pilot evidence demonstrates that documented alias maps are insufficient, or the proposal is rejected.
- **Evidence:** none

## Phase 3 — Archive and preservation

### TASK-301 — Assess archive formats and threats

- **Phase:** 3
- **Feedback:** FB-012, FB-018
- **Status:** complete
- **Depends on:** TASK-001
- **Owner:** maintainers
- **Deliverable:** Format comparison, threat model, and decision inputs.
- **Acceptance:** Determinism, metadata, paths, links, duplicates, compression, and limits are covered without selecting a binding.
- **Evidence:** [`archive-format-assessment.md`](archive-format-assessment.md)

### TASK-302 — Approve an archive binding

- **Phase:** 3
- **Feedback:** FB-012
- **Status:** blocked-decision
- **Depends on:** TASK-301
- **Owner:** governance
- **Deliverable:** Approved archive-binding decision record.
- **Acceptance:** Compatibility, media type, threat model, canonical bytes, and fixtures are approved publicly.
- **Evidence:** none

### TASK-303 — Implement the approved archive binding twice

- **Phase:** 3
- **Feedback:** FB-012
- **Status:** deferred
- **Depends on:** TASK-302
- **Owner:** unassigned
- **Deliverable:** Independent Python and Node pack/unpack implementations and adversarial fixtures.
- **Acceptance:** Canonical archives are byte-identical and each implementation safely consumes the other.
- **Evidence:** none

### TASK-304 — Publish preservation mappings and mirror procedure

- **Phase:** 3
- **Feedback:** FB-012, FB-018
- **Status:** complete
- **Depends on:** TASK-301
- **Owner:** maintainers
- **Deliverable:** BagIt, OCFL, and RO-Crate mapping plans plus immutable mirror procedure.
- **Acceptance:** Every mapping declares scope and loss; the procedure verifies bytes and checksums.
- **Evidence:** [`preservation-mappings.md`](../preservation-mappings.md), [`schema-mirroring.md`](../schema-mirroring.md)

### TASK-305 — Complete a preservation pilot and institutional mirror

- **Phase:** 3
- **Feedback:** FB-012, FB-018, FB-021
- **Status:** blocked-external
- **Depends on:** TASK-302, TASK-304
- **Owner:** external preservation partner
- **Deliverable:** Public recovery report and independently administered mirror.
- **Acceptance:** Fixity verification and recovery are reproduced outside this repository.
- **Evidence:** none

## Phase 4 — Provenance, mappings, and profiles

### TASK-401 — Publish profile governance

- **Phase:** 4
- **Feedback:** FB-007, FB-015, FB-018
- **Status:** complete
- **Depends on:** TASK-001
- **Owner:** maintainers
- **Deliverable:** Evidence and review requirements for every future profile.
- **Acceptance:** No profile can be accepted without security, mappings, fixtures, migration, and two consumers.
- **Evidence:** [`profile-governance.md`](../profile-governance.md)

### TASK-402 — Draft provenance and PROV-O mapping

- **Phase:** 4
- **Feedback:** FB-015, FB-018
- **Status:** complete
- **Depends on:** TASK-401
- **Owner:** maintainers
- **Deliverable:** Non-normative provenance proposal and loss-aware mapping.
- **Acceptance:** Authored, generated, derived, corrected, and adopted knowledge remain distinguishable.
- **Evidence:** [`provenance-profile-proposal.md`](provenance-profile-proposal.md)

### TASK-403 — Approve and implement a provenance profile

- **Phase:** 4
- **Feedback:** FB-015
- **Status:** blocked-external
- **Depends on:** TASK-402, TASK-102
- **Owner:** governance and independent implementers
- **Deliverable:** Versioned schemas, fixtures, threat model, migration, and two implementations.
- **Acceptance:** Profile governance passes and both consumers pass the profile suite.
- **Evidence:** none

### TASK-404 — Publish graph mapping contracts

- **Phase:** 4
- **Feedback:** FB-016, FB-018
- **Status:** complete
- **Depends on:** TASK-401
- **Owner:** maintainers
- **Deliverable:** Loss-aware JSON-LD/RDF and property-graph mapping guidance.
- **Acceptance:** Core is described as directed topology and unsupported semantics are explicit.
- **Evidence:** [`graph-mappings.md`](../graph-mappings.md)

### TASK-405 — Prioritize and implement domain profiles

- **Phase:** 4
- **Feedback:** FB-007, FB-018, FB-021
- **Status:** blocked-external
- **Depends on:** TASK-102, TASK-401
- **Owner:** adopters and governance
- **Deliverable:** Pilot-prioritized, independently implemented domain profiles.
- **Acceptance:** Each accepted profile passes profile governance with two consumers.
- **Evidence:** none

## Phase 5 — Profile negotiation and release

### TASK-501 — Draft namespaced profile negotiation

- **Phase:** 5
- **Feedback:** FB-008
- **Status:** complete
- **Depends on:** TASK-401
- **Owner:** maintainers
- **Deliverable:** Non-normative compatibility proposal for required and advisory profiles.
- **Acceptance:** Discovery, collisions, unknown profiles, preservation, failure reporting, and migration are addressed without changing v1.0.
- **Evidence:** [`profile-negotiation-proposal.md`](profile-negotiation-proposal.md)

### TASK-502 — Approve a versioned negotiation release

- **Phase:** 5
- **Feedback:** FB-008, FB-010
- **Status:** blocked-external
- **Depends on:** TASK-501, TASK-102
- **Owner:** governance and independent implementers
- **Deliverable:** Approved release classification, schemas, migration, and negotiation matrix.
- **Acceptance:** Two independent implementations pass old/new compatibility tests and v1.0 bytes remain unchanged.
- **Evidence:** none

## Phase 6 — Remote delivery discovery

### TASK-601 — Publish a non-normative remote-delivery pattern

- **Phase:** 6
- **Feedback:** FB-006, FB-014, FB-018
- **Status:** complete
- **Depends on:** TASK-002
- **Owner:** maintainers
- **Deliverable:** Transport-neutral operation vocabulary with HTTP and MCP examples at the pattern level.
- **Acceptance:** No endpoint, request schema, retrieval algorithm, or authorization mechanism is standardized.
- **Evidence:** [`remote-delivery-pattern.md`](../remote-delivery-pattern.md)

### TASK-602 — Prototype and evaluate an optional protocol binding

- **Phase:** 6
- **Feedback:** FB-006, FB-014, FB-018, FB-021
- **Status:** blocked-external
- **Depends on:** TASK-102, TASK-601
- **Owner:** independent stores and clients
- **Deliverable:** Two stores and two clients with an interoperability report.
- **Acceptance:** Repeated API incompatibility is demonstrated before a normative proposal is opened.
- **Evidence:** none

## Phase 7 — Adoption-triggered governance

### TASK-701 — Keep maturity claims evidence-bound

- **Phase:** 7
- **Feedback:** FB-001, FB-017, FB-019, FB-021
- **Status:** complete
- **Depends on:** TASK-003
- **Owner:** maintainers
- **Deliverable:** Candidate-standard qualifier and adoption thresholds.
- **Acceptance:** Repository-local implementations are never represented as external adoption.
- **Evidence:** [`status.md`](../status.md), [`GOVERNANCE.md`](../../GOVERNANCE.md)

### TASK-702 — Run adoption-triggered governance reviews

- **Phase:** 7
- **Feedback:** FB-001, FB-019, FB-021
- **Status:** blocked-external
- **Depends on:** TASK-102
- **Owner:** governance
- **Deliverable:** Public representation, recusal, compatibility-group, and neutral-home decisions.
- **Acceptance:** Each adoption milestone has a recorded review; the maturity qualifier changes only after the FB-001 threshold.
- **Evidence:** none
