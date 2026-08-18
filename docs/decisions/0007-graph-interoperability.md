# Decision 7: Graph interoperability

- **Status:** accepted
- **Outcome:** Include directed, labeled topology in the optional core 1.0 `graph` profile. Defer layout, styling, and graph-DSL extraction to the **Graph Languages and Derivation Specification**; reject portable meaning for ordering, hyperedges, ports, groups, and subgraphs in core 1.0.

## Rationale and compatibility

Nodes and directed edges have deterministic validation and useful interchange value. Presentation and extraction require independent grammars and provenance. Namespaced extensions preserve application data but cannot alter core topology.

## Affected requirements and schemas

`REQ-GRAPH-001` through `REQ-GRAPH-003`, `REQ-PROF-002`, and `REQ-EXT-002`; [SPEC §§8, 10, and 11](../../SPEC.md#8-graphs) and [graph schema](../../schemas/v0.1/graph.schema.json).

## Acceptance criteria and evidence

- **Satisfied:** [`basic-engram`](../../tests/valid/basic-engram), [`partial-external`](../../tests/valid/partial-external), [`duplicate-graph-ids`](../../tests/invalid/duplicate-graph-ids), [`duplicate-graph-edge-ids`](../../tests/invalid/duplicate-graph-edge-ids), and [`unresolved-edge-endpoint`](../../tests/invalid/unresolved-edge-endpoint) cover local IDs, Engram/external references, directed edges, duplicates, and broken endpoints.
- **Satisfied:** [SPEC §8](../../SPEC.md#8-graphs) limits portable meaning to topology and labels and explicitly excludes ordering, layout, styling, hyperedges, ports, groups, and subgraphs.
- **Inapplicable by scope:** no DSL mapping is included; grammar, extraction provenance, error handling, and loss reporting belong to the named future specification.
- **Satisfied:** `REQ-EXT-002` and [`extension-preservation`](../../tests/valid/extension-preservation) preserve application data without redefining topology.

## Linked changes

Normative behavior and evidence are in [SPEC](../../SPEC.md), [graph schema](../../schemas/v0.1/graph.schema.json), [graph fixtures](../../tests), and [traceability](../traceability.md).
