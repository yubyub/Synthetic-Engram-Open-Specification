# Synthetic Engram 0.2 repository exchange exercise

The repository contains Python and Node pilot processors that exercise producer,
consumer, and round-trip behavior for the 0.2 package. They are maintained in
the same repository and share the same test design. Their results are useful
implementation feedback, but they are **not independent interoperability
evidence** and do not establish production readiness.

## Reproduce

From the repository root:

```sh
python3 scripts/conformance_harness.py --adapter implementations/python-engram/engram_adapter.py
python3 scripts/conformance_harness.py --adapter implementations/node-engram/engram-adapter.js
python3 scripts/run_interoperability.py
python3 scripts/validate.py
```

The exchange runner creates all output in a temporary directory, sends the
basic example through each processor and then through the other processor, and
compares parsed JSON plus exact bytes for every other inventoried file. It
prints a machine-readable report and returns non-zero if content changes or
disappears. Generated packages and reports are deliberately not committed.

## Claim boundary

A successful run means that these repository-maintained processors pass the
current shared vectors and preserve the basic fixture in this exercise. It does
not cover an application database, hostile-input hardening, performance,
operational recovery, or independently maintained code. Before a stable 1.0
claim, the project should publish evidence from at least one external
implementation and one real application pilot.
