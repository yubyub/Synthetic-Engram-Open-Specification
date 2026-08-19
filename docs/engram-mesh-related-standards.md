# Engram Mesh and related standards

This non-normative document fixes the boundary between Engram Mesh and adjacent
formats, protocols, and applications. Similar concepts do not imply wire or
behavioral compatibility.

| Work | Primary layer | Engram Mesh relationship |
| --- | --- | --- |
| [Open Knowledge Format 0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) | Portable Markdown/YAML knowledge bundles | Preferred materialization and interchange format where its concept model fits |
| [Model Context Protocol](https://modelcontextprotocol.io/specification/latest) | Runtime tools, resources, and client/server interaction | Optional way to expose an Engram Mesh implementation |
| [Basic Memory](https://docs.basicmemory.com/) | File-first Markdown knowledge application with indexing and MCP access | Potential Source, adapter, or application; its runtime behavior is not part of Engram Mesh |
| OpenMemory projects | Various AI-memory engines and session-portability tools | Potential Sources or adapters only after a specific project and version are identified |

## Open Knowledge Format

OKF and Engram Mesh solve complementary problems. OKF provides the portable
content representation. Engram Mesh provides stable logical identity and typed
connections across independently administered Sources. Direct mappings and
losses are documented in [OKF interoperability](okf-interoperability.md).

Engram Mesh does not currently extend, fork, or modify OKF. An implementation
that emits both must evaluate each conformance claim independently.

## Model Context Protocol

MCP can expose source discovery, node lookup, relationship traversal,
materialization, and authorized mutation as resources or tools. Those operation
names and payloads are application-specific until a separate Engram Mesh MCP
binding is standardized.

Engram Mesh does not redefine MCP lifecycle, messages, transport, resource or
tool semantics, capability negotiation, or authorization guidance. A REST API,
GraphQL API, local library, CLI, or application plugin can expose the same
Engram Mesh model.

## Basic Memory

Basic Memory describes a file-first Markdown knowledge graph with a secondary
database index and MCP access. Engram Mesh should not reproduce its editor,
indexer, search behavior, file watching, cloud synchronization, or MCP server.

A Basic Memory project can instead be modeled as a Source. An adapter can bind
Engram Mesh nodes to its stable native objects, expose supported capabilities,
and retain Basic Memory as the content authority.

## The name “OpenMemory” is ambiguous

The decision record names OpenMemory without a repository or publisher. As of
this review, that name refers to multiple unrelated projects, including:

- [`CaviraOSS/OpenMemory`](https://github.com/CaviraOSS/OpenMemory), a
  self-hosted long-term memory engine;
- [`mem0ai/openmemory`](https://github.com/mem0ai/openmemory), a tool for
  porting coding-agent sessions; and
- other local memory engines using the same display name.

No one of these is a normative dependency or presumed target. A future adapter,
comparison, or compatibility statement must cite the exact repository, version,
and represented identity model. Until then, “OpenMemory” is only an example of
an adjacent product category.

## Design test

Before adding a proposed feature to Engram Mesh core, ask which layer owns it:

- portable authored knowledge generally belongs in OKF or another established
  content format;
- runtime tool/resource access belongs in MCP or another API binding;
- memory extraction, decay, ranking, search, and storage belong in the source
  application; and
- stable cross-source identity, binding, typed logical relationships,
  authority distinctions, and bounded mesh selection are Engram Mesh concerns.
