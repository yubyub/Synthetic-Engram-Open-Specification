# Conformance

This document translates the normative rules in `SPEC.md` into a reviewable
checklist. In a conflict, `SPEC.md` wins.

## Package checks

- `engram.json` exists and validates against the v0.1 manifest schema.
- Every inventory path is safe, unique, and exists.
- Every normative object appears in the inventory.
- Object IDs are unique and agree with their inventory entries.
- Every included optional object type has its corresponding declared profile.

## Reference checks

- Non-external links and parents resolve.
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
they fail for the intended reason.
