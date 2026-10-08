# Apple device and simulator libraries

Task ID: `build-apple-mobile`. Workflow: [`.github/workflows/rust-build-apple-mobile.yml`](../../../.github/workflows/rust-build-apple-mobile.yml).

Status: GitHub Actions verification passed for the recorded fixtures. [Verified run](https://github.com/Dosa42/Chatgpt.com-Toolchain/actions/runs/37743001090); [coverage and evidence](../../verification/results/2026-10-08.json).

## Usage

Create a request conforming to [request.schema.json](../../schemas/request.schema.json) under `Rust/requests/`. Set `task` to `build-apple-mobile`. Dispatch this workflow with the request path, request commit/ref and matching unique request ID. Source delivery can reference this repository or another GitHub repository and commit/ref.

The default target is `aarch64-apple-ios` and default profile is `release`. Override them per request. The source is acquired separately from the infrastructure checkout. Setup calls the shared target and toolchain installers; execution calls the shared operation.

This task builds Rust libraries. It does not sign or publish Apple applications. Select the correct device/simulator SDK and target. Use `platform.xcode_path` when the project requires a specific installed Xcode.

## Files

- `task.json`: canonical task definition.
- `config/options.json`: artifact collection rules, read by the shared collector.
- `scripts/setup.py`: connected setup entry point.
- `scripts/execute.py`: connected execution entry point and CLI.

## Target configurations

| Target | GitHub runner | Runtime execution |
| --- | --- | --- |
| `aarch64-apple-ios` | `macos-15` | Build only; explicit runtime required for execution |
| `aarch64-apple-ios-sim` | `macos-15` | Build only; explicit runtime required for execution |
| `x86_64-apple-ios` | `macos-15` | Build only; explicit runtime required for execution |
| `aarch64-apple-tvos` | `macos-15` | Build only; explicit runtime required for execution |
| `aarch64-apple-tvos-sim` | `macos-15` | Build only; explicit runtime required for execution |
| `aarch64-apple-watchos` | `macos-15` | Build only; explicit runtime required for execution |
| `aarch64-apple-watchos-sim` | `macos-15` | Build only; explicit runtime required for execution |
| `aarch64-apple-visionos` | `macos-15` | Build only; explicit runtime required for execution |
| `aarch64-apple-visionos-sim` | `macos-15` | Build only; explicit runtime required for execution |

Target build coverage and task execution coverage are recorded separately in [verification evidence](../../verification/results/2026-10-08.json). See [agent instructions](../../AGENTS.md), [request documentation](../../requests/README.md) and [result documentation](../../schemas/README.md).

The tvOS, watchOS and visionOS target definitions build their standard libraries from source using pinned nightly and rust-src. Source and request toolchain overrides retain precedence.
