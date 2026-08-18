# Changelog

All notable specification changes are recorded here.

## [Unreleased]

## [1.0.0] - 2026-08-18

The reviewed `1.0.0-rc.1` candidate was promoted without changes to normative
text, schemas, examples, fixtures, or interoperability artifacts.

### Added

- Permanent Draft 2020-12 schemas under `schemas/v1.0` and separately versioned
  1.0 examples and conformance fixtures.
- Supported-runtime producer, consumer, round-trip, and two-implementation
  exchange evidence for all four profiles.
- Migration-boundary notes, security review, known limitations, and exact
  governance approval evidence.

### Changed since v0.1

- The normative version is `1.0.0`, object schema version is `1.0`, and schema
  base is `https://synthetic-engram.org/schema/v1.0/`.
- Core 1.0 rejects experimental v0.1 packages rather than silently
  reinterpreting them. The v0.1 artifacts remain archived unchanged.
- Removed the experimental README warning only after candidate promotion.

### Fixed

- Updated GitHub Actions to their Node.js 24 releases and made the pip cache
  use the repository's `requirements-dev.txt` dependency file.

### Added

- Normative version-support, schema-immutability, profile-evolution, and extension-ownership policy with consumer and round-trip conformance cases.

- Experimental v0.1 normative package specification.
- Draft 2020-12 schemas for manifests, records, graphs, and attachments.
- Complete Core + Graph + Media + Action example package.
- Cross-file validator, valid fixture, invalid fixture, and CI workflow.
- Contribution, governance, security, conformance, and versioning guidance.

### Changed

- Replaced the monolithic project README with a concise entry point.
- Retained the original document as a non-normative concept draft.
