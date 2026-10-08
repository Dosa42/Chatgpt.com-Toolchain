"""Install and record a concrete Rust toolchain on the selected runner."""
from __future__ import annotations

import os
from pathlib import Path
import re
import shutil
import urllib.request
from .inspect import toolchain_spec
from .util import BuildError, RUST, read_json, run


def ensure_rustup(context):
    home = Path.home() / ".cargo" / "bin"
    context.env["PATH"] = str(home) + os.pathsep + context.env.get("PATH", "")
    if shutil.which("rustup", path=context.env["PATH"]):
        return
    bootstrap = read_json(RUST / "toolchains/defaults.json")["rustup"]
    machine = __import__("platform").machine().lower()
    if os.name == "nt":
        host = "aarch64-pc-windows-msvc" if machine in ("arm64", "aarch64") else "x86_64-pc-windows-msvc"
        filename = "rustup-init.exe"
    else:
        arch = "aarch64" if machine in ("arm64", "aarch64") else "x86_64"
        system = "apple-darwin" if __import__("sys").platform == "darwin" else "unknown-linux-gnu"
        host, filename = arch + "-" + system, "rustup-init"
    url = f"https://static.rust-lang.org/rustup/archive/{bootstrap}/{host}/{filename}"
    destination = context.work / filename
    with urllib.request.urlopen(url, timeout=120) as response:
        destination.write_bytes(response.read())
    destination.chmod(0o755)
    run([str(destination), "-y", "--no-modify-path", "--default-toolchain", "none"],
        env=context.env, log=context.log)


def setup(context):
    ensure_rustup(context)
    requested = context.request.get("toolchain", {})
    source = toolchain_spec(context.project, context.source_root)
    if source.get("path") and not requested.get("channel"):
        raise BuildError("A source-local custom toolchain requires an explicit installed channel")
    requested_channel = requested.get("channel") or source.get("channel") or read_json(
        RUST / "toolchains/pins.json")["rust"]
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", requested_channel):
        raise BuildError("Invalid toolchain channel")
    for argv in requested.get("setup_commands", []):
        run(argv, cwd=context.project, env=context.env, log=context.log)
    install = ["rustup", "toolchain", "install", requested_channel, "--profile", "minimal"]
    if not requested.get("custom", False):
        run(install, env=context.env, log=context.log)
    info = run(["rustup", "run", requested_channel, "rustc", "-Vv"],
               env=context.env, log=context.log).stdout
    values = dict(line.split(": ", 1) for line in info.splitlines() if ": " in line)
    concrete = requested_channel
    if not requested.get("custom", False) and requested_channel in ("stable", "beta", "nightly"):
        release = values["release"]
        concrete = ("nightly-" + values["commit-date"] if "nightly" in release else
                    "beta-" + values["commit-date"] if "beta" in release else release)
        run(["rustup", "toolchain", "install", concrete, "--profile", "minimal"],
            env=context.env, log=context.log)
    components = set(source.get("components", [])) | set(requested.get("components", []))
    if context.definition["id"] == "lint":
        components.update(("rustfmt", "clippy"))
    if context.request.get("build", {}).get("build_std"):
        if "nightly" not in concrete and not requested.get("custom", False):
            raise BuildError("build_std requires an explicitly selected nightly/custom toolchain")
        components.add("rust-src")
    if components:
        run(["rustup", "component", "add", "--toolchain", concrete, *sorted(components)],
            env=context.env, log=context.log)
    targets = set(source.get("targets", [])) | set(requested.get("targets", []))
    if context.target.get("rustup_target"):
        targets.add(context.target["rustup_target"])
    if targets:
        run(["rustup", "target", "add", "--toolchain", concrete, *sorted(targets)],
            env=context.env, log=context.log)
    context.channel = concrete
    context.env["RUSTUP_TOOLCHAIN"] = concrete
    context.versions["requested_toolchain"] = requested_channel
    context.versions["resolved_toolchain"] = concrete
    context.versions["rustc"] = run(["rustc", "+" + concrete, "-Vv"],
                                    env=context.env, log=context.log).stdout.strip()
    context.versions["cargo"] = run(["cargo", "+" + concrete, "-V"],
                                    env=context.env, log=context.log).stdout.strip()
