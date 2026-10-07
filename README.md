# Chatgpt.com-Toolchain

A central repository of ready-to-use toolchains and request-driven build workflows for ChatGPT agents, with all compilation performed on GitHub Actions runners.

This repository provides a fallback build environment when a ChatGPT workspace or sandbox cannot perform the required build because the necessary toolchain, dependencies, or execution capabilities are unavailable. A user can also explicitly request that a build be performed here.

## Project purpose

The goal is to let a user request a real software build from the ChatGPT web platform, using the GitHub plugin to work with this repository.

The agent identifies the build requirements, finds or creates the appropriate workflow, configures it for the requested source code, starts the workflow, and brings the results back to the conversation.

Compilers, build tools, dependencies, and build configurations should be organized into reusable toolchains so that agents can use this infrastructure consistently across requests.

“Ready to use” describes the intended finished toolchains. It does not mean that they are already implemented.

## Execution boundary

**All compilation provided by this repository runs exclusively on GitHub Actions runners.**

The ChatGPT agent coordinates the request through the GitHub plugin. Its workspace or sandbox is not the compilation environment for this repository.

The fallback is invoked in response to a request. It is not an automatic background mechanism that detects sandbox limitations and starts builds independently.

## Initial language scope

The initial scope includes:

- **Rust**
- **Go**
- **C**
- **C++**

Additional languages and toolchains may be added later. Supported platforms, architectures, compiler versions, and build targets will be documented as they are defined and implemented.

## Request-driven build flow

For example, a user asks the agent to build specified Rust source code using this repository.

The intended flow is:

1. **Understand the request.** Identify the source code and its build requirements.
2. **Find the workflow.** Inspect this repository and select an existing workflow suitable for the requested build.
3. **Create one if needed.** If no suitable workflow exists, create the required workflow in this repository.
4. **Configure the build.** Set the values needed for the current source code and target, updating the workflow configuration where required.
5. **Start the workflow.** Invoke the GitHub Actions **Run workflow** operation for that request.
6. **Inspect the result.** Read the run status and build logs.
7. **Return the outcome.** Retrieve the resulting artifacts after a successful build and present the results in the ChatGPT conversation. If the build fails, report the failure using the actual run output.

The requested trigger model is manual dispatch: builds start when requested, rather than automatically on pushes, pull requests, or a schedule.

The exact dispatch interface, workflow inputs, source-code delivery method, and artifact retrieval mechanism still need to be discussed and implemented.

## Workflow organization and drift prevention

The infrastructure will be organized into multiple workflow and action files. Agents should be able to find the appropriate toolchain without rebuilding the infrastructure from scratch for every request.

**Consistent organization and prevention of configuration drift are core project requirements.**

As the repository grows:

- Existing suitable workflows should be reused.
- New workflows should be added when the requested build requires capabilities that are not already available.
- Toolchain definitions, workflow configuration, and documentation should remain aligned.
- Changes for individual builds should not cause workflows to accumulate conflicting or unexplained configurations.
- Each workflow should clearly document its purpose, requirements, configurable values, and outputs.

The exact directory structure, shared components, version policy, and rules for maintaining this consistency are still to be designed.

## Current status

This repository is at its initial documentation stage.

The confirmed direction is:

- GitHub Actions runners are the exclusive compilation environment.
- ChatGPT agents use the GitHub plugin to coordinate requested builds.
- Agents find or create the appropriate workflow and configure it for the source being built.
- Builds start on request.
- Results are brought back to ChatGPT.
- Infrastructure organization and drift prevention are central requirements.

Build workflows and toolchain implementations have not yet been added. The integration details remain to be specified.

## Guidance for agents

Read this README before extending the repository.

Keep implementation aligned with the confirmed build flow and execution boundary. Reuse suitable infrastructure, document new capabilities, and distinguish planned features from working features.

Report build success only when an actual GitHub Actions run supports that result. Update this README as implementation decisions and verified capabilities become available.
