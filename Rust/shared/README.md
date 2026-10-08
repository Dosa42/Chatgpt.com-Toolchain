# Shared implementation

Python 3.12 standard library only. No local service or AI backend is needed.

| Module | Function |
| --- | --- |
| util.py | Argument-vector process execution, JSON, hashes, confined paths and runner boundary. |
| request.py | Request/schema validation and canonical task/target selection. |
| source.py | GitHub source and request acquisition with exact resolved commits. |
| inspect.py | Manifest, workspace and source toolchain discovery. |
| toolchain.py | Rustup, pinned/resolved Rust, components and targets. |
| target.py | Linux packages, cross linkers, MSVC developer environment, NDK and Apple SDKs. |
| cargo.py | Builds, checks, tests, formatting, lint, docs, packaging, benchmarks and standalone rustc. |
| artifacts.py | Actual workspace products, requested additional files and checksums. |
| result.py | Success/failure reports and GitHub step summary. |
| run.py | Request preparation, matrix construction and connected execution. |
| verification.py | Future real build verification suite. |
| render_workflows.py | Deterministic workflow file generation from catalog and action pins. |
| github.py | Explicit API dispatch, run discovery/watch and binary artifact retrieval. |

The scripts execute source build commands only after the GitHub Actions runner check. render_workflows and static-check do not build or dispatch. Neither file import nor catalog discovery starts a job.

Request argument vectors are passed directly to programs. Workflow request strings are supplied through environment variables. GitHub source tokens are removed from the environment passed to source build scripts. Setup commands are explicit runner operations supplied by the build request.
