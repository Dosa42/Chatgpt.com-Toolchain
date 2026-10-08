# Linux binaries and libraries

Task ID: `build-linux`. Workflow: [`.github/workflows/rust-build-linux.yml`](../../../.github/workflows/rust-build-linux.yml).

Status: GitHub Actions verification passed for the recorded fixtures. [Verified run](https://github.com/Dosa42/Chatgpt.com-Toolchain/actions/runs/37742041638); [coverage and evidence](../../verification/results/2026-10-08.json).

## Usage

Create a request conforming to [request.schema.json](../../schemas/request.schema.json) under `Rust/requests/`. Set `task` to `build-linux`. Dispatch this workflow with the request path, request commit/ref and matching unique request ID. Source delivery can reference this repository or another GitHub repository and commit/ref.

The default target is `x86_64-unknown-linux-gnu` and default profile is `release`. Override them per request. The source is acquired separately from the infrastructure checkout. Setup calls the shared target and toolchain installers; execution calls the shared operation.

Project manifests, features, profiles and selected workspace members remain the source of build requirements.

## Files

- `task.json`: canonical task definition.
- `config/options.json`: artifact collection rules, read by the shared collector.
- `scripts/setup.py`: connected setup entry point.
- `scripts/execute.py`: connected execution entry point and CLI.

## Target configurations

| Target | GitHub runner | Runtime execution |
| --- | --- | --- |
| `x86_64-unknown-linux-gnu` | `ubuntu-24.04` | Yes |
| `aarch64-unknown-linux-gnu` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `armv7-unknown-linux-gnueabihf` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `i686-unknown-linux-gnu` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `x86_64-unknown-linux-musl` | `ubuntu-24.04` | Build only; explicit runtime required for execution |

Target build coverage and task execution coverage are recorded separately in [verification evidence](../../verification/results/2026-10-08.json). See [agent instructions](../../AGENTS.md), [request documentation](../../requests/README.md) and [result documentation](../../schemas/README.md).
