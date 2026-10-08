# Android native binaries and libraries with NDK

Task ID: `build-android`. Workflow: [`.github/workflows/rust-build-android.yml`](../../../.github/workflows/rust-build-android.yml).

Status: implementation written; no GitHub Actions build has been executed or verified.

## Usage

Create a request conforming to [request.schema.json](../../schemas/request.schema.json) under `Rust/requests/`. Set `task` to `build-android`. Dispatch this workflow with the request path, request commit/ref and matching unique request ID. Source delivery can reference this repository or another GitHub repository and commit/ref.

The default target is `aarch64-linux-android` and default profile is `release`. Override them per request. The source is acquired separately from the infrastructure checkout. Setup calls the shared target and toolchain installers; execution calls the shared operation.

The manifest must declare the intended binary or library crate type. A Rust native library is not an APK. NDK version and Android API level are configurable under `platform`. C/C++ compiler and archiver environment variables are configured per ABI.

## Files

- `task.json`: canonical task definition.
- `config/options.json`: artifact collection rules, read by the shared collector.
- `scripts/setup.py`: connected setup entry point.
- `scripts/execute.py`: connected execution entry point and CLI.

## Target configurations

| Target | GitHub runner | Runtime execution |
| --- | --- | --- |
| `aarch64-linux-android` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `armv7-linux-androideabi` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `x86_64-linux-android` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `i686-linux-android` | `ubuntu-24.04` | Build only; explicit runtime required for execution |

Target configurations are written, not build-verified. See [agent instructions](../../AGENTS.md), [request documentation](../../requests/README.md) and [result documentation](../../schemas/README.md).
