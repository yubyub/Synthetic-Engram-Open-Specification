# Engram Mesh project and component status

| Component | Status | Meaning |
| --- | --- | --- |
| Engram Mesh 0.3 model and JSON binding | Pilot specification | `engram-mesh.json` is the canonical 0.3 document. |
| Engram Mesh schemas and fixtures | Pilot conformance set | JSON Schemas plus positive and negative structural fixtures are repository-maintained. |
| Engram Mesh document adapters | Prototype adapters | Python and Node exercises validate and round-trip the document boundary; they do not connect to live Sources. |
| Source adapter contract | Pilot guidance | Discovery, identity reuse, moves, deletion evidence, authority transitions, freshness, and authorization behavior are specified for implementers. |
| OKF 0.2 mapping | Non-normative draft | Direct reuse and known losses are documented; no formal OKF extension is defined. |
| MCP/HTTP bindings | Not standardized | Runtime protocols remain implementation choices. |
| Synthetic Engram 0.2 | Preserved legacy pilot | Root `SPEC.md`, `schemas/v0.2`, `examples/v0.2`, and `tests/v0.2` retain their existing meaning. |
| Existing validator and adapters | Legacy 0.2 tools | They validate Synthetic Engram packages, not Engram Mesh 0.3. |

Engram Mesh 0.3 is usable for controlled pilots that exchange cross-source
identity, bindings, topology, and bounded slices. It is not a live connector,
content format, synchronization engine, or stable compatibility commitment. A
stable release additionally requires independent live-source adapter evidence
and a reviewed compatibility story for OKF and legacy Synthetic Engram data.
