# Contributing

Contributions are welcome as this candidate open standard builds independent
implementation and adoption evidence. Core 1.0 is stable; experimental future
work must not silently alter its frozen schemas or semantics.

## Proposing a change

1. Open an issue describing the interoperability problem rather than only a
   preferred representation.
2. For normative changes, include proposed specification text, valid example
   data, compatibility and security analysis, and conformance fixtures.
3. Keep normative requirements in `SPEC.md`; put rationale and tutorials in
   `docs/`.
4. Check the non-normative
   [`implementation-feedback` register](docs/development/implementation-feedback.md)
   for related adoption concerns, and update its evidence/status when the change
   implements or resolves one of them.
5. Run `python scripts/validate.py` before opening a pull request.
6. Add a changelog entry for user-visible changes.

Use one logical change per pull request. Normative language must use the BCP 14
keywords consistently. JSON Schemas and prose must not contradict one another.
By contributing, you agree that documentation contributions are available under
CC BY-SA 4.0 and code, schemas, and examples under MPL 2.0.
