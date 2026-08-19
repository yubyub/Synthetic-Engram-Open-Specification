# Engram Mesh version policy

This policy covers versioning for the Engram Mesh draft.

## Draft and release identifiers

`0.3.0` identifies the current pilot line. It defines the `engram-mesh.json`
serialization and `schemas/v0.3/` schema set, but remains free to make breaking
minor-line changes before 1.0. A stable release requires independent adapters
and compatibility evidence.

Tagged releases are historical evidence and must not be silently rewritten.

## Serialization and future schema URIs

Engram Mesh 0.3 uses a canonical `engram-mesh.json` document with JSON Schemas
under `schemas/v0.3/`. The pilot schemas deliberately omit `$id` rather than
claiming an unowned or mutable public URL. A public release should add final
tag-addressed immutable schema IDs only after their bytes resolve at those URLs.

A new serialization must carry its own format identifier and specification
version. It must not reuse an existing format identifier, schema ID, or
conformance claim with changed semantics.
