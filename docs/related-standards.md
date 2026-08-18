# Related standards and projects

This document is non-normative. It locates Synthetic Engram among adjacent
work, identifies meaningful differences, and gives adapter authors a starting
point. Similar concepts do **not** imply wire compatibility. Descriptions here
reflect the cited projects at the time of review; implementers must examine the
source version they actually map.

## Position in the ecosystem

Synthetic Engram standardizes a portable, owner-controlled knowledge package
that remains directly usable by human applications, conventional software, and
AI systems. It is not a replacement for an AI cognitive-memory model, an access
protocol, a knowledge-base application, or a live database.

| Work | Primary layer | Unit or boundary | Likely relationship |
|---|---|---|---|
| Synthetic Engram | knowledge interchange | durable knowledge environment/package | source and destination format |
| EngramSpec | governed AI context | scoped context envelope | selective projection |
| PLUR Engram Specification | agent cognition/memory | atomic learned memory | derived memory adapter |
| `ly-wang19/engram` | LLM memory engine | engine-managed facts and episodes | import/export adapter |
| Infinite Brain OS | opinionated knowledge operating system | Git repository and workflows | implementation or repository adapter |
| Model Context Protocol | tool/resource access | client-server protocol | possible delivery mechanism |

## EngramSpec

[EngramSpec](https://engramspec.org/) ([source repository](https://github.com/engramspec/spec)) describes portable, governed AI memory. Its context-envelope orientation overlaps with user ownership, scoped disclosure, corrections, history, and cross-provider AI context.

The scope differs: an EngramSpec envelope is aimed at context supplied to an AI
runtime, while a Synthetic Engram may also contain full notes, project and
action records, authored graphs, and attachments that conventional applications
use directly. An Engram Service could select authorized records and project them
into an EngramSpec envelope. Such a mapping is normally lossy and should be
reported as a **projection**, not a migration. Identity, beliefs, corrections,
constraints, and history need an explicit mapping document rather than being
inferred from record titles or tags.

## PLUR Engram Specification

The [PLUR Engram Specification](https://plur.ai/spec.html) uses *engram* for an
atomic unit of learned agent knowledge. Its cognitive model includes concepts
such as activation, reinforcement, decay, associations, feedback, and retrieval.
It therefore addresses how agent memory behaves, rather than a general archive
of owner-controlled knowledge.

Selected Synthetic Engram records can be transformed into PLUR-style memories,
and useful learned memories can be adopted back as records with provenance in a
future mapping. Activation and decay must remain adapter- or engine-specific:
an authored reference note, project, or architecture graph must not lose
portable significance merely because an agent has not retrieved it recently.
One Synthetic Engram record may yield several atomic memories, so adapters must
not assume a one-to-one identity mapping.

## `ly-wang19/engram`

[`ly-wang19/engram`](https://github.com/ly-wang19/engram) is an open-source
long-term memory engine for LLM agents. The project describes durable facts and
episodes, bi-temporal history, hybrid retrieval, graph relationships,
cross-session memory, and export/import. These features overlap strongly with
AI uses of Synthetic Engram.

The architectural role is different. The engine is a live implementation with
retrieval and memory-management behavior; Synthetic Engram defines the portable
contract and can be useful with no LLM or retrieval engine. An adapter could
hydrate the engine from selected records or export adopted engine memories as
records. It must document mappings for fact versus episode types, valid and
transaction time, graph edges, engine-generated state, provenance, and stable
IDs. Search indexes, embeddings, scores, and runtime retrieval state should not
be treated as durable core data by default.

## Infinite Brain OS

[Infinite Brain OS](https://github.com/starmynd-org/infinite-brain-os) is a
Git-backed knowledge operating system built around Markdown/YAML, explicit
structure, workflows, and AI-agent use. It has conceptual overlap in durable
owner-controlled knowledge, typed records, identifiers, graph edges, projects,
provenance, validation, constrained agent authority, and the separation of
canonical knowledge from operational state.

Infinite Brain OS is an opinionated application and repository architecture;
Synthetic Engram is a lower-level interchange model. An Infinite Brain OS
repository could implement Synthetic Engram export/import, or an external
adapter could translate its entities and edges into a package. Compatibility is
not automatic merely because both use Git, Markdown, or YAML. A mapping must
cover ontology and lifecycle states, namespace or project structure, edge
semantics, provenance, IDs, attachments, and application-specific fields.
Unmapped semantics can be preserved in namespaced extensions where practical.

## Model Context Protocol

[Model Context Protocol](https://modelcontextprotocol.io/) operates at a
different layer: it lets clients discover and access tools, resources, and
prompts exposed by a server. An Engram Service may use MCP to expose searches,
records, or bounded package fragments, just as it might use HTTP or a local
library API. MCP does not replace the durable package, completeness rules, or
stable knowledge identity; Synthetic Engram does not prescribe MCP as its
transport.

## Reused foundational standards

The core deliberately builds on established formats rather than redefining
them:

- BCP 14 (RFC 2119 and RFC 8174) supplies normative requirement language.
- RFC 3339 supplies timestamp syntax, narrowed by the specification to UTC `Z`.
- ULID supplies the sortable identifier suffix used with typed prefixes.
- JSON and JSON Schema represent and validate manifests, graphs, and attachment
  metadata.
- A restricted YAML 1.2 subset provides deterministic Markdown front matter.
- Markdown carries human-readable record bodies without selecting a rendering
  dialect.
- Media types and SHA-256 identify attachment representation and integrity.

Potential future mappings include PROV-O for provenance, RDF or property-graph
formats for graph exchange, iCalendar/VTODO for actions, and RO-Crate for
research-oriented packaging. None is a core dependency until a normative
mapping defines preservation and loss.

## Adapter requirements and decision checklist

Adapters should favor explicit mappings over claims of equivalence. Before
calling a conversion lossless, document:

1. how stable object identity survives `A -> B -> A`;
2. which record types, graph semantics, attachments, and external references map;
3. how unknown extensions and unsupported inventoried objects are preserved;
4. whether hierarchy, history, provenance, and timestamps retain their meaning;
5. which data is projected, derived, merged, split, or omitted; and
6. whether a complete export remains complete after the round trip.

If required information or semantics are lost, call the result a projection,
derived context, derived memory, or export view—not a lossless migration. This
is the practical test an application author or coding agent should use when
deciding whether an adjacent system can interoperate with Synthetic Engram.
