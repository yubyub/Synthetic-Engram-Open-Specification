# Engram Mesh version and legacy policy

This policy explains how the Engram Mesh draft coexists with the earlier
Synthetic Engram package specification.

## Lines and locations

| Line | Location | Status |
| --- | --- | --- |
| Synthetic Engram 0.2 | `docs/legacy/synthetic-engram-0.2/SPEC.md`, `schemas/v0.2`, `examples/v0.2`, `tests/v0.2` | Preserved legacy pilot contract |
| Engram Mesh 0.3 | root `SPEC.md`, `schemas/v0.3` | Implementable pilot contract |

The repository root always points to the current Engram Mesh specification.
Legacy normative prose and its requirement catalog are colocated under the
legacy reference directory.

## Compatibility

Engram Mesh 0.3 is intentionally incompatible with Synthetic Engram 0.2. A
Synthetic Engram package is not an Engram Mesh representation, and an Engram Mesh
prototype does not satisfy the 0.2 package contract merely because it can import
or export some of the same knowledge.

No implicit migration is defined. Because no external users or implementations
are known, 0.3 makes a clean incompatible break rather than maintaining a
misleading wire-compatibility layer. A future optional adapter must report how records,
graphs, attachments, profiles, package completeness, stable IDs, and extension
data are preserved, transformed, or lost.

## Draft and release identifiers

`0.3.0` identifies the current pilot line. It defines the `engram-mesh.json`
serialization and `schemas/v0.3/` schema set, but remains free to make breaking
minor-line changes before 1.0. A stable release requires independent adapters
and compatibility evidence.

Tagged releases are historical evidence and must not be silently rewritten.
The existing 0.2 paths and any tag-addressed schema bytes retain their Synthetic
Engram meaning.

## Serialization and future schema URIs

Engram Mesh 0.3 uses a canonical `engram-mesh.json` document with JSON Schemas
under `schemas/v0.3/`. The pilot schemas deliberately omit `$id` rather than
claiming an unowned or mutable public URL. A public release should add final
tag-addressed immutable schema IDs only after their bytes resolve at those URLs.

A new serialization must carry its own format identifier and specification
version. It must not reuse `synthetic-engram`, `engram.json`, 0.2 schema IDs, or
0.2 conformance claims with changed semantics.
