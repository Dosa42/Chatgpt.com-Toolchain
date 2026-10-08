# Cargo compilation checks

Task ID: `check`. Workflow: [`.github/workflows/rust-check.yml`](../../../.github/workflows/rust-check.yml).

Status: implementation written; no GitHub Actions build has been executed or verified.

## Usage

Create a request conforming to [request.schema.json](../../schemas/request.schema.json) under `Rust/requests/`. Set `task` to `check`. Dispatch this workflow with the request path, request commit/ref and matching unique request ID. Source delivery can reference this repository or another GitHub repository and commit/ref.

The default target is `x86_64-unknown-linux-gnu` and default profile is `dev`. Override them per request. The source is acquired separately from the infrastructure checkout. Setup calls the shared target and toolchain installers; execution calls the shared operation.

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
| `x86_64-pc-windows-msvc` | `windows-2025` | Yes |
| `aarch64-pc-windows-msvc` | `windows-2025` | Build only; explicit runtime required for execution |
| `i686-pc-windows-msvc` | `windows-2025` | Yes |
| `x86_64-pc-windows-gnu` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `aarch64-apple-darwin` | `macos-15` | Yes |
| `x86_64-apple-darwin` | `macos-15` | Build only; explicit runtime required for execution |
| `aarch64-linux-android` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `armv7-linux-androideabi` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `x86_64-linux-android` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `i686-linux-android` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `aarch64-apple-ios` | `macos-15` | Build only; explicit runtime required for execution |
| `aarch64-apple-ios-sim` | `macos-15` | Build only; explicit runtime required for execution |
| `x86_64-apple-ios` | `macos-15` | Build only; explicit runtime required for execution |
| `aarch64-apple-tvos` | `macos-15` | Build only; explicit runtime required for execution |
| `aarch64-apple-tvos-sim` | `macos-15` | Build only; explicit runtime required for execution |
| `aarch64-apple-watchos` | `macos-15` | Build only; explicit runtime required for execution |
| `aarch64-apple-watchos-sim` | `macos-15` | Build only; explicit runtime required for execution |
| `aarch64-apple-visionos` | `macos-15` | Build only; explicit runtime required for execution |
| `aarch64-apple-visionos-sim` | `macos-15` | Build only; explicit runtime required for execution |
| `wasm32-unknown-unknown` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `wasm32-wasip1` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `wasm32-wasip2` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `thumbv6m-none-eabi` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `thumbv7m-none-eabi` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `thumbv7em-none-eabi` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `thumbv7em-none-eabihf` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `thumbv8m.main-none-eabihf` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `riscv32imac-unknown-none-elf` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `riscv64imac-unknown-none-elf` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `aarch64-unknown-none` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `x86_64-unknown-none` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `x86_64-unknown-uefi` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `aarch64-unknown-uefi` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `i686-unknown-uefi` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `custom` | `ubuntu-24.04` | Build only; explicit runtime required for execution |

Target configurations are written, not build-verified. See [agent instructions](../../AGENTS.md), [request documentation](../../requests/README.md) and [result documentation](../../schemas/README.md).
