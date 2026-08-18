# Production SDK release criteria

The current Python and Node processors are reference interoperability
implementations. They must not be described as production SDKs until a release
meets every criterion below.

## Required release properties

- A documented, versioned public API for parsing, validation, production,
  consumption, round trips, diagnostics, and supported profiles.
- Deterministic restricted-front-matter behavior verified by the shared corpus,
  including duplicate-key and scalar-typing cases.
- Structured, stable diagnostic codes that distinguish invalid input,
  unsupported versions/profiles, resource limits, and operational failures.
- Configurable limits for bytes, objects, nesting, archive expansion, media, and
  processing time; secure defaults and no writes outside caller-approved roots.
- Preservation of unknown extensions and unsupported inventoried objects when a
  round-trip claim is made, with explicit loss reports otherwise.
- Compatibility tests for the supported major/minor window and a published
  deprecation policy for API changes.
- Atomic or staged import guidance, cancellation behavior, and recovery from
  partial operational failure.
- Reproducible packaging, signed release provenance where available, supported
  runtime versions, dependency policy, examples, and API reference material.
- A security contact, vulnerability-response policy, threat model, release
  history, and supported-fix window.
- Independent integration feedback and evidence that the SDK is maintained as a
  reusable library rather than only as a conformance adapter.

## Release gate

A candidate passes the repository package suite, language-neutral conformance
harness, front-matter corpus, cross-language exchange tests, and its own API and
security tests. The maturity matrix changes only after a versioned package is
published and the maintenance commitment is recorded.
