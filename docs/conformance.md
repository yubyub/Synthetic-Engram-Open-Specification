# Conformance

This document translates the normative rules in `SPEC.md` into a reviewable
checklist. In a conflict, `SPEC.md` wins.

Normative clauses have stable `REQ-*` identifiers. See the complete
[requirement-to-test matrix](traceability.md) and the
[machine-readable requirement catalog](requirements.json).

## Package checks

- `engram.json` exists and validates against the 0.2 manifest schema.
- Every inventory path is safe, unique, and exists.
- Every normative object appears in the inventory.
- `id`, `engram_id`, and `export_id` identify the package instance, durable Engram, and export event.
- Partial packages supply selection metadata; complete packages close over every current durable source artifact.
- Object IDs are unique and agree with their inventory entries.
- Every included optional object type has its corresponding declared profile.

## Reference checks

- In a complete package, references scoped `synthetic_engram` resolve.
- A missing `synthetic_engram` target is external to a partial package; `outside_engram` means external to the Engram.
- Consumers do not fetch or require the content of an `outside_engram` target to
  establish package validity or complete-export closure.
- Parent relationships are acyclic.
- Graph-node `record` references follow `record_scope`; complete-package `synthetic_engram` references resolve.
- Graph edge endpoints resolve to nodes in the same graph.

## Media checks

- Attachment metadata and payload both exist in the inventory.
- Payload byte size and SHA-256 digest match the metadata.
- Attachment URIs refer to attachment IDs rather than package paths.

## Producer snapshot and complete-export protocol

Package validation proves that the bytes in a package are internally valid. It
cannot, by itself, prove that a producer found every durable object in its
source. A producer claiming complete-export support MUST run the following
black-box protocol against each supported source-store kind. The fixture and
oracle are storage-neutral: an implementation may materialize them in files,
database rows, object-store keys, or another native representation.

### Source-state fixture

Create one isolated Engram, commit all fixture writes, and record a snapshot
boundary. Assign stable, unique identities to the durable logical objects and
retain their exact semantic payloads (and exact bytes for attachment payloads)
in an oracle that is independent of the producer. The snapshot MUST contain at
least:

| Fixture member | Minimum contents | Expected export treatment |
| --- | --- | --- |
| Durable records | Two records with different types, Markdown bodies, metadata, and a relationship between them | Both record identities, metadata, bodies, and relationships are normative |
| Durable graph | One graph with nodes, an edge, and a node referring to a fixture record | Graph identity and complete topology are normative |
| Durable attachment | Metadata plus a non-empty binary payload attached to a record | Metadata identity and payload bytes are normative |
| Durable extensions | Namespaced values on at least one manifest or object, including a nested JSON value | Extension names and values are normative |
| Storage-only record | A current durable record that exists only in database/object-store state and has no pre-existing package file | It MUST be synthesized into and inventoried in the export |
| Storage-only attachment | Current durable attachment metadata and bytes held only in database/object-store state | Its metadata and payload MUST be synthesized into and inventoried in the export |
| Operational artifacts | A cache entry, credential or access token, search index, lock, and temporary or unfinished-write value | None is a normative inventory object |

The operational artifacts SHOULD use distinctive sentinel identities and
payloads so accidental export is detectable. They MUST remain non-durable test
state: merely placing a sentinel beside durable state does not adopt it as
owner-controlled knowledge. Conversely, any derivative fixture deliberately
adopted as durable is part of the durable oracle and is tested as such.

### Procedure and comparison oracle

1. Quiesce writes or use the producer's documented consistent-snapshot
   mechanism. Capture the durable oracle and operational sentinel list at the
   same logical snapshot boundary.
2. Invoke the producer through its public export interface, selecting the
   entire fixture Engram and requesting `completeness: complete`. Do not seed an
   export directory with package-shaped copies of the storage-only cases.
3. Require a successful export whose manifest explicitly says
   `"completeness": "complete"` and has no `partial` selection metadata. Run
   ordinary schema, inventory, reference, media, and path validation against
   the resulting package.
4. Build an inventory-side map from each durable logical identity to its
   normative payload. The comparison MUST follow inventory entries rather than
   filenames. Normalize only representations for which the specification
   defines semantic equivalence; compare attachment payloads byte-for-byte and
   verify their declared size and SHA-256 digest.
5. Compare the source oracle and inventory map in both directions. Every source
   durable identity MUST occur exactly once with the same type and payload, and
   every exported normative identity MUST correspond to a durable artifact in
   the source snapshot. Record bodies, metadata, relationships, graph topology,
   attachment metadata and bytes, and extension values are all part of this
   comparison.
6. Specifically assert that each database/object-store-only durable case is
   present. Failure to discover an object because it was not already a package
   file is a complete-export failure.
7. Search inventory identities, paths, types, and normative payloads for the
   operational sentinels. Caches, credentials and tokens, indexes, locks, and
   temporary or unfinished state MUST NOT be classified as normative objects.
   Their presence as unlisted, non-normative package data is outside this
   inventory assertion, but publishing secrets as extra data remains a security
   failure and MUST be reported.

Run the procedure at least twice: once with all durable objects committed
before export, and once after adding a new storage-only durable object and
removing or changing an operational sentinel. The second run demonstrates that
the producer observes the requested snapshot rather than copying a previous
package or a stale index.

### Reporting and published evidence

A conformance report MUST give **package validation** and **producer complete
export** separate results. `package validation: pass` means only that the
produced package is internally conformant. `producer complete export: pass`
additionally means that the source-to-package comparison above passed for the
claimed source-store kind and snapshot. A validator MUST NOT infer the stronger
result from `completeness: complete`; that field is the producer's claim being
tested. If the source oracle was unavailable, report the producer result as
`not tested`, not `pass`.

For every claimed source-store kind, a producer claiming complete-export
support MUST publish enough evidence for an independent reviewer to reproduce
and audit the result:

- producer name and version, source-store kind and version, export invocation
  or API request, configuration relevant to discovery, and test timestamp;
- fixture construction instructions and a redacted source oracle listing every
  durable identity, type, and payload digest, plus the operational sentinel
  classes (never publish live credentials);
- the snapshot/transaction mechanism and boundary, including proof that the
  storage-only cases had no pre-existing package files;
- the exported package or a stable artifact location, its whole-artifact
  digest, and the validator name, version, command, and complete output;
- a machine-readable source-to-inventory comparison containing per-object
  identity and payload results, explicit storage-only-case results, unexpected
  normative objects, missing durable objects, and operational-sentinel checks;
- separate final statuses for package validation and producer complete export,
  with every failure, exclusion, or unsupported source-store kind disclosed.

## Repository fixtures

Run `python scripts/validate.py`. It validates the complete example and every
fixture in `tests/v0.2/valid`, then asserts that every fixture in `tests/v0.2/invalid` is
rejected. Invalid fixtures contain an `expected-error.txt` substring to ensure
they fail for the intended reason. The suite also checks catalog/traceability
coverage and concrete fixture recipes in `tests/v0.2/vectors`.

Behavioral results are executed, not inferred from vector shape. Run the
[language-neutral harness](harness-protocol.md) against an implementation
adapter. The repository includes two repository-maintained pilot processors:

```sh
python scripts/conformance_harness.py --adapter implementations/python-engram/engram_adapter.py
python scripts/conformance_harness.py --adapter implementations/node-engram/engram-adapter.js
```

The harness materializes every synthetic input in an isolated directory,
invokes the adapter, and recursively asserts every `expected` member for every
`CONSUMER-*` and `ROUNDTRIP-*` case. `tests/requirements-coverage.json` is the
machine-readable coverage gate: every cataloged `REQ-*` must name an executable
assertion or a manual procedure with an owner and evidence location. Passing
these repository tests supports a scoped conformance claim; it does not make
the processors independent implementations, production SDKs, or security
certifications.
