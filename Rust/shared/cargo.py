"""Cargo command construction, lock resolution and actual task execution."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
from .inspect import metadata, project_manifest
from .util import BuildError, digest, run, within


def base(context, operation, selection=True, target=True, profile=True):
    build = context.request.get("build", {})
    command = ["cargo", "+" + context.channel, operation,
               "--manifest-path", str(project_manifest(context.project, context.request))]
    if selection:
        if build.get("workspace", False):
            command.append("--workspace")
        for package in build.get("packages", []):
            command.extend(("--package", package))
        for package in build.get("exclude", []):
            if not build.get("workspace"):
                raise BuildError("Package exclusions require workspace=true")
            command.extend(("--exclude", package))
    if target:
        command.extend(("--target", context.target_argument))
    if profile:
        command.extend(("--profile", build.get("profile", context.definition["default_profile"])))
    if build.get("all_features"):
        command.append("--all-features")
    if build.get("no_default_features"):
        command.append("--no-default-features")
    if build.get("features"):
        command.extend(("--features", ",".join(build["features"])))
    if context.lock:
        command.append("--locked")
    if build.get("offline"):
        command.append("--offline")
    build_std = build.get("build_std", context.target.get("build_std", []))
    if build_std:
        command.extend(("-Z", "build-std=" + ",".join(build_std)))
    for option in build.get("cargo_config", []):
        command.extend(("--config", option))
    return command


def lock_and_inspect(context):
    data = metadata(context)
    workspace = Path(data["workspace_root"])
    if not workspace.resolve().is_relative_to(context.source_root.resolve()):
        raise BuildError("Cargo workspace is outside the acquired source checkout")
    lock = workspace / "Cargo.lock"
    # metadata resolves a missing lockfile. Existing lockfiles are protected before metadata.
    context.lock = lock.is_file()
    if not context.lock:
        run(base(context, "generate-lockfile", selection=False, target=False, profile=False),
            cwd=context.project, env=context.env, log=context.log)
    if not lock.is_file():
        raise BuildError("Cargo did not produce a lockfile")
    context.lock = True
    shutil.copy2(lock, context.report / "Cargo.lock")
    context.versions["dependency_lock_sha256"] = digest(lock)
    return data


def target_selection(request):
    build = request.get("build", {})
    selection = []
    if build.get("lib"):
        selection.append("--lib")
    if build.get("all_targets"):
        selection.append("--all-targets")
    for name in build.get("bins", []):
        selection.extend(("--bin", name))
    for name in build.get("examples", []):
        selection.extend(("--example", name))
    return selection


def cargo_messages(context, argv):
    argv = [*argv, "--message-format=json"]
    response = run(argv, cwd=context.project, env=context.env, log=context.log, check=False)
    (context.report / "cargo-messages.jsonl").write_text(response.stdout, encoding="utf-8")
    for line in response.stdout.splitlines():
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue
        if message.get("reason") == "compiler-artifact":
            artifact = {"package_id": message["package_id"], "target": message["target"],
                        "filenames": message.get("filenames", []),
                        "executable": message.get("executable"), "fresh": message.get("fresh", False)}
            context.compiler_artifacts.append(artifact)
    if response.returncode:
        raise BuildError(f"Cargo failed ({response.returncode}); see build.log and cargo-messages.jsonl")


def wasm_bindings(context):
    mode = context.request.get("wasm", {}).get("bindings", False)
    if not mode:
        return
    packages = [item for item in context.metadata["packages"] if item["name"] == "wasm-bindgen"]
    versions = {item["version"] for item in packages}
    if len(versions) != 1:
        raise BuildError("Bindings require exactly one resolved wasm-bindgen crate version")
    version = versions.pop()
    tools = context.work / "tools"
    run(["cargo", "+" + context.channel, "install", "wasm-bindgen-cli", "--version", version,
         "--locked", "--root", str(tools)], env=context.env, cwd=context.work, log=context.log)
    executable = tools / "bin" / ("wasm-bindgen.exe" if __import__("os").name == "nt" else "wasm-bindgen")
    output = context.products / "wasm-bindings"
    for artifact in context.compiler_artifacts:
        if artifact["package_id"] not in context.metadata["workspace_members"]:
            continue
        for filename in artifact["filenames"]:
            if filename.endswith(".wasm"):
                run([str(executable), filename, "--target", context.request.get("wasm", {}).get("bindgen_target", "web"),
                     "--out-dir", str(output / artifact["target"]["name"])],
                    env=context.env, cwd=context.project, log=context.log)
    if not output.is_dir():
        raise BuildError("No workspace .wasm artifact was produced for bindings")
    context.versions["wasm_bindgen_cli"] = version


def execute(context):
    task = context.definition["id"]
    # Resolve from the manifest's workspace, while preserving an existing lockfile.
    manifest = project_manifest(context.project, context.request)
    locate = ["cargo", "+" + context.channel, "locate-project", "--workspace",
              "--message-format", "json", "--manifest-path", str(manifest)]
    initial = json.loads(run(locate, cwd=context.project, env=context.env, log=context.log).stdout)
    workspace = Path(initial["root"]).parent
    if not workspace.resolve().is_relative_to(context.source_root.resolve()):
        raise BuildError("Cargo workspace is outside the acquired source checkout")
    initial_lock = workspace / "Cargo.lock"
    had_lock = initial_lock.is_file()
    context.lock = had_lock
    if had_lock:
        before = digest(initial_lock)
        # Complete dependency metadata must not silently update a supplied lockfile.
        context.metadata = json.loads(run(["cargo", "+" + context.channel,
            "metadata", "--format-version", "1", "--manifest-path", str(manifest), "--locked"],
            cwd=context.project, env=context.env, log=context.log).stdout)
        from .util import write_json
        write_json(context.report / "cargo-metadata.json", context.metadata)
        if digest(initial_lock) != before:
            raise BuildError("Source Cargo.lock changed despite locked resolution")
        shutil.copy2(initial_lock, context.report / "Cargo.lock")
        context.versions["dependency_lock_sha256"] = before
    else:
        lock_and_inspect(context)
    if task.startswith("build-"):
        cargo_messages(context, base(context, "build") + target_selection(context.request))
        if task == "build-wasm-web":
            wasm_bindings(context)
    elif task == "check":
        cargo_messages(context, base(context, "check") + target_selection(context.request))
    elif task == "test":
        argv = base(context, "test") + target_selection(context.request)
        options = context.request.get("test", {})
        if options.get("no_run"):
            argv.append("--no-run")
        elif not context.target["can_execute"] and not context.request.get("platform", {}).get("runner"):
            raise BuildError("This target cannot execute tests without an explicit target runner")
        argv.append("--message-format=json")
        if options.get("arguments"):
            argv.extend(("--", *options["arguments"]))
        response = run(argv, cwd=context.project, env=context.env, log=context.log)
        (context.report / "test-output.txt").write_text(response.stdout, encoding="utf-8")
    elif task == "lint":
        run(["cargo", "+" + context.channel, "fmt", "--manifest-path", str(manifest), "--all", "--", "--check"],
            cwd=context.project, env=context.env, log=context.log)
        cargo_messages(context, base(context, "clippy") + target_selection(context.request))
    elif task == "docs":
        run(base(context, "doc") + ["--no-deps"], cwd=context.project, env=context.env, log=context.log)
        target_directory = (Path(context.target_argument).stem if context.target_argument.endswith(".json")
                            else context.target_argument)
        documentation = Path(context.env["CARGO_TARGET_DIR"]) / target_directory / "doc"
        if not documentation.is_dir():
            raise BuildError("Rustdoc output was not found")
        shutil.copytree(documentation, context.products / "docs")
    elif task == "package":
        # Package crates individually so old toolchains need not support workspace packaging.
        selected = context.request.get("build", {}).get("packages", [])
        members = set(context.metadata["workspace_members"])
        packages = [p for p in context.metadata["packages"] if p["id"] in members
                    and (not selected or p["name"] in selected)]
        if not packages:
            raise BuildError("No workspace package matched the request")
        for package in packages:
            argv = ["cargo", "+" + context.channel, "package", "--manifest-path", package["manifest_path"], "--locked"]
            run(argv, cwd=Path(package["manifest_path"]).parent, env=context.env, log=context.log)
        archives = list(Path(context.env["CARGO_TARGET_DIR"]).glob("package/*.crate"))
        if not archives:
            raise BuildError("Cargo produced no crate archives")
        for archive in archives:
            shutil.copy2(archive, context.products / archive.name)
    elif task == "benchmark":
        if not context.target["can_execute"] and not context.request.get("platform", {}).get("runner"):
            raise BuildError("This target cannot execute benchmarks without a target runner")
        argv = base(context, "bench") + target_selection(context.request)
        if context.request.get("test", {}).get("arguments"):
            argv.extend(("--", *context.request["test"]["arguments"]))
        response = run(argv, cwd=context.project, env=context.env, log=context.log)
        (context.report / "benchmark-output.txt").write_text(response.stdout, encoding="utf-8")
    else:
        raise BuildError(f"No Cargo operation implemented for {task}")


def standalone(context):
    options = context.request.get("standalone")
    if not options:
        raise BuildError("standalone settings are required for a direct rustc build")
    source = within(context.project, options["source"])
    if not source.is_file():
        raise BuildError("Standalone Rust source does not exist")
    argv = ["rustc", "+" + context.channel, str(source), "--target", context.target_argument,
            "--edition", options.get("edition", "2021"), "--crate-type", options.get("crate_type", "bin"),
            "--out-dir", str(context.products), *options.get("arguments", [])]
    run(argv, cwd=context.project, env=context.env, log=context.log)
    if not any(context.products.iterdir()):
        raise BuildError("rustc did not produce an output file")
