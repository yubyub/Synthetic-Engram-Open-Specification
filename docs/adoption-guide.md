# Adoption guide

This non-normative guide helps product owners and application developers decide
whether Synthetic Engram is the right interoperability boundary. `SPEC.md` and
its referenced schemas remain authoritative.

## Short recommendation

Adopt Synthetic Engram first as an optional import/export format when human
inspection, durable identity, relationship preservation, or exchange between
independently evolving tools matters. Do not redesign a production database
around it until a real-data pilot shows that its model and extension strategy fit
the application.

Synthetic Engram is both a portable knowledge structure and its interchange
representation. The standard defines the meaning that survives interchange; it
does not require an application to store its live state in that representation.
Two components may access one live service without moving a package, but that
service API is application-specific in Core 1.0. Standard interoperability begins
when a conforming package is produced or consumed.

## Benefit versus burden

| Situation | Likely result |
| --- | --- |
| A user needs an inspectable exit from a product | Strong benefit |
| IDs and links must survive renames and migrations | Strong benefit |
| Two applications exchange notes, projects, actions, graphs, or media | Benefit after a round-trip pilot |
| An AI tool needs durable source objects behind derived context | Useful source layer |
| Only one application will read the data | Usually unnecessary burden |
| Plain Markdown already preserves all required meaning | Usually unnecessary burden |
| The primary need is sync, history, ACLs, retrieval, or model memory behavior | Wrong layer by itself |
| The domain requires a mature research, preservation, or semantic-web ecosystem | Compare RO-Crate, BagIt, OCFL, or RDF first |

## What adoption requires

| Implementation level | Responsibilities |
| --- | --- |
| Core producer | Stable IDs, record serialization, manifest inventory, profiles, safe paths, complete/partial scope, and validation |
| Core consumer | Untrusted-input parsing, duplicate-key checks, profile negotiation, references, limits, staged import, and clear diagnostics |
| Round-trip processor | Consumer duties plus preservation of unsupported objects and unknown extensions without false lossless claims |
| Graph support | Node and edge validation, record-reference mapping, and topology preservation |
| Media support | Metadata/payload pairing, size and SHA-256 verification, safe filenames, and attachment-URI resolution |
| Production deployment | Authentication and authorization outside the package, quotas, transactional commit, rendering sanitization, link policy, monitoring, and recovery tests |

Use the included adapters to learn the contract and exercise the harness. They
are interoperability evidence, not a substitute for product-specific security,
storage, transaction, and user-experience work.

## Does the data have to move?

Not always. Several user-facing tools may talk to one application or service that
stores the knowledge once. Those tools can change independently if the service
offers a stable API, but Core 1.0 does not standardize that API. Synthetic Engram
guarantees a common boundary only when data is materialized as a package for
import, export, validation, backup, migration, or bounded delivery.

An implementation may keep proprietary tables or object layouts. This is an
intentional separation: forcing every database to mirror a directory package
would reduce adoption. The tradeoff is that conformance does not make proprietary
live services mutually queryable. A future protocol binding could standardize
remote access without changing the portable information model.

## Canonical internal storage

The package can be used directly as a small local application's canonical store,
but it is not optimized as a general database model. It has no transaction,
index, concurrent-write, revision, tombstone, query, or conflict semantics.
Rewriting manifests and hashing media may also be inefficient for frequent
updates.

It is a reasonable internal model when the application is single-user or
write-light, package-native operation is a deliberate product goal, and the
application separately supplies atomic writes, indexes, history, backups, and
authorization. For most hosted or collaborative applications, use a database
suited to runtime behavior and make the adapter a first-class, continuously
tested boundary.

## AI memory and context

An AI memory engine needs policies and runtime behavior: ingestion, chunking,
retrieval, ranking, context budgeting, provenance, corrections, freshness,
permissions, and often embeddings or episodic state. Synthetic Engram deliberately
does not define those choices, so it is a poor memory engine by itself.

It can be the durable, owner-controlled source beneath such an engine. A
projection selects and transforms records into chunks, facts, or prompts; a
retrieval layer finds the relevant projections for a task. Those layers should
remain application-specific unless interoperable evidence shows that one shared
profile is useful. Derived objects should retain source record IDs, declare loss
or transformation, and never be confused with the durable source.

## Long-term archive caveats

The textual records, explicit inventory, stable IDs, and attachment hashes make
the package promising for preservation, but Core 1.0 alone is not a complete
long-term preservation system:

- only a directory representation is standardized, not a deterministic archive;
- hashes detect changes but do not authenticate a producer;
- current state is preserved, not history, tombstones, or provenance;
- no fixity-refresh, media-migration, replication, retention, or recovery policy
  is defined;
- no Markdown dialect is selected, so future rendering can differ; and
- schema hosting, registries, software preservation, and independent governance
  require durable institutional support.

Make it a stronger archival choice by pairing it with managed preservation
storage, retaining immutable schema and validator copies, periodically checking
fixity, documenting rendering assumptions, and using an established outer
packaging or repository standard where appropriate. The planned archive binding,
provenance profile, history model, signed-package binding, and independent
governance are the highest-value standard-level improvements.

## Pilot checklist

Before committing to adoption:

1. Map every native object and relationship; classify any loss or extension.
2. Export representative real data, including Unicode, large media, and partial
   selections.
3. Validate, import with an independently written implementation, edit, and
   round trip.
4. Rename files and confirm stable IDs and relationships survive.
5. Confirm unsupported profiles and extensions are never silently discarded.
6. Test malicious paths, oversized data, raw HTML, external links, and failed
   imports in the actual product path.
7. Delete the source application and verify that a human can still inspect the
   package and another implementation can recover its intended meaning.
8. Publish preserved, transformed, unsupported, and omitted semantics.
