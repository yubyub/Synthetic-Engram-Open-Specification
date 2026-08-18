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

<a id="req-encoding-json-utf8"></a> **REQ-ENC-001:** JSON documents MUST be UTF-8 encoded.
<a id="req-encoding-json-unique"></a> **REQ-ENC-002:** JSON documents MUST NOT contain duplicate object keys.
<a id="req-encoding-markdown-utf8"></a> **REQ-ENC-003:** Markdown records MUST be UTF-8 encoded.
<a id="req-path-portable"></a> **REQ-PATH-001:** Package paths MUST use `/` as the separator and MUST be relative.
<a id="req-path-safe"></a> **REQ-PATH-002:** Package paths MUST NOT contain an empty segment, `.` segment, `..` segment, or NUL byte.
<a id="req-path-archive"></a> **REQ-PATH-003:** An archive consumer MUST reject entries that escape the extraction root.

<a id="req-time-utc"></a> **REQ-TIME-001:** Timestamps MUST be RFC 3339 `date-time` strings in UTC and use the `Z` suffix.
Producers SHOULD emit seconds even when the value has no sub-second precision.

## 5. Identifiers

<a id="req-id-shape"></a> **REQ-ID-001:** Every durable package object MUST have an ID matching:

```regex
^[a-z][a-z0-9-]{1,31}_[0-9A-HJKMNP-TV-Z]{26}$
```

The prefix communicates an object kind (for example `engram_`, `note_`, or
`attachment_`); the suffix is a canonical uppercase ULID. <a id="req-id-unique"></a> **REQ-ID-002:** IDs MUST be unique within a package.
<a id="req-id-stable"></a> **REQ-ID-003:** IDs MUST NOT be reassigned to a different logical object.
<a id="req-id-independent"></a> **REQ-ID-004:** Identity MUST NOT depend on a title, filename, path, or storage key.

## 6. Package manifest

<a id="req-manifest-root"></a> **REQ-MAN-001:** The package root MUST contain `engram.json`, conforming to
[`schemas/v0.1/manifest.schema.json`](schemas/v0.1/manifest.schema.json).
It declares:

- `format`, fixed to `synthetic-engram`;
- specification `version`;
- the package `id`;
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

## 7. Records

<a id="req-record-envelope"></a> **REQ-REC-001:** A record MUST be a `.md` file consisting of YAML 1.2 front matter followed by Markdown content; front matter begins with `---` on the first line and ends with `---` on a line by itself.
<a id="req-record-schema"></a> **REQ-REC-002:** It MUST conform to
[`schemas/v0.1/record.schema.json`](schemas/v0.1/record.schema.json).

The core envelope requires `id`, `schema_version`, `type`, `title`,
`created_at`, and `updated_at`. `type` is one of `note`, `project`, or `action`
in v0.1. <a id="req-action-status"></a> **REQ-REC-003:** An action additionally MUST provide `status`; it MAY provide `due_at`.

A `parent` denotes hierarchy. Each `links` entry denotes a typed directed link.
A target MAY be external to a partial package only when the link sets
`external: true`; otherwise <a id="req-link-resolve"></a> **REQ-REF-001:** it MUST resolve to an inventoried object.
<a id="req-hierarchy-acyclic"></a> **REQ-REF-002:** A package MUST NOT contain a cycle formed by `parent` references.

## 8. Graphs

A graph is a JSON object conforming to
[`schemas/v0.1/graph.schema.json`](schemas/v0.1/graph.schema.json). Nodes have
local IDs and MAY reference Engram IDs. Directed edges reference local node IDs.
<a id="req-graph-resolve"></a> **REQ-GRAPH-001:** Referenced Engram IDs MUST resolve unless explicitly marked external.
<a id="req-graph-ids"></a> **REQ-GRAPH-002:** Node and edge IDs MUST each be unique within their graph.

The v0.1 graph format describes interoperable topology and optional labels. It
does not standardize layout, rendering, or an application-specific graph DSL.

## 9. Attachments

Attachment metadata is a JSON object conforming to
[`schemas/v0.1/attachment.schema.json`](schemas/v0.1/attachment.schema.json).
It identifies a separate payload by relative `path`, media type, byte size, and
lowercase SHA-256 digest. <a id="req-media-integrity"></a> **REQ-MEDIA-001:** The payload MUST exist and match both declared size and digest.
<a id="req-media-inventory"></a> **REQ-MEDIA-002:** The metadata and payload MUST both be listed in the manifest; the payload inventory entry uses kind `blob` and the attachment ID.

Markdown MAY refer to an attachment with
`engram-attachment:<attachment-id>`. <a id="req-media-uri"></a> **REQ-MEDIA-003:** Consumers MUST resolve that URI by ID and MUST NOT treat an embedded path or remote URL as authoritative.

## 10. Extensions

Core schema objects are closed except for the `extensions` member. <a id="req-extension-name"></a> **REQ-EXT-001:** Extension keys MUST use reverse-DNS form (for example `org.example.priority`). Values MAY
be any JSON-compatible YAML value. An implementation that reads and rewrites an
object SHOULD preserve unknown extensions unchanged. <a id="req-extension-core"></a> **REQ-EXT-002:** An extension MUST NOT change the meaning or validity of a core field.

## 11. Profiles and conformance

v0.1 defines these profiles:

- **core:** manifest, records, stable IDs, hierarchy, links, import, and export;
- **graph:** graph objects and referenced-record preservation;
- **media:** attachment metadata, payloads, hashes, and attachment URIs;
- **action:** action status and due-date semantics.

<a id="req-profile-core"></a> **REQ-PROF-001:** Every package MUST declare `core`.
<a id="req-profile-optional"></a> **REQ-PROF-002:** It MUST declare each optional profile whose objects it contains.
<a id="req-conformance-claim"></a> **REQ-CONF-001:** An implementation MUST state whether it is a producer, consumer, or round-trip processor and which profiles it supports.

<a id="req-producer-valid"></a> **REQ-CONF-002:** A conforming producer MUST create schema-valid packages satisfying all cross-file requirements.
<a id="req-consumer-profile"></a> **REQ-CONF-003:** A conforming consumer MUST either process a declared profile or report it as unsupported; it MUST NOT silently claim successful support. A round-trip processor SHOULD preserve unsupported inventoried objects
and unknown extensions byte-for-byte when it claims preservation.

See [docs/conformance.md](docs/conformance.md) for the testable checklist.

## 12. Versioning

`version` uses Semantic Versioning. Patch releases clarify text or tighten tests
without changing valid data. Minor releases add backward-compatible optional
features. Major releases may make incompatible changes. <a id="req-version-major"></a> **REQ-VERS-001:** A consumer MUST reject a package with an unsupported major version and SHOULD report unsupported minor
features rather than silently discard them.

Schema paths are versioned by major and minor version. Package data uses
`schema_version: "0.1"`; it does not include the patch version.

## 13. Security and privacy

Package content is untrusted input. <a id="req-security-input"></a> **REQ-SEC-001:** Implementations MUST prevent path traversal, MUST enforce resource limits, and MUST NOT execute record content.
<a id="req-security-untrusted"></a> **REQ-SEC-002:** Media types, filenames, links, extensions, Markdown, and graph labels MUST be treated as untrusted. Hashes provide integrity checks, not authenticity. Encryption,
signing, identity proof, and authorization are outside v0.1; <a id="req-security-permission"></a> **REQ-SEC-003:** Applications MUST NOT infer permission merely from possession of a package. See [SECURITY.md](SECURITY.md).

## 14. Non-goals and future work

v0.1 does not define synchronization, conflict resolution, access-control
descriptors, certification branding, query lenses, AI context selection, or
portable revision deltas. These subjects remain documented in
[docs/open-questions.md](docs/open-questions.md).
