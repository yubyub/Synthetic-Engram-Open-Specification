# Changelog

All notable specification changes are recorded here.

## [Unreleased]

### Fixed

- Updated GitHub Actions to their Node.js 24 releases and made the pip cache
  use the repository's `requirements-dev.txt` dependency file.

### Added

- Experimental v0.1 normative package specification.
- Draft 2020-12 schemas for manifests, records, graphs, and attachments.
- Complete Core + Graph + Media + Action example package.
- Cross-file validator, valid fixture, invalid fixture, and CI workflow.
- Contribution, governance, security, conformance, and versioning guidance.

### Changed

- Defined graphs as optional, non-authoritative views with explicit `curated` or
  `complete_records` scope and complete-record coverage validation.

- Replaced the monolithic project README with a concise entry point.
- Retained the original document as a non-normative concept draft.
