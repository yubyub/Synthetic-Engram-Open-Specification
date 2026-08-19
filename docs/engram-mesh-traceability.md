# Engram Mesh 0.3 requirement traceability

This matrix separates rules that a static document validator can prove from
runtime and lifecycle obligations that require adapter or application evidence.
Passing the repository validator is therefore document conformance evidence,
not proof of safe source access or full implementation conformance.

| Requirement family | Automated evidence | Additional evidence required |
| --- | --- | --- |
| `REQ-SER-*`, `REQ-MESH-*` | JSON/schema checks, duplicate-key rejection, ID syntax and global uniqueness | Persistence of `mesh_id` across exports |
| `REQ-SEP-*` | Derived operational state is absent from closed core objects | Architecture review showing storage, indexing, authority, and export are not conflated |
| `REQ-NODE-001`, `REQ-NODE-002` | ID uniqueness and shape | Durable mapping records showing IDs are not derived only from mutable source attributes |
| `REQ-NODE-003`, `REQ-NODE-004` | Source-move fixture covers one successor case | Move, merge, split, and deduplication tests against a real Source |
| `REQ-SOURCE-001`, `REQ-SOURCE-002` | Source identity-domain presence and unique ID | Provider-specific identity-domain documentation |
| `REQ-SOURCE-003`, `REQ-SOURCE-004` | Closed resolver shape and common credential-pattern rejection | Secret scanning and disclosure review; static heuristics cannot prove a locator is safe |
| `REQ-BIND-001`–`REQ-BIND-007` | Endpoint, generation, state, successor, freshness, capability, and single-authority checks | Idempotent discovery, external-ID reuse, deletion evidence, and atomic authority transition tests |
| `REQ-CAP-*` | Namespaced names and binding-subset checks | Per-operation authentication, authorization, precondition, and no-elevation tests |
| `REQ-REL-*`, `REQ-HIER-*` | Endpoint resolution, direction retention by round trip, single parent, and cycle rejection | Application interpretation of custom relationship types |
| `REQ-SLICE-001`–`REQ-SLICE-004` | Entity closure, complete-snapshot and full-inclusion checks, boundary disposition/privacy checks | Authorization-aware selection showing undisclosed identities are not leaked |
| `REQ-SLICE-005`, `REQ-SLICE-006` | None: external resolution is outside the canonical document | Integration tests showing complete slices do not fetch bound content and passive operations never invoke a resolver |
| `REQ-LENS-*` | Mechanism, version, and expression presence | Unsupported-mechanism reporting and proof that evaluation does not mutate membership or authority |
| `REQ-PORT-*` | Closed core objects and namespaced extensions | Recipient-specific disclosure review and unknown-extension round-trip tests |
| `REQ-OKF-*` | None in core validation | Independent OKF validation, stable-ID mapping, and declared-loss report |
| `REQ-MCP-*` | None in core validation | Protocol-specific conformance performed separately, if MCP is used |
| `REQ-SEC-001`, `REQ-SEC-002` | Resource limit and non-executing JSON parser | Resolver sandbox, network/filesystem boundary, and hostile-content tests |
| `REQ-SEC-003`–`REQ-SEC-005` | ID-free `undisclosed` boundary enforcement | Object-level disclosure and mutation authorization tests; tests that hints cannot trigger plugin loading, connections, or fetches |

The expected-diagnostic files under `tests/v0.3/invalid` prevent a negative
fixture from passing because of an unrelated error. New normative requirements
should add automated evidence where static validation is possible and identify
the required manual or integration evidence otherwise.
