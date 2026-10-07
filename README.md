# Chatgpt.com-Toolchain

A central repository of ready-to-use toolchains and modular build workflows for ChatGPT agents to build and compile real software.

The goal is straightforward: a ChatGPT agent writes or changes source code, selects the appropriate build workflow, and uses an actual toolchain to produce a usable build artifact.

## Project purpose

This repository will provide the build infrastructure needed for agent-driven software development. Compilers, build tools, dependencies, and build configurations should be prepared so that an agent can use the appropriate environment without reconstructing the entire setup for every task.

The intended result is a reusable collection of toolchains that can turn source code into binaries, libraries, or other build artifacts, depending on the project and target.

“Ready to use” describes the intended finished toolchains. It does not mean that those toolchains are already implemented in the current repository.

## Initial language scope

The initial scope includes:

- **Rust**
- **Go**
- **C**
- **C++**

Additional languages and toolchains may be added as the project develops. Supported platforms, architectures, compiler versions, and build targets will be documented when they are defined and implemented.

## Modular workflows

The build infrastructure will be organized into multiple workflow and action files rather than one workflow containing every toolchain.

The intended structure allows an agent to select the workflow appropriate to the language, project, platform, or build task. The exact file layout and division of responsibilities will be defined during implementation.

Each implemented workflow should make its inputs, build commands, outputs, and execution requirements clear.

## Intended agent workflow

The planned interaction is:

1. Read the target project's source code and build requirements.
2. Select the appropriate toolchain and workflow.
3. Prepare or update the source code and required build configuration.
4. Execute the build in the selected environment.
5. Inspect the build result and logs.
6. Retrieve the resulting artifacts after a successful build.

The mechanism for starting workflows and returning logs and artifacts to the agent has not yet been defined.

## Execution environment

The execution architecture is still to be decided. Builds may run on GitHub Actions runners, in the ChatGPT agent's execution environment, or through a combination of both.

This README does not yet establish which approach will be used. That decision will be documented before the corresponding integration is presented as working.

## Current status

This repository is at its initial documentation stage.

- The project purpose and initial language scope are defined.
- Build workflows and toolchain implementations have not yet been added.
- Agent integration, execution environments, and artifact retrieval still need to be specified and implemented.

## Guidance for agents working on this repository

Use this README as the starting point for understanding the project.

- Keep work aligned with reusable toolchains and real build execution.
- Distinguish planned capabilities from implemented capabilities.
- Describe build success only when supported by an actual successful build result.
- Document the requirements and usage of each toolchain as it is added.
- Update this README as architecture decisions and working features become available.

Further requirements will be added as the project is developed.
