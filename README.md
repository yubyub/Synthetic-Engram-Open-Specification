# Synthetic Engram Open Standard

**Manage knowledge once; keep it useful across people, applications, and AI.**

Synthetic Engram 0.2 is a pilot specification for portable, human-controlled
knowledge. It represents typed Markdown records, stable identities, explicit
relationships, portable graphs, and verifiable attachments in an inspectable
directory package.

> [!IMPORTANT]
> **Status: 0.2 pilot specification.** It is available for prototypes, pilots,
> and implementation feedback. No external application is known to use it yet.
> Breaking changes are expected before a stable 1.0 release.

## What it is

Synthetic Engram defines the durable information that can move between a human,
an application, and an AI integration. An application may use the package as a
small local store, map it into a database, or expose it through its own API.

The 0.2 interoperability boundary is the package. It is not a database engine,
application framework, synchronization protocol, permission system, retrieval
algorithm, AI-memory policy, or standardized remote API.

```text
application store <--> 0.2 package <--> another application
       |                      |
 human interface       bounded AI context
```

Use it when stable IDs, links, explicit complete/partial exports, human
inspection, or a credible exit path matter. It is probably unnecessary when one
program will always own the data or ordinary Markdown already preserves all
required meaning.

## Pilot expectations

Pilot implementations should:

- begin with import/export rather than redesigning a production database;
- publish mappings, omissions, transformations, and unsupported profiles;
- round trip representative real data and preserve stable IDs;
- treat every package as untrusted input;
- retain source IDs in AI-derived context and citations; and
- report integration friction before proposing new core fields.

The included Python and Node processors are repository-maintained pilot adapters.
They exercise the same vectors in two runtimes, but are not independent external
implementations, production SDKs, or certification evidence.

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

The manifest inventories every normative object. Records are UTF-8 Markdown with
restricted YAML front matter; graphs and attachment metadata are JSON. Inspect
the [complete example](examples/v0.2/basic-engram/README.md) and the
[partial example](examples/v0.2/partial-engram/README.md).

## AI integration

An AI can inspect a package directly, or an application can expose authorized
Engram data through HTTP, MCP, a local library, or another interface. Core 0.2
does not make those live interfaces mutually compatible.

The recommended discovery sequence is capabilities, authorized overview,
available graphs, bounded traversal or selection, and then batched object or
attachment retrieval by stable ID. See the [AI integration guide](docs/ai-integration.md)
and [remote delivery pattern](docs/remote-delivery-pattern.md).

## Evaluate or implement

- Adoption decision: [adoption guide](docs/adoption-guide.md)
- Common objections and planned responses: [adoption questions](docs/adoption-questions.md)
- Normative format: [SPEC.md](SPEC.md)
- JSON Schemas: [schemas/README.md](schemas/README.md)
- Producer/consumer obligations: [conformance guide](docs/conformance.md)
- Architecture boundaries: [architecture](docs/architecture.md)
- Security limitations: [SECURITY.md](SECURITY.md) and
  [0.2 security review](docs/security-review-0.2.md)
- Current maturity: [component status](docs/status.md)
- Related work: [related standards and projects](docs/related-standards.md)
- Contribution process: [CONTRIBUTING.md](CONTRIBUTING.md)

Additional implementation guidance covers [front matter](docs/front-matter.md),
[identity lifecycle](docs/identity-lifecycle.md), [profile governance](docs/profile-governance.md),
[graph mappings](docs/graph-mappings.md), and [preservation](docs/preservation-mappings.md).

## Validate the repository

Requires Python 3.11+, Node 20+ for cross-runtime development tests, and the
Python dependencies in `requirements-dev.txt`.

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 scripts/conformance_harness.py --adapter implementations/python-engram/engram_adapter.py
python3 scripts/conformance_harness.py --adapter implementations/node-engram/engram-adapter.js
python3 scripts/run_frontmatter_tests.py
python3 scripts/run_lifecycle_tests.py
python3 scripts/run_interoperability.py
```

Some systems provide the interpreter as `python` instead of `python3`; either
is acceptable when it resolves to Python 3.11 or newer.

## Licence

The specification, documentation, schemas, examples, fixtures, workflows, and
software are available under the permissive [MIT License](LICENSE). See the
[plain-language licensing guide](docs/licensing.md).
