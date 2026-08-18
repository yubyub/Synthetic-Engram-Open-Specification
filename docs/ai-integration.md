# AI and retrieval integration

This non-normative guide describes how an AI-enabled application can use a
Synthetic Engram without turning Core 0.2 into a model-memory or retrieval
standard.

## Recommended boundary

```text
validated package or conforming store adapter
                    |
       application authorization policy
                    |
       selection and projection pipeline
                    |
       index / embeddings / graph search
                    |
        task-specific context assembly
                    |
                AI runtime
                    |
       proposed output with source IDs
                    |
       human review and explicit adoption
                    v
          durable Engram record update
```

Only the durable objects and portable semantics at the top and bottom are Engram
knowledge. Indexes, embeddings, scores, chunks, prompts, model context, and
unreviewed generations are normally derived operational state.

## Integration rules of thumb

1. Validate untrusted packages before indexing them.
2. Authenticate the caller and authorize every selected object outside the
   package format; ownership metadata and possession are not permission.
3. Project only the records and profiles needed for the task.
4. Preserve each source record ID and relevant attachment or relationship IDs in
   derived chunks so answers can cite durable knowledge.
5. Record which content was omitted, summarized, split, merged, or transformed.
6. Treat Markdown, links, attachments, and instructions inside knowledge as
   untrusted data, not privileged prompts or executable tool requests.
7. Keep embeddings, retrieval scores, and model-specific tokens out of durable
   core data unless a human or application deliberately adopts an artifact under
   a documented extension or future profile.
8. Require an explicit application policy—and usually human review—before model
   output overwrites or becomes durable owner-controlled knowledge.

## Graph-first context discovery

For a large knowledge base, give the client a bounded overview before sending
record bodies. It can inspect authorized manifest/object metadata and available
graphs, traverse a relevant neighborhood, then retrieve selected records and
attachments by stable ID. This supplies broad orientation without treating the
entire package as one prompt and lets later answers cite durable sources.

Graph topology is only one selection signal and may be incomplete or deliberately
authored for another purpose. Implementations should combine it with explicit
filters or application retrieval, enforce authorization at every traversal and
fetch, report omissions, and retain source IDs through projections. The
[remote delivery pattern](remote-delivery-pattern.md) names common operations
without defining a Core API.

## Recommended live-service discovery contract

A package already has a top-level discovery document: `engram.json`. A live
application needs an equivalent help operation so an AI client does not have to
guess endpoint names or retrieval order. Until a protocol binding is
standardized, applications SHOULD expose one read-only operation such as
`describe_capabilities` that returns:

- service and Synthetic Engram version information;
- supported profiles and operations;
- the caller's authorized scope;
- result-size and traversal limits;
- whether overview, graph, search, record, and attachment retrieval are
  available; and
- stable identifiers or links for the next permitted operations.

An AI-oriented client can then follow this default sequence:

1. call `describe_capabilities`;
2. obtain an authorized overview (the manifest/inventory equivalent);
3. inspect available top-level graphs when they are useful;
4. search or traverse within an explicit budget;
5. fetch selected records in batches by stable ID;
6. fetch attachments only when needed and permitted; and
7. retain source IDs and report omitted or transformed content.

This discovery operation is a strong candidate for a future HTTP, MCP, or local
library binding. It is guidance rather than Core 0.2 conformance: naming one
wire-level function now, before application pilots, would create a protocol
claim without interoperability evidence.

## Why Core should remain retrieval-agnostic

Retrieval quality depends on model, language, domain, latency, cost, privacy,
freshness, and task. Freezing chunk sizes, embedding models, ranking algorithms,
or context budgets into the portable knowledge model would make durable data
obsolete when runtime techniques change. Core should therefore preserve source
identity and meaning while applications choose their own retrieval layer.

A future optional projection profile would be justified only if independent
implementations need to exchange derived chunks or citations. Such a profile
should specify source identity, derivation, version, loss reporting, authorization
scope, freshness, and invalidation; it should not make one retrieval algorithm
normative.
