# Namespaced profile negotiation exploration

**Status:** non-normative compatibility proposal; Core 1.0 is unchanged

## Problem

The Core 1.0 manifest enumerates `core`, `graph`, `media`, and `action`. This makes
processing obligations clear but cannot name third-party profiles, and it has no
place for advisory metadata that may be ignored safely.

## Proposed semantic separation

A future version should distinguish:

- **required profiles:** every profile needed to interpret requested package
  content; an unsupported identifier prevents a full successful operation; and
- **advisory declarations:** namespaced hints that may be ignored without
  changing the portable meaning of core or required-profile content.

Third-party identifiers use the existing reverse-DNS ownership principle plus a
profile-local name and version. Exact syntax remains decision-blocked until
prototype manifests and registry/collision analysis exist. `core` remains the
baseline capability for its major version.

## Required behavior

A consumer discovers package version and declarations before processing. It
reports every unsupported required identifier with a non-success result, may
offer an explicitly partial operation, and never relabels that operation as a
full import. Unknown advisory declarations are retained by preservation-capable
round trips and may produce warnings, but do not cause failure by themselves.

Identifiers are opaque and compared exactly after schema validation. Consumers
do not fetch code or schemas automatically, guess compatible versions, merge
colliding definitions, or reinterpret an unknown profile from a similar name.
Namespace ownership, definition discovery, offline behavior, and definition
immutability require an approved decision before release.

## Compatibility matrix

Tests must cover old consumer/new package, new consumer/old package, supported
and unsupported required profiles, unknown advisory declarations, mixed
declarations, partial operations, preservation round trips, collisions, and
newer-minor behavior. Current v1.0 consumers and schemas remain valid for v1.0
bytes and are not silently taught new meanings.

The proposal advances only with a versioning classification, immutable new
schema URI, migration guide, security review, complete fixtures, and two
independent implementations under profile governance.
