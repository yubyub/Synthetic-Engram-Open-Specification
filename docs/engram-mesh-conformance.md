# Engram Mesh 0.3 conformance

The canonical 0.3 representation is a UTF-8 JSON file named `engram-mesh.json`
that conforms to `schemas/v0.3/mesh.schema.json` and the semantic requirements
in [`SPEC.md`](../SPEC.md).

The repository's dependency-free validator checks UTF-8 and unique JSON keys,
closed core objects, identifier shape and global uniqueness, source and resolver
shape, binding generation/lifecycle/successors, single authority, capability
restriction, freshness evidence, relationship resolution, single-parent acyclic
hierarchy, slice closure and privacy-safe boundaries, and lens completeness.

```sh
python3 scripts/validate_engram_mesh.py
python3 scripts/validate_engram_mesh.py examples/v0.3/basic-mesh/engram-mesh.json
python3 scripts/run_engram_mesh_adapter_tests.py
```

After installing `requirements-dev.txt`, also run
`python3 scripts/validate_engram_mesh_schema.py` to validate the schemas against
the Draft 2020-12 meta-schema and check every positive fixture and example with
the schema validator. CI runs both layers.

The Python and Node adapters are prototype conformance exercises, not
independent implementations or production SDKs. A conforming producer or
consumer must report its version, role, capabilities, and binding. A source
adapter must never put credentials in the portable document and must enforce
authorization at execution time.

See [requirement traceability](engram-mesh-traceability.md) for the boundary
between static validation and the runtime evidence required from an adapter.

The fixtures include a valid cross-source mesh, a valid source move, and invalid
cases for endpoint resolution, hierarchy cycles, multiple authorities,
capability escalation, unsafe resolver disclosure, incomplete complete slices,
and unauthorized boundary identity disclosure. Each invalid fixture names the
diagnostic it must trigger so it cannot pass by failing for an unrelated reason.

Loss-aware OKF materialization remains mapping guidance rather than core
conformance because Engram Mesh does not yet define an OKF extension or bundle
sidecar.
