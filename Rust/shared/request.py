"""Validate the closed schemas used by this repository and load build requests."""
from __future__ import annotations

import re
from .util import BuildError, ROOT, RUST, read_json, within


def validate(value, schema, location="$", root=None):
    """Validator for this repository's documented JSON Schema keyword subset."""
    root = schema if root is None else root
    if "$ref" in schema:
        reference = schema["$ref"]
        if not reference.startswith("#/"):
            raise BuildError("Only local schema references are supported")
        node = root
        for token in reference[2:].split("/"):
            node = node[token.replace("~1", "/").replace("~0", "~")]
        return validate(value, node, location, root)
    kinds = {"object": lambda x: isinstance(x, dict),
             "array": lambda x: isinstance(x, list),
             "string": lambda x: isinstance(x, str),
             "integer": lambda x: isinstance(x, int) and not isinstance(x, bool),
             "number": lambda x: isinstance(x, (int, float)) and not isinstance(x, bool),
             "boolean": lambda x: isinstance(x, bool), "null": lambda x: x is None}
    if "type" in schema:
        allowed = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(kinds[kind](value) for kind in allowed):
            raise BuildError(f"{location}: expected {allowed}")
    if "enum" in schema and value not in schema["enum"]:
        raise BuildError(f"{location}: value is not in the allowed set")
    if "const" in schema and value != schema["const"]:
        raise BuildError(f"{location}: unexpected constant")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            raise BuildError(f"{location}: string is too short")
        if len(value) > schema.get("maxLength", len(value)):
            raise BuildError(f"{location}: string is too long")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            raise BuildError(f"{location}: invalid format")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if value < schema.get("minimum", value) or value > schema.get("maximum", value):
            raise BuildError(f"{location}: number is outside the allowed range")
    if isinstance(value, dict):
        missing = set(schema.get("required", [])) - set(value)
        if missing:
            raise BuildError(f"{location}: missing keys {sorted(missing)}")
        properties = schema.get("properties", {})
        extra = schema.get("additionalProperties", True)
        for key, child in value.items():
            if key in properties:
                validate(child, properties[key], f"{location}.{key}", root)
            elif extra is False:
                raise BuildError(f"{location}: unknown key {key}")
            elif isinstance(extra, dict):
                validate(child, extra, f"{location}.{key}", root)
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0) or len(value) > schema.get("maxItems", len(value)):
            raise BuildError(f"{location}: invalid array length")
        if schema.get("uniqueItems") and len({repr(x) for x in value}) != len(value):
            raise BuildError(f"{location}: duplicate array entries")
        for index, item in enumerate(value):
            validate(item, schema.get("items", {}), f"{location}[{index}]", root)


def load(path):
    request = read_json(path)
    validate(request, read_json(RUST / "schemas/request.schema.json"))
    source = request["source"]
    import os
    if (source.get("repository") and source["repository"] != os.environ.get("GITHUB_REPOSITORY", "Dosa42/Chatgpt.com-Toolchain")
        and not source.get("ref")):
        raise BuildError("An external source repository requires an explicit source.ref")
    if request.get("build", {}).get("all_features") and request.get("build", {}).get("features"):
        raise BuildError("Use all_features or specific features, not both")
    return request


def task(task_id):
    catalog = read_json(RUST / "catalog.json")
    found = [entry for entry in catalog["tasks"] if entry["id"] == task_id]
    if len(found) != 1:
        raise BuildError(f"Unknown or duplicated task: {task_id}")
    definition = read_json(within(ROOT, found[0]["definition"]))
    validate(definition, read_json(RUST / "schemas/task.schema.json"))
    return definition


def target(target_id):
    found = [entry for entry in read_json(RUST / "targets/catalog.json")["targets"]
             if entry["triple"] == target_id]
    if len(found) != 1:
        raise BuildError(f"Target is not configured: {target_id}")
    definition = read_json(within(ROOT, found[0]["definition"]))
    validate(definition, read_json(RUST / "schemas/target.schema.json"))
    return definition


def select_targets(request, definition):
    chosen = request.get("build", {}).get("targets", definition["default_targets"])
    if not chosen:
        raise BuildError("At least one target must be specified")
    targets = [target(item) for item in chosen]
    for entry in targets:
        if definition["families"] and entry["family"] not in definition["families"]:
            raise BuildError(f"Target {entry['triple']} is incompatible with {definition['id']}")
        if (definition["id"] in ("test", "benchmark") and not entry["can_execute"]
            and not request.get("test", {}).get("no_run")
            and not request.get("platform", {}).get("runner")):
            raise BuildError(f"No execution runner is configured for {entry['triple']}")
    return targets
