# Security policy

Do not publicly disclose a validator or parser vulnerability that could cause
code execution, path traversal, arbitrary file overwrite, or resource
exhaustion. Report it privately through the repository host's security advisory
feature. If that feature is unavailable, contact a maintainer through a private
channel listed on their profile.

The current repository supplies an experimental validator, not a hardened
archive extractor. Packages are untrusted input. Implementations must constrain
archive paths and sizes, parsing depth, decompressed bytes, record counts, and
attachment sizes; must not execute content; and must sanitize rendered Markdown
and filenames. SHA-256 fields detect accidental or malicious content changes but
do not authenticate an owner or producer.
