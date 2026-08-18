# Contributing

Contributions are welcome while the standard is experimental.

## Proposing a change

1. Open an issue describing the interoperability problem rather than only a
   preferred representation.
2. For normative changes, include proposed specification text, valid example
   data, compatibility and security analysis, and conformance fixtures.
3. Keep normative requirements in `SPEC.md`; put rationale and tutorials in
   `docs/`.
4. Run `python scripts/validate.py` before opening a pull request.
5. Add a changelog entry for user-visible changes.

Use one logical change per pull request. Normative language must use the BCP 14
keywords consistently. JSON Schemas and prose must not contradict one another.
By contributing, you agree that documentation contributions are available under
CC BY-SA 4.0 and code, schemas, and examples under MPL 2.0.
