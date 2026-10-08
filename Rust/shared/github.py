"""Explicit GitHub API dispatch, run tracking and binary artifact download.

Nothing starts on import. Dispatch happens only with the dispatch CLI subcommand.
Credentials are read from GH_TOKEN/GITHUB_TOKEN and are never embedded in requests.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


class Client:
    def __init__(self, repository, token=None):
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
            raise ValueError("Expected owner/repository")
        self.repository = repository
        self.token = token or os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("A GitHub token with the required repository permissions is required")
        self.base = "https://api.github.com/repos/" + repository

    def request(self, path, payload=None):
        data = json.dumps(payload).encode() if payload is not None else None
        headers = {"Accept": "application/vnd.github+json", "Authorization": "Bearer " + self.token,
                   "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "Chatgpt.com-Toolchain"}
        if data is not None:
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(self.base + path, data=data, headers=headers)
        with urllib.request.urlopen(request, timeout=60) as response:
            content = response.read()
            return json.loads(content) if content else {}

    def dispatch(self, workflow, ref, request_path, request_ref, request_id):
        if not re.fullmatch(r"rust-[a-z0-9-]+\.yml", workflow):
            raise ValueError("Expected a Rust workflow filename")
        when = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.request("/actions/workflows/" + urllib.parse.quote(workflow, safe="") + "/dispatches",
                     {"ref": ref, "inputs": {"request_path": request_path,
                                               "request_ref": request_ref, "request_id": request_id}})
        # GitHub's dispatch response alone does not prove a run has started or succeeded.
        return {"dispatch_accepted": True, "workflow": workflow, "request_id": request_id,
                "dispatched_at": when, "build_status": "not_observed"}

    def find_run(self, workflow, request_id, dispatched_at):
        for page in range(1, 11):
            payload = self.request(f"/actions/workflows/{urllib.parse.quote(workflow, safe='')}/runs?event=workflow_dispatch&per_page=100&page={page}")
            matches = [run for run in payload["workflow_runs"]
                       if run.get("display_title", "").endswith(" | " + request_id)
                       and run["created_at"] >= dispatched_at[:19] + "Z"]
            if len(matches) > 1:
                raise ValueError("Request ID matched multiple runs; use the exact run_id")
            if matches:
                return matches[0]
            if len(payload["workflow_runs"]) < 100:
                return None
        raise ValueError("Run search exceeded 1000 runs; select an exact run_id")

    def artifacts(self, run_id):
        result = []
        page = 1
        while True:
            payload = self.request(f"/actions/runs/{int(run_id)}/artifacts?per_page=100&page={page}")
            result.extend(payload["artifacts"])
            if len(payload["artifacts"]) < 100:
                return result
            page += 1

    def download(self, artifact_id, destination):
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                return None
        url = self.base + f"/actions/artifacts/{int(artifact_id)}/zip"
        req = urllib.request.Request(url, headers={"Authorization": "Bearer " + self.token,
            "Accept": "application/vnd.github+json", "User-Agent": "Chatgpt.com-Toolchain"})
        opener = urllib.request.build_opener(NoRedirect)
        try:
            response = opener.open(req, timeout=60)
        except urllib.error.HTTPError as error:
            if error.code != 302:
                raise
            location = error.headers["Location"]
            if urllib.parse.urlparse(location).scheme != "https":
                raise ValueError("Artifact redirect must use HTTPS")
            # The signed storage URL is opened without forwarding the GitHub token.
            response = urllib.request.urlopen(location, timeout=120)
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(destination.name + ".part")
        try:
            with response, temporary.open("wb") as stream:
                while block := response.read(1024 * 1024):
                    stream.write(block)
            temporary.replace(destination)
        except Exception:
            temporary.unlink(missing_ok=True)
            raise
        return {"artifact_id": int(artifact_id), "path": str(destination), "bytes": destination.stat().st_size}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", default="Dosa42/Chatgpt.com-Toolchain")
    commands = parser.add_subparsers(dest="command", required=True)
    dispatch = commands.add_parser("dispatch")
    dispatch.add_argument("--workflow", required=True)
    dispatch.add_argument("--ref", default="main")
    dispatch.add_argument("--request-path", required=True)
    dispatch.add_argument("--request-ref", required=True)
    dispatch.add_argument("--request-id", required=True)
    watch = commands.add_parser("watch")
    watch.add_argument("--run-id", type=int, required=True)
    watch.add_argument("--timeout", type=int, default=3600)
    download = commands.add_parser("download")
    download.add_argument("--run-id", type=int, required=True)
    download.add_argument("--directory", required=True)
    find = commands.add_parser("find-run")
    find.add_argument("--workflow", required=True)
    find.add_argument("--request-id", required=True)
    find.add_argument("--dispatched-at", required=True)
    args = parser.parse_args()
    client = Client(args.repository)
    if args.command == "dispatch":
        output = client.dispatch(args.workflow, args.ref, args.request_path, args.request_ref, args.request_id)
    elif args.command == "find-run":
        output = client.find_run(args.workflow, args.request_id, args.dispatched_at)
    elif args.command == "watch":
        deadline = time.monotonic() + args.timeout
        while True:
            output = client.request(f"/actions/runs/{args.run_id}")
            if output["status"] == "completed":
                break
            if time.monotonic() >= deadline:
                raise TimeoutError("Run is still pending; it has not been reported as successful")
            time.sleep(10)
    else:
        output = []
        for artifact in client.artifacts(args.run_id):
            if artifact["expired"]:
                raise ValueError(f"Artifact {artifact['id']} has expired")
            name = artifact["name"]
            if not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
                raise ValueError("Unsafe artifact filename")
            output.append(client.download(artifact["id"], Path(args.directory) / (name + ".zip")))
    print(json.dumps(output, indent=2))
    if args.command == "watch" and output.get("conclusion") != "success":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
