# Engram Mesh and Open Knowledge Format interoperability

**Status:** non-normative mapping guidance for Engram Mesh 0.3 draft  
**OKF baseline:** Open Knowledge Format 0.2, reviewed 2026-08-19  
**Source:** [GoogleCloudPlatform/knowledge-catalog `okf/SPEC.md`](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)

This document describes how Engram Mesh can use OKF without redefining OKF or
claiming a formal extension. Because the cited OKF source is an evolving branch,
an implementation should record the exact upstream revision it targets and
recheck the mapping before publishing compatibility claims.

## Different interoperability layers

```text
OKF                 portable knowledge documents and bundles
Engram Mesh         stable cross-source identity, binding, and relationships
MCP or another API  optional runtime access
```

An OKF bundle can exist without Engram Mesh. an Engram Mesh can connect sources
that do not use OKF. An implementation can use OKF to materialize knowledge
selected from a mesh, but the OKF bundle is not the mesh itself.

## Concept mapping

| Engram Mesh concept | Closest OKF 0.2 concept | Mapping | Important limitation |
| --- | --- | --- | --- |
| Mesh Slice | Knowledge Bundle | Materialize selected nodes as concept documents in a bundle. | A bundle does not establish that it is a complete mesh or preserve omitted/unauthorized boundary states. |
| Node | Concept | A content-bearing node can be rendered as one concept. | An OKF Concept ID is its bundle-relative path; it is not a stable Engram Mesh node ID. A node may also have no materialized content. |
| Presentation type/title/description/tags | `type`, `title`, `description`, `tags` | Reuse the OKF fields directly. | Do not duplicate these as Engram Mesh-specific fields in the concept. |
| Bound canonical asset URI | `resource` | Use `resource` when the URI identifies the asset the concept describes. | A provider URL, local resolver hint, or binding external ID is not automatically a canonical URI. |
| Content provenance | `sources[]` | Use OKF sources for materials from which the materialized concept derives. | an Engram Mesh Source Binding identifies the object represented by a node; it is not necessarily provenance and must not be rewritten as `sources[]` by default. |
| Generation and verification | `generated`, `verified` | Preserve OKF generation and verification metadata when it applies to the materialized concept. | Verification is not source authorization, binding freshness, or content ownership. |
| Lifecycle hints | `status`, `stale_after` | Reuse them for the OKF concept's lifecycle. | They do not replace a source revision, digest, timestamp, or opaque freshness token on a binding. |
| Relationship | Markdown link | Emit a link when the relationship is meaningfully represented in prose. | OKF links are untyped and path-based; relationship ID, type, and exact cross-source endpoint are lost. |
| Logical hierarchy | Bundle directories or indexes | A producer may choose a matching presentation hierarchy. | OKF layout is physical bundle organization; Engram Mesh hierarchy is logical and need not match it. |
| Source | `sources[]` entry or `resource` in some cases | Map only when the OKF semantics genuinely match provenance or the described asset. | Engram Mesh Source is an administrative identity domain, for which OKF has no direct equivalent. |
| Source Binding | None | Keep it in the Engram Mesh representation or an explicitly documented prototype extension. | OKF does not carry cross-source binding identity, authority classification, resolver hints, or capabilities. |
| Authority classification | None | Preserve outside the plain OKF mapping. | Availability in a bundle does not transfer source ownership. |
| Source capabilities | None | Preserve outside the plain OKF mapping. | OKF content fields do not express discover/read/create/modify/move/delete support or authorization. |
| Lens | None | A lens may select the concepts emitted into a bundle. | The bundle contains the result, not the lens expression or its mechanism. |

## Importing OKF into an Engram Mesh

An importer should treat an OKF bundle as a source, not as an Engram Mesh wire
format.

1. Create or reuse an Engram Mesh Source for the OKF bundle's identity domain.
2. Create or match one node for each imported OKF concept.
3. Bind the node to the concept using the OKF Concept ID as the binding's
   external ID.
4. Keep the Engram Mesh node ID independent of the concept path. A rename or
   move should update the binding when continuity is known, not mint a new node.
5. Reuse OKF `type`, `title`, `description`, `resource`, `tags`, provenance,
   trust, and lifecycle fields with their OKF meaning.
6. Treat Markdown links as candidate untyped relationships. Do not invent a
   typed relationship unless the importer has an explicit mapping rule.
7. Classify the binding as `authoritative` when that Source controls the
   represented content; otherwise use `replica` or `reference` explicitly.

Matching an existing node is an application identity decision. Filename,
title, body similarity, or `resource` alone is insufficient evidence for a
silent merge.

## Exporting or materializing as OKF

An exporter should treat an OKF bundle as one materialization of a Mesh Slice.

1. Select nodes and relationships under application authorization policy.
2. Record the slice boundary and omissions in the Engram Mesh-side export
   report.
3. Emit one OKF concept for each selected content-bearing node.
4. Reuse OKF fields wherever they are sufficient; do not introduce duplicate
   Engram Mesh spellings for them.
5. Use `resource` only for the represented asset's canonical URI and
   `sources[]` only for provenance.
6. Emit Markdown links when an untyped link preserves useful meaning.
7. Report typed relationships, bindings, authority, capability information,
   and stable node identity as losses unless the recipient also receives a
   Engram Mesh representation or understands an explicitly identified
   prototype extension.

A plain OKF bundle can therefore be a useful portable projection but is not
currently a lossless Engram Mesh round trip. Engram Mesh 0.3 does not reserve or
standardize OKF frontmatter keys. A prototype MAY use producer-defined
namespaced fields allowed by OKF, but it must document them and must not call
them a standard Engram Mesh profile.

## Worked examples

### OKF-backed node

```text
Engram Mesh node: node_01...
Source:            source_okf_docs
External ID:       runbooks/incident-response
Authority:         authoritative
Materialization:   runbooks/incident-response.md (OKF Concept)
```

The OKF document carries its normal `type`, `title`, `description`, and content.
The Engram Mesh binding retains the stable node ID and tracks a later concept
path if the file moves.

### Non-OKF external source

```text
Engram Mesh node: node_02...
Source:            source_google_drive_team
External ID:       provider-stable-object-id
Authority:         authoritative
Resolver hint:     google-drive
```

No OKF document is required. If the node is later materialized as OKF, its
canonical share URI may map to `resource` when appropriate; credentials and
provider connection state remain local.

### Bounded materialization

A lens selects three authorized nodes from GitHub, an OKF bundle, and a native
store. The exporter creates one OKF bundle containing three concepts and useful
Markdown links. The accompanying Engram Mesh Slice records the original stable
node IDs, typed relationships, source bindings, authority, selection mechanism,
and omitted boundary edges. Without that companion representation, the OKF
bundle remains valid but the Engram Mesh-specific information is lossy.

## Compatibility claims

An implementation should report the layers separately:

```text
Engram Mesh model: draft 0.3 prototype
OKF output:        OKF 0.2
Mapping:           this document plus an exact implementation version
Known losses:      typed edges, stable mesh IDs, bindings, authority, capabilities
Runtime:           MCP, HTTP, library API, or another declared interface
```

Supporting both specifications does not make either conformance claim imply the
other.
