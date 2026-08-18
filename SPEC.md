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
- data-model `data_model_version` (major and minor only);
- optional minor-version `features`, when used;
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
in v0.1. An action additionally MUST provide `status`; it MAY provide `due_at`.

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
