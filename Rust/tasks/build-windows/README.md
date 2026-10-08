# Windows MSVC and GNU binaries and libraries

Task ID: `build-windows`. Workflow: [`.github/workflows/rust-build-windows.yml`](../../../.github/workflows/rust-build-windows.yml).

Status: implementation written; no GitHub Actions build has been executed or verified.

## Usage

Create a request conforming to [request.schema.json](../../schemas/request.schema.json) under `Rust/requests/`. Set `task` to `build-windows`. Dispatch this workflow with the request path, request commit/ref and matching unique request ID. Source delivery can reference this repository or another GitHub repository and commit/ref.

The default target is `x86_64-pc-windows-msvc` and default profile is `release`. Override them per request. The source is acquired separately from the infrastructure checkout. Setup calls the shared target and toolchain installers; execution calls the shared operation.

Project manifests, features, profiles and selected workspace members remain the source of build requirements.

## Files

- `task.json`: canonical task definition.
- `config/options.json`: artifact collection rules, read by the shared collector.
- `scripts/setup.py`: connected setup entry point.
- `scripts/execute.py`: connected execution entry point and CLI.

## Target configurations

| Target | GitHub runner | Runtime execution |
| --- | --- | --- |
| `x86_64-pc-windows-msvc` | `windows-2025` | Yes |
| `aarch64-pc-windows-msvc` | `windows-2025` | Build only; explicit runtime required for execution |
| `i686-pc-windows-msvc` | `windows-2025` | Yes |
| `x86_64-pc-windows-gnu` | `ubuntu-24.04` | Build only; explicit runtime required for execution |

Target configurations are written, not build-verified. See [agent instructions](../../AGENTS.md), [request documentation](../../requests/README.md) and [result documentation](../../schemas/README.md).
