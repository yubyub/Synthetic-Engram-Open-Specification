# Decision 11: The 1.0 evidence and release bar

- **Status:** accepted
- **Outcome:** Require validator/fixture traceability, supported-runtime results, two independent implementations, security/privacy review, governance approval, and licensing review for core and every included optional profile. Defer certification trademarks and branding to the **Certification and Branding Program**.

## Rationale and compatibility

A schema draft is not interoperability evidence. The experimental label can be removed only when normative rules are testable, independent implementations exchange the same semantics, and governance records the reviewed release contents. Branding is separable and must not block technical conformance.

## Affected requirements and schemas

All `REQ-*`; [SPEC §11](../../SPEC.md#11-profiles-and-conformance), [requirements catalog](../requirements.json), [traceability](../traceability.md), [validator](../../scripts/validate.py), all [schemas](../../schemas/README.md), fixtures and vectors under [`tests`](../../tests), [SECURITY.md](../../SECURITY.md), [governance](../../GOVERNANCE.md), and repository licenses.

## Acceptance criteria and evidence

- **Satisfied for the draft:** every catalogued normative requirement maps to a fixture, assertion, or behavioral vector in [traceability](../traceability.md); repository validation checks catalog coverage. This must be rerun against the frozen v1.0 text.
- **Satisfied:** published validator results for every supported runtime showing all valid fixtures pass and every invalid fixture fails for its intended reason.
- **Satisfied:** published an interoperability report from two independent implementations covering `core`, `graph`, `media`, and `action` (unless another decision removes a profile).
- **Satisfied:** completed and approved a security/privacy review covering archive extraction, exhaustion, execution, links, extensions, and misleading trust/authority claims. [SECURITY.md](../../SECURITY.md) and consumer vectors are inputs, not recorded approval.
- **Satisfied:** recorded governance approval of normative text, schemas, both licenses, changelog, known limitations, and all ten preceding gates.
- **Inapplicable by scope:** certification branding evidence belongs to the named future program.

## Release-candidate check

A release manager MUST NOT create a v1.0 release candidate unless this record and gates 1–10 are merged in an `accepted` or `deferred` state, the [index](README.md) reads **11/11 closed**, and the status table in [`open-questions.md`](../open-questions.md) agrees.

## Linked changes required to close

Freeze and link [SPEC](../../SPEC.md), [schemas](../../schemas/README.md), [fixtures](../../tests), [traceability](../traceability.md), the interoperability report, security/privacy review, governance approval, [licenses](../../LICENSE), and [CHANGELOG](../../CHANGELOG.md).

## Final 1.0 evidence

Promotion is controlled by the authoritative
[1.0 promotion checklist](../releases/1.0-checklist.md); every required review
must have linked evidence, an approver, and a date there.

The exact reviewed release set and supported-runtime matrix are recorded in the
[1.0 release evidence](../release-evidence-1.0.md). The bidirectional artifacts
are retained in the [interoperability report](../interoperability/1.0/REPORT.md),
and the approved threat dispositions remain in the
[security review](../security-review-1.0.md).
