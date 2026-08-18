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
