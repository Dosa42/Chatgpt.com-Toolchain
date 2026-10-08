# Rust toolchains

Complete connected Rust build infrastructure for this repository. Compilation runs exclusively on GitHub Actions runners. Workflows start only through explicit `workflow_dispatch` requests.

**Implementation status:** files and connections written; GitHub Actions builds, runtime behavior and platform targets have not been tested. Local checks are restricted to syntax, schemas and file connections. Target status remains `not-run` until later verification.

## Navigation

| Path | Responsibility |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Agent operating instructions. |
| [catalog.json](catalog.json) | Canonical task discovery index. |
| [tasks/](tasks/) | Eighteen separate task packages, instructions, scripts and configuration. |
| [shared/](shared/) | Source acquisition, toolchains, targets, Cargo, artifacts, results and dispatch helpers. |
| [schemas/](schemas/) | Closed machine-readable request/task/target/catalog/result contracts. |
| [toolchains/](toolchains/) | Concrete default version and GitHub action pins. |
| [targets/](targets/) | Platform-specific runner, linker and SDK definitions. |
| [requests/](requests/) | Request documentation and runnable requests for real verification sources. |
| [sources/](sources/) | Location for user source trees pushed from ChatGPT. |
| [verification/](verification/) | Real Rust projects and future execution checks. |

## Task and workflow mapping

| Task | Workflow |
| --- | --- |
| [build-linux](tasks/build-linux/README.md) | [`rust-build-linux.yml`](../.github/workflows/rust-build-linux.yml) |
| [build-windows](tasks/build-windows/README.md) | [`rust-build-windows.yml`](../.github/workflows/rust-build-windows.yml) |
| [build-macos](tasks/build-macos/README.md) | [`rust-build-macos.yml`](../.github/workflows/rust-build-macos.yml) |
| [build-android](tasks/build-android/README.md) | [`rust-build-android.yml`](../.github/workflows/rust-build-android.yml) |
| [build-apple-mobile](tasks/build-apple-mobile/README.md) | [`rust-build-apple-mobile.yml`](../.github/workflows/rust-build-apple-mobile.yml) |
| [build-wasm-web](tasks/build-wasm-web/README.md) | [`rust-build-wasm-web.yml`](../.github/workflows/rust-build-wasm-web.yml) |
| [build-wasi](tasks/build-wasi/README.md) | [`rust-build-wasi.yml`](../.github/workflows/rust-build-wasi.yml) |
| [build-embedded](tasks/build-embedded/README.md) | [`rust-build-embedded.yml`](../.github/workflows/rust-build-embedded.yml) |
| [build-uefi](tasks/build-uefi/README.md) | [`rust-build-uefi.yml`](../.github/workflows/rust-build-uefi.yml) |
| [build-custom](tasks/build-custom/README.md) | [`rust-build-custom.yml`](../.github/workflows/rust-build-custom.yml) |
| [build-standalone](tasks/build-standalone/README.md) | [`rust-build-standalone.yml`](../.github/workflows/rust-build-standalone.yml) |
| [check](tasks/check/README.md) | [`rust-check.yml`](../.github/workflows/rust-check.yml) |
| [test](tasks/test/README.md) | [`rust-test.yml`](../.github/workflows/rust-test.yml) |
| [lint](tasks/lint/README.md) | [`rust-lint.yml`](../.github/workflows/rust-lint.yml) |
| [docs](tasks/docs/README.md) | [`rust-docs.yml`](../.github/workflows/rust-docs.yml) |
| [package](tasks/package/README.md) | [`rust-package.yml`](../.github/workflows/rust-package.yml) |
| [benchmark](tasks/benchmark/README.md) | [`rust-benchmark.yml`](../.github/workflows/rust-benchmark.yml) |
| [verify-infrastructure](tasks/verify-infrastructure/README.md) | [`rust-verify-infrastructure.yml`](../.github/workflows/rust-verify-infrastructure.yml) |

## Request to artifact

1. Read the catalog, task instructions, manifest and project requirements.
2. Put source code in `Rust/sources/<request-id>/`, or reference another repository and commit/ref.
3. Create a JSON request under `Rust/requests/`, respecting the schema.
4. Commit the source and request. The dispatch input `request_ref` can select their commit. When local source has no separate ref, that request commit is used for source acquisition.
5. Dispatch the chosen workflow with `request_path`, `request_ref`, and matching `request_id`.
6. The prepare job resolves the request commit and target matrix. Each build job uses that exact request commit and its own report/work paths.
7. Inspect the exact run and download its artifacts. A dispatch response is not build success.

Each task supports dynamic build settings. Existing workflows are reused; normal build requests do not rewrite their definitions. An absent capability requires a complete new task/target definition and corresponding implementation.

## Reproducibility and isolation

GitHub actions are pinned by commit SHA. Orchestration Python, default Rust, Rustup bootstrap and default Android NDK versions are recorded under `toolchains/`. Source toolchain files and explicit request overrides are honored. Floating project channels resolve to a concrete version for that run.

Existing dependency lockfiles are protected. Newly resolved locks are returned with the report. Each result records source and infrastructure commits, actual compiler/SDK versions and runner image information. GitHub runner images and OS package repositories can change; this implementation does not claim bit-identical builds across image updates.

Only dependency downloads are cached, with a request/infrastructure/target/host-specific key. Compiled output caches are intentionally disabled in the initial implementation. Cargo resolves and checks dependencies against the lockfile. Target artifacts and reports remain separate per request, run attempt and target.

## Dispatch integration

Use a GitHub plugin dispatch action when available. The current session's exposed plugin lacks a new-run dispatch action, so the connected API helper is provided in `shared/github.py` for authenticated API execution, alongside GitHub's Run workflow interface. Neither helper nor workflow starts automatically. The helper supports dispatch, exact run discovery, tracking and token-safe artifact downloading.

Workflow dispatch definitions must exist on the default branch. A token used for API dispatch needs Actions write access. Private external source repositories require `RUST_SOURCE_TOKEN` with access to that source; the normal repository token cannot grant access it does not have. Build jobs themselves have read-only repository permissions.

## Reports

Artifacts contain `result.json`, the original `request.json`, actual logs, available Cargo metadata and lockfile, product checksums and, after successful product generation, `products.zip`. Failure reports include the exception and available logs. A missing requested product is a failure.

## Editing and static checks

Edit task definitions, target definitions and pins, then regenerate workflow files:

```bash
python Rust/shared/render_workflows.py
```

Check file connections and Python/JSON syntax without any build, install or workflow dispatch:

```bash
python Rust/shared/run.py static-check
```

The manual `rust-verify-infrastructure.yml` workflow is reserved for the later verification phase. It has not been started.

