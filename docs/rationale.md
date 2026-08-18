# Design rationale

> This document is non-normative. [`SPEC.md`](../SPEC.md) and its referenced
> schemas are the sources of format requirements.

## Why this exists

Synthetic Engram separates durable, owner-controlled knowledge from the
application that currently stores or presents it. The interchange layer is
intended for human-facing knowledge tools, graph and task tools, backup tools,
and AI systems. It is not itself a database, user interface, search engine,
agent protocol, or synchronization service.

Core 0.2 deliberately stays small: an explicit package inventory, stable
identities, typed Markdown records, scoped links, optional graph topology,
attachments, and namespaced extensions. Live storage and retrieval remain
application concerns.

## Main design choices

- Stable IDs, rather than titles, filenames, paths, or database keys, identify
  durable knowledge.
- A package is one serialized export; `engram_id`, `export_id`, and package
  `id` distinguish the enduring knowledge base, export event, and physical
  package instance.
- Explicit complete/partial scope avoids pretending that a selected view is a
  full backup.
- Declared profiles let a consumer reject capabilities it cannot safely
  process instead of silently losing governed data.
- Markdown keeps narrative content accessible to humans and common tools;
  restricted YAML provides a readable structured envelope.
- Graphs and attachments are optional profiles so a simple notes consumer does
  not need to implement every feature.
- Extensions retain application-specific data without allowing it to redefine
  core fields.
- External access and portable context are separate concerns. A connector may
  retrieve source bytes, while a future Source Reference profile preserves only
  the owner-adopted identity, relationships, observations, and materialization
  state needed to understand that source across applications.

## Boundaries

Core 0.2 exports current state. It does not standardize revision history,
conflict resolution, synchronization, provenance chains, authentication,
authorization, encryption, canonical archive serialization, retrieval ranking,
or a live AI tool API. Those features should only enter the specification after
pilot evidence shows a portable contract is needed and at least two consumers
can implement it consistently.

Core 0.2 also does not standardize external-source objects. Its
`outside_engram` scope expresses membership, not source identity or resolution.
The [Source Reference exploration](development/source-reference-profile-proposal.md)
keeps provider-specific resolvers and credentials outside the portable model and
requires a new minor schema line before any profile can become normative.

An adapter is not a lossless migration merely because it can read and write a
package. A preservation claim requires a round trip that retains the
information and semantics claimed by that adapter.

## Pilot posture

The 0.2 line is suitable for controlled application pilots and format
experiments. It is expected to change after real use. Stable 1.0 should wait for
real application round trips, independently maintained implementation evidence,
a hosted and immutable schema release, and resolution of material feedback
captured through the public issue tracker.
