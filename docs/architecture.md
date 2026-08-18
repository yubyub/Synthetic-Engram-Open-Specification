# Architecture

This document is a non-normative guide to the system boundaries defined by the
normative [`SPEC.md`](../SPEC.md). It explains how the interchange format fits
between an owner's durable knowledge and implementations that may store and use
that knowledge very differently.

The portable information model can also be part of an application's knowledge-
management architecture: human interfaces, AI integrations, and package adapters
may share one conforming live implementation. Only the materialized package is a
Core 0.2 conformance boundary; its implementation API remains application-specific.

## The interoperability boundary

```text
                        owner-controlled knowledge
                                  |
       +--------------------------+--------------------------+
       |                          |                          |
  notes / project UI        AI or coding agent         graph / task tool
       |                          |                          |
       +--------------------------+--------------------------+
                                  |
                         implementation API
                                  |
                  +---------------+---------------+
                  |       live Engram Store       |
                  | files, SQL, graph DB, service |
                  +---------------+---------------+
                                  |
                         import / export adapter
                                  |
                  +---------------+---------------+
                  | portable Engram Package       |
                  | manifest, records, graphs,    |
                  | attachments                   |
                  +-------------------------------+
```

The package is the conformance boundary, not a mandatory live filesystem.
Applications may normalize records into relational tables, store edges in a
graph database, keep blobs in object storage, or use the package directly. The
stable IDs and declared semantics—not paths or database keys—connect those
representations.

## Portable information model

An Engram Package has four cooperating parts:

1. **Manifest:** identifies the Synthetic Engram and this export, states whether
   it is complete or partial, declares profiles, and inventories every normative
   object. This makes omissions and unsupported capabilities visible.
2. **Records:** typed, human-inspectable Markdown objects. Front matter carries
   identity, timestamps, hierarchy, typed links, and extension data; the body
   carries durable textual knowledge.
3. **Graphs:** portable topology whose local nodes may point to records. A graph
   is an authored view or model, not a replacement for record hierarchy and
   links. Graph layout is deliberately left to applications.
4. **Attachments:** metadata plus a separately inventoried payload. Size and
   digest make accidental corruption detectable without forcing binary data into
   a text representation.

The manifest distinguishes three identities: the logical Engram survives every
migration, an export ID identifies one export event, and a package ID identifies
one serialization of that event. Record, graph, and attachment IDs persist when
files are moved or live storage is replaced.

## Complete and partial flows

A complete export is a closure of the owner's current durable knowledge at a
source snapshot. The producer must compare the package inventory with that
source; package self-consistency alone cannot prove nothing was withheld.

A partial export deliberately carries a subset. Its selection description and
reference scopes prevent a consumer from mistaking an absent record for a
deletion. This supports bounded sharing and agent context without treating the
subset as a complete backup or embedding access credentials in the package.

```text
live store --complete export--> backup / migration / full-fidelity import
     |
     +----partial export-------> selected tool or bounded agent context
```

## Consumer and round-trip behavior

A consumer declares the profiles it supports. It may reject an unsupported
profile or report it explicitly; it must not silently claim support. A
round-trip processor that claims preservation must keep unknown extensions and
unsupported inventoried objects. Consequently, a notes-only tool can participate
without pretending it understands graphs, actions, or media.

Importers should validate before committing writes. A robust import stages the
package, rejects unsafe paths and invalid references, verifies payload hashes,
and then atomically updates the live store. Exporters should take a consistent
snapshot so timestamps, references, inventory, and completeness describe the
same state.

## Portable knowledge versus operational state

The core includes owner-controlled, current, durable knowledge. It excludes
state that can be regenerated or that belongs to a particular runtime:

| Portable when durable | Normally implementation-local |
|---|---|
| authored record bodies and metadata | search indexes and embeddings |
| project and action records | UI layout caches and sessions |
| explicit links and graph topology | model context windows and query results |
| adopted attachments | thumbnails and generated previews |
| namespaced durable extensions | locks, unfinished writes, and telemetry |
| external-reference semantics | credentials, tokens, and authorization state |

An implementation may deliberately adopt a generated artifact as durable
owner-controlled knowledge; once it does, the artifact must be inventoried under
an applicable profile or extension. Authentication, authorization enforcement,
synchronization, conflict resolution, and retrieval remain separate layers.

## Example deployments

**Local-first:** Markdown bodies and blobs may be stored directly on disk with
SQLite indexes. Export reconstructs the manifest and portable graph JSON;
indexes stay local.

**Hosted relational:** records and links may occupy SQL tables and attachments
may use object storage. An API can expose application operations, while a
snapshot exporter serializes the same portable model.

**Graph-oriented:** records may live in a document store and relationships in a
graph database. Graph database internals are mapped to portable graph objects
and typed record links rather than leaked into the exchange contract.

These deployments are interoperable only to the extent that their adapters meet
the same conformance requirements. See the [design rationale](rationale.md) for
why the boundary was selected and [related standards](related-standards.md) for
adjacent formats and possible mappings.
