"""Collect workspace products and exact checksums without filename guesses."""
from __future__ import annotations

import fnmatch
from pathlib import Path
import shutil
import zipfile
from .util import BuildError, ROOT, read_json, digest, write_json, within


def collect(context):
    options = read_json(within(ROOT, context.definition["configuration"]))
    members = set(context.metadata.get("workspace_members", []))
    for artifact in context.compiler_artifacts:
        if artifact["package_id"] not in members:
            continue
        if "custom-build" in artifact["target"]["kind"]:
            continue
        for filename in artifact["filenames"]:
            source = Path(filename)
            if not source.is_file() or source.suffix in options["artifact_exclude_suffixes"]:
                continue
            destination = context.products / "cargo" / artifact["target"]["name"] / source.name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    for pattern in context.request.get("output", {}).get("source_globs", []):
        # Extra generated outputs must be explicitly requested and remain inside the source tree.
        within(context.project, pattern)
        for path in context.project.glob(pattern):
            if path.is_file() and path.resolve().is_relative_to(context.project.resolve()):
                destination = context.products / "extra" / path.relative_to(context.project)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, destination)
    products = sorted(p for p in context.products.rglob("*") if p.is_file())
    expected = context.request.get("output", {}).get("required_globs", [])
    names = [p.relative_to(context.products).as_posix() for p in products]
    for pattern in expected:
        if not any(fnmatch.fnmatch(name, pattern) for name in names):
            raise BuildError(f"Required output is absent: {pattern}")
    if context.definition["operation"] in ("build", "standalone", "docs", "package") and not products:
        raise BuildError("The build produced no deliverable files")
    files = [{"path": p.relative_to(context.report).as_posix(), "bytes": p.stat().st_size,
              "sha256": digest(p)} for p in products]
    write_json(context.report / "artifacts.json", files)
    if products:
        archive = context.report / "products.zip"
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as out:
            for path in products:
                out.write(path, path.relative_to(context.products))
        files.append({"path": "products.zip", "bytes": archive.stat().st_size,
                      "sha256": digest(archive)})
    return files
