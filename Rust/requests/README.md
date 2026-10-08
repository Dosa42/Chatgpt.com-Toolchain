# Build requests

Each request is a JSON file conforming to ../schemas/request.schema.json. Use unique request IDs and retain requests so a run can be reconstructed.

| Field | Meaning |
| --- | --- |
| schema_version | Contract version, currently 1. |
| id | Unique request identifier matching workflow input request_id. |
| task | Catalog task ID matching the selected workflow. |
| source | Optional repository/ref plus project path and submodule choice. Missing repository uses this repo; missing local ref uses the exact request commit. External sources must provide ref. |
| build | Targets, manifest, profile, package/workspace selection, features and explicit Cargo configuration. |
| toolchain | Source/default Rust selection override, components, targets and explicit custom setup. |
| platform | Native dependencies, linker, SDK/NDK/API, custom target and runtime runner. |
| standalone | Direct rustc source, edition, crate type and argument vector. |
| wasm | Optional wasm-bindgen generation settings. |
| test | Explicit no-run mode or test/benchmark arguments. |
| environment | Build environment additions; infrastructure control variables cannot be overridden. |
| output | Additional generated source-tree globs and required product globs. |

The included JSON requests point at real verification projects in this repository. Dispatch requires an explicit execution request. The test-* requests and dated verify-linux requests have execution evidence in [the verification record](../verification/results/2026-10-08.json). They do not stand in for a user's application.

## API dispatch helper

An API-capable agent with an authorized GH_TOKEN can run:

```bash
python Rust/shared/github.py dispatch --workflow rust-build-linux.yml --ref main --request-path Rust/requests/build-linux-workspace.json --request-ref main --request-id build-linux-workspace
```

This is an actual dispatch command, not a static check. Run it only for an explicitly requested build. Use find-run with the returned timestamp and request ID, then watch/download with the observed exact run ID. A plugin dispatch primitive or GitHub Run workflow interface can pass the same three inputs.
