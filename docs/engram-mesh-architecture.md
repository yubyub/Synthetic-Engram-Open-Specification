# Engram Mesh architecture

> This document is non-normative. The current normative draft is
> [`SPEC.md`](../SPEC.md).

Engram Mesh sits between independently controlled sources and the applications
that need one logical view across them.

```text
                         Engram Mesh

 Obsidian source ───────┐
 GitHub source ─────────┤       stable nodes
 Google Drive source ───┼───── typed relationships
 OKF bundle source ─────┤       source bindings
 Native store ──────────┘       authority boundaries
                                │
                 ┌──────────────┼──────────────┐
                 │              │              │
              library API      HTTP           MCP
                 │              │              │
                 └──────── application / agent ┘
```

## Layers

| Layer | Portable Engram Mesh concern | Implementation concern |
| --- | --- | --- |
| Logical mesh | stable nodes, sources, bindings, typed relationships, hierarchy | indexes, graph database layout, caches |
| Source access | safe resolver hints and declared adapter capabilities | credentials, connections, retries, provider SDKs |
| Selection | Mesh Slice boundary and Lens mechanism identity | query planning, ranking, embeddings, context budgets |
| Materialization | preserved identity, authority, mappings, and declared loss | conversion pipeline and temporary files |
| Runtime access | no required protocol | MCP, HTTP, GraphQL, CLI, library, plugin |
| Authorization | portable distinctions must not imply permission | identity provider, policy engine, consent, audit |

## Resolution flow

```text
node ID
   │
   ▼
source binding ──► source ID + external ID + safe resolver hint
   │
   ▼
implementation-local resolver ──► credentials and connection state
   │
   ▼
authoritative source object
```

Resolution failure does not erase the node or its relationships. A source can
be offline, moved, unsupported, or inaccessible to the current caller while the
logical mesh remains useful.

## Materialization flow

```text
lens or explicit selection
          │
          ▼
authorized Mesh Slice
          │
          ├──► OKF bundle
          ├──► application-specific response
          └──► canonical engram-mesh.json
```

Materialization is a view or copy. Authority remains with the declared source
unless the application performs an explicit ownership transition outside this
draft.
