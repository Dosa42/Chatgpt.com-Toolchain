# WASI Preview 1 modules and Preview 2 components

Task ID: `build-wasi`. Workflow: [`.github/workflows/rust-build-wasi.yml`](../../../.github/workflows/rust-build-wasi.yml).

Status: GitHub Actions verification passed for the recorded fixtures. [Verified run](https://github.com/Dosa42/Chatgpt.com-Toolchain/actions/runs/37742171313); [coverage and evidence](../../verification/results/2026-10-08.json).

## Usage

Create a request conforming to [request.schema.json](../../schemas/request.schema.json) under `Rust/requests/`. Set `task` to `build-wasi`. Dispatch this workflow with the request path, request commit/ref and matching unique request ID. Source delivery can reference this repository or another GitHub repository and commit/ref.

The default target is `wasm32-wasip1` and default profile is `release`. Override them per request. The source is acquired separately from the infrastructure checkout. Setup calls the shared target and toolchain installers; execution calls the shared operation.

wasm32-wasip1 emits a core module; wasm32-wasip2 emits a component. Native C dependencies may need a WASI SDK provided through platform setup commands and linker configuration. Runtime execution is not implied by successful compilation.

## Files

- `task.json`: canonical task definition.
- `config/options.json`: artifact collection rules, read by the shared collector.
- `scripts/setup.py`: connected setup entry point.
- `scripts/execute.py`: connected execution entry point and CLI.

## Target configurations

| Target | GitHub runner | Runtime execution |
| --- | --- | --- |
| `wasm32-wasip1` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `wasm32-wasip2` | `ubuntu-24.04` | Build only; explicit runtime required for execution |

Target build coverage and task execution coverage are recorded separately in [verification evidence](../../verification/results/2026-10-08.json). See [agent instructions](../../AGENTS.md), [request documentation](../../requests/README.md) and [result documentation](../../schemas/README.md).
