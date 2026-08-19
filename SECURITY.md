# Security policy

## Supported versions

| Version | Status |
| --- | --- |
| Engram Mesh 0.3.x | Pilot model, schemas, and validator; security and privacy fixes accepted |
| Synthetic Engram 0.2.x | Legacy pilot; parser and package security fixes are accepted |
| Earlier drafts | Unsupported |

Because both lines are pre-stable and have no production SDK, response times and private
patch delivery are best effort. Public advisories should distinguish format
weaknesses from vulnerabilities in a particular application.

Do not publicly disclose a validator or parser vulnerability that could cause
code execution, path traversal, arbitrary file overwrite, or resource
exhaustion. Report it privately through the repository host's security advisory
feature. If that feature is unavailable, contact a maintainer through a private
channel listed on their profile.

The Engram Mesh validator is a document conformance tool, not a hardened Source
resolver or authorization boundary. Treat source metadata, resolver results,
materialized content, relationships, extensions, and Lens expressions as
untrusted input. Keep credentials and local connection state out of portable
documents. Constrain document size, parsing depth, network and filesystem scope,
redirects, retries, and returned content. Authorize every disclosure and
mutation against the Source at execution time; capabilities and mesh membership
are not permission.

The legacy Synthetic Engram validator and processors are not hardened archive
extractors. Legacy packages remain untrusted and require constrained archive
paths and sizes, parsing depth, decompressed bytes, record counts, and attachment
sizes. Legacy hashes provide integrity evidence, not authenticity or authority.
