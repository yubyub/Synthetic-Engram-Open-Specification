# Basic Synthetic Engram

This directory is a complete v1.0 package. It demonstrates:

- a project containing two notes and an action through `parent` references;
- typed links between records;
- a portable graph that represents every project, note, and action record and
  mirrors their meaningful containment and dependency relationships;
- one namespaced extension;
- a text attachment with declared byte size and SHA-256 digest; and
- all four v1.0 conformance profiles.

Run `python scripts/validate.py examples/v1.0/basic-engram` from the repository root.
Files use fixed illustrative ULIDs so references are easy to follow; production
systems must generate collision-resistant IDs.
