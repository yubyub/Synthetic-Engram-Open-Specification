# Normative version and support policy

This document is normative. BCP 14 requirement words have the meanings
established by `SPEC.md`.

## Pre-stable releases

Synthetic Engram uses Semantic Versioning, with the additional explicit policy
that every `0.x` minor line is a potentially breaking pilot version.

- A patch within `0.2.x` MUST NOT change accepted package bytes or normative
  semantics. It may correct prose, tooling, or tests that enforce an existing
  unambiguous rule.
- A new `0.x` minor may change schemas, semantics, identifiers, profiles, or
  serialization. It MUST use a new schema directory and URI and document the
  change.
- Version 1.0 will mark the first stable compatibility commitment.

The manifest `version` identifies the specification release. Object
`schema_version` identifies its major/minor schema line.

## Consumer negotiation

A consumer MUST inspect the manifest version before processing content.

- It MAY process supported patches in the same major/minor line.
- It MUST reject an unsupported 0.x minor or major with a non-success result and
  MUST NOT silently reinterpret the package.
- It MUST process every declared profile required for the requested operation or
  report the profile/capability as unsupported.
- A partial operation MAY be offered only when skipped content and limitations
  are reported explicitly.

No implicit migration from 0.1 or from a future 0.x line is defined.

## Extensions

Extension keys use reverse-DNS namespaces. Producers MUST NOT emit two meanings
for one key. Consumers MUST report namespace collisions rather than merge them.
A round-trip processor claiming preservation MUST retain unknown keys and values
with deep structural equality and SHOULD retain original bytes when possible.

Promoting an extension into core requires documented semantics, compatibility
and security analysis, examples, fixtures, migration behavior, and implementation
evidence. The original namespaced key remains owned by its namespace controller.

## Tagged releases and schemas

A tagged release is historical evidence and MUST NOT be silently rewritten.
Hosted schema bytes for that tag must match the repository tag. Before the first
public tag, schema URLs are publication targets rather than evidence that a
release is already deployed.

The project currently promises support only for the active pilot line. A stable
support window will be defined before 1.0.
