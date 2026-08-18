#!/usr/bin/env python3
"""Development parser for the language-neutral Engram front-matter corpus."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from yaml import tokens as yaml_tokens


class ParseError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


class EngramLoader(yaml.SafeLoader):
    pass


EngramLoader.yaml_implicit_resolvers = {}
EngramLoader.add_implicit_resolver("tag:yaml.org,2002:null", re.compile(r"^null$"), ["n"])
EngramLoader.add_implicit_resolver("tag:yaml.org,2002:bool", re.compile(r"^(?:true|false)$"), ["t", "f"])
EngramLoader.add_implicit_resolver("tag:yaml.org,2002:int", re.compile(r"^-?(?:0|[1-9][0-9]*)$"), list("-0123456789"))
EngramLoader.add_implicit_resolver(
    "tag:yaml.org,2002:float",
    re.compile(r"^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+(?:[eE][+-]?[0-9]+)?|[eE][+-]?[0-9]+)$"),
    list("-0123456789"),
)


def unique_mapping(loader: EngramLoader, node: yaml.MappingNode, deep: bool = False) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise ParseError("yaml-non-string-key", "front-matter mapping keys must be strings")
        if key == "<<":
            raise ParseError("yaml-forbidden-feature", "YAML merge keys are not permitted")
        if key in result:
            raise ParseError("yaml-duplicate-key", f"duplicate YAML key {key!r}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


EngramLoader.add_constructor("tag:yaml.org,2002:map", unique_mapping)


def parse_record(path: Path, max_record_bytes: int) -> dict[str, Any]:
    raw = path.read_bytes()
    if len(raw) > max_record_bytes:
        raise ParseError("resource-limit", "record exceeds max_record_bytes")
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ParseError("bom-not-allowed", "UTF-8 byte-order mark is not permitted")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ParseError("encoding-invalid", str(exc)) from exc
    if re.search(r"\r(?!\n)", text):
        raise ParseError("line-ending-invalid", "bare CR line ending is not permitted")
    lines = text.splitlines(keepends=True)
    if not lines or lines[0] not in ("---\n", "---\r\n"):
        raise ParseError("delimiter-invalid", "opening delimiter must be the first exact line")
    closing = next((i for i, line in enumerate(lines[1:], 1) if line.removesuffix("\n").removesuffix("\r") == "---"), None)
    if closing is None:
        raise ParseError("delimiter-invalid", "missing exact closing delimiter")
    front_matter = "".join(lines[1:closing])
    try:
        for token in yaml.scan(front_matter, Loader=EngramLoader):
            if isinstance(token, (yaml_tokens.TagToken, yaml_tokens.AnchorToken, yaml_tokens.AliasToken)):
                raise ParseError("yaml-forbidden-feature", "tags, anchors, and aliases are not permitted")
            if isinstance(token, (yaml_tokens.DirectiveToken, yaml_tokens.DocumentStartToken, yaml_tokens.DocumentEndToken)):
                raise ParseError("yaml-forbidden-feature", "directives and document markers are not permitted")
            if isinstance(token, (yaml_tokens.FlowMappingStartToken, yaml_tokens.FlowSequenceStartToken)):
                raise ParseError("yaml-forbidden-feature", "flow collections are not permitted")
        value = yaml.load(front_matter, Loader=EngramLoader)
    except ParseError:
        raise
    except yaml.YAMLError as exc:
        raise ParseError("yaml-invalid", str(exc)) from exc
    if not isinstance(value, dict):
        raise ParseError("front-matter-not-mapping", "front matter must be a mapping")
    return value


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] != "parse":
        print("usage: frontmatter_parser.py parse REQUEST.json", file=sys.stderr)
        return 2
    request = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    base = {"protocol_version": "1.0", "case_id": request["case_id"]}
    try:
        value = parse_record(Path(request["record"]), int(request.get("max_record_bytes", 1048576)))
        result = {**base, "outcome": "accepted", "front_matter": value}
    except ParseError as exc:
        result = {**base, "outcome": "rejected", "diagnostic": {"code": exc.code, "message": str(exc)}}
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
