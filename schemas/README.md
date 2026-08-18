# JSON Schemas

The frozen 1.0 schemas use JSON Schema Draft 2020-12. Their permanent base URI
is `https://synthetic-engram.org/schema/v1.0/`. `manifest.schema.json`,
`record.schema.json`, `graph.schema.json`, and `attachment.schema.json` are
entry points; `definitions.schema.json` contains shared definitions. The
archived experimental schemas remain under [`v0.1`](v0.1/) and are not accepted
as 1.0 input.

Published schema URIs and their bytes are immutable. Errata never replace a
released schema in place; see the [normative version and support
policy](../docs/versioning.md) for publication and compatibility rules.
Repository validation checks the published
[v1.0 SHA-256 manifest](../docs/releases/v1.0-schema-sha256.txt). Independent
hosts should follow the [schema mirroring procedure](../docs/schema-mirroring.md)
and publish their own dated fixity and recovery reports.

Record schemas validate parsed YAML front matter, not the Markdown body. Schema
validation alone is insufficient: use `python scripts/validate.py` for package
scope, complete-export closure, inventory, reference, cycle, and checksum
checks.
