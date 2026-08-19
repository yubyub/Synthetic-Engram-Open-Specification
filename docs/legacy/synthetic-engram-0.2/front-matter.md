# Engram Front Matter grammar and parser test contract

This document extracts Core 0.2 record-envelope behavior into a standalone,
non-normative implementation guide. [`SPEC.md`](SPEC.md) remains authoritative.

## Restricted grammar

An Engram record is UTF-8 without a byte-order mark or bare carriage returns.
The first line is exactly `---`; the first later line containing exactly `---`
closes the front matter. The remaining bytes are Markdown and are not parsed by
the front-matter parser.

The enclosed YAML 1.2 value is exactly one block mapping:

```text
document       = opening-line mapping closing-line markdown
opening-line   = "---" newline
closing-line   = "---" (newline / end-of-file)
mapping        = *(mapping-entry / blank-line / comment-line)
mapping-entry  = indentation string-key ":" [scalar / nested-block] newline
nested-block   = mapping / sequence
sequence       = 1*(indentation "-" [scalar / nested-block] newline)
scalar         = null / boolean / json-number / string
```

Indentation uses spaces. Mapping keys are unique strings at every depth. Plain
`null`, `true`, and `false` receive those JSON types. A plain scalar matching the
JSON-number grammar becomes a finite number; every other plain scalar is a
string. Quoted scalars are strings. Result values must be JSON-compatible.

Directives, explicit tags, anchors, aliases, merge keys, explicit document
markers, and flow mappings or sequences are forbidden. Implementations must also
reject malformed YAML and a top-level sequence or scalar.

## Language-neutral parser test contract

The development corpus invokes a parser as:

```text
PARSER parse REQUEST.json
```

The request contains:

```json
{
  "protocol_version": "1.0",
  "case_id": "FM-VALID-001",
  "record": "/absolute/read-only/record.md",
  "max_record_bytes": 1048576
}
```

The parser writes one JSON object to standard output. Acceptance is:

```json
{
  "protocol_version": "1.0",
  "case_id": "FM-VALID-001",
  "outcome": "accepted",
  "front_matter": {}
}
```

Rejection uses `outcome: "rejected"` and one diagnostic with a stable `code`
and human-readable `message`. Corpus codes are:

- `encoding-invalid`
- `bom-not-allowed`
- `line-ending-invalid`
- `delimiter-invalid`
- `resource-limit`
- `yaml-forbidden-feature`
- `yaml-duplicate-key`
- `yaml-non-string-key`
- `yaml-invalid`
- `front-matter-not-mapping`

Accepted and rejected inputs both exit zero; malformed requests or operational
failures exit nonzero. The contract is for differential testing and does not
commit a future SDK API.

## Corpus and limits

[`tests/front-matter/cases.json`](../../../tests/front-matter/cases.json) is the shared
corpus. The runner materializes exact record bytes, invokes the Python and Node
parsers, compares their result to the expected JSON value or diagnostic code,
and runs deterministic generated scalar and resource-limit properties.

`max_record_bytes` is a caller-selected safety control of this test contract,
not a Core 0.2 package limit. Production software must expose limits appropriate
to its deployment.
