# Engram Mesh design rationale

> This document is non-normative. The current normative draft is
> [`SPEC.md`](../SPEC.md).

## Why this exists

Useful knowledge is commonly split across repositories, document stores,
drives, databases, local vaults, and specialized memory systems. Moving all of
it into one new format or database changes ownership, creates synchronization
problems, and duplicates work already handled by portable formats and source
applications.

Engram Mesh instead standardizes the connective layer: one stable logical node
can remain associated with an object controlled by an independent source, and
relationships can cross source boundaries.

## Main design choices

- Node identity is independent of source identity so an object can move without
  changing its logical place in the mesh.
- Source Binding is distinct from provenance. A binding says what source object
  a node represents; provenance says what material content was derived from.
- Authority is explicit because locally materialized content is not necessarily
  the version that may be changed.
- Capabilities describe adapter support, not caller authorization.
- Logical hierarchy does not imply folders, permissions, ownership, or export
  scope.
- Mesh Slices describe bounded selections without pretending that every
  selection is a complete copy of the mesh.
- Search state stays derived and rebuildable. A search chunk becomes durable
  only when deliberately adopted as its own logical object.

## Why not define another Markdown knowledge format?

Open Knowledge Format already defines a minimal Markdown and YAML bundle for
portable, human- and agent-readable knowledge. Engram Mesh should reuse OKF
where that representation fits and should focus its own requirements on stable
cross-source identity, bindings, typed edges, ownership, and boundaries that
OKF does not represent directly.

This is deliberately a mapping relationship rather than a formal OKF extension
while both specifications are evolving. See the
[OKF interoperability document](okf-interoperability.md).

## Why MCP is separate

MCP provides a runtime protocol through which an implementation can expose
resources and tools. It does not need to become the Engram Mesh data model.
The same logical mesh can be exposed through MCP, HTTP, GraphQL, a local library,
a CLI, or an application plugin.

## Pilot posture

The 0.3 pilot defines an abstract model and one canonical JSON serialization.
The schema and fixtures make the contract implementable, while live-source
adapters remain the evidence gate for stability. This prevents convenient
details of one database or service from becoming accidental portable
requirements.
