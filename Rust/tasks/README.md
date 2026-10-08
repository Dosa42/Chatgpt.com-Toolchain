# Rust build tasks

Each directory contains task.json, config/options.json, scripts/setup.py, scripts/execute.py and README.md. Discover tasks through ../catalog.json. Workflow files remain under ../../.github/workflows/ as required by GitHub.

All task scripts are connected to shared setup and execution code. platform tasks vary by target configuration; Cargo selection, lock handling, diagnostics and outputs use a single shared implementation.
