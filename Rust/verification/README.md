# Infrastructure verification sources

These are real compilable Rust sources for the later verification phase. They are not substitutes for user applications. No source has been compiled or executed during the current implementation stage.

The workspace contains checked arithmetic, Euclidean GCD, an actual argument-parsing CLI, integration tests and a timing benchmark. Separate projects cover C ABI libraries, browser WebAssembly, no_std libraries, UEFI and direct rustc compilation. suite.json connects the native build, check, tests, Clippy/Rustfmt, documentation, packaging, benchmark, FFI and standalone cases to shared execution.

The verification workflow runs only on request. Its result distinguishes each actual successful or failed case. Target definitions remain not-run until later platform verification. No hardware flashing, deployment or package publishing occurs.
