# Browser WebAssembly with optional matched wasm-bindgen CLI

Task ID: `build-wasm-web`. Workflow: [`.github/workflows/rust-build-wasm-web.yml`](../../../.github/workflows/rust-build-wasm-web.yml).

Status: implementation written; no GitHub Actions build has been executed or verified.

## Usage

Create a request conforming to [request.schema.json](../../schemas/request.schema.json) under `Rust/requests/`. Set `task` to `build-wasm-web`. Dispatch this workflow with the request path, request commit/ref and matching unique request ID. Source delivery can reference this repository or another GitHub repository and commit/ref.

The default target is `wasm32-unknown-unknown` and default profile is `release`. Override them per request. The source is acquired separately from the infrastructure checkout. Setup calls the shared target and toolchain installers; execution calls the shared operation.

Enable `wasm.bindings` only for a project using wasm-bindgen. The CLI version is selected from the resolved wasm-bindgen dependency, rather than an unrelated global version. Binding output is placed under products/wasm-bindings.

## Files

- `task.json`: canonical task definition.
- `config/options.json`: artifact collection rules, read by the shared collector.
- `scripts/setup.py`: connected setup entry point.
- `scripts/execute.py`: connected execution entry point and CLI.

## Target configurations

| Target | GitHub runner | Runtime execution |
| --- | --- | --- |
| `wasm32-unknown-unknown` | `ubuntu-24.04` | Build only; explicit runtime required for execution |

Target configurations are written, not build-verified. See [agent instructions](../../AGENTS.md), [request documentation](../../requests/README.md) and [result documentation](../../schemas/README.md).
