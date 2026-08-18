# Synthetic Engram Open Standard v0.1

**Status:** Experimental draft

**Version:** 0.1.0
**Schema base:** `https://synthetic-engram.org/schema/v0.1/`

## 1. Scope

This specification defines a portable package and information model for a
Synthetic Engram: a durable collection of records, relationships, graphs, and
attachments controlled by a defined owner. It defines interchange, not a live
storage engine, user interface, retrieval algorithm, authentication protocol,
or synchronization protocol.

## 2. Requirements language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**,
and **MAY** are to be interpreted as described by BCP 14 (RFC 2119 and RFC
8174) when, and only when, they appear in all capitals.

## 3. Terminology

- **Synthetic Engram:** a durable logical knowledge environment whose identity persists across exports, package layouts, and storage migrations.
- **Engram Package:** a directory or archive containing all or part of a
  Synthetic Engram in this portable representation. A package is a transport instance, not the Engram itself.
- **Engram Record:** one durable typed object in an Engram.
- **Engram ID:** the stable `engram_id` of the Synthetic Engram.
- **Package ID:** manifest `id`, identifying one serialized package instance. Repacking creates a new Package ID.
- **Export ID:** manifest `export_id`, identifying the logical export event. Retries retain it but use distinct Package IDs.
- **Implementation:** software that produces or consumes an Engram Package.
- **Extension:** namespaced, non-core data preserved alongside core data.

## 4. Encoding and paths

JSON documents MUST be UTF-8 encoded and MUST NOT contain duplicate object
keys. Markdown records MUST be UTF-8 encoded. Package paths MUST use `/` as the
separator, MUST be relative, and MUST NOT contain an empty segment, `.` segment,
`..` segment, or NUL byte. An archive consumer MUST reject entries that escape
the extraction root.

Timestamps MUST be RFC 3339 `date-time` strings in UTC and use the `Z` suffix.
Producers SHOULD emit seconds even when the value has no sub-second precision.

## 5. Identifiers

Every Synthetic Engram, export event, package instance, and durable object MUST have an ID matching:

```regex
^[a-z][a-z0-9-]{1,31}_[0-9A-HJKMNP-TV-Z]{26}$
```

The prefix communicates an object kind (for example `engram_`, `note_`, or
`attachment_`); the suffix is a canonical uppercase ULID. IDs MUST be unique
within a package and MUST NOT be reassigned to a different logical object.
Identity MUST NOT depend on a title, filename, path, or storage key.

## 6. Package manifest

The package root MUST contain `engram.json`, conforming to
[`schemas/v0.1/manifest.schema.json`](schemas/v0.1/manifest.schema.json).
It declares:

- `format`, fixed to `synthetic-engram`;
- specification `version`;
- package-instance `id`, stable Synthetic Engram `engram_id`, and export-event `export_id`;
- `completeness`, either `complete` or `partial`;
- creation and update timestamps;
- an owner descriptor;
- supported conformance `profiles`; and
- an explicit inventory of package objects.

Each inventory entry MUST name an ID, kind, media type, and package-relative
path. The path MUST exist and its contained object ID MUST equal the inventory
ID. Inventory IDs MUST be unique except that an attachment's `blob` entry MUST
repeat its attachment metadata ID. Producers MUST list every normative object.
Consumers MUST NOT infer that unlisted files are normative package objects.


### 6.1 Package scope

A `partial` package MUST contain `partial` metadata with either a reproducible selection `mechanism` (type and expression) or a non-empty opaque `description`; it MAY contain both. Selection metadata MUST NOT be treated as proof that every matching source object was exported. A `complete` package MUST NOT contain `partial` metadata.

These terms are distinct:

- **Not inventoried** means a file is present in the package but has no `objects` entry. It has no normative object status. In a complete package, a durable artifact in `records/`, `graphs/`, or `attachments/` that is not inventoried is an error.
- **External to this package** means a durable member of this Synthetic Engram is absent from this package. This is permitted only for a partial package. References express Engram membership with `target_scope`, `parent_scope`, or `record_scope` equal to `synthetic_engram` (the default); inventory presence determines whether it is external to the package.
- **External to the Synthetic Engram** means the referenced entity is not a durable member of this Engram. Its corresponding scope field MUST be `outside_engram`; it is never required in the inventory.

The obsolete, ambiguous `external` Boolean MUST NOT be emitted. One Boolean MUST NOT represent inventory status, package selection, and Engram membership.

### 6.2 Complete export closure

With `completeness: complete`, `objects` MUST inventory and the package MUST contain every current durable record and normative Markdown body, every current durable graph, every attachment's normative metadata, every attachment payload, and every other current durable artifact owned by the Synthetic Engram at the export snapshot. Normative extension data MUST appear. References to Engram members MUST resolve. Deleted, superseded, or historical revisions need not appear unless retained as current durable artifacts.

A complete export MUST NOT include transient caches, search indexes, lock files, sessions, credentials, access tokens, telemetry, temporary files, or unfinished writes as normative objects. It need not include thumbnails, previews, embeddings, rendered HTML, compiled views, query results, model outputs, or other reproducible derivative artifacts. If one is deliberately adopted as durable owner-controlled knowledge, it is no longer merely operational or derivative and MUST be inventoried under an applicable profile or namespaced extension.

Completeness is a claim about the producer's source snapshot, not merely archive self-consistency. A producer MUST compare the inventory with that snapshot. A consumer can verify packaged evidence, but cannot prove disclosure of an object for which the package contains no evidence.

## 7. Records

A record MUST be a `.md` file consisting of YAML 1.2 front matter followed by
Markdown content. Front matter begins with `---` on the first line and ends
with `---` on a line by itself. It MUST conform to
[`schemas/v0.1/record.schema.json`](schemas/v0.1/record.schema.json).

The core envelope requires `id`, `schema_version`, `type`, `title`,
`created_at`, and `updated_at`. `type` is one of `note`, `project`, or `action`
in v0.1. An action additionally MUST provide `status`; it MAY provide `due_at`.

A `parent` denotes hierarchy. Each `links` entry denotes a typed directed link.
A `synthetic_engram` target MAY be absent only from a partial package. An `outside_engram` target need not resolve. A package MUST NOT contain a cycle formed by included `parent` references.

## 8. Graphs

A graph is a JSON object conforming to
[`schemas/v0.1/graph.schema.json`](schemas/v0.1/graph.schema.json). Nodes have
local IDs and MAY reference Engram IDs. Directed edges reference local node IDs.
Referenced Engram IDs MUST resolve in a complete package unless their `record_scope` is `outside_engram`. Node and
edge IDs MUST each be unique within their graph.

Graphs are optional, non-authoritative views. A package MAY contain no graphs,
even when it declares relationships between records. No record, attachment,
blob, graph, or other inventoried artifact is required to appear as a graph
node. The manifest inventory, not graph membership, defines package contents.
A graph MAY therefore be an application-specific diagram or a projection of
some package relationships, but it is not an authoritative relationship set.

Every graph MUST declare its coverage with `scope`:

- `curated` means that its nodes and edges are a selected or partial view. It
  MAY omit any inventoried record and MAY contain application-specific nodes;
- `complete_records` claims complete record coverage. It MUST contain at least
  one non-external node whose `record` is each inventoried record ID. It MAY
  also contain application-specific or external nodes. Complete coverage does
  not require attachments, blobs, or other graphs to be nodes and does not make
  the graph authoritative for relationships.

Record `parent` and `links` fields are authoritative package relationships.
Graph edges are independent, descriptive topology: they are not required to be
projections of record relationships, and records are not required to repeat
graph edges in `links` or `parent`. A graph edge that appears to contradict or
omit a record relationship does not create a validation conflict; consumers
MUST use the record field when determining record hierarchy or typed record
links. Producers SHOULD choose graph relations and labels that avoid misleading
users, but validators MUST NOT infer agreement from similarly named relations.

The v0.1 graph format describes interoperable topology and optional labels. It
does not standardize layout, rendering, or an application-specific graph DSL.

These abbreviated examples show the coverage rules (the other required graph
and manifest fields are omitted here for clarity). Complete, validated versions
are provided by the [no-graph](tests/valid/no-graphs),
[curated-graph](tests/valid/basic-engram), and
[complete-record-graph](tests/valid/complete-record-graph) fixtures:

```json
{"profiles":["core"], "objects":[{"id":"note_...", "kind":"record", "path":"records/note.md"}]}
```

The package above has no graph; the record remains a package member because it
is inventoried. A curated graph can select two of several records:

```json
{"scope":"curated", "nodes":[
  {"id":"first", "record":"note_01J00000000000000000000003"},
  {"id":"second", "record":"note_01J00000000000000000000004"}
]}
```

A graph claiming complete coverage must reference every inventoried record:

```json
{"scope":"complete_records", "nodes":[
  {"id":"project", "record":"project_01J00000000000000000000002"},
  {"id":"first", "record":"note_01J00000000000000000000003"},
  {"id":"second", "record":"note_01J00000000000000000000004"}
]}
```

## 9. Attachments

Attachment metadata is a JSON object conforming to
[`schemas/v0.1/attachment.schema.json`](schemas/v0.1/attachment.schema.json).
It identifies a separate payload by relative `path`, media type, byte size, and
lowercase SHA-256 digest. The payload MUST exist and match both declared size
and digest. The metadata and payload MUST both be listed in the manifest; the
payload inventory entry uses kind `blob` and the attachment ID.

Markdown MAY refer to an attachment with
`engram-attachment:<attachment-id>`. Consumers MUST resolve that URI by ID and
MUST NOT treat an embedded path or remote URL as authoritative.

## 10. Extensions

Core schema objects are closed except for the `extensions` member. Extension
keys MUST use reverse-DNS form (for example `org.example.priority`). Values MAY
be any JSON-compatible YAML value. An implementation that reads and rewrites an
object SHOULD preserve unknown extensions unchanged. An extension MUST NOT
change the meaning or validity of a core field.

## 11. Profiles and conformance

v0.1 defines these profiles:

- **core:** manifest, records, stable IDs, hierarchy, links, import, and export;
- **graph:** graph objects and referenced-record preservation;
- **media:** attachment metadata, payloads, hashes, and attachment URIs;
- **action:** action status and due-date semantics.

Every package MUST declare `core`. It MUST declare each optional profile whose
objects it contains. An implementation MUST state whether it is a producer,
consumer, or round-trip processor and which profiles it supports.

A conforming producer MUST create schema-valid packages satisfying all
cross-file requirements. A conforming consumer MUST either process a declared
profile or report it as unsupported; it MUST NOT silently claim successful
support. A round-trip processor SHOULD preserve unsupported inventoried objects
and unknown extensions byte-for-byte when it claims preservation.

See [docs/conformance.md](docs/conformance.md) for the testable checklist.

## 12. Versioning

`version` uses Semantic Versioning. Patch releases clarify text or tighten tests
without changing valid data. Minor releases add backward-compatible optional
features. Major releases may make incompatible changes. A consumer MUST reject
a package with an unsupported major version and SHOULD report unsupported minor
features rather than silently discard them.

Schema paths are versioned by major and minor version. Package data uses
`schema_version: "0.1"`; it does not include the patch version.

## 13. Security and privacy

Package content is untrusted input. Implementations MUST prevent path traversal,
MUST enforce resource limits, and MUST NOT execute record content. Media types,
filenames, links, extensions, Markdown, and graph labels MUST be treated as
untrusted. Hashes provide integrity checks, not authenticity. Encryption,
signing, identity proof, and authorization are outside v0.1; applications MUST
not infer permission merely from possession of a package. See [SECURITY.md](SECURITY.md).

## 14. Non-goals and future work

v0.1 does not define synchronization, conflict resolution, access-control
descriptors, certification branding, query lenses, AI context selection, or
portable revision deltas. These subjects remain documented in
[docs/open-questions.md](docs/open-questions.md).
