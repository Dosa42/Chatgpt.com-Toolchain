# Target environments

catalog.json maps target triples to their canonical definition files. Definitions select the runner and record linker, SDK, packages and execution availability. Each is validated against ../schemas/target.schema.json.

Targets are configurations awaiting build verification. They are not a claim that arbitrary projects work unchanged. Native C/C++ dependencies, system libraries and target-specific build scripts can require additional request configuration.

macOS cross-builds for Intel use the Apple Silicon runner and Xcode SDK. Foreign Linux and Windows targets compile with their specified linker; runtime execution requires an explicit runner. Android uses a pinned NDK and request API level. WASI C dependencies can use a supplied WASI SDK. Custom targets are source-local JSON files with explicit nightly/custom toolchains when build-std is needed.

To add a target, add its definition, index it in catalog.json, document its requirements and keep verification_status=not-run until an actual verification run.
