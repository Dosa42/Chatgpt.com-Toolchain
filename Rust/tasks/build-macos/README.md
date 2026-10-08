# macOS Intel and Apple Silicon binaries and libraries

Task ID: `build-macos`. Workflow: [`.github/workflows/rust-build-macos.yml`](../../../.github/workflows/rust-build-macos.yml).

Status: implementation written; no GitHub Actions build has been executed or verified.

## Usage

Create a request conforming to [request.schema.json](../../schemas/request.schema.json) under `Rust/requests/`. Set `task` to `build-macos`. Dispatch this workflow with the request path, request commit/ref and matching unique request ID. Source delivery can reference this repository or another GitHub repository and commit/ref.

The default target is `aarch64-apple-darwin` and default profile is `release`. Override them per request. The source is acquired separately from the infrastructure checkout. Setup calls the shared target and toolchain installers; execution calls the shared operation.

Project manifests, features, profiles and selected workspace members remain the source of build requirements.

## Files

- `task.json`: canonical task definition.
- `config/options.json`: artifact collection rules, read by the shared collector.
- `scripts/setup.py`: connected setup entry point.
- `scripts/execute.py`: connected execution entry point and CLI.

## Target configurations

| Target | GitHub runner | Runtime execution |
| --- | --- | --- |
| `aarch64-apple-darwin` | `macos-15` | Yes |
| `x86_64-apple-darwin` | `macos-15` | Build only; explicit runtime required for execution |

Target configurations are written, not build-verified. See [agent instructions](../../AGENTS.md), [request documentation](../../requests/README.md) and [result documentation](../../schemas/README.md).
