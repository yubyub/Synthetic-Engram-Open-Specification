# JSON Schemas

## Engram Mesh 0.3

The Engram Mesh pilot schema set lives under `v0.3`. Its entry point is
`mesh.schema.json`; `definitions.schema.json` contains shared identifiers and
extension definitions. The canonical document is UTF-8 JSON named
`engram-mesh.json`. Run `python3 scripts/validate_engram_mesh.py` as well as a
JSON Schema validator because source/binding resolution, capability names,
relationship endpoints, slices, and hierarchy cycles are cross-field rules.

The `v0.3` pilot schemas deliberately omit `$id` until a public, tag-addressed
Engram Mesh release is available. Local tools should resolve sibling references
from the schema directory.

## Synthetic Engram 0.2 legacy schemas

The 0.2 pilot schemas use JSON Schema Draft 2020-12 and live under `v0.2`.
`manifest.schema.json`, `record.schema.json`, `graph.schema.json`, and
`attachment.schema.json` are entry points; `definitions.schema.json` contains
shared definitions.

The schema identifiers use tag-addressed URLs beneath
`https://raw.githubusercontent.com/yubyub/Synthetic-Engram-Open-Standard/v0.2.0/schemas/v0.2/`.
They resolve after this repository is public and the `v0.2.0` tag is published.
Implementations should still bundle the schemas and resolve references locally
when offline. The tag must point to the same bytes as the distributed release.

The manifest requires the package, Engram, and export identities plus an explicit
`completeness` value. Schema validation alone is insufficient: run
`python3 scripts/validate.py` for inventory, reference, profile, cycle, closure,
and attachment-integrity checks.

Because the specification is pre-1.0, later 0.x versions may introduce breaking
changes under a new versioned directory and schema URI.
