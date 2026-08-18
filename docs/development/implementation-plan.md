# Implementation plan for adoption feedback

**Status:** active, non-normative planning document

**Source:** [`implementation-feedback.md`](implementation-feedback.md)

**Execution:** [`implementation-backlog.md`](implementation-backlog.md) is the
maintained source of truth for task status, dependencies, and evidence.

This plan turns FB-001 through FB-021 into sequenced work with evidence gates.
It does not change Core 1.0, promise a future release, or treat documentation as
proof of a wire-format capability. Released `v1.0` schema bytes remain immutable;
normative changes follow [`docs/versioning.md`](../versioning.md).

## Intended outcomes

The work should make Synthetic Engram credible in three related roles:

1. a durable knowledge-management model that an application may use directly or
   map into its own live store;
2. a portable interchange and preservation boundary between independently
   evolving tools; and
3. a stable source layer from which human interfaces and AI systems can discover
   structure, select relevant content, and cite durable objects.

Success is measured by reproducible independent use, preservation and loss
reports, and conformance evidence—not by adding the largest possible core.

## Delivery rules

- Keep package, implementation API, retrieval behavior, authorization, and user
  interface as separate architectural layers.
- Keep Core 1.0 frozen. Publish compatible optional work in a minor release and
  incompatible work in a major release only after the required decision record.
- Start new semantics as mappings or namespaced extensions when practical.
- Require two independent consumers before accepting a new domain profile or
  protocol binding as normative.
- Report transformation and loss explicitly; do not use “lossless” without a
  fixture-backed round trip.
- Track specification, validator, reference adapter, SDK, and security maturity
  separately.
- Update the feedback register only when its stated acceptance evidence exists.

## Work sequence

### Phase 0 — Baseline, positioning, and measurable evaluation

**Feedback:** FB-001–FB-006, FB-013, FB-014, FB-017, FB-020

**Goal:** make the current boundary understandable before expanding it.

Deliverables:

- Reconcile the README, architecture, adoption, AI, licensing, and implementation
  READMEs around the three intended roles above.
- Add a maturity table that separately labels the standard, validator, reference
  adapters, production SDKs, external implementations, and security review.
- Create a short evaluator exercise and answer key covering package versus live
  store, knowledge model versus retrieval engine, implementer versus interface,
  and portability versus authorization.
- Run link checks over each audience path and include them in repository
  validation.
- Add backlog-entry and standards-proposal templates that require affected
  feedback IDs, compatibility classification, security impact, fixtures, and
  acceptance evidence. The repository backlog remains the tracking source of
  truth; no GitHub project is required.

Exit gate:

- A reader unfamiliar with the project can complete the evaluator exercise from
  the front page and linked guides; CI verifies every role-path link; maturity
  claims are consistent across the repository.

### Phase 1 — Independent pilots and implementation ergonomics

**Feedback:** FB-005, FB-009, FB-017, FB-019, FB-021

**Goal:** find repeated integration costs with real adopters before designing
more wire-format surface.

Deliverables:

- Recruit three distinct pilots: a note/project tool, an AI knowledge integration,
  and an archive or migration tool. Record maintainers, use case, supported
  profiles, dataset characteristics, and independence from this repository.
- Publish a common pilot report containing source-to-Engram mappings, unsupported
  semantics, security findings, performance observations, and export/import/edit/
  re-export results.
- Extract the restricted front-matter rules into a standalone grammar and test
  corpus. Add differential tests across the Python and Node parsers, followed by
  fuzzing and editor-diagnostic fixtures.
- Define production SDK release criteria: stable parse/validate APIs, structured
  diagnostics, resource limits, extension preservation, supported-version policy,
  security contact, packaging, and compatibility tests.
- Feed repeated pilot pain into SDK requirements or later design proposals; keep
  one-off application behavior outside the standard.

Exit gate:

- All three pilot categories have published reports; at least one implementation
  is independently maintained; parser behavior is differential-tested; SDK and
  reference-tool maturity labels are no longer conflated.

### Phase 2 — Identity and package lifecycle guidance

**Feedback:** FB-010, FB-011

**Goal:** make imports and repeated exports predictable before adding profiles
that depend on richer identity.

Deliverables:

- Publish an identity-mapping guide for native UUIDs and URIs, alias tables,
  deterministic import maps, collisions, reclassification, merge, split, and
  source-system re-import.
- Add lifecycle examples and conformance vectors for first export, retry of the
  same export event, repackaging, a later snapshot, partial export, and re-export
  by a second implementation.
- Specify application logging and deduplication recommendations without implying
  revision or synchronization semantics.
- Prototype an optional global identifier only if the pilots show that alias
  tables cannot preserve identity adequately; record compatibility and privacy
  consequences in a decision record.

Exit gate:

- Python, Node, and at least one independent implementation produce the expected
  identities for every lifecycle vector; any schema proposal has an explicit
  minor/major compatibility decision.

### Phase 3 — Deterministic archive and preservation work

**Feedback:** FB-012 and the preservation part of FB-018

**Goal:** define safe, reproducible one-file exchange without pretending that an
archive alone is a preservation system.

Deliverables:

- Write an archive-binding decision record comparing candidate formats and
  selecting media type, canonical entry order, timestamps and metadata, Unicode
  path handling, links, duplicates, compression, and resource limits.
- Implement deterministic pack/unpack in both repository implementations and add
  adversarial fixtures for traversal, duplicate paths, decompression bombs,
  member counts, malformed metadata, and cross-platform path behavior.
- Publish mappings and declared losses for BagIt, OCFL, and RO-Crate; run one
  preservation pilot with fixity verification and recovery.
- Establish a documented mirror process for immutable schemas, checksums,
  releases, and validator source. Keep signing as an external binding with its
  own threat model.

Exit gate:

- Independently generated archives are byte-identical for canonical fixtures;
  two implementations safely unpack each other's output; the preservation pilot
  and loss-aware mappings are public.

### Phase 4 — Provenance, mappings, and domain profiles

**Feedback:** FB-007, FB-015, FB-016, FB-018

**Goal:** expand meaning through small, independently implementable profiles that
reuse established vocabularies.

Deliverables:

- Define profile governance: problem statement, vocabulary review, ownership of
  fields, threat model, schema, examples, migration behavior, mappings,
  conformance fixtures, and two-consumer evidence are mandatory.
- Design provenance first. Cover authored, generated, derived, corrected, and
  human-adopted knowledge; map explicitly to PROV-O and preserve source IDs,
  agents, activity, time, and declared transformation or loss.
- Publish loss-aware graph mappings to JSON-LD/RDF and at least one established
  property-graph exchange format. Describe Core graphs consistently as portable
  directed topology, not a general ontology.
- Use pilot demand to order domain-profile proposals for people, organizations,
  sources/citations, events, conversations, bookmarks, datasets, claims,
  observations, decisions, collections, and user-defined semantic types.
- For action/event work, evaluate iCalendar/VTODO mappings before inventing new
  fields. Reject or defer profiles that lack two independent consumers.

Exit gate:

- The provenance profile and each accepted domain profile meet profile governance
  requirements; every mapping publishes semantic scope and losses with executable
  round-trip fixtures.

### Phase 5 — Extensible profile negotiation and versioned release

**Feedback:** FB-008 plus schema-dependent results from FB-010 and Phase 4

**Goal:** allow third-party profile evolution without weakening required
processing or preservation behavior.

Deliverables:

- Specify namespaced profile identifiers and separate required processing from
  optional or advisory declarations.
- Define discovery, collision, unknown-profile preservation, failure reporting,
  and round-trip behavior.
- Test old consumer/new package and new consumer/old package combinations,
  including unknown required and advisory profiles.
- Publish the compatibility analysis, decision record, new immutable schema URI,
  migration guide, conformance fixtures, and supported-release changes.

Exit gate:

- The release classification is approved under `docs/versioning.md`; two
  independent implementations pass the negotiation matrix; no `v1.0` schema
  bytes or identifiers have changed.

### Phase 6 — Remote/API documentation and binding evidence gate

**Feedback:** FB-006, FB-014, and the MCP part of FB-018

**Goal:** determine whether independent tools need a shared request contract in
addition to package interchange.

This is a separate binding track, not an expansion of the durable knowledge
model. Until independent demand meets its gate, the project publishes guidance
only and implementations expose APIs suited to their applications.

Deliverables:

- Publish a non-normative transport-neutral vocabulary for capability discovery,
  manifest and metadata overview, stable-ID and batch retrieval, graph listing
  and traversal, explicit selection, attachment access, and partial-package
  delivery.
- Describe pagination, limits, freshness/version tokens, structured errors,
  source citations, and loss reporting as application concerns. Keep
  authentication and authorization host-specific and require authorization for
  every returned object.
- Describe HTTP and MCP delivery patterns without defining endpoints, request
  schemas, or conformance claims. Do not standardize embedding models,
  semantic-search ranking, chunking, prompts, model context budgets, or autonomous
  write policy.
- Collect concrete incompatibility reports from at least two independent stores
  and two clients before beginning prototypes. Include AI bootstrap, human web UI,
  graph browser, and bounded export rather than assuming one client type.
- Only after that evidence exists, compare independent prototypes and consider a
  normative optional binding if shared operations remain stable across transports.
- Evaluate a derived-context profile separately and only when clients must
  exchange derived chunks rather than retrieve durable records. It must retain
  source IDs, derivation, loss, freshness, and authorization scope.

Exit gate:

- Guidance is explicit about its non-normative status. Prototype and normative
  work remains blocked until two independent stores and two clients demonstrate
  repeated integration cost; later threat-model and interoperability reports
  determine whether to standardize, revise, or stop.

### Phase 7 — Adoption-triggered governance

**Feedback:** FB-001, FB-019, FB-021

**Goal:** align governance and claims with the ecosystem that actually exists.

This phase runs throughout the others. At each independent implementation,
production adopter, or second-maintainer-organization milestone:

- review maintainer representation and invite qualified independent maintainers;
- record recusals and release-signoff independence;
- consider forming a compatibility review group;
- reassess whether a neutral standards or open-source home is warranted; and
- retain “candidate open standard” until the evidence threshold in FB-001 is met.

Exit gate:

- Governance decisions and appointments are public; adoption claims link to
  external evidence; changing the maturity qualifier requires at least two
  external products and maintainers, not repository-local implementations.

## Feedback-to-work crosswalk

| Feedback | Primary phase | Completion evidence |
| --- | --- | --- |
| FB-001 | 0 and 7 | Consistent maturity wording; external product and maintainer threshold |
| FB-002 | 0 | Evaluator exercise demonstrates boundary comprehension |
| FB-003 | 0 | CI-checked audience paths |
| FB-004 | 0 | Security boundary wording and future adversarial authority tests |
| FB-005 | 0 and 1 | Responsibility tables, SDK criteria, external integration feedback |
| FB-006 | 0 and 6 | Current boundary documented; demand-backed binding decision |
| FB-007 | 4 | Profile governance and two-consumer evidence per profile |
| FB-008 | 5 | Versioned negotiation schema, migration notes, and fixtures |
| FB-009 | 1 | Grammar, differential corpus, fuzzing, SDKs, editor diagnostics |
| FB-010 | 2 and 5 | Mapping guide, lifecycle fixtures, and any versioned ID decision |
| FB-011 | 2 | Lifecycle guide and retry/repack vectors |
| FB-012 | 3 | Deterministic binding, safety suite, pilot, mappings, mirror |
| FB-013 | 0 | Package-native guidance and demand decision for a reference app |
| FB-014 | 0 and 6 | AI pipeline guidance and evidence-gated derived-context decision |
| FB-015 | 4 | Provenance profile, threat model, PROV mapping, two implementations |
| FB-016 | 4 | Topology terminology and loss-aware graph mapping reports |
| FB-017 | 0 and 1 | Separate maturity labels and production SDK evidence |
| FB-018 | 3, 4, and 6 | Versioned mappings, fixtures, reports, and community review |
| FB-019 | 1 and 7 | Adoption-triggered appointments and governance decisions |
| FB-020 | 0 | Consistent licensing explanation and adopter legal-review caveat |
| FB-021 | 1 and 7 | Three external adopter reports and independent implementations |

## Tracking and review cadence

Use one public issue or project item per deliverable and label it with every
applicable `FB-*` ID. Each phase review records:

- deliverables completed and links to evidence;
- interoperability, security, compatibility, and maintenance findings;
- feedback-register status changes justified by that evidence;
- work deliberately deferred or rejected and its rationale; and
- the next phase whose entry conditions are now met.

Phases describe dependency order, not calendar commitments. Phase 0 can close
quickly; pilot recruitment, independent implementations, and normative bindings
remain evidence-gated and should not be assigned dates until participants exist.
