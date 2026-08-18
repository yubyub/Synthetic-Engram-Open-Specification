# Governance for future profiles

**Status:** non-normative process; Core 0.2 profiles are unchanged

A profile exists to preserve independently useful semantics without enlarging
core for every domain. A proposal starts from repeated interoperability loss,
not from a desirable vocabulary list.

## Required proposal package

Every profile proposal includes:

1. a problem statement and two independently maintained intended consumers;
2. field ownership, normative semantics, required/optional behavior, and how the
   profile is declared and negotiated;
3. review of established vocabularies and a versioned, loss-aware mapping for
   each reused or competing standard;
4. compatibility classification under `docs/versioning.md`, immutable schema
   identifiers, migration behavior, and unknown-data preservation rules;
5. a threat model covering untrusted content, privacy, identity correlation,
   authority confusion, link fetching, and denial of service;
6. valid, invalid, boundary, round-trip, and cross-version fixtures plus stable
   diagnostics and traceability to normative requirements;
7. complete and partial package examples, implementation guidance, and explicit
   loss reporting; and
8. interoperability reports from two independent consumers, with neither report
   produced solely by the proposal author.

## Review gates

- **Exploration:** namespaced extensions and mapping fixtures may be published;
  no profile name or behavior is reserved.
- **Candidate:** public semantics, schema draft, security review, migration, and
  complete conformance suite exist. Candidate packages cannot claim released
  profile conformance.
- **Accepted:** compatibility approval and two-consumer evidence exist, release
  artifacts use a new immutable identifier, and governance records the decision.
- **Deprecated:** replacements and preservation/migration rules are published;
  released identifiers and bytes remain available.

Profiles are independently implementable. An implementation may decline one,
but it must not claim full consumption of a package whose required profile it
does not process. Unknown extension preservation is not the same as understanding
a profile.

## Domain prioritization

Pilot loss reports determine ordering. Provenance is evaluated before a complete
history/synchronization model. People, organizations, sources/citations, events,
conversations, bookmarks, datasets, claims, observations, decisions,
collections, and user-defined semantic types remain candidates—not commitments—
until two consumers demonstrate the same portable need.
