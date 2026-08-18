# JSON Schemas

The `v0.1` and `v1.0` schemas use JSON Schema Draft 2020-12. `manifest.schema.json`,
`record.schema.json`, `graph.schema.json`, and `attachment.schema.json` are
entry points in each version; `definitions.schema.json` contains shared definitions.

Record schemas validate parsed YAML front matter, not the Markdown body. Schema
validation alone is insufficient: use `python scripts/validate.py` for package
inventory, reference, cycle, and checksum checks.

`v1.0/graph.schema.json` adds kind-neutral durable-object references, structured external references, qualified relation vocabularies, and extension points at every graph level.
scope, complete-export closure, inventory, reference, cycle, and checksum checks. These experimental schemas will move to the `v1.0` schema path when the standard reaches 1.0; their current location implies no 1.0 stability.
