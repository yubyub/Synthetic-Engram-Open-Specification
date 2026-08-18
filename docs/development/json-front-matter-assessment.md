# JSON front matter assessment

**Status:** non-normative; no Core 1.0 change

JSON would remove YAML implicit-typing and feature-control differences and let
implementers reuse strict duplicate-key-aware JSON tooling. It would also make
the record envelope less familiar to Markdown tools, require a new delimiter or
media convention, create two record serializations, and force consumers to
negotiate which byte form they preserve. Merely placing JSON between YAML
delimiters would still be YAML flow syntax, which Core 1.0 forbids.

The immediate implementation problem is better addressed by the standalone
restricted grammar, shared corpus, differential tests, and future maintained
parsing libraries. Core 1.0 therefore remains unchanged.

Reopen a JSON binding only if independent pilots show repeated parser defects or
material integration cost after using the corpus and SDK APIs. Any proposal must
be an explicitly selected, versioned serialization binding with unambiguous media
identification, byte-preservation and conversion rules, migration guidance,
security analysis, and two independent implementations. It must not reinterpret
existing `.md` record bytes.
