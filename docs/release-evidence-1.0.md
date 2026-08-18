# 1.0.0 release evidence

The authoritative promotion decision is the
[`1.0 promotion checklist`](releases/1.0-checklist.md). This document supplies
supporting evidence and does not supersede the checklist.

**Candidate:** `1.0.0-rc.1`
**Promoted unchanged:** `1.0.0`
**Release date:** 2026-08-18
**Disposition:** approved

The release candidate was cut only after the eleven design gates were closed.
Review covered the normative text, the permanent `v1.0` schema bytes, the
versioned examples and fixtures, both implementation reports, the security and
privacy review, CC BY-SA 4.0 and MPL 2.0 license texts, known limitations, and
the changelog. Promotion changed no normative text, schema, example, fixture,
or implementation artifact; it records only the final release status and date.

## Executed evidence

| Gate | Runtime / artifact | Result |
|---|---|---|
| Valid and invalid package suite | CPython 3.11, 3.12, and 3.13 CI matrix | PASS |
| Producer, consumer, round-trip vectors | Python implementation on CPython 3.11, 3.12, and 3.13 | 20/20 PASS |
| Producer, consumer, round-trip vectors | Node implementation on Node 20, 22, and 24 | 20/20 PASS |
| Bidirectional exchange | Python producer → Node round trip; Node producer → Python round trip | PASS; no normative loss |
| Security/privacy | `docs/security-review-1.0.md` | accepted with documented limitations |
| Licensing | `LICENSE` and `LICENSE-CODE` | approved |

The machine-readable harness reports and exchanged packages are retained under
[`docs/interoperability/1.0/artifacts`](interoperability/1.0/artifacts/). The
human-readable comparison is [`docs/interoperability/1.0/REPORT.md`](interoperability/1.0/REPORT.md).

## Governance approval

The exact single-change release set described above is approved under the
maintainer review rule in `GOVERNANCE.md`. Approval includes all eleven closed
decision records and is conditional on merging this change without amendments
to normative or schema content. Any amendment requires the affected gates and
evidence to be rerun; a schema correction must use a new URI rather than alter
`https://synthetic-engram.org/schema/v1.0/` in place.
