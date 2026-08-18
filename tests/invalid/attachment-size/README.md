# Basic Synthetic Engram

This directory is a complete v0.1 package. It demonstrates:

- a project containing two notes and an action through `parent` references;
- typed links between records;
- a portable graph whose nodes reference records;
- one namespaced extension;
- a text attachment with declared byte size and SHA-256 digest; and
- all four v0.1 conformance profiles.

Run `python scripts/validate.py examples/basic-engram` from the repository root.
Files use fixed illustrative ULIDs so references are easy to follow; production
systems must generate collision-resistant IDs.
