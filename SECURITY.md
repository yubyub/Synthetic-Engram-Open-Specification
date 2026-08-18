# Security policy

## Supported versions

| Version | Status |
| --- | --- |
| 0.2.x | Pilot; security fixes are accepted on the active line |
| Earlier drafts | Unsupported |

Because 0.2 is pre-stable and has no production SDK, response times and private
patch delivery are best effort. Public advisories should distinguish format
weaknesses from vulnerabilities in a particular application.

Do not publicly disclose a validator or parser vulnerability that could cause
code execution, path traversal, arbitrary file overwrite, or resource
exhaustion. Report it privately through the repository host's security advisory
feature. If that feature is unavailable, contact a maintainer through a private
channel listed on their profile.

The current repository supplies a pilot validator and processors, not a hardened
archive extractor. Packages are untrusted input. Implementations must constrain
archive paths and sizes, parsing depth, decompressed bytes, record counts, and
attachment sizes; must not execute content; and must sanitize rendered Markdown
and filenames. SHA-256 fields detect accidental or malicious content changes but
do not authenticate an owner or producer.

External references, ordinary links, and any future Source Reference objects
must be treated as untrusted data. Import, validation, preview, graph traversal,
or rendering must not automatically fetch them or execute a named plugin.
Resolvers must apply authentication, per-object authorization, scheme and
destination policy, SSRF and redirect controls, response limits, and safe
content handling. Portable references must not contain credentials, access
tokens, cookies, private keys, or authorization grants.
