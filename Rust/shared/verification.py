"""Future explicitly requested verification using real Rust programs."""
from __future__ import annotations

import os
from . import artifacts, cargo, result
from .run import Context
from .request import task
from .util import RUST, read_json, runner_environment, within, write_json


def execute(context):
    runner_environment()
    cases = read_json(RUST / "verification/suite.json")["cases"]
    completed = []
    for case in cases:
        definition = task(case["task"])
        request = {"schema_version": 1, "id": context.request["id"][:50] + "-" + case["id"],
                   "task": case["task"], "source": context.request["source"],
                   "build": case.get("build", {})}
        if case.get("standalone"):
            request["standalone"] = case["standalone"]
        work = context.work / "verification" / case["id"]
        report = context.products / "verification" / case["id"]
        products = report / "products"
        products.mkdir(parents=True)
        child = Context(request, definition, context.target, context.request_commit, work, report,
                        products, report / "build.log", dict(context.env))
        work.mkdir(parents=True)
        child.project = within(context.project, case["project"])
        child.source_root = context.source_root
        child.source = dict(context.source, verification_project=case["project"])
        child.channel = context.channel
        child.target_argument = context.target_argument
        child.versions = dict(context.versions)
        child.env["CARGO_TARGET_DIR"] = str(work / "target")
        write_json(report / "request.json", request)
        try:
            if definition["operation"] == "standalone":
                cargo.standalone(child)
            else:
                cargo.execute(child)
            child.deliverables = artifacts.collect(child)
            result.emit(child, "success")
        except Exception as error:
            result.emit(child, "failure", str(error))
            completed.append({"id": case["id"], "status": "failure", "error": str(error)})
            write_json(context.report / "verification.json", completed)
            raise
        completed.append({"id": case["id"], "status": "success"})
    write_json(context.report / "verification.json", completed)
