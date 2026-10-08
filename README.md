{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://raw.githubusercontent.com/Dosa42/Chatgpt.com-Toolchain/main/README.md",
  "type": "object",
  "required": [
    "schema_version",
    "repository",
    "purpose",
    "execution",
    "languages",
    "rust_entry",
    "operations",
    "state"
  ],
  "additionalProperties": false,
  "properties": {
    "schema_version": {
      "type": "integer",
      "const": 1
    },
    "repository": {
      "type": "string",
      "const": "Dosa42/Chatgpt.com-Toolchain"
    },
    "purpose": {
      "type": "array",
      "const": [
        "source_build",
        "source_compile",
        "sandbox_capability_fallback"
      ]
    },
    "execution": {
      "type": "object",
      "const": {
        "compilation_environment": "github_actions_runner",
        "coordination_environment": "chatgpt",
        "github_interface": "github_plugin",
        "trigger": "workflow_dispatch",
        "automatic_push_trigger": false,
        "automatic_pull_request_trigger": false,
        "automatic_schedule_trigger": false,
        "workspace_compilation": false
      }
    },
    "languages": {
      "type": "object",
      "const": {
        "Rust": {
          "root": "Rust/",
          "descriptor": "Rust/README.md",
          "catalog": "Rust/catalog.json",
          "implementation": "written",
          "runtime_verification": "not_run"
        },
        "Go": {
          "root": "Go/",
          "implementation": "not_implemented"
        },
        "C": {
          "root": "C/",
          "implementation": "not_implemented"
        },
        "C++": {
          "root": "C++/",
          "implementation": "not_implemented"
        }
      }
    },
    "rust_entry": {
      "type": "object",
      "const": {
        "descriptor": "Rust/README.md",
        "task_catalog": "Rust/catalog.json",
        "target_catalog": "Rust/targets/catalog.json",
        "request_schema": "Rust/schemas/request.schema.json",
        "task_schema": "Rust/schemas/task.schema.json",
        "target_schema": "Rust/schemas/target.schema.json",
        "result_schema": "Rust/schemas/result.schema.json",
        "catalog_schema": "Rust/schemas/catalog.schema.json",
        "workflow_directory": ".github/workflows/",
        "path_base": "repository_root"
      }
    },
    "operations": {
      "type": "object",
      "const": {
        "rust_discover": {
          "read": [
            "Rust/README.md",
            "Rust/catalog.json",
            "Rust/targets/catalog.json"
          ],
          "task_lookup": {
            "index": "/tasks",
            "key": "id",
            "fields": [
              "definition",
              "workflow"
            ]
          }
        },
        "rust_use": {
          "descriptor_path": "Rust/README.md",
          "operation_keys": [
            "discover",
            "request_create",
            "dispatch",
            "run_find",
            "run_watch",
            "artifact_download"
          ]
        },
        "rust_modify": {
          "descriptor_path": "Rust/README.md",
          "operation_keys": [
            "task_modify",
            "task_add",
            "target_modify",
            "target_add",
            "shared_modify",
            "toolchain_modify",
            "workflow_regenerate",
            "static_validate"
          ]
        },
        "readme_modify": {
          "format": "json",
          "schema_dialect": "https://json-schema.org/draft/2020-12/schema",
          "markdown": false,
          "code_fences": false,
          "prose_fields": false
        }
      }
    },
    "state": {
      "type": "object",
      "const": {
        "implementation_commit": "6d6113d62f6b98064f701ef8aa8ae403463506dd",
        "implementation": "written",
        "verification": "static_only",
        "runtime_verification": "not_run",
        "current_phase": "runtime_verification",
        "current_phase_dispatch": true
      }
    }
  },
  "$defs": {
    "rust_contract": {
      "$ref": "Rust/README.md"
    },
    "build_request": {
      "$ref": "Rust/schemas/request.schema.json"
    },
    "build_result": {
      "$ref": "Rust/schemas/result.schema.json"
    }
  }
}
