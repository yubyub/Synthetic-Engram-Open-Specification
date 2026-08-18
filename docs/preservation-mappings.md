# Preservation mapping plans

These non-normative plans describe how a directory-form Engram Package can be
carried by adjacent preservation systems. They are not compatibility claims.

## Common mapping contract

Preserve the package root, exact normative file bytes, inventory, stable IDs,
profiles, completeness, and attachment digests. Record the external standard and
version, mapping version, source package digest set, transformation, omitted
metadata, and restore procedure. A successful outer-package validation does not
replace Engram validation, and Engram hashes do not replace repository fixity or
authenticity controls.

## BagIt

Place the complete Engram directory below the BagIt payload directory without
renaming internal paths. Bag manifests add outer fixity; the Engram manifest
continues to define normative knowledge objects. Bag metadata has no automatic
mapping to `owner`, provenance, or authorization. A round trip loses Bag-specific
tag metadata unless the adapter preserves the entire bag outside Engram.

Required future evidence: a versioned profile of the BagIt recommendation,
fixtures for payload/tag manifests and fetch files, restore comparison of exact
Engram bytes, and declared handling of partial Engram Packages.

## OCFL

Store each Engram Package snapshot as OCFL object content and retain prior OCFL
versions as repository history. Engram `engram_id`, `export_id`, and Package ID
must not be inferred from OCFL object/version identifiers. OCFL version history,
deduplication, fixity, and extensions do not become Core history or provenance.

Required future evidence: object-layout and inventory mapping, snapshot/re-export
fixtures, restore from multiple versions, mutable-head failure tests, and a loss
report for OCFL metadata not represented in Engram.

## RO-Crate

An Engram Package may be described as an RO-Crate dataset, with inventoried files
referenced by crate entities. Synthetic Engram records and graphs are not
automatically Schema.org entities; semantic mappings require explicit types and
stable-ID rules. RO-Crate contextual/provenance metadata is additional unless an
approved Engram profile maps it.

Required future evidence: a versioned RO-Crate profile, entity-to-object mapping,
JSON-LD context policy, identifier/citation cases, attachment cases, and declared
loss in both directions.

## Completion rule

Each mapping remains planned until executable fixtures reproduce exact Engram
objects after `Engram -> adjacent standard -> Engram`, list every semantic loss,
and receive review from the adjacent standard's community or an experienced
implementer.
