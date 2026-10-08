"""Process, path and JSON primitives shared by every task."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
RUST = ROOT / "Rust"


class BuildError(RuntimeError):
    pass


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def within(root, relative):
    root = Path(root).resolve()
    value = Path(relative)
    if value.is_absolute():
        raise BuildError(f"Expected a relative path: {relative}")
    candidate = (root / value).resolve()
    if not candidate.is_relative_to(root):
        raise BuildError(f"Path escapes its root: {relative}")
    return candidate


def digest(path):
    result = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def run(argv, *, cwd=None, env=None, log=None, check=True, timeout=None):
    """Execute an argument vector, without a shell. Preserve the actual exit code."""
    argv = [str(item) for item in argv]
    if not argv:
        raise BuildError("Empty command")
    started = time.monotonic()
    process = subprocess.run(argv, cwd=cwd, env=env, capture_output=True,
                             timeout=timeout, text=True, encoding="utf-8", errors="replace")
    if log:
        path = Path(log)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as out:
            out.write(json.dumps({"argv": argv, "exit_code": process.returncode,
                                  "duration_seconds": round(time.monotonic()-started, 3)}) + "\n")
            out.write(process.stdout)
            out.write(process.stderr)
    if process.stderr:
        print(process.stderr, end="", flush=True)
    if process.returncode and process.stdout:
        print(process.stdout, end="", flush=True)
    if check and process.returncode:
        raise BuildError(f"Command failed ({process.returncode}): {argv[0]}; see build logs")
    return process


def runner_environment():
    if os.environ.get("GITHUB_ACTIONS") != "true":
        raise BuildError("Build execution is restricted to GitHub Actions runners")


def github_output(**values):
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as stream:
            for key, value in values.items():
                text = str(value)
                if "\n" in text or "\r" in text:
                    raise BuildError("Multiline workflow output is not supported here")
                stream.write(f"{key}={text}\n")
