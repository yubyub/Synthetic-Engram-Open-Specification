# Conformance

This document translates the normative rules in `SPEC.md` into a reviewable
checklist. In a conflict, `SPEC.md` wins.

## Package checks

- `engram.json` exists and validates against the v0.1 manifest schema.
- Every inventory path is safe, unique, and exists.
- Every normative object appears in the inventory.
- Object IDs are unique and agree with their inventory entries.
- Every included optional object type has its corresponding declared profile.
- Parsers are selected from inventory media types, never filename extensions.
- Every record media type is `text/markdown`; non-Markdown structured records
  are not part of the 1.0 core.
- Unsupported inventoried media types are reported, and a processor claiming
  round-trip preservation retains their inventory fields and bytes unchanged.

## Reference checks

- Non-external links and parents resolve.
- Parent relationships are acyclic.
- Graph node references resolve unless explicitly external.
- Graph edge endpoints resolve to nodes in the same graph.

## Media checks

- Attachment metadata and payload both exist in the inventory.
- Payload byte size and SHA-256 digest match the metadata.
- Attachment URIs refer to attachment IDs rather than package paths.

## Repository fixtures

Run `python scripts/validate.py`. It validates the complete example and every
fixture in `tests/valid`, then asserts that every fixture in `tests/invalid` is
rejected. Invalid fixtures contain an `expected-error.txt` substring to ensure
they fail for the intended reason.
