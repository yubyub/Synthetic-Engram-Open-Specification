# Synthetic Engram Open Standard 0.2

**Status:** Pilot specification

**Version:** 0.2.0
**Schema base:** `https://raw.githubusercontent.com/yubyub/Synthetic-Engram-Open-Standard/v0.2.0/schemas/v0.2/`

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
- **Engram Package:** a directory containing all or part of a Synthetic Engram
  in this portable representation. A package is an interchange instance, not
  the Engram itself.
- **Engram Record:** one durable typed object in an Engram.
- **Engram ID:** the stable `engram_id` of the Synthetic Engram.
- **Package ID:** manifest `id`, identifying one serialized package instance. Repacking creates a new Package ID.
- **Export ID:** manifest `export_id`, identifying the logical export event. Retries retain it but use distinct Package IDs.
- **Implementation:** software that produces or consumes an Engram Package.
- **Extension:** namespaced, non-core data preserved alongside core data.

## 4. Encoding and paths

<a id="req-encoding-json-utf8"></a> **REQ-ENC-001:** JSON documents MUST be UTF-8 encoded.
<a id="req-encoding-json-unique"></a> **REQ-ENC-002:** JSON documents MUST NOT contain duplicate object keys.
<a id="req-encoding-markdown-utf8"></a> **REQ-ENC-003:** Markdown records MUST be UTF-8 encoded.
<a id="req-path-portable"></a> **REQ-PATH-001:** Package paths MUST use `/` as the separator and MUST be relative.
<a id="req-path-safe"></a> **REQ-PATH-002:** Package paths MUST NOT contain an empty segment, `.` segment, `..` segment, or NUL byte.
<a id="req-path-archive"></a> **REQ-PATH-003:** If an implementation chooses to
extract an archive transport wrapper, it MUST prevent every archive entry from
escaping the extraction root and MUST enforce resource limits during
inspection and extraction.

### 4.1 Canonical directory representation

The canonical core 0.2 interchange representation of an Engram Package is the
directory tree rooted at `engram.json`. Package paths describe locations in
that directory tree.

ZIP, tar, and other archive formats MAY carry a directory-form Engram Package
as transport wrappers. Core 0.2 does not select an archive format, media type,
entry model, or serialization. Consequently, an archive wrapper cannot
independently claim standardized archive conformance under core 0.2. A core
conformance claim applies to the represented directory package after any
implementation-defined, security-constrained extraction.

A future [Archive Binding Specification](docs/archive-binding.md) will define
standardized archive conformance without changing the identity or package-path
semantics of the canonical directory representation.

<a id="req-time-utc"></a> **REQ-TIME-001:** Timestamps MUST be RFC 3339 `date-time` strings in UTC and use the `Z` suffix.
Producers SHOULD emit seconds even when the value has no sub-second precision.

## 5. Identifiers

<a id="req-id-shape"></a> **REQ-ID-001:** Every Synthetic Engram, export event,
package instance, and durable object MUST have an ID matching:

```regex
^[a-z][a-z0-9-]{1,31}_[0-9A-HJKMNP-TV-Z]{26}$
```

The prefix communicates an object kind; the suffix is a canonical uppercase
ULID. Manifest package, Engram, and export IDs MUST use `package_`, `engram_`,
and `export_` respectively. Record implementations SHOULD use a meaningful
type prefix such as `note_`, `project_`, or `action_`; attachments use
`attachment_` for both metadata and its payload inventory entry.
<a id="req-id-unique"></a> **REQ-ID-002:** IDs MUST be unique within a package,
except that the attachment metadata entry and its required `blob` entry share
one attachment ID as specified by REQ-INV-004.
<a id="req-id-stable"></a> **REQ-ID-003:** IDs MUST NOT be reassigned to a different logical object.
<a id="req-id-independent"></a> **REQ-ID-004:** Identity MUST NOT depend on a title, filename, path, or storage key.

## 6. Package manifest

<a id="req-manifest-root"></a> **REQ-MAN-001:** The package root MUST contain `engram.json`, conforming to
[`schemas/v0.2/manifest.schema.json`](schemas/v0.2/manifest.schema.json).
It declares:

- `format`, fixed to `synthetic-engram`;
- specification `version`;
- package-instance `id`, stable Synthetic Engram `engram_id`, and export-event `export_id`;
- `completeness`, either `complete` or `partial`;
- creation and update timestamps;
- an owner descriptor;
- supported conformance `profiles`; and
- an explicit inventory of package objects.

<a id="req-inventory-fields"></a> **REQ-INV-001:** Each inventory entry MUST name an ID, kind, media type, and package-relative path.
<a id="req-inventory-exists"></a> **REQ-INV-002:** The path MUST exist.
<a id="req-inventory-id-match"></a> **REQ-INV-003:** Its contained object ID MUST equal the inventory ID.
<a id="req-inventory-unique"></a> **REQ-INV-004:** Inventory IDs MUST be unique except that an attachment's `blob` entry MUST repeat its attachment metadata ID.
<a id="req-inventory-complete"></a> **REQ-INV-005:** Producers MUST list every normative object.
<a id="req-inventory-no-infer"></a> **REQ-INV-006:** Consumers MUST NOT infer that unlisted files are normative package objects.


### 6.1 Package scope

<a id="req-scope-partial-metadata"></a> **REQ-SCOPE-001:** A package whose `completeness` is `partial` MUST contain `partial` metadata with either a reproducible selection `mechanism` (a `type` and non-empty `expression`) or a non-empty opaque `description`; it MAY contain both.
<a id="req-scope-selection-proof"></a> **REQ-SCOPE-002:** An implementation MUST NOT treat selection metadata as proof that every matching source object was exported.
<a id="req-scope-complete-metadata"></a> **REQ-SCOPE-003:** A package whose `completeness` is `complete` MUST NOT contain `partial` metadata.

These terms are distinct:

- **Not inventoried** means a file is present in the package but has no `objects` entry. It has no normative object status.
- **External to this package** means a durable member of this Synthetic Engram is absent from this package. This is permitted only for a partial package. Inventory presence, rather than a reference flag, determines this status.
- **External to the Synthetic Engram** means the referenced entity is not a durable member of this Engram. It is never required in the inventory.

<a id="req-scope-fields"></a> **REQ-SCOPE-004:** A reference MUST express Engram membership with its context-specific scope field: `target_scope` for a record link, `parent_scope` for a record parent, or `record_scope` for a graph-node record. For each field, omission has the schema-defined default `synthetic_engram`; `outside_engram` denotes a non-member.

### 6.2 Complete export closure

<a id="req-closure-inventory"></a> **REQ-CLOSE-001:** With `completeness: complete`, `objects` MUST inventory every current durable record (including its normative Markdown body), graph, attachment metadata object, attachment payload, and other current durable artifact owned by the Synthetic Engram at the export snapshot, and the package MUST contain each one.
<a id="req-closure-extensions"></a> **REQ-CLOSE-002:** Normative extension data owned at that snapshot MUST appear in a complete package. Deleted, superseded, or historical revisions need not appear unless retained as current durable artifacts.

<a id="req-closure-transient"></a> **REQ-CLOSE-003:** A complete export MUST NOT classify transient caches, search indexes, lock files, sessions, credentials, access tokens, telemetry, temporary files, or unfinished writes as normative objects. It need not include thumbnails, previews, embeddings, rendered HTML, compiled views, query results, model outputs, or other reproducible derivative artifacts.
<a id="req-closure-adopted"></a> **REQ-CLOSE-004:** A derivative artifact deliberately adopted as durable owner-controlled knowledge MUST be inventoried under an applicable profile or namespaced extension.

Completeness is a claim about the producer's source snapshot, not merely package
self-consistency. <a id="req-closure-compare"></a> **REQ-CLOSE-005:** A producer of a complete package MUST compare the inventory with that snapshot. A consumer can verify packaged evidence, but cannot prove disclosure of an object for which the package contains no evidence.

## 7. Records

<a id="req-record-envelope"></a> **REQ-REC-001:** A record MUST be a `.md` file consisting of YAML 1.2 front matter followed by Markdown content; front matter begins with `---` on the first line and ends with `---` on a line by itself.
<a id="req-record-schema"></a> **REQ-REC-002:** Its front matter MUST conform to [`schemas/v0.2/record.schema.json`](schemas/v0.2/record.schema.json).

### 7.1 Serialization

<a id="req-record-no-bom"></a> **REQ-REC-003:** A record MUST be UTF-8 without a byte-order mark. Lines MAY end with LF or CRLF; a bare CR is not a line ending.
<a id="req-record-normalization"></a> **REQ-REC-004:** A consumer MUST NOT require or silently apply a Unicode normalization form. Producers SHOULD emit NFC.

<a id="req-record-delimiters"></a> **REQ-REC-005:** The opening delimiter MUST be exactly the three ASCII characters `---`, followed by LF or CRLF, at byte zero; the closing delimiter MUST be the next line containing exactly `---`, followed by LF, CRLF, or end of file. Everything after the closing delimiter and its optional line ending is record content, which MAY be empty.

<a id="req-record-yaml-document"></a> **REQ-REC-006:** Front matter MUST contain exactly one mapping in exactly one YAML 1.2 document.
<a id="req-record-yaml-keys"></a> **REQ-REC-007:** Every front-matter mapping key MUST be a string and MUST be unique within its mapping.
<a id="req-record-yaml-features"></a> **REQ-REC-008:** Front matter MUST NOT use directives, explicit tags, anchors, aliases, merge keys (`<<`), explicit document markers, or flow collections. Block sequences, block mappings, and JSON-compatible scalar values are permitted.

<a id="req-record-yaml-typing"></a> **REQ-REC-009:** A parser MUST type plain scalars deterministically: the exact lowercase tokens `null`, `true`, and `false` are null and booleans; JSON-number syntax produces finite numbers; every other plain scalar is a string; and all quoted scalars are strings. Producers SHOULD quote strings whose plain spelling would otherwise receive another type.

The content is Markdown, but 0.2 does not select a Markdown dialect and body
rendering is implementation-defined. Raw HTML is allowed as record text. See
[REQ-SEC-003](#req-security-execution) for the authoritative non-execution
rule.
<a id="req-record-render"></a> **REQ-REC-010:** A renderer MUST sanitize or escape unsafe constructs for its output context.

The core envelope fields and allowed record types are defined by the record schema. <a id="req-action-status"></a> **REQ-REC-011:** An action record MUST provide `status`; it MAY provide `due_at`.

### 7.2 References and hierarchy

A `parent` denotes hierarchy. Each `links` entry denotes a typed directed link. The authoritative resolution rule for all record and graph references is:

<a id="req-reference-resolution"></a> **REQ-REF-001:** For a record `parent`, record-link `target`, or graph-node `record`, a reference whose applicable scope (`parent_scope`, `target_scope`, or `record_scope`) is `synthetic_engram` MUST resolve to an inventoried object in a complete package and MAY be absent only from a partial package; a reference scoped `outside_engram` is not required to resolve.

<a id="req-hierarchy-acyclic"></a> **REQ-REF-002:** The directed relation from each included record to its `parent` MUST NOT contain a cycle among included records.

## 8. Graphs

A graph is a JSON object conforming to [`schemas/v0.2/graph.schema.json`](schemas/v0.2/graph.schema.json). Nodes have local IDs and MAY reference Engram record IDs. Directed edges reference local node IDs. Graph-node record references use [REQ-REF-001](#req-reference-resolution).

<a id="req-graph-node-ids"></a> **REQ-GRAPH-001:** Node IDs MUST be unique within their graph.
<a id="req-graph-edge-ids"></a> **REQ-GRAPH-002:** Edge IDs MUST be unique within their graph.
<a id="req-graph-endpoints"></a> **REQ-GRAPH-003:** Each edge's `from` and `to` values MUST resolve to node IDs in the same graph.

The 0.2 graph format describes interoperable topology and optional labels. It
does not standardize layout, rendering, or an application-specific graph DSL.

## 9. Attachments

Attachment metadata is a JSON object conforming to [`schemas/v0.2/attachment.schema.json`](schemas/v0.2/attachment.schema.json). It identifies a separate payload by relative `path`, media type, byte size, and lowercase SHA-256 digest.

<a id="req-media-integrity"></a> **REQ-MEDIA-001:** The payload MUST exist at the metadata object's `path`, and its bytes MUST match both the declared `size` and `sha256` digest.
<a id="req-media-inventory"></a> **REQ-MEDIA-002:** Attachment metadata and its payload MUST both be listed in the manifest; the payload entry MUST use kind `blob`, the attachment ID, and the metadata object's payload `path`.

Markdown MAY refer to an attachment with `engram-attachment:<attachment-id>`.
<a id="req-media-uri-resolve"></a> **REQ-MEDIA-003:** A consumer MUST resolve an `engram-attachment` URI by its attachment ID and MUST NOT treat a path or remote URL suggested elsewhere in the record as authoritative.
<a id="req-media-uri-discovery"></a> **REQ-MEDIA-004:** A consumer MUST discover attachment URIs only as destinations of Markdown links or images and MUST NOT scan arbitrary body text for attachment references. An implementation MAY recognize link and image syntax in its chosen Markdown dialect.

## 10. Extensions

Core schema objects are closed except for the `extensions` member. <a id="req-extension-name"></a> **REQ-EXT-001:** Extension keys MUST use reverse-DNS form (for example `org.example.priority`). Values MAY
be any JSON-compatible YAML value. An implementation that reads and rewrites an
object SHOULD preserve unknown extensions unchanged. <a id="req-extension-core"></a> **REQ-EXT-002:** An extension MUST NOT change the meaning or validity of a core field.

## 11. Profiles and conformance

Version 0.2 defines these profiles:

- **core:** manifest, records, stable IDs, hierarchy, links, import, and export;
- **graph:** graph objects and referenced-record preservation;
- **media:** attachment metadata, payloads, hashes, and attachment URIs;
- **action:** action status and due-date semantics.

<a id="req-profile-core"></a> **REQ-PROF-001:** Every package MUST declare `core`.
<a id="req-profile-optional"></a> **REQ-PROF-002:** It MUST declare each optional profile whose objects it contains.
<a id="req-conformance-claim"></a> **REQ-CONF-001:** An implementation MUST state whether it is a producer, consumer, or round-trip processor and which profiles it supports.

<a id="req-producer-valid"></a> **REQ-CONF-002:** A conforming producer MUST create schema-valid packages satisfying all cross-file requirements.
<a id="req-consumer-profile"></a> **REQ-CONF-003:** A conforming consumer MUST either process a declared profile or report it as unsupported.
<a id="req-consumer-claim"></a> **REQ-CONF-004:** A consumer MUST NOT report successful support for a profile it did not process. A round-trip processor SHOULD preserve unsupported inventoried objects
and unknown extensions byte-for-byte when it claims preservation.

See [docs/conformance.md](docs/conformance.md) for the testable checklist.

## 12. Versioning

`version` has three numeric components and follows the pre-1.0 policy in
[docs/versioning.md](docs/versioning.md). In the pilot series, a new minor
version may be incompatible; patch versions within the same minor line are
compatible corrections.

<a id="req-version-major"></a> **REQ-VERS-001:** A consumer MUST reject a
package with an unsupported major version and MUST NOT report successful
consumption.

<a id="req-version-capability"></a> **REQ-VERS-002:** A consumer MUST reject a
package whose major/minor line it does not support. For a supported major/minor
line, it MUST accept any patch version that satisfies the schemas and other
requirements, but MUST report a non-success result for every unsupported
declared profile or other required capability rather than silently discard its
governed data.

<a id="req-version-preservation"></a> **REQ-VERS-003:** A round-trip processor
claiming unknown-data preservation MUST preserve unknown extension keys and
values with deep structural equality and MUST report namespace collisions
rather than merge or reinterpret them.

Schema paths are versioned by major and minor version. Package data uses
`schema_version: "0.2"`; it does not include the patch version.

## 13. Security and privacy

Package content is untrusted input.
<a id="req-security-path"></a> **REQ-SEC-001:** Implementations MUST prevent path traversal.
<a id="req-security-limits"></a> **REQ-SEC-002:** Implementations MUST enforce resource limits.
<a id="req-security-execution"></a> **REQ-SEC-003:** Implementations MUST NOT execute record content.
<a id="req-security-untrusted"></a> **REQ-SEC-004:** Media types, filenames, links, extensions, Markdown, and graph labels MUST be treated as untrusted. Hashes provide integrity checks, not authenticity. Encryption, signing, identity proof, and authorization are outside core 0.2.
<a id="req-security-permission"></a> **REQ-SEC-005:** Applications MUST NOT infer permission merely from possession of a package. See [SECURITY.md](SECURITY.md).

## 14. Non-goals and future work

Core 0.2 does not define synchronization, conflict resolution, access-control
descriptors, certification branding, query lenses, AI context selection, or
portable revision deltas. Pilot feedback may justify future specifications,
but applications must not infer these capabilities from 0.2 conformance.

Standardized archive serialization is also outside core 0.2 and is reserved
for the future [Archive Binding Specification](docs/archive-binding.md).
