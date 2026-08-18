# Implementation feedback and adoption review register

**Status:** active, non-normative development document

**Purpose:** retain constructive review findings so future work can verify that
adoption concerns were implemented, intentionally deferred, or rejected with a
recorded rationale. This file must not be treated as a change to frozen Core 1.0.

## How to use this register

For each future change, update the applicable row with a decision-record, pull
request, test, adopter report, or documentation link. A documentation statement
does not count as implementing a wire-format capability. Changes to released
schemas follow `docs/versioning.md` and require a new compatible minor or
incompatible major version as appropriate.

Status vocabulary:

- **documented** — current scope or guidance is clear, but no new normative
  capability is claimed;
- **planned** — recommended future work has not been accepted normatively;
- **evidence needed** — the design exists, but independent adoption or operational
  proof is required;
- **complete** — acceptance criteria have reproducible evidence.

## Review checklist

| ID | Constructive feedback | Recommended change and rationale | Acceptance evidence | Status |
| --- | --- | --- | --- | --- |
| FB-001 | “Open Standard” can imply established industry adoption. | Describe the work as a **candidate open standard** until independent vendors, maintainers, and products exist. Honest maturity language lowers adoption risk. | README and governance wording; at least two external products and maintainers before removing the qualifier. | documented; evidence needed |
| FB-002 | Purpose and intended use were not immediately obvious to a human reader. | Put a labeled purpose statement, narrow-scope diagram, benefits, burdens, implementer/interface application types, and explicit non-goals near the README start. | A new evaluator can correctly distinguish package, live store, AI tool, and security boundary from the README alone. | complete |
| FB-003 | Documentation volume makes evaluation expensive. | Maintain audience-specific paths for decision-makers, implementers, AI integrations, agents, and standards reviewers. | README role paths and a five-minute adoption guide remain valid in link checks. | complete |
| FB-004 | “Human owned” could be mistaken for security or privilege enforcement. | State that owner metadata and portability are not authentication, authorization, encryption, consent, or access control; pursue any authority model separately. | README/adoption guidance plus adversarial authority tests for any future binding. | documented |
| FB-005 | Integration obligations are discovered gradually. | Publish producer, consumer, round-trip, profile, and production-hardening responsibility tables. Reusable SDKs should absorb restricted parsing and conformance complexity. | Adoption guide; production-quality SDK release criteria and external integration feedback. | documented; evidence needed |
| FB-006 | It is unclear whether applications can interoperate without moving data. | Explain that multiple tools can share an implementation-specific live API, while Core 1.0 interoperability is the package boundary. Evaluate an optional remote/API binding only from adopter demand. | Architecture/adoption wording; future binding decision and two independent prototypes if pursued. | documented; planned |
| FB-007 | The core record vocabulary is too small for many knowledge applications. | Define versioned, independently implementable domain profiles for people, organizations, sources/citations, events, conversations, bookmarks, datasets, claims, observations, decisions, collections, and user-defined semantic types. Reuse existing vocabularies and avoid bloating core. | Profile governance, schemas, mappings, examples, security review, conformance fixtures, and two independent consumers for each accepted profile. | planned |
| FB-008 | Enumerating four profile names prevents graceful third-party profile evolution. | In a future version, support namespaced profile identifiers and distinguish required processing from optional/advisory metadata. | Versioned schema, unknown-profile preservation/reporting rules, migration notes, and fixtures. | planned |
| FB-009 | Restricted YAML is safer but burdens every parser implementer. | Publish a standalone Engram Front Matter grammar/test corpus, assess JSON front matter, and provide maintained parsing libraries and editor linting. | Cross-runtime differential tests, fuzzing, SDK APIs, and editor diagnostics. | planned |
| FB-010 | Custom prefixed ULIDs complicate mapping existing UUIDs, URIs, and changing types. | Document native-ID aliases, import mapping, reclassification, merge/split, collisions, and URI identity; evaluate an optional global identifier. | Mapping guide, round-trip fixtures, and future decision record if the schema changes. | planned |
| FB-011 | Engram, export, and package identities are logical but easy to confuse. | Add lifecycle examples for first export, retry, repack, later snapshot, partial export, and re-export, including logging and deduplication advice. | Identity lifecycle guide and conformance vectors for retries/repacking. | planned |
| FB-012 | The package is promising but incomplete for long-term preservation. | Prioritize a deterministic archive binding; add preservation guidance, provenance/history, signatures as an external binding, durable schema mirrors, and mappings to BagIt/OCFL/RO-Crate. | Archive media type and safety tests; preservation pilot; mappings with declared loss; independent institutional mirror. | documented; planned |
| FB-013 | Package-native storage can be mistaken for a recommended general database. | Explain when direct storage is reasonable and why transactions, queries, indexes, history, concurrency, and ACLs normally belong to a live store. Do not prohibit package-native applications. | Adoption guide plus a package-native reference application if adopter demand justifies it. | documented |
| FB-014 | AI memory and AI context uses are easily conflated. | Keep Core retrieval-agnostic; provide a pipeline guide for authorization, projection, indexing, retrieval, citations, prompt-injection boundaries, and human adoption of generated knowledge. Evaluate a derived-context profile only with independent demand. | AI guide now; future profile must retain source IDs, derivation, loss, freshness, and authorization scope. | documented; planned |
| FB-015 | Provenance and history are major gaps for human–AI knowledge. | Prioritize a small provenance profile mapping to PROV concepts before attempting a complete synchronization model; distinguish authored, generated, derived, corrected, and adopted knowledge. | Decision record, threat model, schemas, PROV mapping, fixtures, and two independent implementations. | planned |
| FB-016 | Graph interoperability is only topology and labels. | Market it explicitly as portable directed topology and publish loss-aware mappings to JSON-LD/RDF or established graph formats rather than inventing a broad ontology. | Terminology review and round-trip mapping reports with losses identified. | planned |
| FB-017 | A stable standard can be confused with production-hardened reference tooling. | Label the specification, validator, adapters, SDKs, and security certification statuses separately. | README/tool READMEs and release checklist use consistent maturity labels. | planned |
| FB-018 | Existing standards cover important adjacent layers. | Maintain concrete, versioned, loss-aware mappings to BagIt, OCFL, RO-Crate, JSON-LD/RDF, PROV-O, iCalendar/VTODO, and an MCP delivery pattern. | Mapping documents, fixtures, adapter reports, and upstream/community review. | planned |
| FB-019 | Governance is maintainer-led and not yet representative of an industry ecosystem. | Publish adoption-triggered governance transitions: add maintainers from independent implementations, a compatibility review group, transparent recusals, and eventually a neutral home if adoption warrants it. | Governance milestones and recorded appointments/decisions. | documented; evidence needed |
| FB-020 | Commercial adopters may not recognize that the existing licenses permit commercial use. | Explain CC BY-SA 4.0 for prose and MPL 2.0 for code/schema artifacts. Do not add MIT merely for commercial permission because it would weaken the requested openness objective. | Licensing guide and README link; legal review remains adopter responsibility. | complete |
| FB-021 | Adoption claims need market evidence, not only same-repository implementations. | Recruit a note/project application, an AI knowledge integration, and an archive/migration tool; publish real-data round-trip and loss reports. | Three external adopter reports and independently maintained implementations. | evidence needed |

## Recommended implementation sequence

1. Keep README positioning, adoption guidance, licensing, and role paths concise.
2. Recruit independent pilots before expanding normative core.
3. Turn repeated integration pain into production SDK requirements.
4. Complete the archive binding for ordinary one-file exchange.
5. Design provenance and domain profiles through mappings to established work.
6. Address profile extensibility and identity mapping in a versioned release.
7. Consider API, history/sync, signature, or AI-projection bindings only when
   independent implementations demonstrate a shared interoperability need.
8. Reassess governance at each adoption milestone.
