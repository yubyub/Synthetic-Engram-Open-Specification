# Schema and release mirroring procedure

This procedure lets an independent institution mirror released artifacts without
changing their content or implying governance authority.

## Mirror set

For each release, copy the tagged source archive, normative specification,
versioning policy, every schema beneath its released URI path, schema checksums,
validator and conformance-harness source, fixtures/vectors, licenses, and
changelog. Preserve original filenames and bytes.

## Verification

1. Fetch from a signed or otherwise authenticated release channel and record the
   tag, commit, retrieval time, and transport source.
2. Compute SHA-256 for every mirrored file and publish a sorted UTF-8 checksum
   manifest alongside, not inside, the mirrored release tree.
3. Compare schema checksums with the originating release and at least one other
   mirror when available. A mismatch is an incident; never "repair" it silently.
4. Serve immutable cache-controlled bytes. A mirror URL is an alternate
   retrieval location; it does not replace the schema's tag-addressed `$id`.
5. Perform a quarterly fixity check and an annual restore exercise into an empty
   location. Retain dated reports and software/runtime information.

## Failure and succession

Publish contact and succession information, export the mirror catalogue in an
open format, and retain at least two geographically and administratively distinct
copies. If a mirror closes, transfer exact bytes and audit history; do not redirect
a released schema URI to different content.

An institutional mirror is meaningful adoption evidence only when administered
outside this repository and accompanied by public fixity and recovery reports.
