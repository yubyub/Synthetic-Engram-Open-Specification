# Engram Mesh Open Specification

**Connect knowledge across sources without taking ownership of it.**

Engram Mesh is a draft open specification for a source-independent logical mesh.
It gives knowledge stable logical identity and relationships across repositories,
document stores, local vaults, databases, and knowledge applications while the
underlying content remains in its authoritative source.

> [!IMPORTANT]
> **Status: 0.3 pilot specification.** The canonical `engram-mesh.json`
> representation, schemas, fixtures, and prototype adapters are available for
> evaluation. Breaking changes remain possible before 1.0.

## What it standardizes

Engram Mesh focuses on:

- stable node identity independent of filenames, paths, provider IDs, and
  current storage systems;
- Sources and Source Bindings that connect nodes to externally controlled
  objects;
- typed relationships and logical hierarchy across source boundaries;
- explicit source ownership and authority classification;
- portable capability names without treating them as authorization;
- bounded Mesh Slices for sharing, context, export, and traversal; and
- Lenses as query or view definitions distinct from sources and namespaces.

```text
 Obsidian ───────────┐
 GitHub ─────────────┤
 Google Drive ───────┼──► Engram Mesh logical graph
 OKF bundles ────────┤
 Native stores ──────┘
```

The content does not have to move. Mesh membership does not imply storage,
ownership, index inclusion, search representation, modification authority, or
export inclusion.

## Relationship to existing standards

[Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
is the preferred portable knowledge representation where its Markdown/YAML
concept and bundle model fits. Engram Mesh does not define a competing document
format. It adds the cross-source identity, binding, typed relationship,
authority, and capability layer. See the
[OKF interoperability mapping](docs/okf-interoperability.md).

[Model Context Protocol](https://modelcontextprotocol.io/) is one useful way for
agents and applications to access an Engram Mesh implementation. It remains a
runtime protocol, not part of the Engram Mesh data model; HTTP, GraphQL, library
APIs, CLIs, and application plugins are equally possible.

[Basic Memory](https://docs.basicmemory.com/) and projects using the ambiguous
name “OpenMemory” solve adjacent knowledge-base or AI-memory problems. They may
participate as Sources or implement adapters; the Engram Mesh specification
does not reproduce their storage, retrieval, or memory behavior. See the
[adjacent-systems boundary](docs/engram-mesh-related-standards.md).

## Deliberate non-goals

Engram Mesh does not standardize:

- Markdown knowledge documents already covered by OKF;
- search, embeddings, chunks, ranking, or vector databases;
- SQLite, PostgreSQL, graph databases, or filesystem layouts;
- web servers, containers, frontends, or MCP server implementations;
- authentication mechanisms, credentials, or application authorization policy;
  or
- synchronization and conflict-resolution algorithms.

## Current documents

- First use: [Getting started](docs/getting-started.md)
- Normative pilot specification: [Engram Mesh Open Specification 0.3](SPEC.md)
- Architecture: [Engram Mesh architecture](docs/engram-mesh-architecture.md)
- Rationale: [Engram Mesh design rationale](docs/engram-mesh-rationale.md)
- Version policy: [Engram Mesh versioning](docs/engram-mesh-versioning.md)
- Conformance: [Engram Mesh 0.3 conformance](docs/engram-mesh-conformance.md)
- Requirement coverage: [Engram Mesh traceability](docs/engram-mesh-traceability.md)
- Adapter behavior: [Source adapter contract](docs/source-adapter-contract.md)
- OKF mapping: [Engram Mesh and OKF interoperability](docs/okf-interoperability.md)
- Adjacent systems: [Engram Mesh and related standards](docs/engram-mesh-related-standards.md)
- Maturity: [Engram Mesh component status](docs/engram-mesh-status.md)
- Refocus decision: [Engram Mesh refocus and OKF alignment](docs/decisions/refocus.md)

## Contributing

The immediate need is implementation evidence for the 0.3 model: adapters for
independently controlled sources, stable identity across source moves,
cross-source relationship round trips, authority handling, and OKF
materialization with explicit loss reporting. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

The specification, documentation, schemas, examples, fixtures, workflows, and
software are available under the permissive [MIT License](LICENSE). See the
[plain-language licensing guide](docs/licensing.md).
