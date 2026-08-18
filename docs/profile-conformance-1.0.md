# 1.0 role and profile conformance matrix

Every row is exercised by the versioned vectors in `tests/v1.0/vectors` and by
both implementations. A full consumer must process every declared profile or
return a non-success result naming the unsupported profile.

| Profile | Producer | Consumer | Round trip |
|---|---|---|---|
| core | Emit valid manifest/records, inventory, identities, and references | Validate and resolve core objects; reject unsupported major | Preserve IDs, Markdown bytes, inventory, and extensions |
| graph | Declare `graph`; emit valid topology | Resolve node bindings and edge endpoints | Preserve all nodes, edges, bindings, and extensions |
| media | Declare `media`; emit descriptor and payload | Verify size/hash and resolve attachment IDs | Preserve descriptors and exact payload bytes |
| action | Declare `action`; emit required action status | Process action status and optional due date | Preserve action fields and record content |

Fixtures cover all eight legal combinations of the three optional profiles:
`core` alone and `core` plus every subset of `graph`, `media`, and `action`.
