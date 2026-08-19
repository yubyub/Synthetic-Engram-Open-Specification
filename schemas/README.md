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
