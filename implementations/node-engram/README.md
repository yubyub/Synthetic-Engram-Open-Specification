# Node Engram Package Processor

Version **0.2.0**. Roles: **producer, consumer, round-trip**. Processing and
preservation profiles: **core, graph, media, action**.

**Maturity:** repository-maintained pilot processor. This executable exercises
the conformance vectors; it is not an independently maintained implementation,
production SDK, supported service, or security certification.

The executable is separately implemented with Node built-ins. It owns its
JSON/UTF-8 inventory parser, attachment-link discovery, safety checks, and
four-space JSON serializer and imports no repository validator or Python code.
