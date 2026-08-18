# Related standards

This document is non-normative. Synthetic Engram is an interchange model, not a
replacement for transport, authentication, or application protocols.
Implementations should reuse established standards, including RFC 3339 for
timestamps, ULID for sortable identifiers, JSON Schema for validation, YAML for
record metadata, Markdown for textual content, and standard media types for
attachments.

Adapters to agent-memory formats, tool protocols, note formats, and graph
formats should document whether mappings are lossless. Round trips should
preserve stable IDs, unknown extensions, unsupported inventoried objects, and
provenance whenever the adapter claims lossless behavior. Historical research
and candidate projects remain recorded in the [concept draft](concept-draft.md).
