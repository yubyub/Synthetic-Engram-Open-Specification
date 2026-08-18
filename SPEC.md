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

- **Synthetic Engram:** the complete durable knowledge environment.
- **Engram Package:** a directory or archive containing all or part of a
  Synthetic Engram in this portable representation.
- **Engram Record:** one durable typed object in an Engram.
- **Engram ID:** a stable identifier for a package object.
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

Every durable package object MUST have an ID matching:

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
- the package `id`;
- creation and update timestamps;
- an owner descriptor;
- supported conformance `profiles`; and
- an explicit inventory of package objects.

Each inventory entry MUST name an ID, kind, media type, and package-relative
path. The path MUST exist and its contained object ID MUST equal the inventory
ID. Inventory IDs MUST be unique except that an attachment's `blob` entry MUST
repeat its attachment metadata ID. Producers MUST list every normative object.
Consumers MUST NOT infer that unlisted files are normative package objects.

## 7. Records

A record MUST be a `.md` file consisting of YAML 1.2 front matter followed by
Markdown content. Front matter begins with `---` on the first line and ends
with `---` on a line by itself. It MUST conform to
[`schemas/v0.1/record.schema.json`](schemas/v0.1/record.schema.json).

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
A target MAY be external to a partial package only when the link sets
`external: true`; otherwise it MUST resolve to an inventoried object. A package
MUST NOT contain a cycle formed by `parent` references.

## 8. Graphs

A graph is a JSON object conforming to
[`schemas/v0.1/graph.schema.json`](schemas/v0.1/graph.schema.json). Nodes have
local IDs and MAY reference Engram IDs. Directed edges reference local node IDs.
Referenced Engram IDs MUST resolve unless explicitly marked external. Node and
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
MUST NOT treat an embedded path or remote URL as authoritative.

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
