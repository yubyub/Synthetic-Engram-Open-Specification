# Normative version and support policy

This document is normative. The key words **MUST**, **MUST NOT**, **SHOULD**,
and **MAY** have the BCP 14 meanings established by `SPEC.md`. If this policy
and `SPEC.md` conflict, `SPEC.md` wins.

## Release classification

Specification releases use Semantic Versioning and are recorded in
`CHANGELOG.md`. The manifest `version` identifies the specification release;
object `schema_version` values and schema directories identify only the major
and minor line. Patch releases therefore do not change package data or schema
URIs.

Classify a change by its largest compatibility impact:

| Kind | Patch | Minor | Major |
| --- | --- | --- | --- |
| Schema | Correct prose or examples without changing the schema; add an equivalent test | Add an optional field, object kind, or non-required schema entry point | Remove or rename a field; make an optional field required; narrow an accepted value set |
| Validation | Fix a test that did not enforce an existing unambiguous MUST | Add validation for a new optional feature | Reject data that the released specification intentionally allowed, or accept data it required consumers to reject |
| Semantics | Clarify wording without changing any conforming interpretation | Define semantics for a new opt-in field or capability | Change the meaning, identity, default, or resolution of already-valid data |
| Profile | Clarify an existing profile or add tests | Add a new optional profile | Remove a profile, make an optional profile part of core, or require previously optional profile behavior |
| Serialization | Editorially clarify an existing byte rule | Add an optional, explicitly selected serialization binding | Change the canonical encoding, path rules, or interpretation of existing bytes |

An accidental discrepancy in a released schema is not permission to replace
it. If the intended correction changes which packages validate, it is a major
change; alternatively, a new optional mechanism can be introduced in a minor
release. Security impact alone does not waive these compatibility rules.

## Consumer version negotiation

A consumer MUST inspect the manifest version and declared profiles before
processing profile-owned content.

* **Unsupported major.** It MUST stop and return an
  `unsupported-major-version` result. It MUST NOT report successful import,
  silently reinterpret the package using another major, or mutate it.
* **Newer minor in a supported major.** It MUST NOT reject the package merely
  because the minor number is newer. It MAY successfully process the package
  only when it supports every declared profile/capability needed for the
  requested operation and can satisfy the preservation rules below. Otherwise
  it MUST return `unsupported-required-capability` (or the more specific
  `unsupported-profile`) and MUST NOT claim full successful consumption.
* **Unknown required capability.** Every declared profile is a required
  capability for the content governed by that profile. A consumer that does
  not implement one MUST report its identifier and a non-success result. It
  MAY offer an explicitly partial operation, but MUST identify the skipped
  profile and MUST NOT label that result a conforming full import.

A consumer MAY warn about a newer patch, but MUST treat it as the same data
format because patches cannot alter accepted data or semantics.

## Profiles and evolution within a major

`core` is the baseline capability for a major version. Every other profile is
optional for implementations, but required to process when a package declares
it and an implementation claims full consumption of that package. A minor or
patch release MUST NOT add an existing optional profile to core, make support
for an optional profile a condition of core conformance, or add new required
behavior to an existing profile. New profiles introduced within a major MUST
be opt-in and packages using them MUST declare them. Making any optional
profile required requires a new major version.

## Immutable schema identifiers and errata

Every published schema URI is an immutable identifier for exact bytes. The
project MUST NOT replace, redirect to different schema content, or reuse a
released major/minor URI. Mirrors MUST preserve the released bytes.

Non-normative errata are published as dated entries in `CHANGELOG.md` and may
link to corrected prose. A schema-affecting correction is published at a new
URI under a new compatible minor or incompatible major directory, as dictated
by the table above, with migration notes. The old schema and its checksum
remain available. Tooling MAY diagnose a known erratum but MUST identify the
original schema and MUST NOT silently validate against substituted bytes.

## Extension namespaces and promotion

The registrant controlling a DNS name owns the corresponding reverse-DNS
extension prefix. For example, the controller of `example.org` controls
`org.example` and its descendants. Authors MUST use a domain they control or a
namespace explicitly delegated to them; DNS expiry or transfer does not
retroactively change the meaning of package data.

Two definitions of the same extension key are a collision. A consumer MUST
NOT merge, guess between, or reinterpret colliding definitions and MUST report
the collision. Producers MUST NOT emit two meanings for one key. Unknown
extensions are not errors. A round-trip processor claiming preservation MUST
retain each unknown key and its JSON-compatible value with deep structural
equality; it SHOULD retain the original bytes when its processing model
permits. It MUST NOT move an unknown value into another namespace or drop it.

Promoting an extension concept into core requires all of the following:

1. a public proposal with the namespace owner's participation or a documented
   clean-room design when that owner is unavailable;
2. documented semantics, security and collision analysis, schemas, examples,
   and conformance cases;
3. a new, non-namespaced core field—the extension key remains owned by its
   original owner and is never repurposed; and
4. deterministic precedence and migration rules when both forms occur.

Promotion MAY be a minor change only when the core field is optional and the
two forms can coexist without changing existing meaning. Requiring the core
form, removing the extension form, or assigning it new semantics is a major
change. Consumers MUST NOT automatically translate an extension merely
because a similar core concept exists.

## Supported release window

After a new major release, the project promises normative documentation and
reference conformance testing for the current major and **one prior major**.
Older material remains archived at immutable links but receives no promise of
new documentation, fixes, or test execution. This is a project support floor,
not a requirement that every implementation support both majors.

## v0.1 and v1.0

Core v1.0 **does not accept v0.1 packages**. The experimental `0.1.x` format
is not a supported input version of 1.0, and a 1.0 consumer MUST return
`unsupported-major-version` rather than guess or silently migrate it. No
normative v0.1-to-v1.0 migration rules or fixtures are therefore provided.
Conversion tools may exist, but their output is a newly produced package and
cannot claim a lossless standard migration unless a future specification
defines one.
