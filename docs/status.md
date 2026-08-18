# Project and component maturity

This page separates the maturity of the specification from the maturity of its
tooling and ecosystem. A stable format does not make every implementation a
production SDK, and two implementations maintained in this repository do not
constitute independent industry adoption.

| Component | Current status | What the status means |
| --- | --- | --- |
| Synthetic Engram Open Standard | Candidate open standard, release 1.0.0 | Core 1.0 is published and frozen, but multi-vendor adoption is not established. |
| Normative v1.0 schemas | Stable and immutable | Published schema identifiers and bytes cannot be replaced. |
| Repository validator | Reference conformance tooling | It validates the repository and packages; it is not a certification service or security boundary. |
| Python package processor | Reference interoperability implementation | It supplies producer, consumer, and round-trip evidence, not a supported production SDK. |
| Node package processor | Reference interoperability implementation | It is independently coded within this repository, not independently governed or externally adopted. |
| Front-matter parsers and corpus | Development conformance tooling | They demonstrate cross-runtime parsing behavior and remain subject to SDK release criteria. |
| Security review | Completed for the documented 1.0 release scope | It is not a product audit, certification, penetration test, or guarantee about adopters. |
| Production SDKs | Not released | No implementation currently meets the project's production SDK release criteria. |
| External implementations and products | Evidence needed | No external implementation or product is counted until a public pilot report identifies independent maintenance. |
| Archive binding | Not standardized | Directory packages are normative; archives remain transport wrappers pending an approved binding. |
| Provenance and domain profiles | Not standardized | Proposals and mappings are non-normative until profile governance and independent-consumer gates pass. |
| Remote/API binding | Not standardized | Implementations may expose application APIs; Core 1.0 defines no remote request contract. |

The project retains the **candidate open standard** qualifier until at least two
external products and independent maintainers are documented. See the
[execution backlog](development/implementation-backlog.md) for current evidence
and blocked gates.
