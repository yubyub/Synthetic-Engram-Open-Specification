# Five-minute evaluator exercise

Use this exercise after reading the README and the role-specific guide relevant
to your work. It tests architectural boundaries, not memorization of field names.

## Questions

1. A hosted application stores records in SQL and graphs in a graph database.
   Must its tables match the Engram directory layout to conform?
2. Two web clients use one vendor's live HTTP API but never import or export a
   package. Does Core 1.0 make that API interoperable with another vendor?
3. An AI client reads graph structure, retrieves selected record bodies, and
   builds embeddings. Which parts are durable Engram knowledge?
4. Does an `owner` value or possession of a package grant access to its records?
5. Can a graph viewer implement only `core` and `graph` while declining `media`
   and `action`?
6. When is a package-native live store reasonable, and what must the application
   still provide?

## Answer rubric

1. **No.** Conformance is measured at the package boundary. The live store may
   use files, SQL, graph storage, object storage, or a service-specific model.
2. **No.** The clients share one application-specific API. Core 1.0 makes
   conforming packages interoperable; it does not standardize remote queries.
3. The records, stable IDs, declared relationships, graphs, and adopted
   attachments are durable knowledge. Embeddings, scores, chunks, and assembled
   model context are normally derived operational state. Derived results should
   retain source IDs.
4. **No.** Owner metadata and portability do not authenticate a caller or grant
   authorization, consent, encryption, or other privileges.
5. **Yes.** It must declare supported profiles, reject or explicitly report an
   unsupported required profile, and avoid claiming full consumption of content
   it did not process.
6. It is reasonable for a small, local, single-user, or write-light tool that
   deliberately chooses package-native operation. Transactions, atomic writes,
   indexes, concurrency, history, authorization, backups, and recovery remain
   application responsibilities.

A successful evaluator distinguishes all four pairs: package/live store,
knowledge/retrieval state, implementation/interface, and portability/authority.
