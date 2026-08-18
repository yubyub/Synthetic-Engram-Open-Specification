# Versioning policy

Specification releases use Semantic Versioning and are recorded in
`CHANGELOG.md`. Draft schemas live under a major/minor directory so a patch
clarification does not change package data.

A proposal that changes the interpretation of already-valid data is breaking.
Adding an optional extension or optional field is normally additive. Promoting
an optional field to required is breaking. Before 1.0, breaking design changes
may occur but still require a new declared format version and migration notes.
