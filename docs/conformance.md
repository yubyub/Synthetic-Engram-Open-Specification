# Conformance

This document translates the normative rules in `SPEC.md` into a reviewable
checklist. In a conflict, `SPEC.md` wins.

## Package checks

- `engram.json` exists and validates against the v0.1 manifest schema.
- Every inventory path is safe, unique, and exists.
- Every normative object appears in the inventory.
- The Engram ID, package ID, object IDs, attachment IDs, and graph fragment IDs
  are unique across the Engram, except for the attachment/blob alias.
- Every semantic ID prefix agrees with its manifest kind or record/fragment
  type, and contained object IDs agree with their inventory entries.
- The owner descriptor has a stable opaque ID; no authority or authenticity is
  inferred from that attribution metadata.
- `id`, `engram_id`, and `export_id` identify the package instance, durable Engram, and export event.
- Partial packages supply selection metadata; complete packages close over every current durable source artifact.
- Object IDs are unique and agree with their inventory entries.
- Every included optional object type has its corresponding declared profile.
- Parsers are selected from inventory media types, never filename extensions.
- Every record media type is `text/markdown`; non-Markdown structured records
  are not part of the 1.0 core.
- Unsupported inventoried media types are reported, and a processor claiming
  round-trip preservation retains their inventory fields and bytes unchanged.

## Reference checks

- In a complete package, references scoped `synthetic_engram` resolve.
- A missing `synthetic_engram` target is external to a partial package; `outside_engram` means external to the Engram.
- Parent relationships are acyclic.
- Graph node references resolve unless explicitly external.
- Graph edge endpoints resolve to nodes in the same graph.
- Every graph declares `scope` as `curated` or `complete_records`.
- A `complete_records` graph references every inventoried record from at least
  one non-external node; a `curated` graph has no coverage requirement.
- Graph membership is not used to determine package inventory, and graph edges
  are not compared with authoritative record `parent` or `links` relationships.

## Media checks

- Attachment metadata and payload both exist in the inventory.
- Payload byte size and SHA-256 digest match the metadata.
- Attachment URIs refer to attachment IDs rather than package paths.

## Repository fixtures

Run `python scripts/validate.py`. It validates the complete example and every
fixture in `tests/valid`, then asserts that every fixture in `tests/invalid` is
rejected. Invalid fixtures contain an `expected-error.txt` substring to ensure
they fail for the intended reason. `complete-omits-durable-object` proves a package cannot claim a complete backup while leaving a durable object out of its inventory.
