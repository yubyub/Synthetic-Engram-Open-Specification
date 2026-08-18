# Core 1.0 security review

**Review status:** release review complete
**Reviewed surface:** the frozen normative model in [`SPEC.md`](../SPEC.md), the
1.0 wire schemas, reference validator, versioned examples and fixtures, and the
language-neutral conformance harness.
**Threat model:** every package, archive wrapper, pathname, declared media type,
owner value, extension value, link, graph label, Markdown byte, and attachment
byte is attacker-controlled. The reference implementation is evidence about the
format, not a hardened importer.

This review applies to the permanent 1.0 schema identifiers and was approved as
part of the exact release set in [`release-evidence-1.0.md`](release-evidence-1.0.md).
The accepted implementation boundary is the repository's
[security policy](../SECURITY.md): callers must add limits, non-execution,
rendering/filename sanitization, and safe extraction. These limitations are
release conditions, not claims that hostile imports are safe by default.

## Method and disposition vocabulary

The review traced each threat to normative requirement IDs, schema constraints,
validator behavior, fixtures, and harness vectors. Evidence labelled
**executable** is reproducible with the command shown. Evidence labelled
**manual** is an inspection or application-level test because the standard does
not define the relevant runtime (for example, a browser renderer or transactional
database).

Dispositions mean:

- **Accept** — Core 1.0 contains an adequate interoperability rule; applications
  still have the stated residual operational risk.
- **Accept with limitation** — the boundary is deliberately implementation-
  defined or out of scope and is explicitly carried as a release limitation.
- **Block implementation claim** — an implementation must not claim conformance
  for the affected operation until its own evidence satisfies the requirement.

## 1. Path traversal and archive extraction

| Item | Review record |
| --- | --- |
| Threat | Relative traversal, absolute paths, backslash differentials, symlink/hardlink/device entries, and archive extraction races can read or overwrite files outside an import root. Decompression can also exhaust resources before package validation begins. |
| Affected requirements | REQ-PATH-001, REQ-PATH-002, REQ-PATH-003, REQ-INV-002, REQ-SEC-001, REQ-SEC-002. |
| Current mitigation | Schemas constrain package-path spelling; the validator rejects backslashes, absolute paths, dot segments, and resolved paths outside the root. `CONSUMER-005` supplies a tar containing `../../escape` and requires rejection with zero outside-root writes. Core standardizes the directory representation only; it does not supply or endorse an extractor. |
| Evidence | **Executable:** `python scripts/validate.py` exercises `unsafe-path`, `unsafe-absolute-path`, and `unsafe-backslash-path`. **Executable:** `python scripts/conformance_harness.py --adapter implementations/python-engram/engram_adapter.py` exercises `CONSUMER-005`. **Manual:** inspect an importing product's extractor for links and special files, validate each entry before creation, use a fresh private root, avoid following links, cap entry count/name length/compressed and expanded bytes, and verify no outside-root writes. |
| Residual risk | `Path.resolve()` checks in the validator are not a race-free extraction primitive. Archive format ambiguity, links, filesystem case folding, reserved names, and decompression ratios remain transport/platform concerns. |
| Release disposition | **Accept with limitation.** Directory packages are the conformance baseline. Any product that extracts an archive must independently satisfy REQ-PATH-003 and REQ-SEC-001/002; the repository policy explicitly says the validator is not a hardened extractor. |

## 2. Duplicate keys and parser differentials

| Item | Review record |
| --- | --- |
| Threat | First-wins, last-wins, or duplicate-preserving JSON/YAML parsers can validate one value and later consume another. Scalar typing, Unicode, number, and schema-format differences can similarly split producer and consumer interpretation. |
| Affected requirements | REQ-ENC-001, REQ-ENC-002, REQ-REC-006, REQ-REC-007, REQ-REC-009, REQ-SEC-004. |
| Current mitigation | The validator uses a JSON `object_pairs_hook` that fails on repeats and a YAML mapping constructor that rejects repeated or non-string keys. Front-matter scalar resolvers implement the restricted JSON-compatible typing rules. JSON Schema closes core objects and validates formats. |
| Evidence | **Executable:** `python scripts/validate.py` rejects `duplicate-json-key`, `duplicate-yaml-key`, and `invalid-json-utf8` for their expected reasons. **Manual:** feed every package document through the exact production parse-and-use path, rather than validating with one parser and importing with another; compare parsed trees across supported runtimes using the invalid fixtures. |
| Residual risk | JSON Schema alone cannot detect duplicates after an ordinary parser has discarded them. YAML library and RFC 3339/number behavior can differ, while extremely large finite-looking numbers may be expensive or lose precision in downstream runtimes. |
| Release disposition | **Accept.** Unique keys and deterministic YAML typing are normative; a consumer using a lossy pre-schema parse cannot claim it enforced them. Cross-runtime differential testing remains an implementation release gate. |

## 3. YAML tags, aliases, depth, and expansion attacks

| Item | Review record |
| --- | --- |
| Threat | Explicit tags can invoke constructors; anchors, aliases, and merge keys can change meaning or amplify data; deeply nested block structures can exhaust stack, CPU, or memory. Multiple documents and flow syntax can create parser differentials. |
| Affected requirements | REQ-REC-005 through REQ-REC-009, REQ-SEC-002, REQ-SEC-003. |
| Current mitigation | Token scanning rejects tags, anchors, aliases, directives, document markers, and flow collections. The custom safe loader accepts exactly one mapping and rejects merge/non-string/duplicate keys. Schemas bound the permitted record shape after parsing. |
| Evidence | **Executable:** `python scripts/validate.py` rejects `yaml-tag`, `yaml-alias`, `malformed-delimiter`, and duplicate-key fixtures. **Manual:** impose record-byte, token, nesting-depth, collection-size, and parse-time limits before or within the YAML parser, then test generated deeply nested block mappings/sequences under memory and timeout instrumentation. |
| Residual risk | PyYAML scanning/loading occurs before any explicit validator byte/depth/time budget. Prohibited aliases remove the classic alias bomb, but deeply nested or very wide source can still consume resources or hit recursion limits. |
| Release disposition | **Accept with limitation.** The dangerous language features are forbidden; quantitative parsing limits remain implementation-defined under REQ-SEC-002. The reference validator is not approved as an unbounded network-facing parser. |

## 4. JSON, graph, Markdown, attachment, and extension resource exhaustion

| Item | Review record |
| --- | --- |
| Threat | Oversized manifests, deep JSON/extensions, huge Markdown, graph cardinality, quadratic reference checks, numerous files, large attachments, hashes over unbounded streams, and decompressed archives can exhaust CPU, memory, disk, descriptors, or time. |
| Affected requirements | REQ-PATH-003, REQ-INV-005, REQ-CLOSE-001/002, REQ-SEC-002, REQ-SEC-004. |
| Current mitigation | Schemas restrict shapes but intentionally set no universal package quota. The harness's `CONSUMER-008` passes `max_bytes: 8` and requires a rejected import with limits enforced; harness subprocesses have a 30-second timeout. The security policy enumerates archive paths/sizes, parsing depth, decompressed bytes, record counts, and attachment sizes as required limits. |
| Evidence | **Executable:** `python scripts/conformance_harness.py --adapter implementations/python-engram/engram_adapter.py` runs `CONSUMER-008`. **Manual:** configure and verify limits for total/source/expanded bytes, each document and attachment, object/node/edge/link/extension counts, nesting, filenames, redirects, descriptors, memory, CPU, and wall time; ensure rejection cleans temporary data. |
| Residual risk | `scripts/validate.py` reads whole JSON, Markdown, and attachment files and performs no configurable quota enforcement. `CONSUMER-008` verifies an adapter-reported observation, not operating-system containment or a normative minimum. Thresholds necessarily depend on deployment. |
| Release disposition | **Accept with limitation; block implementation claim without evidence.** REQ-SEC-002 is mandatory, but Core 1.0 deliberately does not prescribe one unsafe-for-some or unusable-for-others global quota. |

## 5. Markdown/HTML execution and output-context sanitization

| Item | Review record |
| --- | --- |
| Threat | Raw HTML, scripts, event handlers, dangerous URL schemes, SVG, CSS, template syntax, and renderer/plugin behavior can cause code execution, network requests, credential leakage, or injection into HTML, terminals, logs, SQL, or native UI contexts. |
| Affected requirements | REQ-REC-010, REQ-SEC-003, REQ-SEC-004. |
| Current mitigation | Raw HTML is data and is allowed in records, but execution is forbidden. Rendering must sanitize or escape for its actual output context. `CONSUMER-006` and `CONSUMER-009` require zero record-content executions. Import and rendering are separate trust boundaries. |
| Evidence | **Executable:** run the conformance harness command above for the adversarial `<script>` vectors. **Manual:** as required by the coverage registry for REQ-REC-010, render adversarial Markdown/HTML in an instrumented sandbox for every supported output context; verify no script/plugin/template execution or unauthorized requests and inspect the resulting DOM/output. |
| Residual risk | The reference adapter reports non-execution but is not a real renderer, so it does not prove sanitizer correctness. Sanitization is context-specific and libraries evolve; safe HTML output is not automatically safe in attributes, URLs, shells, terminals, or logs. |
| Release disposition | **Accept with limitation; block renderer claim without manual evidence.** Core cannot select a sanitizer without selecting a Markdown dialect and output runtime. Products must retest their exact renderer and policy. |

## 6. External links, attachment URI handling, and unsafe filenames

| Item | Review record |
| --- | --- |
| Threat | Links can drive phishing, tracking, SSRF, local-file access, custom-protocol execution, or tabnabbing. A displayed/suggested attachment path can redirect resolution. Filenames and media types can contain control characters, reserved names, misleading extensions, or shell/HTML metacharacters. |
| Affected requirements | REQ-MEDIA-001 through REQ-MEDIA-004, REQ-SEC-001, REQ-SEC-004. |
| Current mitigation | Attachment payloads resolve by stable attachment ID and inventory, not body-suggested paths or remote URLs. Discovery is limited to Markdown link/image destinations. Safe package paths constrain storage names, while all links, filenames, and media types remain explicitly untrusted. |
| Evidence | **Executable:** validator fixtures cover unsafe paths, missing payloads, size/hash mismatches, and missing blob inventory. **Executable:** harness vectors `CONSUMER-003` and `CONSUMER-010` verify ID-based resolution, ignored suggested paths, and no arbitrary-text URI discovery. **Manual:** allowlist schemes and destinations, disable implicit fetches, apply SSRF egress controls, generate safe local names instead of trusting labels, and escape names in every display/log/header context. |
| Residual risk | Core does not prescribe URL navigation/fetch policy, DNS/IP filtering, redirect handling, download disposition, MIME sniffing, confusable-name handling, or platform reserved-name mapping. A valid attachment may still be malicious content. |
| Release disposition | **Accept with limitation.** Resolution semantics prevent path substitution; network and presentation policy remain application responsibilities explicitly accepted by `SECURITY.md`. |

## 7. Hash integrity versus authenticity

| Item | Review record |
| --- | --- |
| Threat | An attacker who can replace a payload can also replace its manifest/metadata hash. Users may mistake a matching SHA-256 value for proof of author, origin, approval, freshness, or safety. |
| Affected requirements | REQ-MEDIA-001, REQ-SEC-004. |
| Current mitigation | Attachment size and SHA-256 are checked against bytes. The normative security rule and repository policy explicitly limit hashes to integrity/change detection and place signing, identity proof, and authorization outside Core 1.0. |
| Evidence | **Executable:** `python scripts/validate.py` rejects `attachment-size-mismatch` and `attachment-hash-mismatch`, while accepting valid and zero-byte attachments. **Manual:** replace both an attachment and its declared digest and confirm validation succeeds but the application grants no trust or authority as a consequence. |
| Residual risk | Self-consistent malicious packages validate. There is no signature envelope, trust root, transparency log, timestamp authority, revocation, or anti-rollback mechanism. |
| Release disposition | **Accept with limitation.** This is an intentional non-goal linked from the security policy and release notes. Authenticity claims require an external, explicitly bound signing/trust protocol. |

## 8. Owner metadata and package possession versus identity, trust, and authorization

| Item | Review record |
| --- | --- |
| Threat | Anyone can write an `owner` name or possess/copy a package. Treating either as authenticated identity, ownership proof, consent, ACL membership, or permission enables impersonation and privilege escalation. |
| Affected requirements | REQ-MAN-001, REQ-SEC-004, REQ-SEC-005. |
| Current mitigation | The owner schema provides only a type and non-empty display name. The specification excludes identity proof and authorization and forbids inferring permission from possession. `CONSUMER-007` requires denial when authorization is attempted without a credential. |
| Evidence | **Executable:** run the harness and inspect `CONSUMER-007` (`permission_granted: false`). **Manual:** edit `owner.name`, copy the package between principals, and confirm neither operation changes authenticated principal, tenant binding, ACL, import target, or overwrite permission. |
| Residual risk | UIs can still present attacker-selected owner text as authoritative. Core has no stable owner identifier, authentication ceremony, delegation, consent, access descriptor, or tenant binding. |
| Release disposition | **Accept with limitation.** Identity, trust, and authorization are external. Any product deriving permission from metadata or possession violates REQ-SEC-005 and must not claim a conforming authorization behavior. |

## 9. Sensitive-data leakage through complete or partial exports

| Item | Review record |
| --- | --- |
| Threat | A complete export can disclose all durable owner-controlled knowledge; a partial export can still reveal content, relationships, graph labels, attachment bytes, extension data, owner names, timestamps, IDs, or selection expressions. Incorrect snapshot classification can leak credentials or omitted requested boundaries. |
| Affected requirements | REQ-SCOPE-001 through REQ-SCOPE-003, REQ-CLOSE-001 through REQ-CLOSE-005, REQ-INV-005/006, REQ-SEC-004/005. |
| Current mitigation | Completeness is explicit; partial packages require selection metadata but that metadata is not proof of closure. Complete-export rules exclude credentials, tokens, sessions, telemetry, temporary files, and unfinished writes from normative objects, and require producer comparison against a bounded snapshot. Consumers ignore unlisted files as normative objects. |
| Evidence | **Executable:** validator runs `partial-engram`, `partial-external`, and `complete-omits-durable-object`; `CONSUMER-001` verifies an unlisted scratch file is not imported as normative. **Manual:** perform the producer-side snapshot comparison required for REQ-CLOSE-003/004/005, scan the final package including extensions and unlisted transport files for secrets, and review the intended recipient and selection before release. |
| Residual risk | A consumer cannot prove absence of an undisclosed source object, and “complete” intentionally means durable current state—not safe-to-share. Unlisted files are non-normative but can still leak when the directory/archive is transmitted. Selection descriptions and stable IDs may themselves be sensitive. No encryption or redaction protocol is defined. |
| Release disposition | **Accept with limitation.** Completeness is an interoperability claim, not confidentiality or consent. Producers need an application-level disclosure preview, secret policy, recipient authorization, and protected transport/storage. |

## 10. Unknown profiles and extensions

| Item | Review record |
| --- | --- |
| Threat | Unknown profiles or extension data can hide active content, excessive data, security-sensitive semantics, or objects a consumer silently drops. Namespace resemblance can mislead consumers into treating extension semantics as core. |
| Affected requirements | REQ-CLOSE-002, REQ-EXT-001, REQ-EXT-002, REQ-PROF-001/002, REQ-CONF-003/004, REQ-SEC-002/004, REQ-VERS-001. |
| Current mitigation | Core objects are closed except at reverse-DNS extension points; extensions cannot alter core validity or meaning. Consumers must process a declared profile or report it unsupported and cannot claim support for content they did not process. Round-trip preservation claims require preservation of unsupported objects and unknown extensions. Current manifest schemas enumerate the frozen known profiles, so an actually unknown profile is schema-invalid rather than silently accepted. |
| Evidence | **Executable:** validator rejects `invalid-extension-name`, `unknown-core-field`, and `missing-profile`, verifies every legal known-profile combination, and accepts `extension-preservation`. **Executable:** `CONSUMER-002` reports `graph` unsupported; `ROUNDTRIP-003` checks extension preservation. **Manual:** apply the same byte/depth/count limits to unknown values, display them as untrusted, and verify no extension dispatcher/plugin executes merely because a namespace is present. |
| Residual risk | JSON-compatible extension values are recursively unconstrained in semantic meaning and can be large/deep. Byte-for-byte preservation is stronger than the reference adapter's deep-equality observation. Rejecting future profile names limits forward compatibility, while accepting them outside this schema risks silent loss. |
| Release disposition | **Accept with limitation.** Frozen Core 1.0 rejects schema-unknown profiles; known-but-unsupported declared profiles require a deterministic unsupported result. Unknown extensions are opaque data, not trusted instructions. |

## 11. Atomic import behavior and incomplete writes

| Item | Review record |
| --- | --- |
| Threat | Failure after partial extraction, validation, or database mutation can expose an incomplete Engram, overwrite existing objects, leave attacker-controlled temporary files, or make retries duplicate/corrupt state. Concurrent readers can observe a package before all hashes and references are checked. |
| Affected requirements | REQ-INV-002/003/005, REQ-CLOSE-001/003/005, REQ-MEDIA-001/002, REQ-CONF-002, REQ-SEC-001/002/005. Atomic commit is not otherwise standardized by Core 1.0. |
| Current mitigation | Cross-file validation detects missing/mismatched objects, attachment bytes, references, and broad complete-package closure before a package should be accepted. The complete-export model excludes unfinished writes. No reference importer, transaction protocol, rollback rule, or atomic filesystem publication primitive is supplied. |
| Evidence | **Executable:** `python scripts/validate.py` rejects missing payload/blob, object-ID mismatch, broken references, attachment mismatch, and omitted durable artifacts. **Manual:** inject failure and cancellation after every extraction/parse/hash/store step; confirm the destination remains unchanged, staging is private and removed, a final atomic transaction/rename publishes only fully validated state, retries are idempotent, and concurrent readers never observe staging. |
| Residual risk | A package can be internally valid while application-side transformation or commit fails. Filesystem rename atomicity, cross-device moves, database transactions, recovery, merge/overwrite policy, and retry identity are deployment-specific. The harness does not currently assert rollback or incomplete-write cleanup. |
| Release disposition | **Accept with limitation; block importer deployment without manual evidence.** Atomic import is a necessary product safety property but is outside the frozen interchange semantics. Implementations must stage, validate, authorize, and commit as separate phases, failing closed before publication. |

## Release conclusion

No reviewed item requires changing the frozen package model. The model has clear
normative boundaries for path spelling, duplicate keys, restricted YAML,
non-execution, attachment integrity/resolution, unsupported profiles, untrusted
content, and non-authority. The release is acceptable only with the limitations
already stated in [`SECURITY.md`](../SECURITY.md) and the known limitations in
the [1.0 release notes](../CHANGELOG.md#100---2026-08-18):

1. archive extraction and transactional import are product responsibilities;
2. every parser and content class needs deployment-appropriate quotas;
3. every renderer/output context needs its own sanitizer and execution test;
4. external navigation, fetching, filenames, and attachment opening need policy;
5. hashes and owner metadata convey neither authenticity nor authority; and
6. complete/partial export labels convey scope, not confidentiality.

For release evidence, retain the validator output, the implementation harness
reports, and the product-specific manual records identified above. A passing
reference suite is necessary evidence of model interoperability, but it is not a
security certification of an extractor, renderer, network fetcher, or importer.
