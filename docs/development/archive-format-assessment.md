# Archive binding format and threat assessment

**Status:** decision input; no archive format or media type is selected

Core 1.0 standardizes a directory. This assessment defines the questions an
Archive Binding decision must answer before implementations or fixtures claim
archive conformance.

## Candidate comparison

| Property | ZIP | POSIX/pax tar | Compressed tar |
| --- | --- | --- | --- |
| Broad end-user tooling | Strong | Strong on Unix-like systems | Strong on Unix-like systems |
| Random entry access | Native central directory | Sequential | Sequential after decompression |
| Duplicate-path possibility | Yes | Yes | Yes |
| Symlink/hard-link model | Platform-dependent extensions | Native and security-sensitive | Same as tar |
| Filename/Unicode behavior | Multiple historical encodings and flags | Header-format and locale concerns | Same as tar |
| Deterministic metadata | Requires fixed headers, ordering, flags, and extra-field policy | Requires fixed headers, owners, modes, times, padding, and format | Also fixes compressor headers and implementation differences |
| Expansion risk | Per-entry and aggregate compression bombs | Member count and size abuse | Archive-wide and member expansion abuse |
| Browser/native desktop access | Generally strongest | Weaker | Weaker |

No candidate is acceptable merely because a standard library can open it. The
decision must include canonical bytes and adversarial behavior, not only a file
extension.

## Required canonical decisions

The decision record must fix the archive version/variant, registered or vendor
media type, UTF-8 path encoding and normalization, path comparison, entry order,
directory entries, timestamps, owners, groups, modes, platform fields, comments,
extra fields, compression method and level, compressor metadata, zero-length
files, and whether non-package entries are forbidden.

It must reject duplicate normalized paths. Symbolic links, hard links, devices,
FIFOs, sockets, absolute paths, parent traversal, NULs, backslashes as separators,
and case-fold collisions must either be forbidden or have one explicitly tested
portable meaning. The safer default for a package binding is to forbid special
filesystem entries and inventory only regular files and directories.

## Threat model and limits

An archive reader treats names and metadata as untrusted before extraction. It
must inspect without writes, normalize using the binding's rules, reject unsafe
or duplicate destinations, then enforce caller-configurable limits for compressed
bytes, expanded bytes, ratio, members, member bytes, path length, nesting, CPU,
and elapsed time. Limits apply cumulatively and before allocating claimed sizes.

Extraction uses a new staging directory, never follows pre-existing or extracted
links, opens destinations without link traversal, and commits only after archive
and Core package validation. Failure removes staging data and reports a stable
diagnostic without leaving a partial live-store update.

Adversarial fixtures must cover traversal, absolute and drive paths, mixed
separators, Unicode normalization collisions, case collisions, duplicates,
special entries, malformed/truncated headers, misleading sizes, excessive member
counts, deep paths, compression bombs, and trailing data.

## Decision gate

Governance chooses a binding only after two prototype writers produce identical
bytes for canonical fixtures and two readers agree on every adversarial outcome.
Until then, `docs/archive-binding.md` remains a placeholder and archives are only
implementation-defined transport wrappers.
