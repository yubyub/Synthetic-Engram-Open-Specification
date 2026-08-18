# Versioning policy

## The four versioning axes

| Concept | Example | Where declared | Meaning |
| --- | --- | --- | --- |
| Specification release | `0.1.1` | `SPEC.md`, release tag, and `CHANGELOG.md` | SemVer release of prose, schemas, and tests |
| Data-model version | `0.1` | manifest `data_model_version` | Compatibility boundary for the package core |
| Schema version | `…/schema/v0.1/manifest.schema.json` | schema `$id`, directory, and object `schema_version` | Validator language selected for a data-model major/minor |
| Optional feature | `org.example.summary` | manifest `features` | Advertised, ignorable minor-version semantics |

Patch specification releases MUST NOT alter the set of valid package data.
Consequently patch numbers do not belong in package data. A package written
using specification 0.1.0 and one written using 0.1.1 both declare data model
`0.1`; schemas MUST match the major/minor rather than an exact release constant.

## Pre-validation negotiation

A consumer performs these steps, in order:

1. Parse `engram.json` as untrusted JSON, rejecting duplicate keys, and extract
   only `format`, `data_model_version`, and optional `features`. Require the
   expected format, `MAJOR.MINOR` decimal syntax, and an array of unique,
   syntactically valid feature identifiers. Absence means no features.
2. Reject an unsupported major. From locally supported schemas with that major,
   select the greatest minor less than or equal to the package minor. Reject if
   there is no such schema.
3. Compare declarations with implemented features. Reading may continue with
   unsupported optional features, provided they are reported as unsupported.
   Round-trip processing may continue only if their declarations and extension
   payloads will be preserved unchanged.
4. Validate the complete manifest and every package object against the selected
   schema, followed by all cross-file checks. Validation failure is rejection.

The selected older schema can validate a newer-minor core because minor
features are confined to extension points already present in the closed core
schemas. Feature identifiers use reverse-DNS syntax. A feature's payload, when
present, is the value under the same key in `extensions`. It cannot add new
core properties, reinterpret core fields, or be required to understand the
core package. A producer MUST declare every feature it uses. An unaware reader
MAY ignore its payload; a rewriting consumer MUST preserve declaration and
payload unchanged or reject.

Profiles describe broad conformance capabilities and object families; they do
not replace `features`. A feature incompatible with safe ignore/preservation,
or any change to the interpretation of valid core data, requires a new major.
Promoting optional core data to required is likewise breaking, including before
1.0, and requires migration notes.

## Expected outcomes

The machine-checked cases in `tests/versioning` use a consumer supporting data
model 0.1 and no optional features:

| Fixture | Expected outcome |
| --- | --- |
| `supported-patch-0.json`, `supported-patch-1.json` | `ACCEPT` — out-of-band specification patches both declare data model 0.1 |
| `unsupported-minor-no-features.json` | `ACCEPT` — select schema 0.1 and validate the compatible core |
| `unsupported-minor-optional-feature.json` | `ACCEPT_WITH_UNSUPPORTED_FEATURES` — read core, report `org.example.summary`; preserve it for round trip |
| `unsupported-major.json` | `REJECT_UNSUPPORTED_MAJOR` — do not attempt full schema validation |
