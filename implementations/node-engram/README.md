# Node Engram Package Processor

Version **1.0.0**. Roles: **producer, consumer, round-trip**. Processing and
preservation profiles: **core, graph, media, action**.

**Maturity:** reference interoperability implementation. This executable is
conformance evidence, not a production SDK, supported service, or security
certification. See the project [maturity matrix](../../docs/status.md) and
[SDK release criteria](../../docs/development/sdk-release-criteria.md).

The executable is implemented independently with Node built-ins. It owns its
JSON/UTF-8 inventory parser, attachment-link discovery, safety checks, and
four-space JSON serializer and imports no repository validator or Python code.
