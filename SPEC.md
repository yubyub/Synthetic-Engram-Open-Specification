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

A `parent` denotes hierarchy. Each `links` entry denotes a typed directed link.
A `synthetic_engram` target MAY be absent only from a partial package. An `outside_engram` target need not resolve. A package MUST NOT contain a cycle formed by included `parent` references.

## 8. Graphs

A graph is a JSON object conforming to
[`schemas/v0.1/graph.schema.json`](schemas/v0.1/graph.schema.json). Nodes have
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
