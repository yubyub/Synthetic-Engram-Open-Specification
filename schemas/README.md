# JSON Schemas

The v0.1 schemas use JSON Schema Draft 2020-12. `manifest.schema.json`,
`record.schema.json`, `graph.schema.json`, `attachment.schema.json`, and
`capabilities.schema.json` are entry points; `definitions.schema.json` contains
shared definitions. The capabilities schema describes implementation claims;
it is not package content and is not referenced by `engram.json`.

Record schemas validate parsed YAML front matter, not the Markdown body. Schema
validation alone is insufficient: use `python scripts/validate.py` for package
inventory, reference, cycle, and checksum checks.
