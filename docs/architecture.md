# Architecture and rationale

This document is non-normative. The standard separates a portable representation
from live storage. An application may use files, a relational database, a graph
database, or object storage internally, provided its declared import/export
behavior conforms to `SPEC.md`.

The v0.1 boundary deliberately favors a small lossless interchange core:

1. stable object identity;
2. human-readable records;
3. explicit relationships and inventory;
4. verifiable binary payloads; and
5. declared optional profiles.

Indexes, embeddings, caches, generated summaries, credentials, and runtime
policy are derivative or operational state and do not belong in the core
package. See the [original concept draft](concept-draft.md) for broader design
rationale and possible future capabilities.
