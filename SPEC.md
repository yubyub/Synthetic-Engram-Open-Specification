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
[`schemas/v0.1/manifest.schema.json`](schemas/v0.1/manifest.schema.json).
It declares:

- `format`, fixed to `synthetic-engram`;
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
in v0.1. An action additionally MUST provide `status`; it MAY provide `due_at`.

A `parent` denotes hierarchy. Each `links` entry denotes a typed directed link.
A `synthetic_engram` target MAY be absent only from a partial package. An `outside_engram` target need not resolve. A package MUST NOT contain a cycle formed by included `parent` references.

## 8. Graphs

A graph is a JSON object conforming to
[`schemas/v0.1/graph.schema.json`](schemas/v0.1/graph.schema.json). Nodes have
fragment IDs and MAY reference Engram IDs. Directed edges reference node fragment
IDs. Referenced Engram IDs MUST resolve unless explicitly marked external. Node
and edge IDs participate in the Engram-wide uniqueness domain described in
Section 5; they are not merely local to a graph.
local IDs and MAY reference Engram IDs. Directed edges reference local node IDs.
Referenced Engram IDs MUST resolve in a complete package unless their `record_scope` is `outside_engram`. Node and
edge IDs MUST each be unique within their graph.

The v0.1 graph format describes interoperable topology and optional labels. It
does not standardize layout, rendering, or an application-specific graph DSL.

## 9. Attachments

Attachment metadata is a JSON object conforming to
[`schemas/v0.1/attachment.schema.json`](schemas/v0.1/attachment.schema.json).
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
