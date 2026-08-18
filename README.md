# Synthetic Engram Open Standard

**Keep knowledge useful when the application, AI provider, database, or hosting
model changes.** Synthetic Engram is a candidate open interchange standard for a
human-owned knowledge base: typed Markdown records, explicit relationships,
portable graphs, and verifiable attachments with stable identities.

> [!NOTE]
> **Status: Synthetic Engram Open Standard 1.0.0.** The normative schemas use
> permanent `v1.0` identifiers; published schema bytes are immutable.

## Purpose

Synthetic Engram is a **candidate open interchange standard and portable
knowledge structure** for durable, human-owned application knowledge. It gives
humans, conventional applications, and AI-enabled tools a shared definition of
typed records, stable identities, relationships, graphs, and attachments without
requiring them to use the same database, hosting provider, or AI runtime.

The standard is currently an emerging, maintainer-led specification with two
included cross-language implementations, not an established multi-vendor
industry standard. Adopt it first as an import/export boundary and evaluate it
with real round trips.

It standardizes the knowledge **at the interoperability boundary**. An
application may also use the model internally, but conformance does not require
its live database or filesystem to match an Engram Package. Human ownership here
means durable data remains portable and inspectable; it does **not** mean the
package grants or enforces authentication, authorization, encryption, consent,
or access privileges.

## Where it fits

```text
 human owner
     |
     | creates, reviews, controls, and moves durable knowledge
     v
 +---------------- application that implements Synthetic Engram ---------------+
 | notes / projects / knowledge service / personal data store / migration tool |
 |                                                                             |
 | proprietary or package-native live store                                    |
 |                 |                                                           |
 |          import / export adapter                                             |
 +-----------------|-----------------------------------------------------------+
                   v
       portable Synthetic Engram Package
       records + stable IDs + links + graphs + attachments
                   |
          +--------+---------+------------------+
          |                  |                  |
     another app       AI/retrieval tool    archive/validator
     imports it        selects context      preserves/checks it

 Outside core 1.0: live sync, retrieval/ranking, model memory policy,
 authentication, authorization, encryption, rendering, and database design.
```

Applications that commonly **implement** the standard are knowledge bases,
note/project/task tools, personal-data stores, migration and backup products,
and hosted services that promise a portable exit. Applications that may
**interface with an implementation** include AI assistants, coding agents,
search/indexing systems, graph viewers, archive validators, and other importers.
The latter do not need to use an Engram Package as their own live store.

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

It is most likely to provide a net benefit when users need a credible exit path,
IDs and links must survive renames or migrations, multiple independently evolving
tools need the same durable objects, or complete and deliberately partial exports
must be distinguishable. It is more likely to be a burden when only one program
will ever read the data, plain Markdown is sufficient, or the real requirement is
live synchronization, collaborative history, authorization, semantic-web
reasoning, or an AI retrieval engine.

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

Choose the shortest path for your role:

- **Deciding whether to adopt:** read the
  [adoption guide](docs/adoption-guide.md), inspect the
  [complete example](examples/v1.0/basic-engram/README.md), and compare
  [related standards](docs/related-standards.md).
- **Building an exporter or importer:** read the
  [architecture](docs/architecture.md), then the [normative specification](SPEC.md)
  and [conformance checklist](docs/conformance.md).
- **Building an AI or retrieval integration:** read the
  [AI integration guide](docs/ai-integration.md), then implement only the profiles
  needed by the integration.
- **Reviewing or evolving the standard:** use the
  [implementation-feedback register](docs/development/implementation-feedback.md)
  and the [decision records](docs/decisions/README.md).
- **Using an agent to implement support:** provide `SPEC.md`, the applicable JSON
  Schemas, `docs/conformance.md`, and the relevant fixtures as authoritative
  context; rationale and guides are non-normative.

## Documentation map

- [Normative specification](SPEC.md)
- [Complete 1.0 example package](examples/v1.0/basic-engram/README.md)
- [JSON Schemas](schemas/README.md)
- [Conformance and validation](docs/conformance.md)
- [Language-neutral conformance harness protocol](docs/harness-protocol.md)
- [Design rationale](docs/rationale.md)
- [Architecture and implementation boundaries](docs/architecture.md)
- [Related standards and projects](docs/related-standards.md)
- [Adoption and implementation-cost guide](docs/adoption-guide.md)
- [AI and retrieval integration guide](docs/ai-integration.md)
- [Implementation-feedback register](docs/development/implementation-feedback.md)
- [Non-normative design-decision matrix](docs/design-decisions.md)
- [Open design questions](docs/open-questions.md)
- [Authoritative 1.0 promotion checklist](docs/releases/1.0-checklist.md)

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
[`examples/v1.0/basic-engram`](examples/v1.0/basic-engram) for a small valid package.

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
under [MPL 2.0](LICENSE-CODE). Both licenses permit commercial use while keeping
changes to the covered specification or source files open under their respective
terms; see the [plain-language licensing guide](docs/licensing.md).
