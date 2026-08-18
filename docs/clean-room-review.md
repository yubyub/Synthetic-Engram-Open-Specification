# Clean-room normative-text review

## Method

A reviewer ignored the validator implementation, examples, schemas, and
non-normative design documents while first writing the pseudocode below from
`SPEC.md` alone. Only after recording questions did the reviewer compare the
result with every `schemas/v0.1/*.schema.json` file, `requirements.json`, and
`traceability.md`. The review covers the full specification, beginning with
Sections 6.1, 7, 8, and 9 as requested.

```text
read engram.json as unique-key UTF-8 JSON; validate manifest schema
for each inventory entry:
    reject unsafe or repeated paths; require file
    parse by kind; validate its schema; compare object ID
apply completeness/partial conditional and declared-profile checks
for every parent, link target, and graph-node record:
    scope = context scope field or synthetic_engram
    if complete and scope == synthetic_engram: require inventoried target
reject cycles among included parent relations
for each graph: require unique node IDs, unique edge IDs, local endpoints
for each attachment: match its blob entry/path, then size and SHA-256
for Markdown links/images with engram-attachment scheme: resolve by ID
apply extension, version, conformance-role, and security requirements
```

## Ambiguity log and disposition

| Area | Ambiguity found using normative text alone | Disposition |
|---|---|---|
| Package absence vs Engram membership | The former `external` Boolean conflated selection absence and membership. | Resolved in REQ-SCOPE-004: the three context scope fields express membership; inventory presence expresses package absence. |
| Missing references | Record and graph sections previously stated different resolution rules. | Resolved by one authoritative REQ-REF-001, linked from the graph section. |
| Parent cycles | Duplicate clauses differed on whether only included parents were considered. | Resolved by REQ-REF-002: cycle detection is over included records. |
| Graph identifiers | Duplicate prose did not say separately whether node IDs and edge IDs shared a namespace. | Resolved by REQ-GRAPH-001 and REQ-GRAPH-002: each collection has its own uniqueness constraint. |
| Edge endpoints | Schema shape alone could not ensure endpoint existence. | Resolved explicitly by REQ-GRAPH-003. |
| Attachment URI | The URI and consumer rule appeared twice, and “embedded path” was unclear. | Consolidated in REQ-MEDIA-003; discovery is independently specified by REQ-MEDIA-004. |
| Attachment blob pairing | “Both listed” did not fully identify the correct blob entry. | REQ-MEDIA-002 now fixes kind, repeated attachment ID, and payload path. |
| Manifest identity fields | Section 6's descriptive list sounded required, while the v0.1 manifest schema does not require `engram_id`, `export_id`, or `completeness`. | Left descriptive rather than made a new normative requirement; schema conformance is authoritative for v0.1. A future version may make them required without silently changing v0.1 valid data. |
| Default completeness | Resolution needs complete/partial behavior when `completeness` is absent, but neither normative text nor schema defines a default. | **Open ambiguity:** implementations cannot infer a portable completeness claim. They can perform schema and internal checks, but source-closure claims require an explicit value. |
| Reference target kind | REQ-REF-001 says “inventoried object”; the schemas constrain ID shape but not whether parents/links/graph records must resolve to records. | **Open ambiguity:** resolution by ID is interoperable, but target-kind validation is not specified. |
| Media type agreement | Inventory and attachment metadata each contain a media type, but no normative equality rule exists. | **Open ambiguity:** validate both syntactically; do not infer that equality is required. |
| Markdown dialect | Attachment discovery depends on links/images while v0.1 selects no dialect. | Intentionally implementation-defined; REQ-MEDIA-004 fixes what constructs qualify once a dialect is selected. |
| YAML numeric range | “JSON-number syntax” does not define implementation precision or overflow handling beyond excluding non-finite values. | **Open ambiguity:** preserve a finite JSON-compatible value; exact arbitrary-precision behavior is not mandated. |
| Resource limits | REQ-SEC-002 requires limits but gives no minima or configuration model. | **Open ambiguity:** conformance can observe that configured limits are enforced, not compare universal thresholds. |
| Complete snapshot proof | A consumer cannot detect deliberately undisclosed source objects. | Explicitly bounded by REQ-CLOSE-005: producer comparison is required; consumers verify only package evidence. |

## Cross-artifact result

Every `REQ-*` definition occurs once in `SPEC.md`, every ID occurs once in the
machine catalog, and every catalog ID appears in `traceability.md`. Schema-backed
requirements name their schema evidence in the matrix. Cross-file or behavioral
requirements name validator assertions, fixtures, vectors, or a manual review.
The remaining open ambiguities above are recorded rather than filled with
implementation-specific assumptions.
