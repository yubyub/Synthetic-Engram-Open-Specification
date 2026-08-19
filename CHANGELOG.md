# Changelog

All notable specification and repository changes are recorded here.

## [Unreleased]

### Changed

- Refocused future development under the Engram Mesh name around a
  source-independent logical mesh.
- Established Engram Mesh 0.3 as a pilot model with a canonical JSON
  serialization and repository conformance exercises.
- Relicensed the entire repository under the MIT License.
- Removed completed planning registers, self-approval release records, the
  original concept dump, obsolete v0.1 material, duplicate unversioned fixtures,
  and generated release-gate artifacts.
- Corrected governance language to describe the current single-maintainer model
  and repository-local adapters honestly.

### Fixed

- Made `engram_id`, `export_id`, and `completeness` required manifest
  properties and added rejection fixtures for each omission.
- Corrected the unsupported-version vector and made pilot adapter observations
  derive from requests and fixture content instead of case IDs.
- Removed validator checks for deleted temporary planning and frozen-release
  artifacts.
- Required unambiguous `package_`, `engram_`, and `export_` prefixes for
  manifest identities and corrected the attachment-ID uniqueness exception.

### Added

- A normative Engram Mesh 0.3 pilot covering stable mesh identity, sources,
  source bindings, authority, capabilities, typed relationships, Mesh Slices,
  Lenses, and security boundaries.
- Engram Mesh schemas, fixtures, dependency-free validator, prototype Python and
  Node adapters, CI coverage, and non-normative architecture, rationale, status,
  versioning, and OKF 0.2 import/export mapping guidance.
- Executable binding lifecycle, authority-conflict, capability-subset,
  freshness, hierarchy, slice-closure, privacy-boundary, resolver-disclosure,
  and expected-diagnostic checks, plus getting-started, source-adapter, and
  requirement-traceability guidance.
- A public adoption-question table covering likely implementer objections,
  current answers, and evidence-driven follow-up work.
- Pilot and stable-release readiness criteria.
- Public issue and pull-request templates, tag-addressed schema identifiers,
  and AI live-service discovery guidance.

## [0.2.0] - unreleased

First public pilot line. It defines the directory package, typed Markdown
records, stable identifiers, explicit complete/partial scope, portable graph
topology, attachments, profiles, extensions, validation fixtures, and
repository-maintained cross-runtime exercises.

This line is intentionally pre-stable. No external applications or independent
implementations are known at publication preparation time, and incompatible
changes may be introduced in later 0.x versions.
