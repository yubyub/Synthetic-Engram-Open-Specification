# Changelog

All notable specification and repository changes are recorded here.

## [Unreleased]

### Changed

- Relicensed the entire repository under the MIT License.
- Reclassified the work from a claimed stable 1.0 release to a 0.2 pilot
  specification intended for real-world implementation feedback.
- Removed completed planning registers, self-approval release records, the
  original concept dump, obsolete v0.1 material, duplicate unversioned fixtures,
  and generated release-gate artifacts.
- Consolidated the active schemas, examples, fixtures, security review, and
  interoperability exercises under explicit 0.2 paths.
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

- A public adoption-question table covering likely implementer objections,
  current answers, and evidence-driven follow-up work.
- Pilot and stable-release readiness criteria.
- Public issue and pull-request templates, tag-addressed schema identifiers,
  and AI live-service discovery guidance.
- A non-normative Source Reference profile exploration for portable context
  about externally stored knowledge, with resolver, completeness, graph,
  provenance, security, and pilot boundaries.

### Clarified

- Complete-export closure includes durable Engram-owned contextual assertions
  but not the content of external entities merely reachable through links.
- Plugins, connectors, APIs, and MCP servers may resolve external knowledge but
  their credentials, authorization, and provider-specific state are not
  portable Engram context.

## [0.2.0] - unreleased

First public pilot line. It defines the directory package, typed Markdown
records, stable identifiers, explicit complete/partial scope, portable graph
topology, attachments, profiles, extensions, validation fixtures, and
repository-maintained cross-runtime exercises.

This line is intentionally pre-stable. No external applications or independent
implementations are known at publication preparation time, and incompatible
changes may be introduced in later 0.x versions.
