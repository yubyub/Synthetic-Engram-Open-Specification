# Source Reference profile exploration

**Status:** non-normative exploration; no profile name, object kind, or wire
representation is standardized

## Interoperability problem

People increasingly let AI and conventional applications reach knowledge held
in external services through connectors, plugins, APIs, local adapters, and MCP
servers. Those integrations can retrieve useful data without copying it into a
Synthetic Engram, but their source identity, selection, relationships, and
context are normally trapped in the integrating application.

Core 0.2 can say that a linked object is `outside_engram`, but the link carries
only an Engram-shaped target ID and a relation. It cannot portably identify the
external system or object, distinguish a dataset from a document, preserve an
observed version, describe how much content was materialized, or provide
resolver hints. A Markdown URL is human-readable but does not supply those
structured semantics.

A future Source Reference profile should make the **user-controlled contextual
layer** portable while allowing the referenced content to remain where it is.
An Engram may retain all, some, or none of that content.

## Boundary and terminology

Four concepts must remain distinct:

| Concept | Portable responsibility |
| --- | --- |
| Source Reference | Durable Engram object that identifies and describes external knowledge without containing it |
| Materialized object | Engram record or attachment containing an adopted snapshot, excerpt, summary, or other representation |
| Provenance relation | Assertion about how an Engram object was authored, observed, or derived from a source |
| Resolver | Implementation-specific component that accesses a source through a connector, MCP server, API, filesystem, or other mechanism |

A Source Reference is not a credential, authorization grant, live connection,
guarantee of availability, assertion of truth, or proof that the owner owns the
external content. It must remain meaningful when no compatible resolver is
installed, access has expired, the client is offline, or the source has moved.

The portable context is the owner's durable selection, labels, relationships,
annotations, source identities, observations, and adopted representations. It
does not include provider-owned indexes, hidden connector state, model-specific
ranking, credentials, or interpretations that were never exported or adopted.

## Minimum conceptual model

The following is a requirements inventory for pilots, not a proposed schema.

| Concept | Candidate portable meaning |
| --- | --- |
| Stable identity | An Engram ID for the Source Reference, retained independently of locators or titles |
| External subject | A typed URI or a namespace plus native identifier for the referenced external entity |
| Source system | The authority, service, repository, device, or application namespace in which the subject is identified |
| Granularity | Service, workspace, repository, dataset, collection, document, record, object, or application-defined resource |
| Display metadata | Optional human-readable title and description, treated as an observation rather than authoritative source content |
| Selection | Optional opaque description of a relevant subset or provider query; no universal query language is implied |
| Locators | Zero or more identity, access, or human-display locators, each explicitly typed by purpose |
| Resolver hint | Optional non-secret hint that helps an implementation choose a compatible resolver without prescribing it |
| Observation | Optional observation time and opaque revision, ETag, cursor, or digest, with its authority identified |
| Materialization | Whether no content, metadata, part of the content, or a snapshot has been adopted into inventoried Engram objects |
| Extensions | Namespaced provider- or domain-specific metadata that does not redefine common fields |

Stable subject identity and a current access locator are not necessarily the
same value. Pilots must not silently treat a mutable sharing URL, local path, or
provider UI URL as permanent identity. Multiple locators may describe one
subject, but equivalence must be asserted explicitly rather than inferred from
similar names.

## Relationships and graph participation

The role a source has belongs primarily to its relationship with another
object. The same dataset can be evidence for one record, background for a
project, the origin of an imported note, and the subject monitored by an action.
Pilots should test a small relation vocabulary such as `references`,
`derived_from`, `evidence_for`, `background_for`, `monitors`, and `materializes`,
using profile-specific extension data when common semantics have not been
demonstrated. Core 0.2's closed link schema and relation syntax remain unchanged.

Core 0.2 graph nodes can point only to records. A future profile should test
generalized graph references to any durable Engram object rather than requiring
every source, person, dataset, or later semantic object to masquerade as a note.
That change requires a new minor schema line and migration guidance.

## Completeness and materialization

A complete Engram export includes every current durable Source Reference,
owner-controlled contextual assertion, and adopted materialized object at the
export snapshot. It does **not** need to download the external subject.

Consequently:

- a referenced-only source can appear in a complete Engram package;
- copied content is normative only when adopted into an inventoried object;
- partial materialization must not be represented as a complete copy of the
  external source;
- an observed revision describes what the producer saw, not guaranteed current
  source state; and
- package `completeness` describes the bounded Engram snapshot, not all data
  reachable through its locators or resolvers.

The profile needs explicit, testable mappings between a Source Reference and
any materialized records or attachments. Provenance should identify derivation,
transformation, and loss; mere co-occurrence or matching titles are insufficient.

## Resolver boundary

Google Drive integrations, GitHub integrations, MCP servers, APIs, local
libraries, and future connector systems may all resolve the same conceptual
profile. The profile should standardize enough identity and metadata for a
resolver to recognize a source, but should not standardize connector discovery,
OAuth flows, tool names, API routes, query syntax, or refresh scheduling.

A live Engram service may offer source-reference listing, metadata inspection,
resolution, and authorized materialization operations. Results should retain
the Source Reference ID, expose freshness or observed-version information, and
report omissions and transformations. Resolution failure must not make an
otherwise valid portable reference invalid.

## Security and privacy

Source References introduce correlation and network risks even when they carry
no source content. Identifiers, titles, locators, selections, account names,
repository names, version tokens, and relationship topology may reveal private
activity or the existence of sensitive data.

Implementations must treat every locator and returned value as untrusted. They
should not fetch automatically during import, preview, validation, graph
traversal, or rendering. A resolver must authenticate and authorize through its
host environment, apply SSRF and redirect policy, constrain response sizes and
types, separate not-found from not-authorized without leaking existence, and
require explicit policy before adopting retrieved content.

Credentials, access tokens, cookies, refresh tokens, private keys, and
authorization grants must not be stored in Source References. A provider hint
must not be interpreted as permission or cause a plugin to execute merely
because its name appears in a package.

## Pilot and acceptance plan

Core 0.2 remains unchanged. Initial pilots may use a namespaced extension on a
record, with the limitation that such a record is only an experimental carrier
and not a standardized Source Reference object.

Candidate-profile work requires the evidence in
[`profile-governance.md`](../profile-governance.md), including at least two
independently maintained consumers. Fixtures should cover:

1. referenced-only, metadata-only, partial, and snapshot materialization;
2. offline and unsupported resolvers without data loss;
3. stable identity across changed or multiple locators;
4. opaque source versions becoming stale;
5. complete Engram packages whose external content is absent;
6. graph participation and relationship-role round trips;
7. malicious schemes, redirects, local-network targets, and oversized results;
8. rejection of credentials and authorization material;
9. privacy-preserving partial exports; and
10. mappings to provenance and at least two different connector technologies.

An accepted profile would require a new minor version, a new inventoried object
kind or equivalent profile mechanism, generalized graph-reference semantics,
schemas, migration rules, security review, conformance requirements, and
round-trip evidence. The exploration does not reserve a profile identifier.
