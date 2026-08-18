# Synthetic Engram Open Standard v1.0

**Status:** Experimental draft

**Version:** 1.0.0
**Schema base:** `https://synthetic-engram.org/schema/v1.0/`

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

- **Synthetic Engram:** a portable collection of the record, graph, and
  attachment forms defined by this specification. It is not a universal data
  model for every kind of durable information.
- **Synthetic Engram:** a durable logical knowledge environment whose identity persists across exports, package layouts, and storage migrations.
- **Engram Package:** a directory or archive containing all or part of a
  Synthetic Engram in this portable representation. A package is a transport instance, not the Engram itself.
- **Engram Record:** one durable typed object in an Engram.
- **Synthetic Engram ID:** the stable identity of the knowledge environment,
  independent of any particular export.
- **Package ID:** the identity of one package/export of a Synthetic Engram.
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

IDs are semantic. Every durable ID MUST have a canonical uppercase ULID suffix,
and its prefix MUST agree with its role:

| Role | Required prefix |
| --- | --- |
| Synthetic Engram | `engram_` |
| package/export | `package_` |
| note record | `note_` |
| project record | `project_` |
| action record | `action_` |
| graph | `graph_` |
| attachment metadata and its blob inventory alias | `attachment_` |
| graph node fragment | `node_` |
| graph edge fragment | `edge_` |

The complete identifier matches the role prefix followed by
`[0-9A-HJKMNP-TV-Z]{26}`. The prefix is normative, not decorative. A producer
MUST NOT use an ID whose prefix disagrees with its manifest kind or record type.

The uniqueness domain is one Synthetic Engram, including its Synthetic Engram
ID, every package/export ID, every durable object ID, every attachment metadata
ID, and every graph node or edge fragment ID in every export. No two logical
entities in that domain may share an ID. The sole permitted repetition is the
attachment metadata ID on its `blob` inventory alias; both entries identify the
same logical attachment. IDs are only guaranteed unique within one Synthetic
Engram, not globally unique by construction. Producers SHOULD nevertheless use
ULID generation practices that make cross-Engram collisions negligible and
MUST NOT reassign an ID to a different logical entity. Identity MUST NOT depend
on a title, filename, path, or storage key.
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
[`schemas/v1.0/manifest.schema.json`](schemas/v1.0/manifest.schema.json).
It declares:

- `format`, fixed to `synthetic-engram`;
- data-model `data_model_version` (major and minor only);
- optional minor-version `features`, when used;
- the package `id`;
- specification `version`;
- the Synthetic Engram `engram_id` and this package/export's `id`;
- package-instance `id`, stable Synthetic Engram `engram_id`, and export-event `export_id`;
- `completeness`, either `complete` or `partial`;
- creation and update timestamps;
- an owner descriptor containing a stable opaque `id` and optional
  `display_name`;
- supported conformance `profiles`; and
- an explicit inventory of package objects.

Each inventory entry MUST name an ID, kind, media type, and package-relative
path. The path MUST exist and its contained object ID MUST equal the inventory
ID. Inventory IDs MUST be unique except that an attachment's `blob` entry MUST
repeat its attachment metadata ID. Producers MUST list every normative object.
Consumers MUST NOT infer that unlisted files are normative package objects.

The owner ID is stable attribution or ownership metadata only. It does not
represent a public key, signature, authenticated principal, authorization
grant, or other cryptographic authority, and consumers MUST NOT treat it as
proof of identity or control. `display_name` is presentation metadata and MAY
change without changing the owner ID.

Ownership MAY be transferred by changing `owner.id` (and, if desired,
`owner.type` and `owner.display_name`) while retaining `engram_id`. A transfer
therefore does not create a new Synthetic Engram identity. Producers SHOULD
update `updated_at`; v0.1 does not define a transfer history, consent protocol,
signature, or authorization mechanism. A policy that requires a transfer to
create a distinct Engram MUST issue a new `engram_id` and treat it as a new
Engram rather than describing that operation as a v0.1 ownership transfer.
The inventory `media_type`, not the path or filename extension, is the
authoritative representation discriminator. A consumer MUST select a parser
using `media_type` and MUST NOT infer or override an object's format from its
filename extension. In v0.1, the media type of a `record` MUST be
`text/markdown`; the media types of `graph` and `attachment` objects MUST be
`application/vnd.synthetic-engram.graph+json` and
`application/vnd.synthetic-engram.attachment+json`, respectively. A `blob`
MAY use any valid media type and remains attachment content, not a record.

A consumer that encounters an inventoried media type it does not support MUST
still retain the inventory entry and MUST report the object as unsupported; it
MUST NOT parse it as another format or silently claim to have consumed it. If
the consumer emits a package while claiming round-trip preservation, it MUST
copy the unsupported object's bytes and its inventory fields unchanged. A
processor that cannot do so MUST report a lossy operation before emitting the
package and MUST NOT claim round-trip preservation.

## 7. Records and the 1.0 representation decision

Markdown with YAML front matter is the sole canonical core record
representation for 1.0. Representation negotiation does not apply to core
records: a manifest entry with kind `record` and any media type other than
`text/markdown` is not a core-conforming record. This explicit restriction is
intentional; the 1.0 core does not include JSON records, binary records, or a
format-independent record envelope.

A record MUST consist of YAML 1.2 front matter followed by Markdown content.
Front matter begins with `---` on the first line and ends with `---` on a line
by itself. The inventory path conventionally ends in `.md`, but the extension
has no role in representation detection. The front matter MUST conform to

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
[`schemas/v1.0/record.schema.json`](schemas/v1.0/record.schema.json).

### 7.1 Serialization

Records MUST be UTF-8 without a byte-order mark. Lines MAY end with either LF
or CRLF; a bare CR is not a line ending. Unicode text is compared as encoded:
consumers MUST NOT require or silently apply a normalization form. Producers
SHOULD emit Unicode Normalization Form C (NFC).

The opening delimiter is exactly the three ASCII characters `---`, followed by
LF or CRLF, at byte zero. The closing delimiter is the next line whose content
is exactly `---`; spaces, comments, or other characters are not permitted on a
delimiter line. It MAY be followed by LF, CRLF, or end of file. Everything
after that delimiter and its optional line ending is record content. Record
content MAY be empty. Thus, the delimiter is structural and is not found by
parsing YAML or by searching for a prefix.

Front matter MUST use the following restricted YAML 1.2 subset:

- it is exactly one mapping in exactly one YAML document;
- mapping keys MUST be strings and MUST be unique within their mapping;
  consumers MUST reject duplicate keys rather than select a value;
- sequences, mappings, and JSON-compatible scalar values are permitted;
- directives, explicit tags, anchors, aliases, merge keys (`<<`), and explicit
  YAML document-start or document-end markers are prohibited; and
- only block collections are permitted; flow collections are prohibited.

Plain scalars use this deterministic typing rule. The exact lowercase tokens
`null`, `true`, and `false` are null and booleans. JSON-number syntax produces
numbers (with no non-finite values); every other plain scalar is a string.
Single-quoted and double-quoted scalars are always strings. In particular,
timestamps, Engram IDs, schema versions, and values such as `yes`, `no`, `on`,
and `off` are strings. Schema constraints still determine where numbers,
booleans, null, or strings are valid. Producers SHOULD quote strings when their
plain spelling would otherwise be typed as null, a boolean, or a number.

The content is Markdown, but v0.1 does not select a Markdown dialect and body
rendering is implementation-defined. Raw HTML is allowed as record text, but
no consumer is required to render it. As required by Section 13, Markdown and
raw HTML are untrusted input: consumers MUST NOT execute them and renderers
MUST sanitize or escape unsafe constructs for their output context.

The core envelope requires `id`, `schema_version`, `type`, `title`,
`created_at`, and `updated_at`. `type` is one of `note`, `project`, or `action`
in v0.1. An action additionally MUST provide `status`; it MAY provide `due_at`. A
non-action record MUST NOT contain either field. `due_at` is the instant by
which the action is intended to be complete (inclusive): an incomplete action
is overdue when the current instant is later than `due_at`. It is not a start
time, reminder time, or floating local date.

The portable status state is a snapshot, not a workflow log. `open` means work
has not started, `in_progress` means work has started, `done` means it was
completed, and `cancelled` means no completion is intended. Producers MAY make
any transition among these values, including reopening a terminal state;
consumers MUST NOT infer a restricted transition graph or transition time.
in v1.0. An action additionally MUST provide `status`; it MAY provide `due_at`.

A `parent` denotes hierarchy. Each `links` entry denotes a typed directed link.
A `synthetic_engram` target MAY be absent only from a partial package. An `outside_engram` target need not resolve. A package MUST NOT contain a cycle formed by included `parent` references.

Structured or binary information that does not map losslessly to this envelope
and Markdown body MUST be carried as a typed attachment, or in an `extensions`
value governed by a named extension profile declared in the manifest. The
attachment's media type identifies its payload format; an extension profile
defines the schema and semantics of its namespaced values. Neither mechanism
turns that data into a core record or gives core-only consumers knowledge of
its application semantics.

Consequently, converting a structured object into a core record can lose data
types, ordering, numeric precision, validation constraints, binary fidelity,
or application-specific semantics. Producers requiring exact fidelity MUST
preserve the original bytes as an attachment (including its media type, size,
and digest) rather than treating a Markdown rendering as lossless. A Markdown
summary MAY link to that attachment; the summary is a human-readable projection
and is not an authoritative replacement for the payload.

## 8. Graphs

A graph is a JSON object conforming to
[`schemas/v1.0/graph.schema.json`](schemas/v1.0/graph.schema.json). A node's
`id` is local to that graph and is only an edge endpoint; it is not an Engram
ID. A node MAY be a local annotation or grouping node with no durable-object
reference. Such a node exists only in its containing graph, MUST NOT be treated
as a package object, and MAY carry a `label` and `extensions`.

A node that represents an inventoried durable object MUST provide both its
kind-neutral `object_id` and `object_kind`. The ID MUST resolve in the package
inventory and the declared kind MUST match; records, graphs, and attachments
are permitted. A node MUST NOT use `object_id` for an object absent from the
package. An external node instead MUST contain `external_ref`, a structured
reference whose required absolute `uri` supplies its identity. An
`engram:<Engram-ID>` URI MAY identify an Engram object outside this package;
other URI schemes MAY identify non-Engram resources. `external_ref` and
`object_id` are mutually exclusive. A bare Engram ID or an `external: true`
flag does not represent an external node in v1.0.

Edges are directed ordered pairs of local node IDs, and direction is always
semantically meaningful: reversing an edge creates a different assertion.
Self-edges (`from` equal to `to`) are permitted. Multiple edges, including
edges with identical endpoints and relation, are permitted when their edge IDs
differ; they are distinct assertions and consumers MUST preserve them rather
than deduplicate them. Node IDs and edge IDs MUST each be unique within their
own sets and every endpoint MUST resolve. Empty `nodes` and `edges` arrays are
valid; a graph with edges and no nodes cannot satisfy endpoint resolution.

Core relations use the reserved `core:` vocabulary:

- `core:related_to`: the source is generally associated with the target; it
  makes no stronger claim and its reverse is not implied;
- `core:depends_on`: the source requires or relies on the target;
- `core:contains`: the source logically includes the target (not ownership or
  package inventory containment);
- `core:references`: the source cites or points to the target without claiming
  dependency; and
- `core:annotates`: the source supplies commentary or metadata about the target.

Non-core relations MUST be qualified as `prefix:term`. The prefix MUST be
declared in `relation_namespaces` as an absolute vocabulary URI. `core` is
reserved and MUST NOT be redeclared. A consumer that does not support a
declared vocabulary MUST report it as unsupported and preserve the relation
and its edge unchanged when claiming round-trip preservation; it MUST NOT
silently interpret it as a core relation. An undeclared prefix is invalid.
Vocabulary owners define non-core term semantics.

The v1.0 graph format describes interoperable topology and optional labels. It
[`schemas/v0.1/graph.schema.json`](schemas/v0.1/graph.schema.json). Nodes have
fragment IDs and MAY reference Engram IDs. Directed edges reference node fragment
IDs. Referenced Engram IDs MUST resolve unless explicitly marked external. Node
and edge IDs participate in the Engram-wide uniqueness domain described in
Section 5; they are not merely local to a graph.
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
[`schemas/v1.0/attachment.schema.json`](schemas/v1.0/attachment.schema.json).
It identifies a separate payload by relative `path`, media type, byte size, and
lowercase SHA-256 digest. The payload MUST exist and match both declared size
and digest. The metadata and payload MUST both be listed in the manifest; the
payload inventory entry uses kind `blob` and the attachment ID.

Markdown MAY refer to an attachment with
`engram-attachment:<attachment-id>`. Consumers MUST resolve that URI by ID and
MUST NOT treat an embedded path or remote URL as authoritative. The text is a
URI with the `engram-attachment` scheme and is discovered only when it is the
destination of a normal Markdown link or image. Consumers MUST NOT scan
arbitrary body text for attachment references. Because Markdown parsing is
implementation-defined, implementations MAY recognize link and image syntax
in their chosen dialect, but MUST apply this discovery rule consistently.

## 10. Extensions

Core schema objects are closed except for the `extensions` member. Graphs,
nodes, edges, and structured external references each consistently allow this
member. Extension keys MUST use reverse-DNS form (for example `org.example.priority`). Values MAY
be any JSON-compatible YAML value. An implementation that reads and rewrites an
object SHOULD preserve unknown extensions unchanged. An extension MUST NOT
change the meaning or validity of a core field.

## 11. Package features and implementation conformance

The manifest `profiles` array declares features present in **that package**; it
is not a claim about the software that wrote it. Every package MUST declare
`core`. It MUST declare `graph` when it inventories a graph, `media` when it
inventories an attachment or blob, and `action` when it contains an action
record. It MUST NOT declare an optional profile when no corresponding object is
present. Profile dependencies are only on `core`.

Implementation conformance is separately claimed per profile and role:

- A **producer** serializes packages. It MUST meet the producer requirements of
  every profile it claims; it need not import packages.
- A **consumer** reads packages. It MUST meet the consumer requirements of every
  profile it claims; it need not export packages.
- A **round-trip processor** reads and subsequently writes a package. It MUST
  meet both roles and the round-trip requirements of every profile it claims.

Thus `core` describes data required in every package; it does **not** require
every implementation to implement both import and export. An implementation
MAY claim different roles for different profiles.

To **process** a profile is to validate its normative data and expose or apply
the semantics defined here without loss that changes those semantics. To
**preserve** data is to emit the same normative values and relationships; where
this specification requires byte preservation, the exact original bytes MUST
be emitted. To **reject** is to stop processing the package without reporting
success or returning a partial package as complete. To **report unsupported**
is to return a distinct, machine-detectable outcome naming every unsupported
declared profile before processing dependent objects; a warning, log-only
message, or silent omission is not a report.

A consumer MUST either process every declared package profile or reject the
package and report all profiles it does not support. It MUST NOT silently drop
profile data. A round-trip processor MAY accept an unsupported optional profile
only in preservation mode, in which case it MUST copy every inventory entry
belonging to that profile byte-for-byte, retain its inventory metadata and
profile declaration, and report that the profile was preserved rather than
processed. Unknown extensions on processed objects MUST be preserved as the
same JSON-compatible value (byte identity is not required).

Normative requirements for each profile are:

| Profile | Producer | Consumer | Round trip |
| --- | --- | --- | --- |
| `core` | Emit a valid manifest and records; safe, complete inventory; valid unique IDs, timestamps, hierarchy, and links. | Validate those constraints, resolve internal references, and expose record Markdown and core fields. | Meet both roles; retain record identity, Markdown, hierarchy, links, timestamps, inventory membership, and unknown extensions. |
| `graph` | Declare `graph`; emit schema-valid graphs with unique local IDs, resolvable endpoints, and resolvable non-external record references. | Validate and expose graph topology, labels, and record references. | Meet both roles and preserve all nodes, edges, labels, references, and unknown extensions. |
| `media` | Declare `media`; inventory metadata and blob; emit matching path, media type, size, digest, and ID-based attachment URIs. | Verify payload presence, size, SHA-256, inventory pairing, and resolve attachment URIs by ID. | Meet both roles and preserve payload bytes, attachment identity and metadata, and URI targets. |
| `action` | Declare `action`; emit `status` on actions, optional UTC `due_at`, and neither field on other records. | Interpret status and due time exactly as in Section 7 and expose both without inventing workflow restrictions. | Meet both roles and preserve type, status, due instant, and unknown extensions. |

An implementation making public interoperability or compatibility claims MUST
publish a JSON capability document conforming to
[`schemas/v0.1/capabilities.schema.json`](schemas/v0.1/capabilities.schema.json).
The document lists supported specification versions and, independently for each
profile, any of `producer`, `consumer`, and `round-trip`. Claiming `round-trip`
also entails the producer and consumer requirements even if those strings are
omitted. Branding or certification programs MUST test the claimed matrix and
MUST NOT infer capabilities from a package's `profiles` array.
A named extension profile uses the same reverse-DNS form and MUST appear in the
manifest `profiles` array when a package relies on that profile's schema or
semantics. The profile definition MUST identify the extension keys it governs.
Declaring a profile does not make its values core fields, and consumers that do
not support it follow the unsupported-profile preservation rules below.

## 11. Profiles and conformance

v1.0 defines these profiles:

- **core:** manifest, records, stable IDs, hierarchy, links, import, and export;
- **graph:** graph objects, local nodes, and durable-object reference
  preservation;
- **media:** attachment metadata, payloads, hashes, and attachment URIs;
- **action:** action status and due-date semantics.

Additional reverse-DNS profile names designate extension profiles; their
schemas and semantics are defined outside the core specification.

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

Four different concepts MUST NOT be conflated:

- The **specification release version** (the `Version` displayed by this
  document and recorded in `CHANGELOG.md`) is Semantic Versioning. It versions
  the prose, schemas, tests, and release bundle, but is not package data.
- The **data-model version** identifies the package's core data language.
  Manifests use `data_model_version: "MAJOR.MINOR"`; it has no patch component.
- A **schema version** is a concrete validation artifact for one data-model
  major/minor, identified by its `$id` under `schema/vMAJOR.MINOR/`. Corrected
  schemas may ship in multiple specification patch releases without changing
  their `$id` or the package's data-model version, because a patch release MUST
  NOT change which package data is valid. Object `schema_version` fields record
  the schema language used for that object and likewise contain major/minor.
- **Declared optional features** are identifiers in the manifest's optional
  `features` array. They advertise semantics introduced by a minor release;
  they are not version numbers or conformance profiles.

Before full schema validation, a consumer MUST parse only a minimal manifest
envelope: `format`, `data_model_version`, and `features` (treating an absent
`features` as empty). It MUST reject malformed values and an unsupported major.
It then MUST select the highest schema it supports with the same major and a
minor no greater than the package minor. If none exists, it MUST reject the
package. Finally it validates the entire package with that schema and performs
the cross-file conformance checks. Schema selection MUST NOT begin by applying
an exact-version full manifest schema: that would prevent compatibility
negotiation.

A later minor MUST retain the earlier minor's closed core schema. New optional
feature payloads MUST therefore be stored beneath the existing `extensions`
member, keyed by the same reverse-DNS feature identifier; they MUST NOT add a
property to a closed core object, change a core field's meaning, or make
previously valid core data invalid. Producers MUST list every such feature in
`features`. A consumer that does not implement a declared feature MAY ignore
its extension payload while reading the understood core, but MUST report the
feature as unsupported. A round-trip processor MUST preserve the feature's
declaration and payload unchanged or reject the package; it MUST NOT silently
discard either. Features whose semantics cannot satisfy these rules require a
new major version.

Thus specification releases `0.1.0` and `0.1.1`, for example, both produce
`data_model_version: "0.1"`. Patch numbers never appear in package version
fields, and validators MUST NOT use an exact specification-release constant.
See [docs/versioning.md](docs/versioning.md) for the normative decision table
and fixtures.
`version` uses Semantic Versioning. Patch releases clarify text or tighten tests
without changing valid data. Minor releases add backward-compatible optional
features. Major releases may make incompatible changes. A consumer MUST reject
a package with an unsupported major version and SHOULD report unsupported minor
features rather than silently discard them.

Schema paths are versioned by major and minor version. Package data uses
`schema_version: "1.0"`; it does not include the patch version.

## 13. Security and privacy

Package content is untrusted input. Implementations MUST prevent path traversal,
MUST enforce resource limits, and MUST NOT execute record content. Media types,
filenames, links, extensions, Markdown, and graph labels MUST be treated as
untrusted. Hashes provide integrity checks, not authenticity. Encryption,
signing, identity proof, and authorization are outside v1.0; applications MUST
not infer permission merely from possession of a package. See [SECURITY.md](SECURITY.md).

## 14. Non-goals and future work

v1.0 does not define synchronization, conflict resolution, access-control
descriptors, certification branding, query lenses, AI context selection, or
portable revision deltas. Non-Markdown structured records and binary core
records are explicitly deferred beyond 1.0; adding them requires a future
specification to define a format-independent envelope and normative recovery
mappings rather than relying on filename extensions. These subjects remain
documented in
[docs/open-questions.md](docs/open-questions.md).
