# Source delivery from ChatGPT

Push a complete source tree under Rust/sources/<unique-request-id>/. A request can refer to that path in this repository. Commit source and request together; omit source.ref to use the request commit resolved by the workflow.

External source repositories use source.repository, source.ref and source.path. Branches and tags are resolved to an exact commit and recorded. Prefer a commit SHA when the build must refer to a predetermined snapshot. Access to private external sources is configured through RUST_SOURCE_TOKEN.

No user application source is supplied here yet. Real verification projects are in ../verification/projects/.
