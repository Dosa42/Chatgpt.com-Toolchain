"""Write a truthful report on success and failure."""
from __future__ import annotations

import datetime
import os
import platform
from .request import validate
from .util import RUST, read_json, write_json


def emit(context, status, error=None):
    result = {"schema_version": 1, "status": status,
              "request_id": context.request["id"], "task": context.definition["id"],
              "target": context.target["triple"], "source": context.source,
              "request_commit": context.request_commit,
              "infrastructure_commit": os.environ.get("GITHUB_SHA", ""),
              "run_id": os.environ.get("GITHUB_RUN_ID", ""),
              "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT", ""),
              "run_url": f"https://github.com/{os.environ.get('GITHUB_REPOSITORY', '')}/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}",
              "runner": {"os": platform.platform(), "architecture": platform.machine(),
                         "image_os": os.environ.get("ImageOS", ""),
                         "image_version": os.environ.get("ImageVersion", ""),
                         "python": platform.python_version()},
              "versions": context.versions, "artifacts": context.deliverables,
              "completed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "error": error}
    validate(result, read_json(RUST / "schemas/result.schema.json"))
    write_json(context.report / "result.json", result)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as out:
            out.write(f"## Rust {context.definition['id']}\n\n")
            out.write(f"Request: `{context.request['id']}` · Target: `{context.target['triple']}` · Status: **{status}**\n\n")
            out.write(f"Source commit: `{context.source.get('commit', 'not acquired')}`\n\n")
            out.write("The downloadable report contains result.json, logs and available products.\n")
    return result
