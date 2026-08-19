# Getting started with Engram Mesh 0.3

Engram Mesh is useful when one logical knowledge graph must refer to objects in
two or more independently controlled systems without copying their content into
one new store.

Use it for cases such as:

- relating an OKF concept to a GitHub repository, issue, or document;
- giving one logical identity to an object that may move between source paths;
- exporting an authorization-aware subset of cross-source topology; or
- allowing several applications to exchange source bindings and typed edges
  while each source remains authoritative for its own content.

Do not use Engram Mesh alone as a note format, backup, search engine,
synchronization protocol, permissions system, or MCP API. Use OKF or a native
source format for content, source-specific mechanisms for access control, and
an application or protocol binding for runtime operations.

## The smallest useful mesh

A canonical document is named `engram-mesh.json` and contains four essential
collections:

```text
Source ── Source Binding ── Node ── Relationship ── Node
```

- A Source defines one administrative identity domain.
- A Node gives one logical object a source-independent identity.
- A Source Binding maps that Node to one generation of one source object.
- A Relationship connects Nodes without depending on their physical location.

Start from [the cross-source example](../examples/v0.3/basic-mesh/engram-mesh.json).
Validate it with:

```sh
python3 scripts/validate_engram_mesh.py examples/v0.3/basic-mesh/engram-mesh.json
```

The validator has no third-party dependencies. It rejects duplicate JSON keys,
unknown core fields, unsafe-looking credential-bearing resolver locators,
identity collisions, invalid binding transitions, multiple active authorities,
capability escalation, broken relationships, hierarchy cycles, and invalid
slice closure.

## Add a Source

Choose an `identity_domain` narrow enough that an `external_id` is unambiguous.
For GitHub this might be one repository; for a filesystem it might be one
managed vault. Declare only operations the adapter actually implements.

```json
{
  "id": "source_01ARZ3NDEKTSV4RRFFQ69G5FAW",
  "kind": "github",
  "identity_domain": "github.com/example/service",
  "capabilities": ["discover", "read"]
}
```

Credentials, local mount paths, sessions, and authorization policy stay outside
the document. A portable `resolver` is optional and must be safe to disclose.

## Bind a Node

```json
{
  "id": "binding_01ARZ3NDEKTSV4RRFFQ69G5FB0",
  "node": "node_01ARZ3NDEKTSV4RRFFQ69G5FAY",
  "source": "source_01ARZ3NDEKTSV4RRFFQ69G5FAW",
  "external_id": "docs/runbook.md",
  "object_generation": "git-object-history-1",
  "state": "active",
  "authority": "authoritative"
}
```

`external_id` belongs to the Source. `object_generation` prevents a reused path
or provider ID from silently taking over the old logical Node. The binding is
not proof that the current caller can read or modify the object.

## Handle moves and replacement

When a provider-stable object ID survives a path move, keep the binding and Node
IDs and update non-identity resolver metadata. When the external ID itself
changes, retain the Node ID, mark the old binding `superseded`, and point it to a
new active binding. See the [source-move fixture](../tests/v0.3/valid/source-move/engram-mesh.json).

If the source reuses an external ID for a different logical object, create a new
`object_generation`, Node, and Binding. Never decide continuity from title or
content similarity alone.

## Create a safe Mesh Slice

A slice includes explicit Source, Node, Binding, and Relationship IDs. Included
bindings require their Source and Node; included relationships require both
endpoint Nodes.

Use boundary dispositions as follows:

- `omitted`: a known entity was excluded by selection;
- `unresolved`: a referenced entity could not be resolved; and
- `undisclosed`: authorization prevents disclosure—the entry carries no ID.

A `complete` slice requires snapshot evidence. Most application and agent
context exports should be `partial`.

## Implement an adapter

Follow the [source adapter contract](source-adapter-contract.md). An adapter
must keep durable identity mapping state, distinguish lookup failures, enforce
authorization at operation time, and never treat advertised capabilities as
permission.
