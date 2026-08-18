# Archive Binding Specification

**Status:** Future work placeholder; no archive binding is standardized by
Synthetic Engram core 0.2.

The non-normative [archive format and threat assessment](development/archive-format-assessment.md)
records decision inputs but deliberately selects no binding.

The canonical core 0.2 interchange representation is the directory form
defined by [`SPEC.md`](../SPEC.md#41-canonical-directory-representation).
ZIP, tar, and other archives are transport wrappers unless and until a future
version of this document defines a binding for one or more formats. This
placeholder grants no media type and provides no basis for an archive-specific
conformance claim.

A future Archive Binding Specification will define, at minimum:

- the archive format and media type;
- duplicate-entry and duplicate-path behavior;
- symbolic-link and hard-link handling;
- permission and other filesystem metadata semantics;
- Unicode path encoding, comparison, and normalization behavior;
- compressed and decompressed size, compression-ratio, member-size, and
  member-count limits; and
- deterministic serialization, including entry ordering and metadata values.

It will also provide adversarial conformance fixtures for the selected format.
Until then, implementations that choose to extract transport wrappers remain
subject to [REQ-PATH-003](../SPEC.md#req-path-archive) and the core security
requirements.
