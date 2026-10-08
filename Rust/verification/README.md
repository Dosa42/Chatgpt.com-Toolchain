# Infrastructure verification sources

These Rust fixtures have been compiled on GitHub Actions runners. The [verification record](results/2026-10-08.json) records 18 verified task entry points, 40 target builds, nine suite cases and four native Rust tests. Coverage applies to the recorded sources and toolchains.

The workspace contains checked arithmetic, Euclidean GCD, an actual argument-parsing CLI, integration tests and a timing benchmark. Separate projects cover C ABI libraries, browser WebAssembly, no_std libraries, UEFI and direct rustc compilation. suite.json connects the native build, check, tests, Clippy/Rustfmt, documentation, packaging, benchmark, FFI and standalone cases to shared execution.

The verification workflow runs only on request. Its result distinguishes each actual successful or failed case. Task and target verification_status values reflect the recorded successful runs. No hardware flashing, deployment or package publishing occurs.
