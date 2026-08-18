# Original concept: historical rationale

> [!IMPORTANT]
> This document is historical and non-normative. It contains no requirements.
> [`SPEC.md`](../SPEC.md) and its referenced schemas are the only sources of
> format requirements. The disposition of the original proposal is recorded in
> the [design-decision matrix](design-decisions.md).

## Purpose and interoperability rationale

The project began from a desire to separate durable knowledge ownership from
application ownership. The proposed interchange layer covered human-facing
applications, AI systems, graph tools, task tools, search systems, and backup
tools. AI memory was one consumer, not the definition of the format.

The surviving 1.0 direction is deliberately smaller: a portable package of
stable, typed records, links, graph topology, and attachments. Live storage,
user interfaces, retrieval, and protocols remain implementation concerns.

## Vocabulary rationale

“Synthetic Engram” distinguished the complete portable knowledge environment
from projects that use “engram” for one atomic learned memory. “Record” named a
durable object, “Package” named its portable serialization, and “Store” and
“Service” described non-portable implementation roles.

The draft also proposed Namespace, Lens, Surface, Fragment, Trace, Pulse,
Anchor, Capsule, Shard, Echo, Ghost, Cortex, Mesh, Gate, Thread, and Vault.
Only terms present in the normative terminology section form part of core 1.0.
The matrix records the disposition of every proposed term.

## User authority and surface-boundary rationale

The concept separated portable knowledge from credentials, caches, UI state,
indexes, embeddings, generated context, and other runtime state. It also
distinguished a description of granted authority from authentication and
enforcement. Core 1.0 retains security boundaries and partial packages, but it
does not serialize access grants or surface capabilities.

## Package and record-model rationale

The original model used stable identifiers rather than paths or titles,
Markdown records with structured metadata, explicit hierarchy and typed links,
inventoried attachments, namespaced extensions, and declared capability
profiles. These choices allow partial consumers to detect unsupported content
without requiring live stores to resemble exports.

Projects and actions became core record types. Generic reminders remain
representable as action extensions. Graph topology received an optional
profile; graph layout and application graph languages did not.

## References, provenance, and non-narrative-data rationale

The concept distinguished a link to authoritative external data, a portable
snapshot, and a native deterministic data record. Core 1.0 only standardizes
typed links, explicit unresolved external targets, attachments, and extension
hooks. Rich source descriptors, provenance chains, tabular/numeric snapshots,
units, and operational-data semantics remain future work.

## Current-state, history, and migration rationale

The draft explored revision snapshots, deltas, deletion markers, supersession,
conflicts, change feeds, and the difference between current state and history.
Core 1.0 exports current state only. Stable IDs and extensions leave room for a
future History and Synchronization Specification.

Migration originally meant transferring portable knowledge between different
stores through a package, with an explicit loss and preservation report. Core
1.0 defines import/export conformance but no standardized migration report.

## Partial consumption, AI, and remote-use rationale

Notes, graphs, tasks, search, backup tools, and AI consumers were expected to
read only the profiles they understand. That premise survives as declared
profiles and explicit unsupported-profile reporting. Query lenses, bounded AI
context, remote APIs, and protocol bindings are outside core 1.0.

## Adapters and related-work rationale

The draft compared EngramSpec, PLUR Engram Specification, ly-wang19/engram,
Infinite Brain OS, Model Context Protocol, and general open-data standards.
The lasting design principle is that an adapter is not a lossless migration
unless a round trip preserves the claimed information and semantics.
Cross-standard mapping and provenance metadata remain future work.

## Governance, conformance, and naming rationale

The repository now contains governance, licensing, schemas, fixtures, and a
validator rather than leaving them as aspirations. Certification branding is
not part of core conformance. The optional cyberpunk vocabulary was rejected
as standards terminology except where a future specification explicitly
adopts a term.

## Historical examples

The original examples depicted application-to-application package migration,
several services consuming different record types, and an AI receiving a
permission-limited subset. They motivated package portability, profiles, and
partial-package links; they never defined wire formats or authorization rules.

## Remaining decisions

Questions that can block a stable 1.0, each with closure criteria, are tracked
in [`open-questions.md`](open-questions.md). Historical possibilities not
listed there are not implicitly planned features.
