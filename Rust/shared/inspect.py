"""Inspect the actual project without inventing build requirements."""
from __future__ import annotations

from pathlib import Path
import tomllib
from .util import BuildError, run, within, write_json
import json


def toolchain_spec(project, source_root=None):
    project = Path(project)
    boundary = Path(source_root).resolve() if source_root else project.resolve()
    if not project.resolve().is_relative_to(boundary):
        raise BuildError("Project lies outside source checkout")
    # Rustup gives the legacy file precedence if both forms exist.
    legacy = project / "rust-toolchain"
    modern = project / "rust-toolchain.toml"
    if legacy.is_file():
        content = legacy.read_text(encoding="utf-8").strip()
        if content.startswith("["):
            return tomllib.loads(content).get("toolchain", {})
        return {"channel": content}
    if modern.is_file():
        return tomllib.loads(modern.read_text(encoding="utf-8")).get("toolchain", {})
    if project.resolve() != boundary:
        return toolchain_spec(project.parent, boundary)
    return {}


def project_manifest(project, request):
    path = within(project, request.get("build", {}).get("manifest_path", "Cargo.toml"))
    if not path.is_file():
        raise BuildError("Cargo.toml was not found; use build-standalone for direct rustc builds")
    return path


def metadata(context):
    manifest = project_manifest(context.project, context.request)
    result = run(["cargo", "+" + context.channel, "metadata", "--format-version", "1",
                  "--manifest-path", str(manifest)], cwd=context.project,
                 env=context.env, log=context.log)
    data = json.loads(result.stdout)
    write_json(context.report / "cargo-metadata.json", data)
    context.metadata = data
    return data
