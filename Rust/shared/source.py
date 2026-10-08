"""Acquire an immutable source tree separately from the infrastructure checkout."""
from __future__ import annotations

import base64
import os
from pathlib import Path
import re
from .util import BuildError, ROOT, run, within, write_json


def git_environment(token):
    env = dict(os.environ)
    env["GIT_TERMINAL_PROMPT"] = "0"
    if token:
        # Git configuration is passed through the environment, never written into a URL or log.
        env["GIT_CONFIG_COUNT"] = "1"
        env["GIT_CONFIG_KEY_0"] = "http.https://github.com/.extraheader"
        encoded = base64.b64encode(("x-access-token:" + token).encode()).decode()
        env["GIT_CONFIG_VALUE_0"] = "AUTHORIZATION: basic " + encoded
    return env


def fetch_repository(repository, ref, destination, log):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise BuildError("Expected a GitHub owner/repository")
    if not ref or ref.startswith("-") or any(x in ref for x in ("\n", "\r", " ")):
        raise BuildError("Invalid source ref")
    destination = Path(destination)
    if destination.exists():
        raise BuildError(f"Source destination already exists: {destination}")
    destination.mkdir(parents=True)
    token = (os.environ.get("GH_TOKEN", "") if repository == os.environ.get("GITHUB_REPOSITORY")
             else os.environ.get("SOURCE_TOKEN") or os.environ.get("GH_TOKEN", ""))
    env = git_environment(token)
    run(["git", "init", str(destination)], log=log)
    run(["git", "remote", "add", "origin", f"https://github.com/{repository}.git"],
        cwd=destination, log=log)
    run(["git", "fetch", "--depth=1", "origin", ref], cwd=destination, env=env, log=log)
    run(["git", "checkout", "--detach", "FETCH_HEAD"], cwd=destination, log=log)
    sha = run(["git", "rev-parse", "HEAD"], cwd=destination, log=log).stdout.strip()
    return sha, env


def acquire(specification, destination, log):
    repository = specification.get("repository") or os.environ.get("GITHUB_REPOSITORY")
    if not repository:
        raise BuildError("Source repository is required outside a GitHub workflow")
    ref = specification.get("ref") or os.environ.get("GITHUB_SHA")
    if not ref:
        raise BuildError("Source ref is required")
    sha, env = fetch_repository(repository, ref, destination, log)
    if specification.get("submodules"):
        run(["git", "submodule", "update", "--init", "--recursive", "--depth=1"],
            cwd=destination, env=env, log=log)
    project = within(destination, specification.get("path", "."))
    if not project.is_dir():
        raise BuildError("Source project path is not a directory")
    description = {"repository": repository, "requested_ref": ref, "commit": sha,
                   "path": specification.get("path", "."),
                   "submodules": specification.get("submodules", False)}
    return project, description


def acquire_request(path, ref, destination, log):
    """Read a request from a separately selected, immutable commit of this repo."""
    if not path.startswith("Rust/requests/") or not path.endswith(".json"):
        raise BuildError("Request path must be a JSON file under Rust/requests/")
    within(ROOT, path)
    repository = os.environ["GITHUB_REPOSITORY"]
    commit, _ = fetch_repository(repository, ref or os.environ["GITHUB_SHA"], destination, log)
    request_path = within(destination, path)
    if not request_path.is_file():
        raise BuildError("Request file does not exist at the specified ref")
    return request_path, commit
