"""CLI and coordinated build execution for all Rust tasks."""
from __future__ import annotations

from pathlib import Path
import sys

if __package__ in (None, ""):
    # Do not let sibling inspect.py shadow Python's standard-library inspect module.
    script_directory = Path(__file__).resolve().parent
    sys.path[:] = [p for p in sys.path if Path(p or ".").resolve() != script_directory]
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import argparse
import ast
from dataclasses import dataclass, field
import json
import os
import runpy
import traceback

from shared import request as requests
from shared import artifacts, result, source, target, toolchain
from shared.util import BuildError, ROOT, RUST, github_output, read_json, runner_environment, within, write_json


@dataclass
class Context:
    request: dict
    definition: dict
    target: dict
    request_commit: str
    work: Path
    report: Path
    products: Path
    log: Path
    env: dict
    project: Path | None = None
    source_root: Path | None = None
    source: dict = field(default_factory=dict)
    versions: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    compiler_artifacts: list = field(default_factory=list)
    deliverables: list = field(default_factory=list)
    channel: str = ""
    target_argument: str = ""
    lock: bool = False


def identity(request):
    suffix = f"{os.environ.get('GITHUB_RUN_ID', 'local')}-{os.environ.get('GITHUB_RUN_ATTEMPT', '1')}"
    return RUST / ".runs" / request["id"] / suffix


def request_from_arguments(args):
    checkout = Path(os.environ.get("RUNNER_TEMP", str(RUST / ".runs"))) / ("rust-request-" + args.task)
    path, commit = source.acquire_request(args.request_path, args.request_ref, checkout,
                                          checkout.parent / "rust-request-fetch.log")
    request = requests.load(path)
    if request["task"] != args.task:
        raise BuildError("The selected workflow/task does not match request.task")
    if args.request_id and args.request_id != request["id"]:
        raise BuildError("The dispatch request_id does not match the request file")
    return request, commit


def prepare(args):
    runner_environment()
    request, commit = request_from_arguments(args)
    definition = requests.task(args.task)
    targets = requests.select_targets(request, definition)
    matrix = {"include": [{"target": item["triple"], "runner": item["runner"]} for item in targets]}
    github_output(matrix=json.dumps(matrix, separators=(",", ":")), request_id=request["id"],
                  request_commit=commit)
    print(json.dumps({"task": args.task, "request_id": request["id"], "matrix": matrix}))


def setup(context):
    runner_environment()
    spec = dict(context.request["source"])
    if not spec.get("repository"):
        spec["repository"] = os.environ["GITHUB_REPOSITORY"]
    if not spec.get("ref") and spec["repository"] == os.environ["GITHUB_REPOSITORY"]:
        spec["ref"] = context.request_commit
    context.source_root = context.work / "source"
    context.project, context.source = source.acquire(spec, context.source_root, context.log)
    # Source-fetch credentials must not leak into arbitrary source build scripts.
    context.env.pop("GH_TOKEN", None)
    context.env.pop("SOURCE_TOKEN", None)
    for key in context.request.get("environment", {}):
        if key.startswith(("GITHUB_", "RUNNER_")) or key in ("GH_TOKEN", "SOURCE_TOKEN", "RUSTUP_TOOLCHAIN", "CARGO_TARGET_DIR"):
            raise BuildError(f"Request cannot override reserved environment variable: {key}")
    target.setup(context)
    toolchain.setup(context)
    context.env["CARGO_TARGET_DIR"] = str(context.work / "target")
    runner = context.request.get("platform", {}).get("runner")
    if runner:
        configuration = context.work / "runner.toml"
        triple = context.target["triple"]
        configuration.write_text(f'[target.{json.dumps(triple)}]\nrunner = {json.dumps(runner)}\n', encoding="utf-8")
        context.request.setdefault("build", {}).setdefault("cargo_config", []).append(str(configuration))


def execute(args):
    runner_environment()
    request, commit = request_from_arguments(args)
    definition = requests.task(args.task)
    candidates = requests.select_targets(request, definition)
    selected = [t for t in candidates if t["triple"] == args.target]
    if len(selected) != 1:
        raise BuildError("The matrix target does not match the validated request")
    work = identity(request) / args.target
    report = work / "report"
    products = report / "products"
    products.mkdir(parents=True, exist_ok=False)
    context = Context(request, definition, selected[0], commit, work, report,
                      products, report / "build.log", dict(os.environ))
    write_json(report / "request.json", request)
    code = 0
    try:
        directory = within(ROOT, definition["directory"])
        runpy.run_path(str(directory / "scripts/setup.py"))["setup"](context)
        runpy.run_path(str(directory / "scripts/execute.py"))["execute"](context)
        context.deliverables = artifacts.collect(context)
        result.emit(context, "success")
    except Exception as error:
        code = 1
        (report / "exception.txt").write_text(traceback.format_exc(), encoding="utf-8")
        result.emit(context, "failure", str(error))
        print(f"Build failed: {error}", file=sys.stderr)
    return code


def static_check():
    """No compiler, subprocess, installer, network request or workflow dispatch."""
    catalog = read_json(RUST / "catalog.json")
    identifiers = []
    for entry in catalog["tasks"]:
        definition = requests.task(entry["id"])
        identifiers.append(entry["id"])
        for path in (entry["definition"], entry["workflow"], definition["directory"] + "/README.md",
                     definition["directory"] + "/scripts/setup.py", definition["directory"] + "/scripts/execute.py", definition["configuration"]):
            if not within(ROOT, path).is_file():
                raise BuildError(f"Missing linked file: {path}")
        workflow = within(ROOT, entry["workflow"]).read_text(encoding="utf-8")
        if "workflow_dispatch:" not in workflow or any(x in workflow for x in ("  push:", "  pull_request:", "  schedule:")):
            raise BuildError(f"Invalid trigger model: {entry['workflow']}")
        if f"--task {entry['id']}" not in workflow:
            raise BuildError(f"Workflow/task mismatch: {entry['workflow']}")
        for triple in definition["default_targets"]:
            requests.target(triple)
    if len(set(identifiers)) != len(identifiers):
        raise BuildError("Duplicate task identifiers")
    for path in RUST.rglob("*.json"):
        if ".runs" not in path.parts:
            read_json(path)
    for path in RUST.rglob("*.py"):
        if ".runs" not in path.parts:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for path in (RUST / "requests").glob("*.json"):
        value = requests.load(path)
        requests.select_targets(value, requests.task(value["task"]))
    print(json.dumps({"status": "static-check-passed", "tasks": len(identifiers),
                      "builds_executed": 0, "workflows_started": 0}))


def main(forced_task=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "execute", "static-check"))
    parser.add_argument("--task", default=forced_task)
    parser.add_argument("--request-path", default=os.environ.get("REQUEST_PATH", ""))
    parser.add_argument("--request-ref", default=os.environ.get("REQUEST_REF", ""))
    parser.add_argument("--request-id", default=os.environ.get("REQUEST_ID", ""))
    parser.add_argument("--target", default=os.environ.get("BUILD_TARGET", ""))
    args = parser.parse_args()
    if forced_task and args.task != forced_task:
        parser.error("This entry point is bound to a different task")
    try:
        if args.command == "static-check":
            static_check()
            return 0
        if not args.task or not args.request_path:
            parser.error("--task and --request-path are required")
        if args.command == "prepare":
            prepare(args)
            return 0
        return execute(args)
    except Exception as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
