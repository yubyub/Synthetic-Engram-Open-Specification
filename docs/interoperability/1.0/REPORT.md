# Synthetic Engram 1.0 interoperability report

- **Report version:** 1.0
- **Executed:** 2026-08-18 (UTC)
- **Exchange fixture:** [`examples/basic-engram`](../../../examples/basic-engram)
- **Required profile set:** `core`, `graph`, `media`, and `action`
- **Overall result:** **PASS** — both independent implementations pass as producers,
  consumers, and round-trip processors for core and every optional profile retained
  for 1.0. No semantic or normative-content loss was detected in either direction.

## Implementations and declarations

| Implementation | Version | Runtime | Roles | Processing and preservation profiles |
|---|---:|---|---|---|
| [Python Engram Package Processor](../../../implementations/python-engram/README.md) | 1.0.0 | Python 3 standard library | producer, consumer, round-trip | core, graph, media, action |
| [Node Engram Package Processor](../../../implementations/node-engram/README.md) | 1.0.0 | Node built-ins | producer, consumer, round-trip | core, graph, media, action |

The implementations were built independently. They neither import
`scripts/validate.py` nor `scripts/reference_adapter.py`, and they do not import
one another. Python owns a two-space JSON serializer and its parser, inventory
walk, archive-path check, and Markdown-link recognition. Node independently owns
corresponding logic and deliberately emits four-space JSON. The repository
harness is only the language-neutral test driver.

## Reproduction commands

Run from the repository root:

```sh
python scripts/conformance_harness.py \
  --adapter implementations/python-engram/engram_adapter.py \
  --report docs/interoperability/1.0/artifacts/python/conformance.json
python scripts/conformance_harness.py \
  --adapter implementations/node-engram/engram-adapter.js \
  --report docs/interoperability/1.0/artifacts/node/conformance.json
python scripts/run_interoperability.py
python scripts/validate.py
```

The common suite contains one producer, ten consumer, and five round-trip cases.
Both implementations passed all **16/16** cases. `PRODUCER-001` imports and
exports `examples/basic-engram` with no logical edits; the exchange runner then
feeds each export to the other implementation's round-trip operation.

## Result artifacts

- [`artifacts/python/conformance.json`](artifacts/python/conformance.json): Python
  common-suite result.
- [`artifacts/node/conformance.json`](artifacts/node/conformance.json): Node
  common-suite result.
- [`artifacts/python/adapter-artifacts/package`](artifacts/python/adapter-artifacts/package):
  Python's direct basic-package export and its adapter request/result.
- [`artifacts/node/adapter-artifacts/package`](artifacts/node/adapter-artifacts/package):
  Node's direct basic-package export and its adapter request/result.
- [`artifacts/exchange/node-import-python`](artifacts/exchange/node-import-python):
  Node import/export of the Python-produced package.
- [`artifacts/exchange/python-import-node`](artifacts/exchange/python-import-node):
  Python import/export of the Node-produced package.
- [`artifacts/exchange/comparison.json`](artifacts/exchange/comparison.json):
  machine-readable bidirectional comparison and loss classification.

## Bidirectional comparison

Both directions retained:

- stable Engram ID, package ID, and every `(object ID, kind)` inventory entry,
  including the shared attachment/blob logical ID;
- exact Markdown UTF-8 bytes for all inventoried records;
- graph node-to-record bindings and every edge ID, endpoint, and relation;
- attachment descriptor values, payload bytes, size, and SHA-256 identity;
- JSON-compatible extension values (the fixture contains no extension value, so
  the empty extension collection is preserved);
- reference scopes (the fixture contains no scoped external reference, so the
  empty scope collection is preserved); and
- ordered profile declarations: `core`, `graph`, `media`, `action`.

### Serialization differences versus loss

The comparison records intentional byte differences in `engram.json`,
`graphs/architecture.json`, and `attachments/package-overview.json`. These are
only JSON whitespace changes: Python emits two-space indentation and Node emits
four-space indentation. Parsed JSON values remain deeply equal. Markdown and
blob payload bytes are unchanged.

The separate `semantic_or_normative_content_loss` list is empty for both
exchange directions. There were no failures, unsupported retained profiles,
omitted inventory objects, changed references, or content transformations.

## Profile-by-profile conclusion

| Profile | Python 1.0.0 | Node 1.0.0 | Exchange evidence | Conclusion |
|---|---|---|---|---|
| `core` | PASS | PASS | IDs, inventory, profile declarations, Markdown, extensions, and scope collection equal | **PASS** |
| `graph` | PASS | PASS | Node bindings and complete edge topology equal | **PASS** |
| `media` | PASS | PASS | Attachment descriptor and payload bytes/hash equal | **PASS** |
| `action` | PASS | PASS | Action record ID, kind, inventory membership, and Markdown bytes equal | **PASS** |

Accordingly, both implementations satisfy the required producer, consumer, and
round-trip roles for core and **every** optional 1.0 profile retained by this
repository. This report makes no claim for deferred profiles or for semantics
that are absent from the exchange fixture; absent extensions and reference
scopes were explicitly compared as empty rather than silently ignored.
