# ThoughtMesh Open Specification — Refocus and OKF Alignment

## Purpose of this change

Refactor the ThoughtMesh Open Specification around a narrower and more distinctive purpose.

ThoughtMesh should **not attempt to define another general AI memory format, Markdown knowledge format, search system, MCP protocol, or storage engine**.

Existing projects and standards already cover substantial parts of those problems.

The distinctive purpose of ThoughtMesh is:

> **A source-independent logical mesh that maps and connects knowledge across independently owned storage systems without requiring that knowledge to be moved, rewritten, or owned by ThoughtMesh.**

The specification should concentrate on that problem.

---

# 1. Terminology

Use `ThoughtMesh` and `ThoughtMesh Open Specification` consistently. Review
terminology semantically rather than applying mechanical substitutions.

---

# 2. Relationship to Existing Standards

ThoughtMesh should explicitly avoid rebuilding capabilities already addressed by existing standards.

The specification should recognise at least:

* Open Knowledge Format (OKF)
* Model Context Protocol (MCP)
* existing memory/knowledge systems such as Basic Memory and OpenMemory

These systems may be used independently of ThoughtMesh or in conjunction with it.

---

# 3. Relationship to OKF

OKF should be treated as the preferred existing open representation for portable knowledge where its model is suitable.

ThoughtMesh should NOT create another competing Markdown + YAML knowledge-document format where OKF already provides the necessary semantics.

Conceptually:

```text
OKF
    portable representation of knowledge

ThoughtMesh
    mapping and relationships across knowledge sources

MCP
    runtime interface through which agents may access systems
```

ThoughtMesh may use OKF for:

* import;
* export;
* materialization of externally stored knowledge;
* portable knowledge bundles;
* concepts that can be represented directly using OKF;
* provenance and source metadata where OKF already provides suitable semantics.

Do not duplicate OKF fields merely to give them ThoughtMesh-specific names.

---

# 4. Do Not Make ThoughtMesh Merely an OKF Extension Yet

Do not currently define ThoughtMesh as formally extending or modifying OKF.

Instead:

1. define the ThoughtMesh-specific problem independently;
2. identify direct mappings to OKF;
3. use OKF concepts wherever they are sufficient;
4. define ThoughtMesh-specific structures only where OKF does not solve the mesh problem;
5. document how a ThoughtMesh can be imported/exported using OKF.

This reduces unnecessary coupling while OKF and ThoughtMesh are both evolving.

A future version may define a formal ThoughtMesh profile or extension for OKF if that becomes useful.

---

# 5. The Distinctive ThoughtMesh Problem

ThoughtMesh should primarily standardize how independently stored knowledge participates in one logical graph.

Example:

```text
                 ThoughtMesh

 Obsidian ───────────┐
                     │
 GitHub ─────────────┤
                     │
 Google Drive ───────┼──► Logical Knowledge Mesh
                     │
 OpenMemory ─────────┤
                     │
 Native Storage ─────┤
                     │
 Other Systems ──────┘
```

The underlying information does not need to move.

The source system can remain authoritative.

ThoughtMesh provides the connective layer.

---

# 6. Core Concepts the Specification SHOULD Define

Focus the specification around concepts such as:

## Stable ThoughtMesh identity

A logical node requires an identity that is independent of:

* filename;
* filesystem path;
* database primary key;
* provider-specific location;
* current storage system.

Moving an underlying object should not inherently create a new logical object.

---

## Source

A Source identifies a system or storage boundary from which knowledge is obtained.

Examples:

```text
Obsidian vault
GitHub repository
Google Drive
SharePoint
OpenMemory
Basic Memory
ThoughtMesh native storage
filesystem
database
other application
```

---

## Source binding

A ThoughtMesh node may map to an object controlled by a Source.

Conceptually:

```text
ThoughtMesh Node
      │
      ▼
Source Binding
      │
      ├── Source
      ├── external identity
      └── resolver information
```

Separate portable source identity from implementation-local credentials and connection state.

---

## Graph relationships

ThoughtMesh defines relationships between logical nodes regardless of where their underlying knowledge is stored.

For example:

```text
Obsidian Note
      │
      ├── related-to ──► GitHub Project
      │
      └── parent ──────► Project
                              │
                              └── contains ──► Google Drive Document
```

---

## Hierarchy

Parent/child structure remains useful.

Hierarchy should describe logical organisation rather than necessarily matching physical storage hierarchy.

---

## Fragment

Retain the useful concept currently called an Engram Fragment, but rename/reconsider it in ThoughtMesh terminology.

A fragment is a bounded subset of the mesh suitable for:

* sharing;
* agent context;
* permissions;
* export;
* constrained traversal.

Choose final terminology carefully rather than automatically calling it `ThoughtMesh Fragment`.

---

## Lens

A Lens remains a query/filter/view over the mesh.

It is not equivalent to a namespace or physical source.

---

## Source ownership

ThoughtMesh must distinguish:

```text
ThoughtMesh knows about an object
```

from:

```text
ThoughtMesh owns the object's content
```

Externally stored knowledge remains owned by its source.

---

## Capabilities and modification boundaries

A source may expose different capabilities:

```text
discover
read
create
modify
move
delete
```

An implementation may additionally require elevated privileges.

The specification should describe portable capability semantics where useful without prescribing an authentication implementation.

---

# 7. Important Separation of Concerns

Make this principle prominent:

```text
Storage ownership
        ≠
ThoughtMesh membership
        ≠
Index scope
        ≠
Search representation
        ≠
Modification authority
        ≠
Export inclusion
```

These are independent concerns.

---

# 8. Search Is NOT Part of the Portable Specification

Do not standardize:

* full-text search;
* vector databases;
* embeddings;
* chunking algorithms;
* semantic ranking;
* reranking;
* search caches.

An implementation can create these from indexed content.

Search chunks should NOT automatically become durable ThoughtMesh nodes.

Example:

```text
ThoughtMesh:

Requirements.pdf
        │
        └── one logical node


Implementation search index:

Requirements.pdf
    ├── chunk 001
    ├── chunk 002
    ├── chunk 003
    └── chunk 004
```

The second representation is operational and rebuildable.

---

# 9. Database and Runtime Are NOT Part of the Specification

Remove or clearly mark as implementation concerns any requirement for:

* SQLite;
* PostgreSQL;
* graph databases;
* vector databases;
* filesystem layouts;
* web servers;
* Docker;
* MCP server implementation;
* frontend technology.

The ThoughtMesh Open Specification must be implementable using different technologies.

---

# 10. MCP Relationship

MCP should be described as one useful runtime access mechanism, not as part of the ThoughtMesh data model.

Conceptually:

```text
AI
 │
 ▼
MCP
 │
 ▼
ThoughtMesh implementation
```

Another implementation could expose:

```text
REST
GraphQL
library API
CLI
application plugin
```

and still implement the ThoughtMesh specification.

Do not redefine MCP concepts that MCP already standardizes.

---

# 11. Basic Memory and OpenMemory

Document these as examples of systems that solve adjacent problems.

Do not attempt to reproduce them simply to claim equivalent features.

## Basic Memory

Basic Memory is an example of a knowledge/memory system where Markdown is the source of truth and a database provides derived indexing, graph traversal and search.

A user could potentially use:

```text
Basic Memory
      │
      ▼
ThoughtMesh Source Adapter
      │
      ▼
ThoughtMesh
```

ThoughtMesh does not need to replace Basic Memory.

## OpenMemory

OpenMemory is an example of a persistent AI memory layer exposed through MCP.

A user might use:

```text
OpenMemory
     │
     ├── AI persistent memories
     │
     ▼
ThoughtMesh Source
```

or use OpenMemory independently.

ThoughtMesh should not attempt to become a better version of OpenMemory merely because persistent AI memory is useful.

---

# 12. ThoughtMesh Native Storage Is Not a mandatory Part of the Specification even if it is included

A ThoughtMesh implementation may provide its own knowledge storage.

This is optional.

Conceptually:

```text
                 ThoughtMesh

External Sources ──┐
                   ├── mesh
Native Source ─────┘
```

Native storage should conceptually behave as another Source.

The Open Specification should not require a particular native-storage format.

---

# 13. Import and Export

ThoughtMesh should support portable interchange without forcing external sources to change format.

OKF should be the preferred format to investigate and use for portable knowledge materialization.

An export may choose:

```text
Materialize
    Include the knowledge in the portable export.

Reference
    Include the ThoughtMesh mapping/reference without copying source data.

Exclude
    Leave the source/object outside this export.
```

For example:

```text
ThoughtMesh

Obsidian note ───── materialize ──► OKF concept
GitHub repo ─────── reference ────► source/resource reference
Private source ──── exclude
Native note ─────── materialize ──► OKF concept
```

The exact OKF mapping must be based on the actual current OKF specification rather than assumptions.

Where OKF already provides appropriate semantics for:

* concepts;
* sources;
* resources;
* provenance;
* lifecycle;
* links;
* hierarchy;
* metadata;

use them.

Only add ThoughtMesh-specific metadata where necessary.

---

# 14. What ThoughtMesh Should NOT Try to Be

Explicitly state that ThoughtMesh is not intended to be:

```text
another Markdown note format
another Obsidian replacement
another vector database
another RAG framework
another MCP protocol
another AI memory server specification
another knowledge storage engine
another OKF competitor
```

Individual ThoughtMesh implementations may provide some of those capabilities for convenience.

They are not the purpose of the Open Specification.

---

# 15. Target Definition

Refactor the specification around a concise definition similar to:

> ThoughtMesh is an open model for creating a stable, portable knowledge graph across independently owned and heterogeneous information sources. It defines identity, source mapping, relationships, bounded views and portability without requiring the underlying information to move into a new storage system.

The exact wording may be improved, but preserve this scope.

---

# 16. Desired Outcome of the Refactor

After the refactor, a reader should understand that:

```text
OKF
    describes portable knowledge

MCP
    provides agent/tool communication

Basic Memory / OpenMemory / Obsidian / GitHub / Drive
    may own or provide knowledge

ThoughtMesh
    maps these things into one logical mesh
```

ThoughtMesh's value is the connective layer.

Do not retain old specification material merely because it already exists.

Prefer deleting, simplifying or replacing concepts that duplicate mature external standards.
