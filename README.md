# Synthetic Engram Open Standard

A human-owned, portable format for persistent knowledge that can be used by
people, AI systems, and non-AI applications without tying that knowledge to one
vendor, database, or service.

> [!IMPORTANT]
> **Status: experimental v0.1 draft.** The format is implementable so that its
> assumptions can be tested, but it is not yet a stable 1.0 standard.

## Start here

- [Normative specification](SPEC.md)
- [Complete example package](examples/basic-engram/README.md)
- [JSON Schemas](schemas/README.md)
- [Conformance and validation](docs/conformance.md)
- [Original concept and design rationale](docs/concept-draft.md)
- [Open design questions](docs/open-questions.md)

## Design principles

- **User authority:** knowledge remains under the defined owner's control.
- **Portability:** an export remains useful after its creating application is gone.
- **Partial consumption:** an implementation may support only declared profiles.
- **Stable identity:** links use durable IDs, not filenames or database keys.
- **Human inspection:** textual records use UTF-8 Markdown with YAML front matter.
- **Extensibility:** namespaced additions survive round trips without redefining core fields.
- **Storage independence:** live storage does not need to resemble an exported package.

## Package at a glance

```text
my-engram/
├── engram.json
├── records/
│   ├── notes/
│   ├── projects/
│   └── actions/
├── graphs/
└── attachments/
```

Every package has a JSON manifest. Records are Markdown files with a normative
YAML front matter envelope; graphs and attachment metadata are JSON. See
[`examples/basic-engram`](examples/basic-engram) for a small valid package.

## Validate the repository

Requires Python 3.11+ and the dependencies in `requirements-dev.txt`.

```sh
python -m pip install -r requirements-dev.txt
python scripts/validate.py
```

The validator checks schemas, identifiers, references, attachment hashes, and
the repository's valid and invalid conformance fixtures.

## Contributing and licensing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [GOVERNANCE.md](GOVERNANCE.md).
Specification prose is licensed under
[CC BY-SA 4.0](LICENSE); schemas, examples, and validation software are licensed
under [MPL 2.0](LICENSE-CODE).
