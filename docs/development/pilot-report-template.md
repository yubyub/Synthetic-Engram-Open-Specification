# Independent adoption pilot report template

**Status:** template; a completed report is evidence only when maintained and
published by an adopter independent of this repository.

## Pilot identity

- Organization or project:
- Public repository or product:
- Maintainers and organizational relationship to Synthetic Engram maintainers:
- Category: note/project, AI knowledge, or archive/migration
- Dates and Synthetic Engram version:
- Implementation language and supported roles/profiles:

## Use case and data

Describe the user outcome, live storage architecture, dataset size, record and
relationship types, media sizes, Unicode and adversarial samples, and whether
the export is complete or partial. Do not publish private source data.

## Mapping and loss

| Source concept | Engram representation | Direction | Loss or extension | Stable-ID rule |
| --- | --- | --- | --- | --- |
| | | | | |

Identify every omitted, merged, split, derived, reclassified, or
application-specific concept. Describe preservation of unknown extensions and
unsupported inventoried objects.

## Round-trip procedure

Record versions and commands for export, independent validation, import, edit,
re-export, rename, and comparison. Link sanitized fixtures, conformance reports,
and semantic/byte-loss reports. State whether another implementation performed
the import.

## Operational findings

- Parsing and integration effort:
- Structured diagnostics and failure recovery:
- Runtime, peak memory, object count, and media limits:
- Transaction, concurrency, and deployment behavior:
- Security and privacy findings, including untrusted input and authorization:
- Documentation or SDK gaps:

## Conclusion

State what worked, what did not, whether the implementation is independently
maintained, which feedback IDs the evidence informs, and whether a repeated
interoperability problem justifies standard work. A documentation-only exercise
or repository-maintainer self-test is not an independent pilot.
