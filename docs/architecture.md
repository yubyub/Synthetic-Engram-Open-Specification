# Architecture and rationale

This document is non-normative. The standard separates a portable representation
from live storage. An application may use files, a relational database, a graph
database, or object storage internally, provided its declared import/export
behavior conforms to `SPEC.md`.

The v0.1 boundary deliberately favors a small lossless interchange core:

1. stable object identity;
2. human-readable records;
3. explicit relationships and inventory;
4. verifiable binary payloads; and
5. declared optional profiles.

Indexes, embeddings, caches, generated summaries, credentials, and runtime
policy are derivative or operational state and do not belong in the core
package. See the [original concept draft](concept-draft.md) for broader design
rationale and possible future capabilities.

## Graphs as views

Graph objects deliberately do not provide a second source of truth. Record
`parent` and `links` values define the package's durable record relationships;
graph edges are independent presentation topology. This permits a product to
export a task map, a hand-curated explanatory diagram, or a generated knowledge
view without manufacturing record links merely to support that visualization.
When an edge and a record field appear inconsistent, the record wins for record
relationship semantics and the graph remains valid as a diagram.

Graph coverage is similarly separate from package membership. The manifest
inventory is the only package-membership boundary, so a package may have no
graphs and a graph need not mention every artifact. The required `scope` value
makes the graph author's coverage claim explicit: `curated` is a selected view,
while `complete_records` promises a node reference for every inventoried record.
The latter is useful to consumers seeking a complete record index, but it does
not promise attachment coverage, edge completeness, or relationship authority.
