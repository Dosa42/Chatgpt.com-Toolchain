{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://raw.githubusercontent.com/Dosa42/Chatgpt.com-Toolchain/main/Rust/README.md",
  "type": "object",
  "required": [
    "schema_version",
    "language",
    "root",
    "path_base",
    "format",
    "execution",
    "navigation",
    "canonical_sources",
    "template_bindings",
    "shared_modules",
    "operations",
    "source_delivery",
    "build_isolation",
    "artifacts",
    "drift_controls",
    "state"
  ],
  "additionalProperties": false,
  "properties": {
    "schema_version": {
      "type": "integer",
      "const": 1
    },
    "language": {
      "type": "string",
      "const": "Rust"
    },
    "root": {
      "type": "string",
      "const": "Rust/"
    },
    "path_base": {
      "type": "string",
      "const": "repository_root"
    },
    "format": {
      "type": "object",
      "const": {
        "serialization": "json",
        "contract": "json_schema",
        "dialect": "2020-12",
        "prose_fields": false,
        "markdown": false,
        "code_fences": false
      }
    },
    "execution": {
      "type": "object",
      "const": {
        "compile_on": "github_actions_runner",
        "dispatch_event": "workflow_dispatch",
        "workspace_compile": false,
        "automatic_dispatch": false,
        "current_phase": "runtime_verification",
        "current_phase_dispatch": true
      }
    },
    "navigation": {
      "type": "object",
      "const": {
        "task_catalog": "Rust/catalog.json",
        "target_catalog": "Rust/targets/catalog.json",
        "tasks": "Rust/tasks/",
        "shared": "Rust/shared/",
        "schemas": "Rust/schemas/",
        "toolchains": "Rust/toolchains/",
        "targets": "Rust/targets/",
        "requests": "Rust/requests/",
        "sources": "Rust/sources/",
        "verification": "Rust/verification/",
        "generated_workflows": ".github/workflows/"
      }
    },
    "canonical_sources": {
      "type": "object",
      "const": {
        "task_index": "Rust/catalog.json",
        "task_definition": "Rust/tasks/{task_id}/task.json",
        "task_configuration": "Rust/tasks/{task_id}/config/options.json",
        "task_setup": "Rust/tasks/{task_id}/scripts/setup.py",
        "task_execute": "Rust/tasks/{task_id}/scripts/execute.py",
        "target_index": "Rust/targets/catalog.json",
        "target_definition": "Rust/targets/{target_family}/{target_id}.json",
        "toolchain_pins": "Rust/toolchains/pins.json",
        "toolchain_defaults": "Rust/toolchains/defaults.json",
        "workflow_renderer": "Rust/shared/render_workflows.py",
        "workflow_path_lookup": "Rust/catalog.json#/tasks",
        "task_runtime_status_pointer": "/verification_status",
        "target_runtime_status_pointer": "/verification_status"
      }
    },
    "template_bindings": {
      "type": "object",
      "const": {
        "syntax": "brace_identifier",
        "identifiers": [
          "task_id",
          "target_id",
          "target_family",
          "request_id",
          "request_path",
          "request_commit",
          "workflow_file",
          "workflow_ref",
          "run_id",
          "dispatched_at",
          "download_directory"
        ],
        "resolution": "runtime_values",
        "literal_argument_passthrough": false
      }
    },
    "shared_modules": {
      "type": "object",
      "const": {
        "request": "Rust/shared/request.py",
        "source": "Rust/shared/source.py",
        "project_inspection": "Rust/shared/inspect.py",
        "toolchain": "Rust/shared/toolchain.py",
        "target": "Rust/shared/target.py",
        "cargo": "Rust/shared/cargo.py",
        "artifacts": "Rust/shared/artifacts.py",
        "result": "Rust/shared/result.py",
        "orchestration": "Rust/shared/run.py",
        "dispatch_tracking_download": "Rust/shared/github.py",
        "verification": "Rust/shared/verification.py",
        "workflow_rendering": "Rust/shared/render_workflows.py",
        "utilities": "Rust/shared/util.py"
      }
    },
    "operations": {
      "type": "object",
      "const": {
        "discover": {
          "read": [
            "Rust/catalog.json",
            "Rust/targets/catalog.json"
          ],
          "task_selector": {
            "array_pointer": "/tasks",
            "key": "id",
            "value_binding": "task_id"
          },
          "target_selector": {
            "array_pointer": "/targets",
            "key": "triple",
            "value_binding": "target_id"
          },
          "load_task_fields": [
            "definition",
            "workflow"
          ],
          "load_target_fields": [
            "definition"
          ]
        },
        "request_create": {
          "schema": "Rust/schemas/request.schema.json",
          "write": "Rust/requests/{request_id}.json",
          "required_fields": [
            "schema_version",
            "id",
            "task",
            "source"
          ],
          "optional_groups": [
            "build",
            "toolchain",
            "platform",
            "standalone",
            "wasm",
            "test",
            "environment",
            "output"
          ],
          "task_binding": "task_id",
          "id_binding": "request_id",
          "settings_source": [
            "source_manifest",
            "source_toolchain",
            "requested_output",
            "selected_task",
            "selected_target"
          ],
          "workflow_definition_edit": false,
          "commit_request": true,
          "commit_local_source": true
        },
        "dispatch": {
          "enabled_in_current_phase": true,
          "event": "workflow_dispatch",
          "workflow_lookup": "Rust/catalog.json#/tasks",
          "workflow_default_branch_presence_required": true,
          "inputs": {
            "request_path": {
              "binding": "request_path",
              "prefix": "Rust/requests/",
              "suffix": ".json"
            },
            "request_ref": {
              "binding": "request_commit"
            },
            "request_id": {
              "binding": "request_id",
              "equality": "request_json.id"
            }
          },
          "interfaces": [
            "github_plugin_dispatch_if_available",
            "github_actions_run_workflow",
            "github_rest_api"
          ],
          "api_helper": {
            "argv": [
              "python",
              "Rust/shared/github.py",
              "--repository",
              "Dosa42/Chatgpt.com-Toolchain",
              "dispatch",
              "--workflow",
              "{workflow_file}",
              "--ref",
              "{workflow_ref}",
              "--request-path",
              "{request_path}",
              "--request-ref",
              "{request_commit}",
              "--request-id",
              "{request_id}"
            ],
            "credential_environment": [
              "GH_TOKEN",
              "GITHUB_TOKEN"
            ],
            "required_repository_permission": "actions_write"
          },
          "accepted_dispatch_equals_build_success": false
        },
        "run_find": {
          "argv": [
            "python",
            "Rust/shared/github.py",
            "find-run",
            "--workflow",
            "{workflow_file}",
            "--request-id",
            "{request_id}",
            "--dispatched-at",
            "{dispatched_at}"
          ],
          "output_binding": "run_id",
          "request_id_reuse": false
        },
        "run_watch": {
          "argv": [
            "python",
            "Rust/shared/github.py",
            "watch",
            "--run-id",
            "{run_id}"
          ],
          "success_values": {
            "status": "completed",
            "conclusion": "success"
          }
        },
        "artifact_download": {
          "argv": [
            "python",
            "Rust/shared/github.py",
            "download",
            "--run-id",
            "{run_id}",
            "--directory",
            "{download_directory}"
          ],
          "alternative_interface": "github_plugin_artifact_download",
          "run_identity": "exact_run_id",
          "archive_format": "zip"
        },
        "task_modify": {
          "read": [
            "Rust/catalog.json",
            "Rust/schemas/task.schema.json",
            "Rust/tasks/{task_id}/task.json",
            "Rust/tasks/{task_id}/config/options.json",
            "Rust/tasks/{task_id}/scripts/setup.py",
            "Rust/tasks/{task_id}/scripts/execute.py"
          ],
          "write_scope": "selected_task_and_required_shared_dependencies",
          "ordinary_build_values_location": "Rust/requests/{request_id}.json",
          "verification_status_after_behavior_change": "not-run",
          "workflow_regeneration_inputs": [
            "Rust/catalog.json",
            "Rust/toolchains/pins.json",
            "Rust/shared/render_workflows.py"
          ],
          "static_validation_operation": "static_validate"
        },
        "task_add": {
          "required_files": [
            "Rust/tasks/{task_id}/task.json",
            "Rust/tasks/{task_id}/config/options.json",
            "Rust/tasks/{task_id}/scripts/setup.py",
            "Rust/tasks/{task_id}/scripts/execute.py",
            "Rust/tasks/{task_id}/README.md"
          ],
          "index_update": {
            "file": "Rust/catalog.json",
            "array_pointer": "/tasks",
            "entry_fields": [
              "id",
              "definition",
              "workflow"
            ]
          },
          "enum_updates": [
            {
              "file": "Rust/schemas/request.schema.json",
              "pointer": "/properties/task/enum"
            },
            {
              "file": "Rust/schemas/task.schema.json",
              "pointer": "/properties/id/enum"
            }
          ],
          "shared_operation_mapping": "Rust/shared/cargo.py",
          "additional_target_operation": "target_add",
          "workflow_operation": "workflow_regenerate",
          "validation_operation": "static_validate",
          "verification_status": "not-run",
          "stub_execution": false
        },
        "target_modify": {
          "schema": "Rust/schemas/target.schema.json",
          "index": "Rust/targets/catalog.json",
          "definition": "Rust/targets/{target_family}/{target_id}.json",
          "required_runtime_fields": [
            "triple",
            "family",
            "runner",
            "can_execute",
            "rustup_target",
            "verification_status"
          ],
          "platform_implementation": "Rust/shared/target.py",
          "verification_status_after_behavior_change": "not-run",
          "validation_operation": "static_validate"
        },
        "target_add": {
          "definition": "Rust/targets/{target_family}/{target_id}.json",
          "schema": "Rust/schemas/target.schema.json",
          "index_update": {
            "file": "Rust/targets/catalog.json",
            "array_pointer": "/targets",
            "entry_fields": [
              "triple",
              "definition"
            ]
          },
          "compatibility_fields": [
            "task.families",
            "target.family",
            "target.runner",
            "target.can_execute"
          ],
          "required_dependencies": [
            "rust_target",
            "linker_if_required",
            "sdk_if_required",
            "native_dependencies_if_required"
          ],
          "validation_operation": "static_validate",
          "verification_status": "not-run"
        },
        "shared_modify": {
          "root": "Rust/shared/",
          "dependent_task_lookup": "Rust/catalog.json",
          "request_schema_changes": "Rust/schemas/request.schema.json",
          "result_schema_changes": "Rust/schemas/result.schema.json",
          "validator": "Rust/shared/request.py",
          "validator_supported_keywords": [
            "type",
            "properties",
            "required",
            "additionalProperties",
            "enum",
            "const",
            "pattern",
            "minLength",
            "maxLength",
            "minItems",
            "maxItems",
            "uniqueItems",
            "minimum",
            "maximum",
            "$ref_local"
          ],
          "unsupported_schema_keyword_change_requires_validator_change": true,
          "validation_operation": "static_validate"
        },
        "toolchain_modify": {
          "write": [
            "Rust/toolchains/pins.json",
            "Rust/toolchains/defaults.json"
          ],
          "action_pin_format": "git_commit_sha",
          "source_toolchain_precedence": [
            "request_override",
            "source_toolchain_file",
            "repository_default"
          ],
          "workflow_operation": "workflow_regenerate",
          "validation_operation": "static_validate"
        },
        "workflow_regenerate": {
          "argv": [
            "python",
            "Rust/shared/render_workflows.py"
          ],
          "cwd": "repository_root",
          "inputs": [
            "Rust/catalog.json",
            "Rust/toolchains/pins.json",
            "Rust/shared/render_workflows.py"
          ],
          "outputs_lookup": "Rust/catalog.json#/tasks",
          "output_directory": ".github/workflows/",
          "starts_workflow": false,
          "compiles_source": false
        },
        "static_validate": {
          "argv": [
            "python",
            "Rust/shared/run.py",
            "static-check"
          ],
          "cwd": "repository_root",
          "checks": [
            "task_schema",
            "request_schema",
            "target_selection",
            "python_syntax",
            "json_parsing",
            "file_connections",
            "trigger_model",
            "workflow_task_binding"
          ],
          "compiles_source": false,
          "installs_dependencies": false,
          "starts_workflow": false,
          "runtime_verification": false
        },
        "runtime_verify": {
          "workflow": ".github/workflows/rust-verify-infrastructure.yml",
          "request": "Rust/requests/verify-linux.json",
          "suite": "Rust/verification/suite.json",
          "implementation": "Rust/shared/verification.py",
          "source_root": "Rust/verification/projects/",
          "enabled_in_current_phase": true,
          "trigger": "explicit_workflow_dispatch",
          "status": "not_run"
        }
      }
    },
    "source_delivery": {
      "type": "object",
      "const": {
        "modes": [
          "repository_source_commit",
          "external_repository_commit_or_ref"
        ],
        "local_source_path": "Rust/sources/{request_id}/",
        "repository_default": "GITHUB_REPOSITORY",
        "local_ref_default": "resolved_request_commit",
        "external_ref_required": true,
        "resolved_commit_output": "result.json#/source/commit",
        "source_token_secret": "RUST_SOURCE_TOKEN",
        "source_checkout_separate_from_infrastructure": true
      }
    },
    "build_isolation": {
      "type": "object",
      "const": {
        "work_path": "Rust/.runs/{request_id}/{run_id}-{run_attempt}/{target_id}/",
        "source_subpath": "source/",
        "cargo_target_subpath": "target/",
        "report_subpath": "report/",
        "product_subpath": "report/products/",
        "tracked_runtime_output": false,
        "cache": {
          "compiled_outputs": false,
          "dependency_downloads": true,
          "key_components": [
            "runner_os",
            "runner_arch",
            "infrastructure_commit",
            "target_id",
            "request_commit"
          ]
        },
        "runner_image_immutability": false,
        "record_actual_versions": true
      }
    },
    "artifacts": {
      "type": "object",
      "const": {
        "result_schema": "Rust/schemas/result.schema.json",
        "always_expected": [
          "result.json",
          "request.json"
        ],
        "conditional": [
          "build.log",
          "cargo-metadata.json",
          "Cargo.lock",
          "cargo-messages.jsonl",
          "test-output.txt",
          "benchmark-output.txt",
          "verification.json",
          "exception.txt",
          "artifacts.json",
          "products.zip"
        ],
        "product_selection": "cargo_compiler_artifact_messages_and_explicit_output_globs",
        "checksums": "sha256",
        "required_output_missing_status": "failure"
      }
    },
    "drift_controls": {
      "type": "object",
      "const": {
        "task_discovery": "catalog_reference",
        "target_discovery": "catalog_reference",
        "shared_implementation_reuse": true,
        "per_build_configuration": "request_json",
        "duplicate_executable_workflow_definitions": false,
        "generated_workflow_source": "Rust/shared/render_workflows.py",
        "existing_lockfile_policy": "locked",
        "resolved_lockfile_delivery": true,
        "recorded_identity": [
          "source_commit",
          "request_commit",
          "infrastructure_commit",
          "run_id",
          "run_attempt",
          "target"
        ],
        "static_success_equals_runtime_success": false
      }
    },
    "state": {
      "type": "object",
      "const": {
        "implementation": "written",
        "runtime_verification": "not_run",
        "task_status_source": "Rust/tasks/{task_id}/task.json#/verification_status",
        "target_status_source": "Rust/targets/{target_family}/{target_id}.json#/verification_status",
        "current_phase": "runtime_verification"
      }
    }
  },
  "$defs": {
    "build_request": {
      "$ref": "schemas/request.schema.json"
    },
    "task": {
      "$ref": "schemas/task.schema.json"
    },
    "target": {
      "$ref": "schemas/target.schema.json"
    },
    "catalog": {
      "$ref": "schemas/catalog.schema.json"
    },
    "result": {
      "$ref": "schemas/result.schema.json"
    }
  }
}
