# Synthetic Engram Open Standard

**Keep knowledge useful when the application, AI provider, database, or hosting
model changes.** Synthetic Engram is an open interchange standard for a
human-owned knowledge base: typed Markdown records, explicit relationships,
portable graphs, and verifiable attachments with stable identities.

> [!IMPORTANT]
> **Status: experimental v0.1 draft.** The format is implementable so that its
> assumptions can be tested, but it is not yet a stable 1.0 standard.

## Why use it?

Most knowledge tools make their own storage model the boundary of what can be
kept, linked, or moved. A folder of Markdown is inspectable but does not by
itself define durable identity, typed records, graph semantics, package
completeness, or preservation rules. A database can provide those features but
usually binds them to one implementation.

Synthetic Engram defines the boundary between **portable knowledge** and the
software that stores or uses it. Choose it when you want to:

- move a knowledge base between local files, SQL, graph databases, object
  storage, or hosted services without changing its portable meaning;
- let note tools, project tools, graph viewers, AI assistants, and coding agents
  consume the same durable objects without making any one of them authoritative;
- preserve IDs and relationships across renames, exports, and migrations;
- exchange a complete archive or an explicitly partial package;
- validate what an export contains, including references and attachment hashes;
- allow partial implementations to declare exactly which profiles they support.

It is **not** a database, sync protocol, application framework, retrieval
algorithm, or AI-memory policy. Implementations keep their preferred live
architecture and import or export the standard package at the interoperability
boundary.

## Who is it for?

- **Knowledge-base owners** who need an inspectable exit path from a product.
- **Application authors** who want a documented import/export contract rather
  than another proprietary backup format.
- **Agent and AI developers** who need durable, bounded context that remains
  useful outside a model runtime.
- **Adapter authors and coding agents** who need schemas, normative rules,
  fixtures, and observable conformance behavior to make implementation choices.

## Evaluate the standard

1. Read the [architecture](docs/architecture.md) to understand what belongs in
   the portable layer and what remains implementation-specific.
2. Inspect the [complete example](examples/basic-engram/README.md), including a
   project, notes, an action, their graph, and an attachment.
3. Read the [normative specification](SPEC.md) and
   [conformance checklist](docs/conformance.md).
4. Run the validator, then compare the model with the
   [related-work analysis](docs/related-standards.md).

## Documentation map

- [Normative specification](SPEC.md)
- [Complete example package](examples/basic-engram/README.md)
- [JSON Schemas](schemas/README.md)
- [Conformance and validation](docs/conformance.md)
- [Language-neutral conformance harness protocol](docs/harness-protocol.md)
- [Design rationale](docs/rationale.md)
- [Architecture and implementation boundaries](docs/architecture.md)
- [Related standards and projects](docs/related-standards.md)
- [Non-normative design-decision matrix](docs/design-decisions.md)
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
