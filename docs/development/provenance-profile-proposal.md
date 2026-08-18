# Provenance profile exploration and PROV-O mapping

**Status:** non-normative exploration; no profile name or wire representation is
standardized

## Interoperability problem

Core timestamps do not say who authored knowledge, whether a model generated it,
which sources or transformation produced it, whether a human adopted it, or what
was corrected. These distinctions matter to human–AI knowledge systems but do not
require a full revision or synchronization model.

## Minimum conceptual model

| Concept | Required portable meaning | PROV-O analogue |
| --- | --- | --- |
| Knowledge entity | The durable record, graph, or attachment identified by its Engram ID | `prov:Entity` |
| Agent | Person, organization, software, or model associated with an activity | `prov:Agent` |
| Activity | Authorship, generation, derivation, correction, or adoption event | `prov:Activity` |
| Attribution | Agent responsible for an entity or activity in a stated role | `prov:wasAttributedTo`, qualified association |
| Generation | Activity produced the current durable entity | `prov:wasGeneratedBy` |
| Derivation | Entity used one or more source entities with a stated transformation | `prov:wasDerivedFrom`, `prov:used` |
| Adoption | A human or policy accepted generated/derived material as durable knowledge | qualified activity and association |
| Correction | Current entity corrects another identified entity without implying deletion | specialization/derivation plus a typed activity |

Every source inside the Engram uses its stable object ID and explicit membership
scope. External sources use typed URIs or future Source Reference objects as
explored in [`source-reference-profile-proposal.md`](source-reference-profile-proposal.md);
fetching is never implied. A derivation declares activity type, responsible agent when
known, time when known, source IDs, transformation description or identifier,
and whether content was omitted, summarized, split, merged, or otherwise lossy.

Authored, generated, derived, corrected, and adopted are not mutually exclusive
record types. They describe activities and responsibility. Human adoption does
not erase model generation, and correction does not rewrite historical source
identity.

## Mapping and loss

Export to PROV-O maps Engram objects to entities and retains Engram IDs as source
identifiers. Activities and agents need stable identifiers in the future profile;
blank nodes would prevent reliable round trips. Roles, authorization decisions,
model prompts, confidence, and signatures have no automatic mapping.

Import from arbitrary PROV-O is normally lossy: bundles, collections,
specialization, delegation, alternate entities, plans, dictionaries, and complex
qualified relations exceed this minimum model. The adapter must list omitted or
collapsed relations and must not infer authorship from file ownership or package
possession.

## Threat model and acceptance gate

Provenance assertions can expose identities, prompts, private sources, locations,
and organizational relationships; they can also falsely imply authority. Treat
agents and source URIs as untrusted claims, apply disclosure authorization to the
entire relation, avoid automatic URL fetching, and distinguish integrity from
authenticity. Signatures remain a separate binding.

Source Reference and provenance remain separate profiles: the former identifies
external knowledge and its portable context; the latter describes activities,
agents, derivation, and responsibility. A reference can exist without any
derivation, and provenance may refer entirely to Engram-native objects.

The next step is pilot-backed field design under
[`profile-governance.md`](../profile-governance.md). No schema is published until
two consumers agree on the minimum model, privacy behavior, identifier rules, and
round-trip fixtures.
