# Toolchain definitions

pins.json contains exact GitHub action commit SHAs, orchestration Python, default stable Rust, the pinned nightly used for build-std, and default NDK. defaults.json contains the Rustup bootstrap version and cache policy. The default Rust release is a baseline, not a claim to be the newest release.

The source rust-toolchain/rust-toolchain.toml and request toolchain overrides take precedence over the baseline. stable/beta/nightly project channels are resolved and fixed for the running build. Custom toolchains require explicit setup commands and an installed channel. Cargo rust-version incompatibilities are reported by the real toolchain.

Runner images and system packages are not immutable archives. The result records their actual versions. Change pins deliberately, regenerate workflows and verify in an explicitly requested run.

The orchestration Python pin is 3.12.10 because the official Actions distribution manifest supplies that exact release for Linux, Windows and macOS. Tier-three Apple targets define build_std and have no rustup_target download; their standard libraries are compiled from rust-src.
