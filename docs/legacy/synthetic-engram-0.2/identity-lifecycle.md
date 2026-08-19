# Identity mapping and package lifecycle

This guide is non-normative. Core identity requirements remain in `SPEC.md`.

## Native identity maps

Importers should maintain an application-local mapping from a source-system
namespace and native identifier (UUID, URI, database key, or other stable key) to
an Engram object ID. The namespace is part of the key; `123` from two systems is
not one identity. Store the map transactionally with imported objects and reuse
it on re-import. Do not derive identity from a title, path, or mutable type.

Core 0.2 has no alias field. An implementation may retain mappings in its live
store or a documented namespaced extension. A round trip must not invent aliases
or claim that an external URI and Engram ID are globally equivalent without an
explicit mapping policy.

On collision—two logical source objects resolving to one Engram ID—stop and
report both source keys. Never merge automatically. Likewise, one source key
must not silently map to multiple current objects.

## Three package identities

| Event | Engram ID | Export ID | Package ID | Durable object IDs |
| --- | --- | --- | --- | --- |
| First export | new | new | new | new or reused from an established map |
| Retry of one logical export | retain | retain | new | retain |
| Repack the same export bytes/model | retain | retain | new | retain |
| Later snapshot | retain | new | new | retain for continuing objects |
| Partial export | retain | new | new | retain selected object IDs |
| Re-export by another implementation | retain when logical continuity is known | new | new | retain imported object IDs |

A retry repeats one export event after an operational failure. A later snapshot
observes the source again and therefore creates a new export event even when no
logical data changed. Repacking changes serialization and always creates a new
package instance.

Logs should record all three IDs, source snapshot/cursor when available, producer
version, completeness, selection description, and the native-ID map version.
Deduplicate retries by Export ID, not Package ID; verify contents rather than
assuming equal Export IDs imply equal bytes.

## Reclassification, merge, and split

- Reclassifying a continuing logical record retains its ID. The prefix records
  its originally assigned kind hint and is not rewritten merely because a note
  becomes a project or action. Record the semantic change outside Core history.
- For a merge, choose a surviving logical object deliberately. Retain its ID,
  retire the other IDs without reassigning them, and redirect native aliases only
  under an explicit application policy. Report merged meaning as loss because
  Core 0.2 has no tombstones or merge history.
- For a split, retain the old ID for at most one result with clear continuity and
  issue new IDs for the others. If no result has primary continuity, retire the
  old ID and issue new IDs for every result. Never reuse the retired ID later.

## URI identity

Treat a URI as a native identifier only when its authority and persistence policy
are known. Retrieval location, citation, and object identity are separate. A URL
change need not change an Engram ID; two URLs are not automatically aliases.

[`tests/lifecycle/cases.json`](../../../tests/lifecycle/cases.json) makes these decisions
executable in the repository implementations. It is guidance evidence, not a
history, synchronization, alias, or global-identifier profile.
