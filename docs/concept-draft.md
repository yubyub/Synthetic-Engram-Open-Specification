# Synthetic Engram Open Standard: original concept draft

> [!NOTE]
> This historical, non-normative draft is retained as design rationale. The
> current normative requirements are in [`../SPEC.md`](../SPEC.md).

> **A human-owned and controlled, portable format for persistent human and AI knowledge, designed to be usable by people, AI systems, and non-AI applications.**

## Status

This document describes the initial concept for the **Synthetic Engram Open Standard**.

It is intended to define an open interoperability layer for durable personal and shared knowledge. It is deliberately independent of any particular:

- application
- AI provider
- database
- cloud platform
- operating system
- graph renderer
- task manager
- calendar service
- storage vendor

A Synthetic Engram should remain useful even when the application that created, hosted, or modified it is no longer used.

The term **Synthetic Engram** is intentionally more specific than the increasingly overloaded term **engram**, which is already used by several AI-memory projects and specifications with different meanings.

---

# 1. Purpose and Long-Term Intent

A **Synthetic Engram** is a durable, portable body of knowledge that is owned and controlled by a person or other defined owner and can be used across:

- human-facing applications
- AI assistants
- AI agents
- coding agents
- graph and diagram tools
- note applications
- project systems
- task and calendar applications
- search/indexing systems
- self-hosted services
- cloud services
- other tools that understand some or all of the standard

The purpose of the standard is to separate **knowledge ownership from application ownership**.

```text
                    USER'S SYNTHETIC ENGRAM
                              |
               +--------------+--------------+
               |              |              |
               v              v              v
          Human App       AI Service     Other Tool
               |              |              |
               +--------------+--------------+
                              |
                              v
                    same durable knowledge
```

Applications will change.

AI providers will change.

Storage technologies will change.

A user's accumulated:

- notes
- understanding
- decisions
- graphs
- project structures
- relationships
- actions
- history
- attachments
- contextual knowledge

should not have to disappear with them.

A successful Synthetic Engram ecosystem should allow a user to move between applications, combine multiple tools, or replace an AI provider without abandoning their accumulated knowledge.

## The primary interoperability target is broader than AI memory

Synthetic Engram can provide context to AI and can be used as a source for AI-agent memory.

However, it is **not primarily defined as an AI-agent memory algorithm**.

Its primary purpose is to provide a cross-compatibility layer between:

```text
human
+
knowledge
+
applications
+
AI
```

A Synthetic Engram should therefore still be useful if no AI system is connected to it.

For example, a non-AI graph application could use the graph records and relationships, a note application could use Markdown records, a task application could consume actions, and a backup/migration tool could preserve the whole package.

---

# 2. Terminology

The word **engram** has existing meanings in neuroscience and is also used differently by several AI-memory systems.

This standard therefore uses more specific terminology.

## Synthetic Engram

A **Synthetic Engram** is the complete durable knowledge environment represented according to this standard.

It may contain:

```text
records
graphs
relationships
attachments
projects/context
actions/reminders
history
external references
extensions
```

A Synthetic Engram may be stored locally, hosted by a service, synchronised between systems, or exported as a package.

## Engram

Within this specification, **Engram** may be used as a short-form reference to a **Synthetic Engram** when the meaning is unambiguous.

It does **not** mean one individual learned memory item.

Other specifications may use the lowercase word `engram` for an atomic agent memory. Implementations and documentation should avoid assuming those meanings are equivalent.

## Engram Record

An **Engram Record** is one durable typed object inside a Synthetic Engram.

Examples:

```text
note
project
action
reminder
graph metadata record
reference
custom record
```

An individual record should not normally be called simply "an engram", because that terminology conflicts with existing agent-memory models.

## Engram Package

An **Engram Package** is a portable serialised representation of all or part of a Synthetic Engram.

It may be:

```text
a directory
an archive
a stream
an export bundle
```

An Engram Package is intended for:

- migration
- backup
- transfer
- import/export
- interoperability testing
- offline inspection

## Engram Namespace

An **Engram Namespace** is a durable logical boundary or domain within a Synthetic Engram.

A Namespace may represent:

```text
a project
a personal domain
a work domain
a hobby
an organisation area
a shared team space
```

A Namespace has persistent identity and may be used for:

- organisation
- navigation
- ownership
- permission boundaries
- default context
- policy
- metadata

A Namespace is **not merely a query or filter result**.

A record may belong to one Namespace while linking to records in another.

## Engram Lens

An **Engram Lens** is a reusable selection or filter definition over a Synthetic Engram.

A Lens may select:

- all or part of one Namespace
- several Namespaces
- records independent of Namespace
- particular types
- tags
- statuses
- time windows
- graph neighbourhoods
- explicit records
- another deterministic selection rule

Examples:

```text
Namespace = Project A

Namespace = Project A
AND type = graph

Namespace IN [Project A, Project B]
AND tag = architecture

graph_distance(anchor, <= 2)
AND status = active
```

A Lens may therefore be narrower than a Namespace, equivalent to a Namespace for a particular purpose, or broader than one Namespace.

The Lens is the **selection definition**.

The resulting selected view is an **Engram Fragment**.

## Engram Surface

An **Engram Surface** is an application, agent, user interface, protocol endpoint, or integration through which some portion of a Synthetic Engram is accessed or modified.

Examples:

```text
notes application
graph editor
AI agent
web interface
mobile application
task integration
MCP endpoint
filesystem adapter
```

A Surface should have an explicit boundary describing, where applicable:

```text
what it reads
what it may write
which Namespaces it can access
which operations it may perform
what temporary state it owns
how durable writes are committed back to the Engram
```

A Surface may own ephemeral or derivative state such as:

- caches
- UI state
- session state
- temporary drafts
- indexes
- generated context

but should not become the only durable home of portable user knowledge unless it is also acting as an Engram Store.

The concept reinforces:

> **A Surface uses an Engram; it does not automatically own the Engram.**

## Engram Fragment

An **Engram Fragment** is a deliberately constrained partial view or subset of a Synthetic Engram.

A Fragment may be produced from an Engram Lens, an access policy, explicit selection, or a combination of them.

A Fragment may therefore be constrained by:

```text
namespace
project
context
record type
graph
relationship neighbourhood
tag
time range
explicit record IDs
permission scope
query/filter rules
```

Examples:

```text
"Project Alpha only"

"Notes and graphs related to architecture"

"Actions due this week"

"Everything within two graph hops of record X"

"Only records the AI client is authorised to read"
```

A Fragment is not necessarily a separate copy of the data.

It may be:

- dynamically resolved by an Engram Service
- exported as a partial Engram Package
- exposed through an API
- mounted into another application
- generated temporarily for an AI or agent session

Conceptually:

```text
                 SYNTHETIC ENGRAM
                        |
                scope / filter / policy
                        |
                        v
                 ENGRAM FRAGMENT
                        |
             +----------+----------+
             |                     |
             v                     v
          AI Agent            Other Tool
```

A Fragment should preserve the stable IDs of the records it contains.

This means a record appearing in several Fragments remains the same underlying Engram Record rather than becoming a duplicated copy.

### Permission-scoped fragments

An Engram Fragment is especially useful for access control.

For example:

```text
AI client
   |
   | authorised for:
   | project = "Example Project"
   | record types = note, graph
   | operations = read
   v
Engram Fragment
```

The client does not need permission to the complete Synthetic Engram.

The Engram Service can enforce the scope and expose only the Fragment that the client is authorised to consume.

### Context-scoped fragments

Fragments may also be defined for relevance rather than security.

For example, an AI may be allowed to access the whole Synthetic Engram but request:

```text
project = example-project
+
graph neighbourhood depth <= 2
+
status = active
```

to create a smaller context-oriented Fragment.

The distinction is important:

```text
permission constraint
    = what the consumer is allowed to access

context constraint
    = what is useful for the current task
```

A Fragment may apply either or both.

### Portable fragments

A partial Engram Package may represent a Fragment.

Its manifest should indicate that it is not necessarily a complete Synthetic Engram and, where appropriate, record:

```text
source Engram ID
fragment ID
selection criteria
created_at
authorising scope
whether references outside the Fragment exist
```

Applications must not assume that missing linked records were deleted merely because they are outside the Fragment.

## Engram Store

An **Engram Store** is a live storage implementation that holds a Synthetic Engram.

Examples:

```text
Markdown + SQLite
PostgreSQL + object storage
document database
graph database + blob store
filesystem
```

The Engram Store is an implementation detail.

Different Engram Stores should be able to exchange equivalent knowledge through the standard.

## Engram Service

An **Engram Service** is an application or service that exposes some portion of a Synthetic Engram to authorised consumers.

An Engram Service may provide:

- read access
- write access
- graph traversal
- AI context retrieval
- search
- migration
- history
- synchronisation
- access control

The service itself is not the Engram.

---

# 3. User Data Authority

A central goal of the Synthetic Engram standard is to give users greater authority over what happens with their information.

An Engram-compatible system should make it possible to distinguish:

- what data exists
- where it is stored
- which service is requesting access
- what portion of the Synthetic Engram that service can access
- whether access is read-only or writable
- whether access is temporary or persistent
- whether access applies to particular projects, record types, graphs, tags, or other scopes

The standard should make this authority representable even though enforcement remains the responsibility of the application or service hosting the Engram.

Conceptually:

```text
                         USER
                          |
                  grants authority
                          |
            +-------------+-------------+
            |             |             |
            v             v             v
       Notes App      AI Agent      Task Service
       notes only     project A     actions only
       read/write     read-only     read/write
            \             |             /
             +------------+------------+
                          |
                          v
                  SYNTHETIC ENGRAM
```

## Access should be scoped

A service should not require access to the entire Synthetic Engram simply because it understands the format. An Engram Service may instead expose an authorised **Engram Fragment**.

Examples:

```text
AI coding agent
    read:
        one project
        selected notes
        selected graphs

task service
    read/write:
        actions
        reminders

graph viewer
    read:
        graph objects
        referenced record titles

backup service
    read:
        complete Engram Package
```

## Access descriptors

The standard may define portable access descriptors such as:

```text
subject / client identity
operations
record types
projects
contexts
record IDs
tags
valid_from
valid_until
maximum uses
```

Example conceptual descriptor:

```yaml
access:
  subject: "client-example"
  operations:
    - read
  record_types:
    - note
    - graph
  contexts:
    projects:
      - project_01K...
  valid_until: 2026-08-17T18:00:00Z
```

An implementation may enforce authority using:

- OAuth
- API keys
- capability tokens
- operating-system permissions
- application sessions
- another security model

The Synthetic Engram standard should describe **what authority is being granted**, without mandating how identity is authenticated.

## Knowledge versus runtime security configuration

Access policy and credentials are not necessarily part of the user's durable knowledge archive.

An implementation may:

- export policy descriptors
- omit secrets
- regenerate runtime credentials
- preserve audit metadata
- retain only descriptive authority information

The standard should distinguish:

```text
portable knowledge and authority semantics
```

from:

```text
runtime credentials and security implementation
```

---

## Surface boundary

A Surface should be explicit about the boundary between:

```text
the authoritative Synthetic Engram
```

and:

```text
surface-local runtime state
```

Examples of surface-local state include:

- a UI layout cache
- an AI conversation buffer
- generated embeddings
- local search indexes
- temporary drafts
- task execution state

A Surface MAY maintain such state.

A Surface SHOULD NOT silently make portable user knowledge dependent on that private state.

Where a Surface modifies durable Engram content, the modification should pass through a defined write path that preserves:

- stable identity
- permissions
- provenance
- revisions where supported
- validation

This makes it possible to replace the Surface without losing the underlying knowledge.


# 4. Core Goals

The Synthetic Engram standard should be:

## Open

Anyone should be able to implement it.

Commercial and non-commercial software should be able to:

- read Synthetic Engrams
- write Synthetic Engrams
- import and export Engram Packages
- build services around the standard
- extend it through documented mechanisms

## Portable

A complete Synthetic Engram should be exportable into ordinary files or another documented portable representation.

## Human-readable where practical

Core textual knowledge should use formats such as:

```text
Markdown
JSON
YAML
plain-text DSL
```

rather than requiring opaque proprietary binary formats.

## Stable

Knowledge objects should have identities that survive:

- renaming
- moving
- migration
- cloud/self-hosted transitions
- changes in storage implementation

## Extensible

Applications should be able to add capabilities without breaking applications that implement only the core standard.

## Graph-aware

Hierarchy and arbitrary relationships should be first-class concepts rather than being inferred only from folders or filenames.

## AI-friendly

An AI should be able to inspect structure and retrieve relevant information without loading the entire Synthetic Engram into its context window.

## Human-usable

The representation should support information that is directly useful to people and conventional applications.

AI-generated summaries or embeddings must not be required to make the core knowledge understandable.

## User-controlled

The standard should support user decisions about:

- migration
- export
- access
- read/write authority
- partial access
- service replacement

## Application-independent

The format should not depend on a particular:

```text
database
cloud provider
AI provider
graph engine
application
operating system
```

---

# 5. Non-Goals

The Synthetic Engram standard should not define a mandatory:

- user interface
- AI provider
- LLM
- AI memory algorithm
- database
- cloud provider
- authentication system
- graph renderer
- task provider
- calendar provider
- sync service
- live filesystem layout

It defines the **portable information model and interoperability rules**.

---

# 6. Synthetic Engram Model

At its simplest, a Synthetic Engram is a collection of durable objects with stable identities and explicit relationships.

```text
Synthetic Engram
├── Records
│   ├── Notes
│   ├── Projects
│   ├── Actions
│   ├── Reminders
│   └── Other typed records
│
├── Graphs
│
├── Relationships
│   ├── hierarchy
│   └── links
│
├── Attachments
│
├── External References
│
├── Metadata
│
└── Optional History / Provenance
```

A service does not need to support every object type in order to use a Synthetic Engram.

For example:

```text
notes app
    understands:
        notes
        links
        attachments

architecture / graph application
    understands:
        graphs
        notes
        relationships

task application
    understands:
        actions
        reminders

file-navigation tool
    understands:
        file references
        graphs
        projects

AI context service
    understands:
        metadata
        graphs
        relationships
        selected record content
```

This allows partial interoperability.

---

# 7. Stable IDs

Every durable object should have a stable globally unique identifier.

Examples:

```text
note_01K...
graph_01K...
project_01K...
action_01K...
attachment_01K...
```

The exact identifier scheme should be standardised separately.

Suitable schemes may include:

- UUID
- ULID
- another documented collision-resistant identifier

Identity must not depend on:

```text
filename
folder path
database row
cloud object key
display title
```

Example:

```yaml
---
engram_id: note_01K7K9...
type: note
title: Production Hosting
---
```

A record may be moved or renamed while relationships continue to reference the same ID.

---

# 8. Core Record Model

A minimal Engram Record should contain:

```text
id
type
title
created_at
updated_at
content or content reference
```

Common optional fields may include:

```text
status
tags
parent
links
contexts
source
revision
schema_version
extensions
```

Example Markdown record:

```markdown
---
engram_id: note_01K7K9J4...
engram_version: "1.0"
type: note
title: Production Hosting
created_at: 2026-08-17T03:00:00Z
updated_at: 2026-08-17T03:10:00Z
parent: note_01K7K8...
tags:
  - hosting
  - architecture
links:
  - target: note_01K7M1...
    relation: related_to
---

# Production Hosting

Production services are deployed separately from the application control plane.
```

---

# 9. Relationship Model

Synthetic Engram should distinguish at least two core relationship concepts.

## 9.1 Hierarchy

Hierarchy answers:

> **Where does this object belong?**

Example:

```text
Project
└── Architecture
    └── Hosting
```

A record may define a primary parent:

```yaml
parent: note_01K...
```

The initial standard should favour a single primary parent because it gives hierarchy predictable tree-like behaviour.

Additional placement or aliasing can be represented later through extensions or another standard relationship.

## 9.2 Links

Links answer:

> **What is this object related to?**

Example:

```text
[Hosting] -------- [Authentication]
     |
     +------------ [Deployment]
```

Example:

```yaml
links:
  - target: note_01K...
    relation: related_to
```

At minimum, applications should understand a generic relationship:

```text
related_to
```

Additional common relationship types may later be standardised:

```text
depends_on
derived_from
supersedes
references
supports
contradicts
implements
```

Applications should preserve relationship types they do not understand where practical.

---

# 10. Graphs

A graph is a first-class Synthetic Engram object.

A graph may describe:

- architecture
- project structure
- knowledge relationships
- learning pathways
- skill trees
- folder/file navigation
- organisation models
- workflows
- any other connected structure

A graph should be able to reference other Engram Records without embedding their entire contents.

Example conceptual graph:

```text
node hosting {
    ref: note_01K...
    title: "Hosting"
}

node authentication {
    ref: note_01L...
    title: "Authentication"
}

edge hosting -> authentication
```

The graph contains:

- node identity
- layout/presentation
- graph relationships
- references to Engram Records

The referenced record contains the durable content.

This lets multiple graphs reuse the same record.

---

# 11. Graph Representation

The Synthetic Engram standard should not initially require one mandatory graph DSL syntax unless interoperability requires it.

A graph object should identify its representation.

Example:

```yaml
engram_id: graph_01K...
type: graph
format: example-graph-dsl/v1
```

Applications that understand the format can render or edit it directly.

Applications that do not understand the format should still be able to:

- preserve it
- identify its type
- retain its metadata
- expose it as unsupported content

## Relationship extraction

Where practical, graph formats should provide a deterministic way to extract:

```text
nodes
references
relationships
```

This allows generic Synthetic Engram indexing and graph navigation without requiring every application to understand graph layout semantics.

A future version of the standard may define a generic graph interchange representation in addition to application-specific graph DSLs.

---

# 12. Attachments

Large binary content should remain outside Markdown bodies.

Attachments may include:

- images
- PDFs
- audio
- video
- documents
- diagrams
- datasets
- arbitrary supporting files

Each attachment should have a stable ID.

Example metadata:

```json
{
  "id": "attachment_01K...",
  "filename": "network-diagram.png",
  "media_type": "image/png",
  "size": 428310,
  "sha256": "...",
  "path": "attachments/attachment_01K.../network-diagram.png"
}
```

Textual content can reference attachments using a portable URI scheme:

```markdown
![Network](engram-attachment://attachment_01K...)
```

An application may resolve that reference to:

- a local file
- an object-store URL
- a cached copy
- another authorised location

without changing the record.

---

# 13. Projects and Context

Projects are optional organisational context rather than mandatory ownership containers.

A record may be:

```text
general
project-scoped
linked to one or more projects
```

Example:

```yaml
contexts:
  visibility: general
  projects:
    - project_01K...
```

A human application or AI system can use context to filter retrieval without changing the underlying record identity.

---

# 14. Actions and Reminders

Synthetic Engram may define portable action and reminder records.

Example:

```yaml
engram_id: action_01K...
type: action
title: Configure production backup
status: open
due: 2026-09-01
project: project_01K...
```

An application may:

- manage the action itself
- display it
- synchronise it with an external task provider
- preserve it without providing task-specific features

The Engram Record remains portable even if an external task service is later removed.

---

# 15. External References

A Synthetic Engram does not need to copy everything it references.

A record may reference an external resource such as:

```text
Git repository
calendar event
service-management record
website
cloud document
local file
API resource
```

Example:

```yaml
external_refs:
  - type: git_repository
    uri: "..."
  - type: calendar_event
    provider: "..."
    external_id: "..."
```

External references should clearly distinguish:

```text
portable Engram content
```

from:

```text
a pointer to something outside the Engram
```

An application must not imply that an external resource is included in an Engram Package unless it actually is.

---

## Authoritative, Numeric and Operational Data

Synthetic Engram should distinguish **durable knowledge** from **live authoritative operational data**.

Examples of data that may remain authoritative in another system include:

```text
telemetry
historian measurements
financial balances
inventory
live queues
analytics datasets
CMDB state
transactional database rows
rapidly changing metrics
```

The standard should permit three related patterns.

### 1. Data reference

An Engram Record may describe and point to externally authoritative data.

It may include:

```text
name
meaning
schema
unit
owner
source URI/reference
retrieval/query information
access requirements
```

The referenced data is not implied to be contained in the Engram Package.

### 2. Portable snapshot

A bounded value or dataset may be captured as part of the Engram when its historical state is meaningful.

Where practical, include provenance such as:

```text
source
observed_at
retrieved_at
unit
precision
source version/checksum
```

A snapshot must be distinguishable from a live authoritative source.

### 3. Native deterministic record

Some numeric or structured information genuinely belongs to the Engram itself.

Examples include:

- a manually recorded target
- a calculated value used in a durable decision
- a small table maintained as personal knowledge
- a fixed configuration value

The standard should allow such records without forcing them into narrative Markdown.

## Principle

Synthetic Engram should not attempt to become the authoritative transactional database for every external system it references.

A useful rule is:

```text
meaning, context, relationships and durable snapshots
    may belong in the Engram

rapidly changing operational truth
    may remain in the system that owns it
```

This keeps the standard useful to both human knowledge applications and deterministic data systems without conflating their roles.


# 16. History and Revisions

History is an **optional but standardised capability**.

An Engram-compatible application does not need to maintain revision history.

However, if it does maintain history and wishes that history to remain portable, it should represent revisions using standard semantics.

This allows:

```text
application without history
        |
        | imports current state
        v
 Synthetic Engram

application with history
        |
        | imports current state + revisions
        v
 Synthetic Engram
```

## Record revision model

A portable revision should identify at least:

```text
record_id
revision_id
timestamp
```

Optional fields may include:

```text
previous_revision
origin
author
client
change_type
message
content snapshot
content delta
```

Example:

```json
{
  "record_id": "note_01K...",
  "revision_id": "rev_01M...",
  "previous_revision": "rev_01L...",
  "timestamp": "2026-08-17T03:20:00Z",
  "origin": "example-application"
}
```

## Current state versus history

Every record should have a clear current state.

History must not be required merely to read the current Synthetic Engram.

An application that does not understand or support history should still be able to import the current record state.

## History capability levels

A future compatibility profile may distinguish:

```text
current-state only
revision-aware
sync-capable
```

## Deleted or superseded information

Where a system preserves deleted, archived, or superseded content, that information may also be represented through revision/history metadata.

The standard should prefer preserving identity and history over silently reusing IDs.

---

# 17. Engram Package

A complete portable Engram Package may be represented as a directory or archive.

Example:

```text
my-engram/
├── engram.json
├── records/
│   ├── notes/
│   ├── projects/
│   ├── actions/
│   └── reminders/
├── graphs/
├── attachments/
├── revisions/
└── extensions/
```

`engram.json` describes the package.

Example:

```json
{
  "format": "synthetic-engram",
  "version": "1.0",
  "id": "engram_01K...",
  "created_at": "2026-08-17T03:00:00Z",
  "record_count": 1284,
  "capabilities": [
    "notes",
    "graphs",
    "hierarchy",
    "links",
    "attachments",
    "actions",
    "history"
  ]
}
```

---

# 18. Live Storage Does Not Need to Match the Package

The standard distinguishes between:

```text
portable representation
```

and:

```text
Engram Store implementation
```

An application may internally use:

```text
Markdown + SQLite
PostgreSQL
S3-compatible object storage
document database
graph database
distributed object store
```

provided it can correctly import and export the Synthetic Engram representation it claims to support.

Example:

```text
Application A
Markdown + SQLite
       |
       v
 Engram Package
       |
       v
Application B
PostgreSQL + object storage
```

The applications do not need the same database.

They need to preserve the same **meaning**.

---

# 19. Migration Between Services

Migration should be a normal Synthetic Engram capability rather than a product-specific emergency export.

## Service A → Service B

```text
Service A
   |
   | export
   v
Engram Package
   |
   | validate
   v
Service B
   |
   | import
   v
Service B Engram Store
```

The importing service should:

1. validate the manifest
2. validate object IDs
3. validate required schemas
4. import supported record types
5. preserve unsupported but valid content where possible
6. import attachments
7. rebuild its own indexes
8. report unsupported capabilities
9. preserve useful provenance

A service should not silently discard valid user data it does not understand.

## Migration report

An import should provide a compatibility report.

Example:

```text
Imported:
  934 notes
  12 projects
  8 graphs
  86 attachments
  42 actions

Preserved but not natively supported:
  3 custom record types
  2 graph layout extensions

Not imported:
  0 records
```

---

# 20. Application Use and Partial Consumption

Synthetic Engram is intended to be **usable by applications that are not AI-specific**.

A service does not need to import or understand the whole Synthetic Engram.

## Notes application

May consume:

```text
notes
attachments
tags
links
hierarchy
```

## Architecture or diagram application

May consume:

```text
graphs
record titles
relationships
attachments
project context
```

## File-navigation application

May consume:

```text
projects
external file references
graphs
folder/file metadata
```

without needing access to unrelated note bodies.

## Search service

May index:

```text
titles
Markdown content
relationships
tags
```

without becoming the system of record.

## Calendar or task integration

May consume:

```text
actions
reminders
calendar references
```

only.

## Backup or migration tool

May consume:

```text
complete Engram Package
```

without interpreting most of its semantic content.

This broad application compatibility is a defining property of the standard.

---

# 21. AI Context Consumption

Synthetic Engram should support AI context retrieval as a first-class use case without making AI context the definition of the format.

An AI-facing service should be able to request structure before full content, typically within an authorised or context-selected **Engram Fragment**.

Example:

```text
AI asks for project context
        |
        v
project + graph metadata
        |
        v
AI identifies relevant nodes
        |
        v
retrieve selected records
```

A lightweight context response may contain:

```text
ID
type
title
short description
parent
links
available content size
```

without returning the complete body.

Example:

```json
{
  "id": "note_01K...",
  "title": "Production Hosting",
  "type": "note",
  "parent": "note_01J...",
  "links": ["note_01L...", "note_01M..."],
  "summary": "Production hosting design",
  "content_available": true
}
```

An AI can decide whether the full record is necessary.

This enables:

- graph-guided retrieval
- context-window efficiency
- scoped disclosure
- project-specific context
- deterministic retrieval before semantic summarisation

## Context views may be derived

An Engram Service may generate AI-oriented context views from the underlying Synthetic Engram.

Examples:

```text
project briefing
relevant decisions
user preferences
selected graph neighbourhood
open actions
recent changes
```

These context views may be generated dynamically and do not need to be the canonical stored form.

---

# 22. AI Agent Memory

A Synthetic Engram can also be used as a source for AI-agent memory.

For example, an agent may persist:

- learned user preferences
- project decisions
- useful procedures
- corrections
- prior outcomes
- task state

as Engram Records.

However, the Synthetic Engram standard should not require every stored item to use agent-memory behaviours such as:

- activation decay
- reinforcement
- confidence weighting
- automatic forgetting
- semantic extraction
- autonomous consolidation

Those behaviours may be implemented:

```text
inside an AI application
through an extension
through an adapter to another memory standard
```

rather than becoming mandatory semantics for all human-owned knowledge.

Conceptually:

```text
             Synthetic Engram
                    |
      durable human-owned knowledge
                    |
                    v
            Agent-memory adapter
                    |
         +----------+----------+
         |                     |
         v                     v
   AI memory model       AI context model
```

This allows Synthetic Engram to support AI memory without forcing a conventional notes app or graph application to implement an AI cognitive-memory model.

---

# 23. Cross-Standard Interoperability

Synthetic Engram should be able to coexist with more specialised standards.

It should not assume that it must replace:

- AI context protocols
- agent-memory formats
- tool protocols
- identity protocols
- task/calendar standards
- graph/semantic-web standards

Instead, an implementation may expose adapters.

## Adapter principle

A Synthetic Engram may act as the broad durable source and produce a narrower representation appropriate to another standard.

Example:

```text
                 SYNTHETIC ENGRAM
                       |
        +--------------+--------------+
        |              |              |
        v              v              v
   AI Context      Agent Memory     Human App
    Adapter          Adapter
        |              |
        v              v
  Other context    Other memory
    standard         standard
```

The Synthetic Engram remains usable without any adapter.

## Lossless and lossy mappings

Adapters should clearly distinguish:

```text
lossless mapping
```

from:

```text
derived / lossy projection
```

For example, converting a long project note into several atomic agent-memory facts may be useful but is not a lossless representation of the original record.

The original Synthetic Engram Record should remain authoritative unless the user explicitly chooses otherwise.

## Provenance

Derived records or external-memory projections should be able to retain provenance such as:

```text
source_record_id
source_revision_id
adapter
derived_at
target_standard
```

This allows a receiving service to understand where the derived context came from.

---

# 24. Remote Consumption

A service may consume a Synthetic Engram without copying the entire Engram Package.

An Engram-compatible API could expose concepts such as:

```text
GET /engram/manifest
GET /records/{id}
GET /records?type=note
GET /relationships/{id}
GET /graphs/{id}
GET /attachments/{id}
GET /changes?since=<revision>
```

The exact API protocol should be standardised separately from the portable package format.

The package should remain useful without the API.

The API should remain useful without requiring a full archive export for every query.

---

# 25. Indexes Are Derivative

Search indexes, graph indexes, and AI context caches should generally be treated as derivative information.

Examples:

```text
SQLite FTS
PageRank scores
backlinks
embedding vectors
generated summaries
search caches
graph traversal tables
```

An Engram Package should not require these to survive migration unless they contain non-reconstructable user-authored information.

An importing application can rebuild its own indexes.

This keeps the standard independent of particular search and AI technologies.

---

# 26. Extensions

Applications need a safe way to add functionality.

An Engram Record may contain namespaced extensions.

Example:

```yaml
extensions:
  com.example.writer:
    chapter_colour: blue

  org.example.graph:
    graph_position:
      x: 421
      y: 118
```

Rules:

1. unknown extensions must not invalidate an otherwise valid record
2. applications should preserve unknown extensions where practical
3. extension names should be globally namespaced
4. extensions should not redefine the meaning of core fields
5. widely adopted extensions may later become part of the core standard

This allows innovation without requiring every vendor to wait for the standard to change.

---

# 27. Compatibility Profiles

Not every application needs to implement every Synthetic Engram capability.

The standard may define capability profiles.

## Engram Core

Minimum interoperability:

```text
manifest
stable IDs
notes
basic metadata
import/export
```

## Engram Linked

Adds:

```text
hierarchy
links
relationship consumption
```

## Engram Graph

Adds:

```text
graph objects
graph references
relationship extraction
```

## Engram Media

Adds:

```text
attachments
attachment URIs
checksums
```

## Engram Data

Potentially adds:

```text
typed deterministic records
data references
units
snapshot provenance
authoritative-source descriptors
```

## Engram Action

Adds:

```text
actions
reminders
status/due semantics
```

## Engram History

Adds:

```text
revisions
provenance
change history
```

## Engram Access

Potentially adds:

```text
portable access descriptors
scopes
operation grants
time-limited authority metadata
```

## Engram AI Context

Potentially adds:

```text
structure-first retrieval
context views
bounded graph traversal
record summaries
AI-oriented scope descriptors
```

## Engram Fragment

Potentially adds:

```text
partial Engram views
selection criteria
permission-constrained subsets
context-constrained subsets
partial-package manifests
external-reference preservation
```

## Engram Sync

Future profile:

```text
change streams
revision exchange
conflict representation
```

An application can advertise the profiles it supports without claiming complete support for every Synthetic Engram feature.

---

# 28. Standard Versioning

The Synthetic Engram standard should use explicit versions.

Example:

```text
Synthetic Engram 1.0
Synthetic Engram 1.1
Synthetic Engram 2.0
```

Compatibility rules should distinguish:

## Additive change

Example:

```text
new optional field
```

Older applications may ignore it.

## Breaking change

Example:

```text
field meaning changes
mandatory structure changes
```

Requires a new major version.

Migration rules should be defined where practical.

---

# 29. Core Interoperability Principle

The central requirement of the standard is:

> **A Synthetic Engram should preserve the meaning of a user's knowledge independently of the application, AI system, or storage technology used to store, view, search, or modify it.**

That means:

- stable identity survives migration
- durable content remains exportable
- relationships remain reconstructable
- unsupported data is not silently discarded
- conventional applications can use useful subsets without AI
- Surfaces remain replaceable and do not silently become the sole owner of durable knowledge
- AI systems can retrieve only the scopes they need
- users can control read/write authority
- users can move between services
- history can travel when supported
- runtime indexes remain replaceable
- externally authoritative operational data can remain external while its meaning and references remain portable
- specialised AI-memory/context standards can be bridged through adapters
- no application needs to become the sole owner of the user's knowledge

---

---

# Supporting Material and Future Specification Work

> **This section is intentionally non-normative.**
>
> It contains related work, compatibility guidance, governance, licensing, implementation notes, examples, and future work that may later move into separate files or repositories.

---

# A. Related Works

The term **engram** is already used by several adjacent AI-memory projects and standards.

Synthetic Engram should acknowledge these works explicitly and avoid presenting itself as the first use of the term or the only approach to portable memory.

## A.1 EngramSpec

Reference:

```text
https://engramspec.org/
https://github.com/engramspec/spec
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6878038
```

EngramSpec describes itself as an open standard for **portable, governed AI memory**.

Its current protocol is oriented around an AI runtime retrieving a signed, scoped context envelope containing concepts such as:

```text
identity
beliefs
corrections
evolution/history
constraints
```

This has meaningful overlap with Synthetic Engram:

- user ownership
- portability
- corrections/history
- scoped disclosure
- cross-provider AI context
- governance of what AI knows about a user

The primary distinction is scope.

EngramSpec is principally concerned with:

```text
portable user memory / context
        |
        v
     AI runtime
```

Synthetic Engram is intended to represent a broader durable knowledge environment directly usable by:

```text
human applications
AI applications
non-AI tools
```

A Synthetic Engram may therefore contain substantial information that is not appropriate for an EngramSpec context envelope, such as:

- full notes
- graph diagrams
- project structures
- attachments
- task records
- file references
- arbitrary application records

### Potential cross-compatibility

An Engram Service could generate an EngramSpec-compatible context envelope from authorised Synthetic Engram Records.

For example:

```text
Synthetic Engram
├── profile/preferences
├── project context
├── corrections/history
├── notes
└── access rules
        |
        | EngramSpec adapter
        v
EngramSpec context envelope
        |
        v
AI runtime
```

This is likely a **projection** rather than a lossless conversion.

The Synthetic Engram remains the broader durable source.

## A.2 PLUR Engram Specification

Reference:

```text
https://plur.ai/spec.html
```

PLUR's Engram Specification defines an `engram` as an **atomic unit of learned AI-agent knowledge**.

Its model includes concepts such as:

- activation strength
- decay
- reinforcement
- associations
- feedback
- retrieval
- learned preferences
- procedures and behavioural patterns

This is closer to a cognitive/agent-memory model than a general personal knowledge interchange format.

Synthetic Engram overlaps through:

- persistent knowledge
- graph relationships
- provenance
- human-readable data
- AI retrieval

The major distinction is that Synthetic Engram does not require ordinary human knowledge to behave like agent memory.

For example, a person's architecture diagram or permanent reference note should not necessarily decay simply because an AI has not retrieved it recently.

### Potential cross-compatibility

Selected Synthetic Engram Records could be transformed into PLUR-style atomic agent memories.

Example:

```text
project note
       |
       | extract selected durable lessons
       v
PLUR-compatible engrams
       |
       v
agent retrieval / activation system
```

PLUR-specific activation, reinforcement, and decay can remain in the agent-memory layer rather than being mandatory Synthetic Engram semantics.

## A.3 ly-wang19/engram

Reference:

```text
https://github.com/ly-wang19/engram
```

This project describes itself as an open-source long-term memory engine for LLM agents.

Its approach includes:

- durable facts
- episodes
- bi-temporal history
- hybrid retrieval
- graph relationships
- cross-session agent memory
- export/import

It overlaps strongly with the AI-memory use cases of Synthetic Engram.

However, it is primarily an **agent-memory engine/implementation**, whereas Synthetic Engram is intended to define a portable knowledge/interoperability model usable independently of an AI memory engine.

A future adapter could allow selected Synthetic Engram records to populate such a memory engine, or allow useful memories produced by the engine to be represented as Synthetic Engram Records.

## A.4 Infinite Brain OS

Reference:

```text
https://github.com/starmynd-org/infinite-brain-os
```

Infinite Brain OS is a Git-backed knowledge operating system for running a business with AI agents using plain Markdown and YAML.

It has significant conceptual overlap with Synthetic Engram, including:

- user/operator-owned durable knowledge
- typed Markdown/YAML records
- stable identifiers
- explicit graph edges
- namespaces
- projects
- provenance
- agent-readable structure
- deterministic validation
- constrained agent authority
- human approval of canonical knowledge
- minimal-context retrieval
- separation between durable knowledge and live operational state

Its **surface boundary** concept is particularly relevant: applications and agents declare what they read, what state they may own, and how durable writes occur.

### Primary distinction

Infinite Brain OS is an opinionated knowledge operating system with a prescribed Git repository structure, entity ontology, workflows, lifecycle states, and operating doctrine.

Synthetic Engram is intended to be a lower-level interoperability model.

It should be possible to implement Synthetic Engram using:

```text
Git + Markdown/YAML
```

but also using:

```text
PostgreSQL + object storage
filesystem + SQLite
graph database
another implementation
```

without changing the portable meaning of the records.

### Potential compatibility

Infinite Brain OS is **not automatically Synthetic Engram compatible** merely because the concepts overlap.

Compatibility could be achieved in either of two ways:

1. Infinite Brain OS could implement the Synthetic Engram standard directly by mapping its records, edges, namespaces, provenance and exports to the standard.
2. An adapter could translate between an Infinite Brain repository and an Engram Package.

Conceptually:

```text
Infinite Brain OS
 opinionated application / knowledge architecture
                |
                | implements or maps to
                v
Synthetic Engram Open Standard
 interoperability representation
```

This is a layering relationship, not necessarily a software dependency.

Neither system needs to be installed "inside" the other.

If compatible mappings exist, a user could migrate or expose selected knowledge between them while preserving the richer application-specific semantics through extensions where practical.

## A.5 Model Context Protocol (MCP)

MCP addresses a different layer.

Conceptually:

```text
Synthetic Engram:
    what durable knowledge exists
    and how it can remain portable

MCP:
    how an AI client can call tools
    and access exposed resources
```

An Engram Service could expose Synthetic Engram capabilities through MCP while also supporting:

- HTTP APIs
- local filesystem access
- direct library integration
- other future protocols

MCP should therefore be considered a possible access mechanism, not the canonical storage format.

## A.6 Relationship to other open data standards

Where practical, later Synthetic Engram specifications should reuse or map to established standards rather than inventing equivalents unnecessarily.

Potential areas include:

- MIME media types for attachments
- ISO 8601 / RFC 3339 timestamps
- URI/IRI identifiers
- JSON Schema
- semantic-web / graph representations
- provenance standards
- calendar/task interchange formats
- identity and authorisation protocols

The core standard should remain understandable without requiring every implementation to adopt the full semantic-web or enterprise standards stack.

---

# B. Cross-Compatibility Guidance

Synthetic Engram should favour adapters over forced equivalence.

## Context-standard adapter

```text
Synthetic Engram
      |
      | select + transform
      v
AI context standard
      |
      v
AI runtime
```

Useful for identity, preferences, corrections, project context, or other selected information.

## Agent-memory adapter

```text
Synthetic Engram
      |
      | derive atomic memories
      v
agent-memory standard/engine
      |
      v
retrieval + reinforcement
```

Useful when an agent needs its own task-oriented memory semantics.

## Tool-protocol adapter

```text
AI client
   |
   | MCP / HTTP / other protocol
   v
Engram Service
   |
   v
Synthetic Engram
```

Useful for controlled remote consumption.

## Round-trip requirement

Adapters should not claim round-trip compatibility unless:

```text
A -> B -> A
```

preserves the information and semantics required by both systems.

Where conversion is lossy, it should be described as:

```text
projection
derived context
derived memory
export view
```

rather than migration.

---

# C. Standard Governance

The standard should ideally live in its own public repository.

Example:

```text
synthetic-engram-standard/
├── README.md
├── SPEC.md
├── schemas/
├── examples/
├── migrations/
├── reference/
└── tests/
```

Possible contents:

```text
formal specification
JSON schemas
Markdown/frontmatter conventions
graph interchange conventions
sample Engram Packages
conformance fixtures
validator
migration utilities
reference parser
```

The goal is for another developer to implement Synthetic Engram support without needing to inspect any particular product's source code.

---

# D. Licensing Intent

The standard should explicitly permit commercial adoption.

A commercial application should be able to implement Synthetic Engram support without being forced to release the rest of its proprietary application.

At the same time, the **standard itself should remain open**.

A useful licensing split to investigate is:

## Specification/documentation

A licence such as **Creative Commons Attribution-ShareAlike 4.0** may be appropriate for the specification documents.

The intended outcome is:

- commercial use is permitted
- copying and redistribution are permitted
- modifications are permitted
- modified versions of the licensed specification material remain under the same licence

## Reference software

Reference parsers, validators, CLI tools, and interoperability libraries may use a software licence such as **Mozilla Public License 2.0**.

The desired outcome is:

```text
commercial adoption
+
open reference implementation
+
no requirement that an entire proprietary application become open source merely because it uses the reference library
```

## Schemas

Machine-readable schemas should have a clearly stated licence.

They may follow:

```text
the specification/documentation licence
```

or:

```text
the reference software licence
```

depending on repository structure.

## Trademark and compatibility branding

Format licensing does not necessarily need to grant unrestricted rights to product branding.

Terms such as:

```text
Synthetic Engram Compatible
Synthetic Engram Certified
```

may later have separate trademark or conformance rules.

> Final licence and trademark choices should be reviewed carefully before public release.

---

# E. Conformance and Certification

A future Synthetic Engram ecosystem could provide automated conformance tests.

Example:

```text
Synthetic Engram Compatibility Suite
       |
       +--> import fixtures
       +--> export fixtures
       +--> ID preservation
       +--> relationship preservation
       +--> attachment checks
       +--> history checks
       +--> extension preservation
```

Applications passing defined tests could claim compatibility with a particular version/profile.

Example:

```text
Synthetic Engram 1.0
Core + Linked + Graph compatible
```

---

# F. Validation and Reference Tooling

The open standard should eventually provide deterministic validation tools.

Potential commands:

```text
engram validate <path>
engram inspect <path>
engram migrate <old-version> <new-version>
engram graph <path>
engram pack <directory>
engram unpack <archive>
```

Validation may check:

- manifest version
- duplicate IDs
- broken references
- hierarchy cycles
- missing attachments
- invalid schemas
- unsupported required extensions
- checksum failures
- malformed revision chains

These tools should be implementable independently of any particular Synthetic Engram product.

---

# G. Future Synchronisation Specification

The first Synthetic Engram standard should prioritise:

```text
import
export
migration
partial consumption
history representation
access scoping
```

before defining a complete distributed synchronisation protocol.

A later sync specification could define an append-only change stream.

Example:

```text
revision 100
revision 101
revision 102
```

A client asks:

```text
changes since revision 100
```

and receives:

```text
101
102
```

Conflicting concurrent changes should preserve both versions rather than silently losing one.

Sync should remain a separate capability/profile so simple applications can implement Synthetic Engram without implementing distributed conflict resolution.

---

# H. Access-Control Specification Work

The core document defines the intent that users should control which services can access which portions of their Synthetic Engram.

A later dedicated access-control specification may define:

- scope grammar
- resource selectors
- record-type selectors
- project/context selectors
- read/write/archive operations
- temporary grants
- one-time grants
- delegation
- revocation metadata
- audit events
- capability-token representation

This should remain separate from authentication protocols such as OAuth.

The standard should describe **authority**, while implementations decide how identities prove who they are.

---

# I. Graph Interchange Specification Work

Application-specific graph DSLs should be allowed.

A future generic graph interchange format may define:

```text
graph ID
node IDs
referenced Engram Record IDs
edge IDs
edge types
labels
groups
layout hints
subgraph references
```

Such a representation should focus on interoperability rather than replacing richer application-specific graph languages.

---

# J. Examples

The examples in this section are explanatory and should eventually move to an `examples/` directory.

## J.1 Example migration

A user begins with one Synthetic Engram-compatible application using:

```text
Markdown + SQLite + local attachments
```

They export:

```text
user-engram.zip
```

Later they move to another application using:

```text
PostgreSQL + object storage + a different UI
```

The second application reconstructs:

- notes
- graph relationships
- projects
- attachments
- portable history

It may generate completely different:

- search indexes
- embeddings
- graph-layout caches
- AI summaries

The user changes application without abandoning accumulated knowledge.

## J.2 Example multi-service consumption

```text
                         SYNTHETIC ENGRAM
                               |
         +---------------------+----------------------+
         |                     |                      |
         v                     v                      v
   Graph/Notes App        AI Context Service      Task Service
         |                     |                      |
         +---------------------+----------------------+
                               |
                               v
                          Backup Service
```

Each system consumes only the portion it needs.

No service must become the sole owner of the user's knowledge.

## J.3 Example scoped AI access

An AI assistant may receive:

```text
read:
    project metadata
    graph structure
    selected notes

write:
    new project notes

not permitted:
    unrelated personal notes
    archive
    permanent deletion
```

Another service may receive:

```text
read/write:
    actions
    reminders

not permitted:
    note bodies
    graph content
```

The standard does not prescribe a security product.

It makes selective authority and partial consumption natural parts of the model.

---

# K. Naming Considerations

The qualifier **Synthetic** helps distinguish this standard from other projects that use the word `engram`.

The name also reflects that the knowledge environment may be:

- created by a person
- generated by AI
- refined jointly by humans and AI
- imported from applications
- derived from external systems

In that sense, the Engram is "synthetic" because it is an assembled, system-mediated memory environment rather than a biological memory trace.

There is a deliberate tension in the name: compared with some agent-centric engram models, Synthetic Engram gives the human unusually strong ownership and authority.

That is not a contradiction in the standard. The word **Synthetic** describes the constructed knowledge environment, not who ultimately controls it.

---


# L. Optional Terminology and Naming Vocabulary

The following terms are **non-normative naming ideas** that may be useful for product interfaces, APIs, extensions, or future specification concepts.

The core standard should generally prefer plain technical terminology where clarity matters, but a restrained cyberpunk vocabulary can give the ecosystem a distinctive identity.

## Fragment

Already proposed as a formal term.

```text
Engram Fragment
```

Meaning:

> A context- or permission-constrained partial view of a Synthetic Engram.

This is strong terminology because it is understandable without being overly technical.

## Shard

```text
Engram Shard
```

Possible meaning:

> A physically or administratively partitioned portion of an Engram.

This could be useful if the standard later distinguishes logical Fragments from physically separate storage partitions.

Suggested distinction:

```text
Fragment = logical/selective view
Shard    = physical/storage partition
```

Because "shard" already has a strong distributed-database meaning, it should not be used casually for filters.

## Trace

```text
Engram Trace
```

Possible meaning:

> A record of provenance, activity, or how information arrived at its current state.

Potential uses:

- provenance chain
- AI contribution history
- import history
- relationship derivation
- revision lineage

It has a useful memory/cyberpunk feel without being obscure.

## Echo

```text
Engram Echo
```

Possible meaning:

> A derived or cached representation of information from another Engram source.

Examples:

- read-only replicated record
- cached remote Fragment
- projection into another service
- context snapshot used temporarily by an AI

This should not be confused with the authoritative record.

## Ghost

```text
Engram Ghost
```

Possible meaning:

> A retained reference to information that is archived, deleted, unavailable, or outside the current Fragment.

For example, a graph could preserve:

```text
record A -> record B
```

while record B is not present in the current Fragment.

A lightweight Ghost could retain:

```text
ID
title if permitted
relationship
availability status
```

This could be useful technically, although the term may be too playful for the normative standard.

A more formal equivalent would be:

```text
External Stub
Reference Stub
Unresolved Reference
```

## Pulse

```text
Engram Pulse
```

Possible meaning:

> A stream or summary of recent changes.

Examples:

```text
changes since revision 104
recent activity
updated records
new relationships
```

This could be a useful UI/API term for change feeds without making it part of the core record model.

## Cortex

```text
Engram Cortex
```

Possible meaning:

> A generated structural index or high-level map over an Engram.

Potentially:

- graph index
- navigation layer
- semantic map
- project overview

This is more product-like than standards-like and should probably remain optional terminology.

## Mesh

```text
Engram Mesh
```

Possible meaning:

> A network of several Engram Stores or services that can reference, exchange, or synchronise knowledge.

Example:

```text
personal Engram
     |
     +--> work Engram
     |
     +--> organisation Engram
```

This could become relevant if federated or cross-owner Engrams are introduced later.

## Gate

```text
Engram Gate
```

Possible meaning:

> A policy-controlled access boundary that exposes one or more Engram Fragments.

For example:

```text
AI Agent
   |
Engram Gate
   |
authorised Fragment
```

A more conventional technical term would be:

```text
Access Gateway
Capability Endpoint
Policy Boundary
```

## Lens

```text
Engram Lens
```

Possible meaning:

> A reusable filter or view definition used to derive a Fragment.

This is particularly useful terminology.

Example:

```text
Lens:
  project = "Example"
  types = [note, graph]
  status = active
```

Applying the Lens produces an Engram Fragment.

Suggested distinction:

```text
Lens     = reusable selection/filter definition
Fragment = the resulting partial Engram view
```

This is one of the strongest optional terms because it maps cleanly to a real technical concept.

## Thread

```text
Engram Thread
```

Possible meaning:

> A sequence of related records or revisions following a topic, decision, or activity over time.

Potential uses:

- decision history
- conversation-derived knowledge
- project storyline
- revision lineage

This overlaps with common conversation terminology, so use carefully.

## Anchor

```text
Engram Anchor
```

Possible meaning:

> A stable reference point used to begin graph traversal or context retrieval.

For AI retrieval:

```text
search finds Anchor
    |
    v
explore neighbouring records
```

This could be useful in API language such as:

```text
anchor_record_id
```

without needing to be a formal object type.

## Capsule

```text
Engram Capsule
```

Possible meaning:

> A deliberately packaged, self-contained Fragment intended for transfer or sharing.

Suggested distinction:

```text
Fragment = logical partial view
Capsule  = portable/shareable packaged Fragment
Package  = formal generic serialised container
```

"Capsule" is evocative, but the standard should probably retain **Engram Package** as the normative term.

## Vault

```text
Engram Vault
```

Possible meaning:

> A secured Engram Store or highly protected section.

This is understandable but is heavily used in password-manager and secrets-management products, so it may create unwanted expectations.

## Suggested vocabulary hierarchy

A useful restrained vocabulary could be:

```text
Synthetic Engram
    complete durable knowledge environment

Engram Record
    one durable object

Engram Store
    live storage implementation

Engram Service
    service exposing Engram capabilities

Engram Lens
    reusable query/filter/scope definition

Engram Fragment
    partial context- or permission-constrained view

Engram Package
    portable serialised representation

Engram Trace
    provenance / lineage information

Engram Pulse
    recent-change feed
```

Of the optional terms, **Lens**, **Trace**, and **Pulse** have the clearest technical meanings while still fitting the identity of the project.

---

# M. Open Questions


The following areas still require formal decisions before a stable 1.0 specification:

- exact ID format
- canonical Engram Package layout
- canonical Markdown/frontmatter schema
- required versus optional timestamps
- graph interchange representation
- graph DSL relationship extraction rules
- Namespace membership and cross-Namespace relationship rules
- Lens representation and deterministic selection grammar
- Surface capability/boundary descriptors
- data reference and snapshot schemas
- access descriptor syntax
- history snapshot versus delta conventions
- extension namespace rules
- MIME/attachment handling
- capability-profile definitions
- AI-context profile details
- adapter/conversion metadata
- cross-standard mappings
- sync semantics
- validation requirements
- migration compatibility rules
- normative terminology such as MUST/SHOULD/MAY
- licensing and governance process
