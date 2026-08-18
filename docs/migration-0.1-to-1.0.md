# Migrating experimental v0.1 packages to 1.0

There is deliberately no normative, lossless v0.1-to-1.0 migration. A 1.0
consumer MUST reject a `0.1.x` manifest as `unsupported-major-version` and MUST
NOT reinterpret its objects using the 1.0 schemas. The archived v0.1 schemas,
examples, and fixtures remain evidence of what those bytes meant.

A conversion tool may read v0.1 as an explicitly separate input format and
produce a new 1.0 package. It must validate the input against `schemas/v0.1`,
map every object explicitly, set manifest `version` to `1.0.0`, set object
`schema_version` to `1.0`, validate against `schemas/v1.0`, preserve durable IDs
only where identity is known to be equivalent, and report every dropped,
changed, or unmapped value. Its output is a newly produced package, not proof
of a standard-defined lossless migration.

`CONSUMER-004` is the executable migration-boundary fixture. It verifies the
required rejection rather than inventing a migration rule.
