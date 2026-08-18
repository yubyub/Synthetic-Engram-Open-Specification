# Design-decision matrix for core 1.0

> [!NOTE]
> This document is non-normative. It records the disposition of the major
> headings in the original concept draft; it does not add requirements.
> Normative behavior comes only from [`SPEC.md`](../SPEC.md) and the schemas it
> references. “Included” below means the intended 1.0 disposition of the
> currently experimental specification, not a claim that 1.0 has shipped.

## Status vocabulary and compatibility hooks

| Status | Meaning |
|---|---|
| **Core 1.0** | Required by the core profile. |
| **Optional 1.0 profile** | Normative only when the named profile is declared. |
| **Deferred — _name_** | Reserved for the named future specification; not a 1.0 promise. |
| **Rejected** | Deliberately not standardized. |
| **Superseded** | Replaced by the linked 1.0 mechanism or terminology. |

A “hook” is only an existing representation that can preserve identity or
extension data. It does not grant semantics from a deferred specification.

## Crosswalk for the retained historical document

Every major heading that remains in [`rationale.md`](rationale.md) maps
to the detailed original-heading decisions below.

| Current historical heading | Matrix coverage |
|---|---|
| Purpose and interoperability rationale | Original headings 1, 4–6, 18, 20, and 29. |
| Vocabulary rationale | Original heading 2 and appendix L. |
| User authority and surface-boundary rationale | Original heading 3 and appendix H. |
| Package and record-model rationale | Original headings 7–14, 17, 26, and 27. |
| References, provenance, and non-narrative-data rationale | Original headings 15 and 23. |
| Current-state, history, and migration rationale | Original headings 16, 19, 25, and appendix G. |
| Partial consumption, AI, and remote-use rationale | Original headings 20–24. |
| Adapters and related-work rationale | Original heading 23 and appendices A–B. |
| Governance, conformance, and naming rationale | Original heading 28 and appendices C–I and K–L. |
| Historical examples | Appendix J. |
| Remaining decisions | Appendix M and [`open-questions.md`](open-questions.md). |

## Original headings 1–8: intent and core model

| Original heading | Decision | Normative location / schema, or rationale and retained hook |
|---|---|---|
| 1. Purpose and Long-Term Intent | **Core 1.0** | Interchange scope: [SPEC §1](../SPEC.md#1-scope). |
| The primary interoperability target is broader than AI memory | **Core 1.0** | The information model is application-independent: [SPEC §1](../SPEC.md#1-scope). |
| 2. Terminology: Synthetic Engram, Engram Package, Engram Record | **Core 1.0** | Definitions: [SPEC §3](../SPEC.md#3-terminology); envelopes: [manifest](../schemas/v0.1/manifest.schema.json), [record](../schemas/v0.1/record.schema.json). The ambiguous short form “Engram” is superseded by the defined terms. |
| Engram Namespace | **Deferred — Namespace and Selection Specification** | Membership and cross-namespace policy are unresolved. Hook: record `extensions` and stable IDs. |
| Engram Lens | **Deferred — Namespace and Selection Specification** | No deterministic query grammar is ready. Hook: stable IDs, tags, types, links, and extensions are selectable inputs. |
| Engram Surface | **Rejected** as a package object | It describes application architecture, not portable knowledge. Hook: implementations declare roles/profiles under [SPEC §11](../SPEC.md#11-profiles-and-conformance). |
| Engram Fragment (permission-, context-, and portable fragments) | **Superseded** | A partial Engram Package plus explicit external links covers portable subsets: [SPEC §§6–7](../SPEC.md#6-package-manifest), [manifest schema](../schemas/v0.1/manifest.schema.json), [record schema](../schemas/v0.1/record.schema.json). Selection and authorization semantics are deferred. |
| Engram Store and Engram Service | **Rejected** as format concepts | Storage engines and services are outside interchange scope. Hook: packages are storage-independent and protocol bindings can consume them. |
| 3. User Data Authority / Access is scoped | **Deferred — Access and Authority Specification** | Portable authorization without misleading enforcement claims needs a threat model. Hook: partial packages, external links, owner descriptor, and security rules in [SPEC §13](../SPEC.md#13-security-and-privacy). |
| Access descriptors | **Deferred — Access and Authority Specification** | Identity, operations, expiry, delegation, and revocation are unresolved. Hook: manifest/record `extensions`; possession conveys no permission. |
| Knowledge versus runtime security configuration / Surface boundary | **Rejected** as serialized core data | Secrets, sessions, caches, and UI state are runtime concerns. Hook: closed core schemas plus namespaced extensions prevent accidental core interpretation: [SPEC §10](../SPEC.md#10-extensions). |
| 4. Core Goals: open, portable, human-readable, stable, extensible, user-controlled, application-independent | **Core 1.0** | Encoding, IDs, packages, extensions, and security: [SPEC §§4–6](../SPEC.md#4-encoding-and-paths), [§10](../SPEC.md#10-extensions), [§13](../SPEC.md#13-security-and-privacy). |
| Core Goals: graph-aware | **Optional 1.0 profile — graph** | [SPEC §§8, 11](../SPEC.md#8-graphs), [graph schema](../schemas/v0.1/graph.schema.json). |
| Core Goals: AI-friendly and human-usable | **Superseded** | Concrete UTF-8 JSON/Markdown and profile mechanisms replace subjective conformance labels: [SPEC §§4, 7, 11](../SPEC.md#4-encoding-and-paths). |
| 5. Non-Goals | **Core 1.0** | Scope exclusions and future work: [SPEC §§1, 14](../SPEC.md#14-non-goals-and-future-work). |
| 6. Synthetic Engram Model | **Core 1.0** | Manifest inventory and typed objects: [SPEC §§6–9](../SPEC.md#6-package-manifest). |
| 7. Stable IDs | **Core 1.0** | [SPEC §5](../SPEC.md#5-identifiers), shared ID definition in [definitions schema](../schemas/v0.1/definitions.schema.json). |
| 8. Core Record Model | **Core 1.0** | [SPEC §7](../SPEC.md#7-records), [record schema](../schemas/v0.1/record.schema.json). |
| Production Hosting | **Rejected** | Deployment is outside a portable format. No compatibility hook is needed; any host can import/export a conforming package. |

## Original headings 9–18: relationships and package content

| Original heading | Decision | Normative location / schema, or rationale and retained hook |
|---|---|---|
| 9. Relationship Model: hierarchy and links | **Core 1.0** | `parent` and typed directed `links`: [SPEC §7](../SPEC.md#7-records), [record schema](../schemas/v0.1/record.schema.json). |
| 10. Graphs | **Optional 1.0 profile — graph** | Interoperable topology: [SPEC §8](../SPEC.md#8-graphs), [graph schema](../schemas/v0.1/graph.schema.json). |
| 11. Graph Representation | **Optional 1.0 profile — graph** | Nodes, edges, record references, labels: [graph schema](../schemas/v0.1/graph.schema.json). Layout is excluded by [SPEC §8](../SPEC.md#8-graphs). |
| Relationship extraction / graph DSLs | **Deferred — Graph Languages and Derivation Specification** | DSL parsing cannot be deterministic across applications without a grammar and provenance rules. Hook: native graph topology and extensions can preserve source-language data. |
| 12. Attachments | **Optional 1.0 profile — media** | [SPEC §9](../SPEC.md#9-attachments), [attachment schema](../schemas/v0.1/attachment.schema.json), inventory in [manifest schema](../schemas/v0.1/manifest.schema.json). |
| 13. Projects and Context | **Core 1.0** for projects; **Deferred — Namespace and Selection Specification** for contextual selection | `project` is a record type: [SPEC §7](../SPEC.md#7-records), [record schema](../schemas/v0.1/record.schema.json). Hook: links, tags, and extensions. |
| 14. Actions and Reminders | **Optional 1.0 profile — action** | Action status/due date: [SPEC §§7, 11](../SPEC.md#7-records), [record schema](../schemas/v0.1/record.schema.json). A distinct reminder type is rejected; hook: action extensions. |
| 15. External References | **Core 1.0** | Explicit external record and graph references: [SPEC §§7–8](../SPEC.md#7-records), [record](../schemas/v0.1/record.schema.json) and [graph](../schemas/v0.1/graph.schema.json) schemas. |
| Authoritative, Numeric and Operational Data: data reference | **Deferred — Data and Provenance Specification** | Authority/freshness cannot be inferred from a URL. Hook: typed external links and extensions. |
| Authoritative, Numeric and Operational Data: portable snapshot | **Deferred — Data and Provenance Specification** | Canonical tables, units, precision, and source timestamps are unresolved. Hook: media attachments with hashes and extension metadata. |
| Authoritative, Numeric and Operational Data: native deterministic record | **Deferred — Data and Provenance Specification** | Core has no non-narrative data record type. Hook: inventoried media, stable IDs, and extensions. |
| 16. History and Revisions / record revision model | **Deferred — History and Synchronization Specification** | Snapshot/delta identity and conflict rules are unresolved. Hook: stable IDs, `created_at`, `updated_at`, and extensions. |
| Current state versus history | **Core 1.0** for current-state export; history **deferred** | Record envelope is current state: [SPEC §7](../SPEC.md#7-records), [record schema](../schemas/v0.1/record.schema.json). No revision chain is implied. |
| History capability levels / deleted or superseded information | **Deferred — History and Synchronization Specification** | Capability tiers, tombstones, and supersession need common lifecycle semantics. Hook: profiles/extensions; external links preserve unresolved identity. |
| 17. Engram Package | **Core 1.0** | [SPEC §6](../SPEC.md#6-package-manifest), [manifest schema](../schemas/v0.1/manifest.schema.json). Canonical archive serialization remains deferred. |
| 18. Live Storage Does Not Need to Match the Package | **Core 1.0** | Interchange—not storage—is defined by [SPEC §1](../SPEC.md#1-scope). |

## Original headings 19–29: consumption and compatibility

| Original heading | Decision | Normative location / schema, or rationale and retained hook |
|---|---|---|
| 19. Migration Between Services | **Core 1.0** for conforming import/export; richer migration **deferred — Migration Specification** | Producer/consumer roles: [SPEC §11](../SPEC.md#11-profiles-and-conformance). Stable IDs and complete inventory are the hook. |
| Migration report | **Deferred — Migration Specification** | No agreed loss taxonomy or machine-readable report. Hook: unsupported-profile reporting and extension preservation under [SPEC §11](../SPEC.md#11-profiles-and-conformance). |
| 20. Application Use and Partial Consumption (notes, diagrams, file navigation, search, calendar/task, backup) | **Core 1.0** via role/profile declarations | [SPEC §11](../SPEC.md#11-profiles-and-conformance). Search indexes remain derivative; graph, media, and action data use their schemas. |
| 21. AI Context Consumption / derived context views | **Deferred — AI Context Profile** | Retrieval policy and bounded context are application-specific until a testable selection model exists. Hook: partial packages, stable IDs, profiles, and extensions. |
| 22. AI Agent Memory | **Rejected** as a core memory algorithm | The standard exchanges durable knowledge rather than defining learning/retrieval. Hook: records and adapters. |
| 23. Cross-Standard Interoperability / adapter principle | **Deferred — Adapter and Provenance Specification** | Mappings require standard-specific contracts. Hook: media types, typed links, stable IDs, and extensions. |
| Lossless and lossy mappings | **Deferred — Adapter and Provenance Specification** | “Lossless” needs round-trip fixtures and declared semantic scope. Hook: conformance roles and unknown-extension preservation. |
| Provenance | **Deferred — Data and Provenance Specification** | Creator/source/derivation semantics and signatures are unresolved. Hook: owner descriptor, timestamps, IDs, hashes, links, extensions. |
| 24. Remote Consumption | **Deferred — Protocol Bindings Specification** | HTTP, MCP, filesystem, and other transports are deployment choices. Hook: the package model is transport-neutral. |
| 25. Indexes Are Derivative | **Rejected** as package data | Indexes, embeddings, and caches are reproducible implementation state. No hook is required; extensions or unlisted non-normative files can carry private data. |
| 26. Extensions | **Core 1.0** | Reverse-DNS keys and preservation behavior: [SPEC §10](../SPEC.md#10-extensions); extension members occur in all four entry schemas. |
| 27. Compatibility Profiles: Engram Core | **Core 1.0** | Superseded name: profile `core`, [SPEC §11](../SPEC.md#11-profiles-and-conformance), [manifest schema](../schemas/v0.1/manifest.schema.json). |
| Compatibility Profiles: Linked | **Superseded** | Hierarchy and links are in `core`: [SPEC §§7, 11](../SPEC.md#7-records). |
| Compatibility Profiles: Graph, Media, Action | **Optional 1.0 profiles — graph, media, action** | [SPEC §11](../SPEC.md#11-profiles-and-conformance) and [graph](../schemas/v0.1/graph.schema.json), [attachment](../schemas/v0.1/attachment.schema.json), [record](../schemas/v0.1/record.schema.json) schemas. |
| Compatibility Profiles: Data | **Deferred — Data and Provenance Specification** | Hook: attachments and extensions. |
| Compatibility Profiles: History and Sync | **Deferred — History and Synchronization Specification** | Hook: IDs, timestamps, profiles, and extensions. |
| Compatibility Profiles: Access | **Deferred — Access and Authority Specification** | Hook: partial packages, owner descriptor, and extensions. |
| Compatibility Profiles: AI Context and Fragment | **Deferred — AI Context Profile / Namespace and Selection Specification** | Hook: partial packages, external links, profiles, and stable IDs. |
| 28. Standard Versioning: additive and breaking changes | **Core 1.0** | [SPEC §12](../SPEC.md#12-versioning). |
| 29. Core Interoperability Principle | **Core 1.0** | Producer, consumer, and round-trip obligations: [SPEC §11](../SPEC.md#11-profiles-and-conformance). |

## Original supporting headings A–M

| Original heading | Decision | Normative location / schema, or rationale and retained hook |
|---|---|---|
| A. Related Works (EngramSpec, PLUR, ly-wang19/engram, Infinite Brain OS, MCP, other standards) | **Rejected** from the normative specification | Informative comparisons age independently and do not establish compatibility. Hook: future mappings can use extensions and typed links. |
| B. Cross-Compatibility Guidance: context, agent-memory, and tool-protocol adapters | **Deferred — Adapter and Provenance Specification** | Adapter claims need mapping tables and fixtures. Hook: core objects and profiles. |
| Round-trip requirement | **Core 1.0** for package processors | Preservation claim behavior: [SPEC §11](../SPEC.md#11-profiles-and-conformance). Cross-standard round trips remain deferred. |
| C. Standard Governance | **Superseded** | Adopted process: [`GOVERNANCE.md`](../GOVERNANCE.md) and [`CONTRIBUTING.md`](../CONTRIBUTING.md). |
| D. Licensing Intent: specification, software, and schemas | **Superseded** | Adopted licenses: [`LICENSE`](../LICENSE) and [`LICENSE-CODE`](../LICENSE-CODE). |
| Trademark and compatibility branding | **Deferred — Certification and Branding Program** | Legal governance and a stable test suite are prerequisites. Hook: explicit profile/role claims. |
| E. Conformance and Certification | **Core 1.0** for conformance; certification **deferred — Certification and Branding Program** | [SPEC §11](../SPEC.md#11-profiles-and-conformance), [`docs/conformance.md`](conformance.md). |
| F. Validation and Reference Tooling | **Superseded** | Implemented validator and schema checks: [`scripts/validate.py`](../scripts/validate.py), [`schemas/README.md`](../schemas/README.md). CLI names from the concept were rejected. |
| G. Future Synchronisation Specification | **Deferred — History and Synchronization Specification** | Conflict-safe change streams depend on revision semantics. Hook: IDs, timestamps, and extensions. |
| H. Access-Control Specification Work | **Deferred — Access and Authority Specification** | Hook: partial packages, owner descriptor, and extensions; authentication remains external. |
| I. Graph Interchange Specification Work | **Superseded** for topology by optional `graph`; layout/DSLs **deferred — Graph Languages and Derivation Specification** | [SPEC §8](../SPEC.md#8-graphs), [graph schema](../schemas/v0.1/graph.schema.json). |
| J. Examples: migration, multi-service consumption, scoped AI access | **Superseded** as format examples | Executable fixtures replace conceptual examples: [`examples/basic-engram`](../examples/basic-engram/README.md). Access example remains non-normative. |
| K. Naming Considerations | **Rejected** from normative content | Branding rationale has no interoperability effect. No hook is required. |
| L. Optional Terminology: Fragment and Lens | **Deferred — Namespace and Selection Specification** | Hook: partial packages, IDs, tags, links, and extensions. |
| L. Optional Terminology: Trace | **Deferred — Data and Provenance Specification** | Hook: timestamps, links, and extensions. |
| L. Optional Terminology: Pulse | **Deferred — History and Synchronization Specification** | Hook: timestamps and stable IDs. |
| L. Optional Terminology: Shard, Echo, Ghost, Cortex, Mesh, Gate, Thread, Anchor, Capsule, Vault | **Rejected** as standard terminology | Meanings overlap established storage, cache, reference, index, federation, access, sequence, traversal, package, and security terms. Existing core objects and extensions are sufficient compatibility hooks. |
| Suggested vocabulary hierarchy | **Superseded** | Normative vocabulary is limited to [SPEC §3](../SPEC.md#3-terminology). |
| M. Open Questions | **Superseded** | Decision gates and closure criteria are maintained in [`open-questions.md`](open-questions.md). |
