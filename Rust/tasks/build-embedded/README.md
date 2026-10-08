# Embedded and bare-metal no_std projects

Task ID: `build-embedded`. Workflow: [`.github/workflows/rust-build-embedded.yml`](../../../.github/workflows/rust-build-embedded.yml).

Status: GitHub Actions verification passed for the recorded fixtures. [Verified run](https://github.com/Dosa42/Chatgpt.com-Toolchain/actions/runs/37742191999); [coverage and evidence](../../verification/results/2026-10-08.json).

## Usage

Create a request conforming to [request.schema.json](../../schemas/request.schema.json) under `Rust/requests/`. Set `task` to `build-embedded`. Dispatch this workflow with the request path, request commit/ref and matching unique request ID. Source delivery can reference this repository or another GitHub repository and commit/ref.

The default target is `thumbv7em-none-eabihf` and default profile is `release`. Override them per request. The source is acquired separately from the infrastructure checkout. Setup calls the shared target and toolchain installers; execution calls the shared operation.

The source project supplies the board-specific link script, memory layout, startup code and panic implementation. Those requirements are preserved. Compiling firmware does not mean flashing or running it on physical hardware.

## Files

- `task.json`: canonical task definition.
- `config/options.json`: artifact collection rules, read by the shared collector.
- `scripts/setup.py`: connected setup entry point.
- `scripts/execute.py`: connected execution entry point and CLI.

## Target configurations

| Target | GitHub runner | Runtime execution |
| --- | --- | --- |
| `thumbv6m-none-eabi` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `thumbv7m-none-eabi` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `thumbv7em-none-eabi` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `thumbv7em-none-eabihf` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `thumbv8m.main-none-eabihf` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `riscv32imac-unknown-none-elf` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `riscv64imac-unknown-none-elf` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `aarch64-unknown-none` | `ubuntu-24.04` | Build only; explicit runtime required for execution |
| `x86_64-unknown-none` | `ubuntu-24.04` | Build only; explicit runtime required for execution |

Target build coverage and task execution coverage are recorded separately in [verification evidence](../../verification/results/2026-10-08.json). See [agent instructions](../../AGENTS.md), [request documentation](../../requests/README.md) and [result documentation](../../schemas/README.md).
