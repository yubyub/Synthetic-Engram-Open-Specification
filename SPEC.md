# Engram Mesh Open Specification 0.3

**Status:** pilot specification

**Version:** 0.3.0
**Supersedes:** Synthetic Engram 0.2 for future development; it does not alter
the 0.2 package contract

## 1. Scope

Engram Mesh defines a source-independent logical mesh that identifies knowledge
and relates it across independently owned storage systems. Knowledge may remain
in its authoritative source. an Engram Mesh implementation supplies the
connective model without requiring the source content to be copied, rewritten,
or owned by Engram Mesh.

This specification defines the abstract information model, a canonical JSON
document, and conformance obligations. The document is `engram-mesh.json` and
MUST conform to [`schemas/v0.3/mesh.schema.json`](schemas/v0.3/mesh.schema.json).

Engram Mesh does not define:

- a general knowledge-document format;
- a storage engine, database, filesystem layout, or synchronization service;
- full-text or semantic search, embeddings, chunks, ranking, or indexes;
- an authentication mechanism or credential representation;
- an application server, user interface, container, or deployment model;
- an AI-memory algorithm or agent policy; or
- a runtime protocol. MCP, HTTP, GraphQL, library APIs, CLIs, and application
  plugins can expose Engram Mesh implementations without becoming part of the
  Engram Mesh data model.

## 2. Requirements language and conformance

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**,
and **MAY** are to be interpreted as described by BCP 14 (RFC 2119 and RFC
8174) when, and only when, they appear in all capitals.

This specification defines three implementation roles:

- a **producer** emits a portable representation of the abstract model;
- a **consumer** reads that representation; and
- a **resolver** uses implementation-local connection state to locate or
  operate on a source-bound object.

An implementation MAY perform more than one role. A conformance claim MUST name
the specification version, role, supported optional capabilities, and concrete
serialization or API binding used.

## 3. Terminology

- **Mesh:** a logical set of nodes and relationships with a stable identity.
- **Node:** the source-independent identity of one logical object known to the
  mesh. A node is not automatically a copy of the object's content.
- **Source:** an independently administered system or storage boundary from
  which objects can be identified, such as a repository, vault, drive,
  database, or knowledge application.
- **Source Binding:** the association between a node and one source-controlled
  object, using an identity meaningful within that source.
- **External ID:** the stable identity of an object within a source's identity
  domain. It is not an Engram Mesh node ID.
- **Resolver Hint:** non-secret portable information that can help an
  implementation select a resolver or locate an object. A hint does not grant
  access and need not be directly dereferenceable.
- **Connection State:** implementation-local configuration, credentials,
  tokens, sessions, mounts, endpoints, or account mappings used to access a
  source.
- **Relationship:** a typed, directed connection between two mesh nodes.
- **Hierarchy:** logical organization expressed by the distinguished `parent`
  relationship. It need not mirror physical source hierarchy.
- **Mesh Slice:** a bounded selection of nodes, relationships, source
  descriptors, and bindings. A slice can support sharing, context assembly,
  authorization decisions, traversal, or export. The name replaces the
  provisional term *Engram Fragment*.
- **Lens:** a reusable query, filter, or view definition over a mesh. A lens is
  neither a source nor a namespace and does not itself own the selected data.
- **Materialization:** a representation of source-controlled knowledge created
  for transport or local use. Materialization does not transfer authority over
  the source object.

## 4. Separation of concerns

The following properties are independent:

```text
storage ownership
        !=
mesh membership
        !=
index scope
        !=
search representation
        !=
modification authority
        !=
export inclusion
```

<a id="req-separation"></a> **REQ-SEP-001:** An implementation MUST NOT infer
one of these properties solely from another.

<a id="req-membership-content"></a> **REQ-SEP-002:** A node's membership in a
mesh MUST NOT be interpreted as evidence that Engram Mesh stores, owns, can
read, or can modify the node's source content.

<a id="req-derived-state"></a> **REQ-SEP-003:** Search indexes, embeddings,
chunks, rankings, caches, and query results MUST be treated as operational,
rebuildable state unless an application deliberately creates a distinct
durable node for an adopted artifact.

## 5. Abstract information model

A portable Engram Mesh representation is one UTF-8 JSON object named
`engram-mesh.json`. It contains one mesh identity and zero or more sources,
nodes, bindings, relationships, mesh slices, and lenses. JSON object keys MUST
be unique. Implementations MAY provide other bindings, but MUST NOT claim this
canonical-document conformance unless they produce and consume this document.

<a id="req-serialization"></a> **REQ-SER-001:** The document MUST be UTF-8 JSON,
MUST NOT contain duplicate object keys, MUST use `format: "engram-mesh"` and
`version: "0.3"`, and MUST conform to the 0.3 schema before semantic checks.

All entity IDs use a visible kind prefix and canonical uppercase ULID suffix:

```regex
^[a-z][a-z0-9-]{1,31}_[0-9A-HJKMNP-TV-Z]{26}$
```

Producers SHOULD use `mesh_`, `source_`, `node_`, `binding_`, `relationship_`,
`slice_`, and `lens_` prefixes for the corresponding entity kinds.

### 5.1 Mesh identity

<a id="req-mesh-id"></a> **REQ-MESH-001:** A mesh MUST have a stable `mesh_id`
that does not depend on a serialization instance, filesystem location, service
endpoint, or storage implementation.

<a id="req-version"></a> **REQ-MESH-002:** A portable representation MUST
identify the Engram Mesh specification version it targets.

<a id="req-global-id"></a> **REQ-MESH-003:** Every ID MUST match the core ID
syntax and MUST be globally unique within one `engram-mesh.json` document.

### 5.2 Node

A node has a stable `id`. It MAY have presentation metadata and MAY have
zero or more source bindings. Presentation metadata is a mesh description, not
the authoritative source content unless authority is declared explicitly.

<a id="req-node-id"></a> **REQ-NODE-001:** A node ID MUST be unique within its
mesh and MUST NOT be reassigned to a different logical object.

<a id="req-node-independent"></a> **REQ-NODE-002:** Node identity MUST NOT
depend solely on a filename, path, database primary key, provider URL, source,
or current storage system.

<a id="req-node-move"></a> **REQ-NODE-003:** Moving a source object or changing
its resolver information MUST NOT create a new node when the implementation
knows the logical object is continuous.

<a id="req-node-merge"></a> **REQ-NODE-004:** An implementation that merges,
splits, or deduplicates logical objects MUST make the resulting node-identity
decision explicit and MUST NOT silently assign one node ID to multiple logical
objects.

### 5.3 Source

A source descriptor identifies a storage or administrative boundary. It has a
stable `id`, a `kind`, an `identity_domain`, a capability list, and optional
human-readable and resolver metadata. The optional `resolver` has a mechanism
name and a non-secret locator. A source descriptor does not contain source
credentials.

<a id="req-source-id"></a> **REQ-SOURCE-001:** A source ID MUST be unique within
its mesh and MUST remain stable while the same administrative identity domain
is represented.

<a id="req-source-boundary"></a> **REQ-SOURCE-002:** A producer MUST document
the identity domain covered by each source narrowly enough that an external ID
is unambiguous within it. One document MUST NOT declare the same identity domain
under multiple Source IDs.

<a id="req-source-secrets"></a> **REQ-SOURCE-003:** A portable source descriptor
MUST NOT contain passwords, access tokens, private keys, session identifiers,
or other authentication secrets.

<a id="req-source-connection"></a> **REQ-SOURCE-004:** Connection state MUST
remain implementation-local. A resolver hint MAY be portable only when its
disclosure is safe for the intended recipients.

### 5.4 Source binding

A source binding contains a stable `id`, `node`, `source`, `external_id`,
`object_generation`, `state`, and `authority`, plus optional capability and
freshness metadata. Multiple bindings MAY connect one logical node to source
objects in different systems. `object_generation` distinguishes reuse of the
same external ID for a later, logically different source object.

Binding `state` has these core values:

- `active`: the binding currently identifies the node's source object;
- `superseded`: a later binding continues the same logical node;
- `deleted`: the identified source generation is known to be deleted; and
- `unresolved`: the producer cannot currently establish resolution.

Authority classification has these core values:

- `authoritative`: this is the binding whose source controls current content;
- `replica`: the bound object copies content controlled elsewhere; and
- `reference`: the binding identifies historical or associated source state but
  is not a current content authority.

<a id="req-binding-resolution"></a> **REQ-BIND-001:** Every binding MUST
reference an existing node and source in the same mesh representation.

<a id="req-binding-identity"></a> **REQ-BIND-002:** The tuple of source,
external ID, and object generation MUST identify at most one logical object. A
new logical object that reuses an external ID MUST use a new object generation
and a new node ID.

<a id="req-binding-authority"></a> **REQ-BIND-003:** Every binding MUST declare
its authority classification. Consumers MUST NOT treat a materialization or
replica as authoritative merely because its content is locally available.

<a id="req-binding-resolution-failure"></a> **REQ-BIND-004:** Failure to
resolve a binding MUST NOT invalidate the node or its mesh relationships. A
consumer MUST distinguish unresolved, unavailable, not found, and not
authorized when its runtime can safely do so.

<a id="req-binding-freshness"></a> **REQ-BIND-005:** When `freshness` is
present, it MUST include `observed_at` and at least one source revision, digest,
or opaque token. Absence of `freshness` means freshness is unknown; a consumer
MUST NOT infer currency from an active binding alone.

<a id="req-binding-authority-unique"></a> **REQ-BIND-006:** A node MUST NOT
have more than one active `authoritative` binding. Changing authority requires
an explicit state or authority transition; a consumer MUST NOT choose between
conflicting authorities by array order.

<a id="req-binding-successor"></a> **REQ-BIND-007:** A `superseded` binding
MUST identify an existing successor binding for the same node. `deleted` and
`unresolved` bindings MUST NOT advertise executable capabilities.

### 5.5 Capabilities and modification boundaries

A source MUST advertise the capability names it supports and a binding MAY
advertise a restricted subset. Core names are `discover`, `read`,
`create`, `modify`, `move`, and `delete`. Additional names MUST be namespaced.

<a id="req-capability-support"></a> **REQ-CAP-001:** A capability declaration
describes operations the source adapter may support; it MUST NOT be interpreted
as authorization for a caller or as evidence that an operation will succeed.

<a id="req-capability-authorize"></a> **REQ-CAP-002:** A runtime MUST perform
the source's required authentication, authorization, validation, and
conflict/freshness checks when an operation is requested.

<a id="req-capability-elevation"></a> **REQ-CAP-003:** An implementation that
distinguishes ordinary and elevated operations MUST preserve that distinction
and MUST NOT silently elevate a request.

<a id="req-capability-subset"></a> **REQ-CAP-004:** Binding capabilities MUST
be a subset of their Source capabilities. A missing binding capability list
inherits Source support but still conveys no caller authorization.

### 5.6 Relationships and hierarchy

A relationship has a stable `relationship_id`, a `from` node, a `to` node, and
a non-empty `type`. Relationship types are open vocabulary values; producers
SHOULD use namespaced values when their semantics are not defined by this
specification.

<a id="req-rel-resolution"></a> **REQ-REL-001:** Both endpoints of a
relationship MUST resolve to nodes in the represented mesh or MUST be marked as
omitted by a bounded Mesh Slice.

<a id="req-rel-direction"></a> **REQ-REL-002:** A consumer MUST preserve edge
direction and type and MUST NOT infer that a relationship is symmetric.

<a id="req-hierarchy-logical"></a> **REQ-HIER-001:** A `parent` relationship
expresses logical organization only. A consumer MUST NOT infer a source folder,
permission boundary, ownership boundary, or storage containment from it.

<a id="req-hierarchy-cycle"></a> **REQ-HIER-002:** The `parent` relation MUST be
acyclic among nodes included in one mesh representation.

<a id="req-hierarchy-single"></a> **REQ-HIER-003:** A node MUST NOT have more
than one outgoing `parent` relationship in the core hierarchy.

### 5.7 Mesh Slice

A Mesh Slice identifies a bounded subset of the enclosing mesh. It records an
`id`, `scope`, structured `selection`, included Source, Node, Binding, and
Relationship IDs, and `boundary` entries. A boundary disposition is `omitted`,
`unresolved`, or `undisclosed`. `undisclosed` entries carry no entity ID so the
slice does not reveal an unauthorized object's identity. A slice MAY be used to
drive materialization using an external format such as OKF.

<a id="req-slice-no-completeness"></a> **REQ-SLICE-001:** A Mesh Slice MUST NOT
claim to represent the complete mesh unless its producer evaluated that claim
against an identified source snapshot or equivalent bounded state.

<a id="req-slice-boundary"></a> **REQ-SLICE-002:** A slice MUST distinguish a
node or relationship omitted by selection from one absent from the mesh and
from one the producer was not authorized to disclose.

<a id="req-slice-authority"></a> **REQ-SLICE-003:** Export or materialization in
a slice MUST preserve source authority classifications and MUST NOT imply a
transfer of ownership or modification authority.

<a id="req-slice-closure"></a> **REQ-SLICE-004:** Every included binding MUST
include its Node and Source, and every included relationship MUST include both
endpoint Nodes. A `complete` slice MUST provide an opaque snapshot identifier;
it MUST include every entity in the represented mesh and have an empty boundary.
A `partial` slice MUST NOT be promoted to complete by a consumer.

### 5.8 Lens

A lens is a query, filter, or view definition that MAY produce a Mesh Slice.
Its expression language is implementation-specific in 0.3 unless identified by
a namespaced mechanism.

<a id="req-lens-no-membership"></a> **REQ-LENS-001:** Matching a lens MUST NOT
by itself add a node to the mesh, change its authority, authorize access, or
require it to be exported.

<a id="req-lens-mechanism"></a> **REQ-LENS-002:** A portable lens MUST identify
its expression mechanism and version. A consumer that does not support that
mechanism MUST report it as unsupported rather than silently reinterpret it.

## 6. Portable and implementation-local information

The portable model includes stable mesh, node, source, binding, relationship,
slice, and lens identities; external IDs; authority classifications; safe
resolver hints; capability names; and explicit freshness evidence.

The following remain implementation-local unless a separate binding defines a
safe portable representation:

- credentials and authentication sessions;
- account-to-user mappings and authorization policy;
- network routing, mounts, database handles, and connection pools;
- search documents, chunks, embeddings, scores, and indexes;
- caches, retry state, locks, and telemetry; and
- source-specific mutation transactions and conflict-resolution state.

<a id="req-portable-disclosure"></a> **REQ-PORT-001:** A producer MUST apply
the intended disclosure policy before emitting portable source descriptors,
resolver hints, relationships, or materialized content.

<a id="req-portable-unknown"></a> **REQ-PORT-002:** A consumer claiming
round-trip preservation SHOULD retain unknown namespaced fields without
changing their meaning.

## 7. Relationship to other standards

### 7.1 Open Knowledge Format

OKF is the preferred existing portable representation when its concept and
bundle model is suitable. Engram Mesh does not define a competing Markdown and
YAML knowledge-document envelope. an Engram Mesh node may bind to an OKF concept,
and a Mesh Slice may materialize selected knowledge as an OKF bundle.

The normative Engram Mesh identity, cross-source binding, typed relationship,
authority, and capability semantics are not inferred from ordinary OKF fields.
The version-specific mapping and its known losses are documented in
[the OKF interoperability guide](docs/okf-interoperability.md).

<a id="req-okf-claim"></a> **REQ-OKF-001:** An implementation MUST NOT claim
that an Engram Mesh representation is OKF-conformant unless the generated bundle
independently satisfies the targeted OKF version.

<a id="req-okf-identity"></a> **REQ-OKF-002:** Importing, exporting, or moving
an OKF concept MUST NOT silently replace a stable Engram Mesh node ID with the
OKF path-derived Concept ID.

### 7.2 Model Context Protocol

MCP is one possible runtime access mechanism for an Engram Mesh implementation.
MCP resources or tools may expose discovery, traversal, resolution, or mutation
operations. Engram Mesh does not redefine MCP messages, lifecycle, capability
negotiation, transport, or authorization behavior.

<a id="req-mcp-independence"></a> **REQ-MCP-001:** Engram Mesh conformance MUST
NOT require MCP, and MCP compatibility MUST NOT imply Engram Mesh conformance.

## 8. Security and privacy

All source metadata, source content, resolver output, relationships, and
materializations are untrusted input.

<a id="req-security-content"></a> **REQ-SEC-001:** An implementation MUST NOT
execute source content or treat it as privileged instructions merely because it
is reachable through the mesh.

<a id="req-security-resolution"></a> **REQ-SEC-002:** A resolver MUST constrain
network, filesystem, and provider access to the configured source boundary and
MUST enforce resource limits.

<a id="req-security-disclosure"></a> **REQ-SEC-003:** An implementation MUST
authorize disclosure of each returned node, relationship, binding, resolver
hint, and materialized object. It SHOULD avoid revealing whether an
unauthorized external object exists.

<a id="req-security-mutation"></a> **REQ-SEC-004:** A mutation request MUST be
authorized at execution time against the authoritative source. Mesh membership,
a capability declaration, possession of a slice, or prior read access is not
authorization.

## 9. Version and migration status

Engram Mesh 0.3 is a new, incompatible pilot line. Synthetic Engram 0.2 remains
defined by `docs/legacy/synthetic-engram-0.2/SPEC.md`, `schemas/v0.2`, `examples/v0.2`, and
`tests/v0.2`. No implicit conversion or conformance equivalence exists between
the two lines.

The 0.3 canonical representation is `engram-mesh.json` under
`schemas/v0.3/`. The repository validator and fixtures exercise this pilot
binding. Published or tagged 0.2 artefacts MUST NOT be rewritten to use
Engram Mesh names or semantics.

## 10. Deferred work

The following require implementation evidence before standardization:

- source-type registries or standard resolver-hint fields;
- a formal Engram Mesh extension or profile for OKF;
- a portable lens expression language;
- source synchronization, conflict resolution, and revision history;
- runtime protocol bindings, including MCP and HTTP profiles; and
- authentication, authorization, consent, signing, and encryption bindings.
