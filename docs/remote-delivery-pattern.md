# Remote delivery pattern

**Status:** non-normative integration guidance; no endpoint, request schema, or
transport binding is standardized

A live Engram implementation can let a human interface or AI client discover a
broad structural view and retrieve only relevant durable content. Core 1.0
interoperability still begins with a conforming package; this pattern helps
implementations use consistent concepts without claiming mutually compatible
APIs.

## Conceptual operation sequence

```text
authenticate caller outside Engram
        |
discover service/version/profile capabilities
        |
read authorized manifest and object metadata overview
        |
list graphs or traverse an authorized graph neighborhood
        |
select stable object IDs
        |
retrieve record bodies or attachments by ID, preferably in a batch
        |
return source IDs, freshness token, omissions, and transformation/loss
        |
optionally materialize the authorized selection as a partial Engram Package
```

An implementation may expose these concepts through HTTP resources, RPC, a local
library, filesystem access, or MCP resources and tools. An MCP server might offer
capability and graph resources plus tools for ID lookup or bounded selection; an
HTTP service might expose analogous application routes. Those examples describe
roles only—names, paths, methods, parameters, response objects, status codes, and
pagination tokens remain application-specific.

## Operation vocabulary

- **Capability discovery:** service version, understood Engram versions,
  supported profiles, operation availability, and declared limits.
- **Overview:** authorized Engram identity, completeness context, profiles, object
  IDs/kinds, titles or other safe projections, and available graph IDs.
- **Object retrieval:** one or more durable objects by stable ID, with media type,
  source version/freshness, and explicit not-found versus not-authorized behavior
  that avoids unintended disclosure.
- **Graph traversal:** graph ID, starting nodes, direction, depth and result limit;
  returned nodes and edges retain Core IDs, direction, relation, and record scope.
- **Selection:** explicit filters or application search resulting in stable IDs
  and a declared selection description. Ranking remains implementation-local.
- **Attachment delivery:** metadata and authorized bytes with size, digest,
  content-disposition, and range behavior chosen by the host.
- **Partial-package delivery:** materialize selected authorized objects using Core
  partial-package completeness and reference-scope rules.

Every paged or cached result should expose an opaque freshness/version token and
stable continuation behavior or declare that the view changed. Errors should
separate invalid input, unsupported capability, limits, stale view, and internal
failure without leaking unauthorized object existence.

## Security and AI boundaries

Authenticate using the host environment and authorize every returned record,
edge, neighbor, attachment, and derived projection. Package owner metadata is not
permission. Treat record bodies, graph labels, links, and attachments as
untrusted data; they are not privileged prompts or executable tool instructions.

This pattern does not standardize semantic-search ranking, embeddings, chunks,
prompts, model context budgets, autonomous write policy, authentication methods,
authorization policy, synchronization, or conflict resolution. AI outputs become
durable knowledge only through an explicit adoption policy and should cite source
IDs and disclose transformation.

## Standardization gate

Working protocol prototypes remain blocked until at least two independently
implemented stores and two clients publish evidence that incompatible APIs cause
repeated integration cost. Only stable transport-neutral operations may then be
considered for a separate optional binding; HTTP and MCP representations require
their own threat models and interoperability reports.
