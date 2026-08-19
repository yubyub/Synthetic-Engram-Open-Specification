# Source adapter contract

This guide defines the minimum behavior expected from a usable Engram Mesh 0.3
Source adapter. It is non-normative where it discusses implementation technique;
the linked `REQ-*` rules in the specification remain authoritative.

## Durable mapping state

An adapter must maintain this association outside the portable document:

```text
source identity domain
  + external ID
  + object generation
        ↕
Engram Mesh Node ID and Binding ID
```

The mapping must survive process restarts, retries, path moves, and repeated
imports. Titles, paths, URLs, and content hashes can be evidence but are not by
themselves logical identity.

## Discovery algorithm

For every source object visible to the authorized caller:

1. Determine the Source identity domain and stable external ID.
2. Obtain a provider generation/version identifier when the provider can reuse
   IDs. Otherwise create and persist an adapter generation token.
3. Reuse the mapped Node and Binding only when continuity is established.
4. If the same logical object has a changed external ID, supersede the old
   Binding and create a successor for the same Node.
5. If an external ID is reused for a new logical object, create a new generation,
   Binding, and Node.
6. Record `deleted` only from authoritative deletion evidence. A timeout,
   offline source, or permission failure is not deletion.

Discovery must be idempotent: repeating it against the same source snapshot
must not mint new IDs or change authority.

## Resolution outcomes

A runtime resolver should distinguish:

- resolved;
- temporarily unavailable;
- not found with authoritative evidence;
- unsupported source or resolver mechanism; and
- not authorized.

These outcomes do not delete the Node or its relationships. A service should
avoid disclosing whether an unauthorized object exists; a portable slice uses
an ID-free `undisclosed` boundary entry.

## Authority rules

At most one active Binding can be `authoritative` for a Node. Other active
bindings are `replica` or `reference`. An authority transition should be one
atomic application operation:

1. verify the destination object and expected revision;
2. mark the prior Binding `replica`, `reference`, or `superseded`;
3. mark the destination Binding `authoritative`; and
4. record application audit evidence outside the portable core.

If two authorities are observed, stop and report a conflict. Array order,
freshness timestamps, or last-writer-wins behavior must not resolve it silently.

## Capabilities and authorization

Source capabilities describe adapter support. Binding capabilities can only
restrict that set. Before every read or mutation, the adapter must authenticate
the caller, authorize the specific object and operation, enforce source
preconditions, and validate freshness/conflict tokens.

`modify`, `move`, and `delete` should require explicit application intent.
Possession of `engram-mesh.json`, a Mesh Slice, a resolver hint, or an earlier
successful read is never authorization.

## Freshness

Freshness evidence contains `observed_at` plus a revision, digest, or opaque
source token. It says what state was observed and when; it is not a universal
guarantee that the object is current now. Before mutation, compare the recorded
evidence with the Source and fail on conflict unless the calling application
has an explicit conflict policy.

## Adapter test checklist

- repeated discovery preserves IDs;
- path move preserves the Node and creates or updates the correct Binding;
- external-ID reuse creates a new generation and Node;
- timeout and permission denial do not become deletion;
- multiple authority is rejected;
- binding capabilities cannot exceed source support;
- caller authorization is checked on every operation;
- stale mutation is rejected;
- resolver configuration emits no credentials; and
- partial export preserves authority and privacy-safe boundary states.
