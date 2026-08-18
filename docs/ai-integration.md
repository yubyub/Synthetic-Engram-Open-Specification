# AI and retrieval integration

This non-normative guide describes how an AI-enabled application can use a
Synthetic Engram without turning Core 1.0 into a model-memory or retrieval
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
