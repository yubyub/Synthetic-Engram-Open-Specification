# Conformance

This document is the testable companion to `SPEC.md`. In a conflict, `SPEC.md`
wins. Package feature declarations and implementation claims are deliberately
separate: `engram.json#profiles` describes package contents, while a capability
document describes implementation roles.

## Outcomes and claims

A test harness supplies a package, a claimed role, and a profile. **Process**
means validate and expose the profile's normative semantics. **Preserve** means
write its normative values and relationships without loss (and bytes where the
specification says byte-for-byte). **Reject** means return no successful or
complete result. **Report unsupported** means a distinct machine-readable
failure naming every unsupported declared profile before dependent data is
processed. Logs and warnings do not qualify.

Public compatibility claims MUST provide a document validated by
`schemas/v0.1/capabilities.schema.json`. Claims are per profile and may contain
`producer`, `consumer`, or `round-trip`; the latter entails both other roles.
The `core` package declaration never implies that an implementation supports
both import and export.

## Profile test matrix

| Profile | Producer assertions | Consumer assertions | Round-trip assertions |
| --- | --- | --- | --- |
| `core` | Manifest/records validate; inventory is safe and complete; IDs, timestamps, hierarchy, and links satisfy cross-file rules. | Validate all producer invariants; resolve internal references; expose core fields and Markdown; reject invalid input. | Revalidate output; compare identity, Markdown, hierarchy, links, timestamps, inventory, and extension values. |
| `graph` | Declaration is present; graph schema, local ID uniqueness, endpoints, and non-external references validate. | Expose topology, labels, and references; reject violations or report `graph` unsupported. | Revalidate and compare every node, edge, label, reference, and extension value. |
| `media` | Declaration is present; metadata/blob inventory pairing, ID, path, media type, size, digest, and attachment URI validate. | Resolve URI by ID and verify payload, size, digest, and pairing; reject violations or report `media` unsupported. | Revalidate; compare payload bytes, identity, metadata, and URI targets. |
| `action` | Declaration is present; actions have valid status and optional UTC due instant; other types have neither action field. | Expose status/due instant with Section 7 meanings and no invented transition restrictions; reject violations or report `action` unsupported. | Revalidate and compare type, status, due instant, and extension values. |

A consumer presented with multiple unsupported declarations MUST report all of
them. A preservation-mode round trip may accept an unsupported optional profile
only if its objects, inventory entries, and declaration survive; its inventoried
files must be byte-identical and the result must say "preserved", not
"processed".

## Repository fixtures

`tests/conformance/cases.json` is the machine-readable fixture index. It has one
producer, consumer, and round-trip case for every profile. Producer cases name a
package that must validate. Consumer cases state the observable requirements
and unsupported-profile result. Round-trip cases list values or files that must
be preserved. `tests/conformance/capabilities.json` is a capability-document
fixture covering independent roles.

Run `python scripts/validate.py`. It validates the example, all valid and invalid
packages, the capability document, every indexed conformance package, the
profile/role coverage, and each fixture's declared preservation paths.
This document translates the normative rules in `SPEC.md` into a reviewable
checklist. In a conflict, `SPEC.md` wins.

Normative clauses have stable `REQ-*` identifiers. See the complete
[requirement-to-test matrix](traceability.md) and the
[machine-readable requirement catalog](requirements.json).

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
they fail for the intended reason. The suite also checks catalog/traceability
coverage and the structure of the consumer and round-trip vectors in
`tests/vectors`. Unlike producer fixtures, vectors name an operation and an
observable `expected` result so implementations can report behavioral evidence.
they fail for the intended reason. `complete-omits-durable-object` proves a package cannot claim a complete backup while leaving a durable object out of its inventory.
