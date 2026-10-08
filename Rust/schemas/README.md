# Machine-readable contracts

request.schema.json defines per-build configuration. task.schema.json defines tasks. target.schema.json defines target environments. catalog.schema.json defines task discovery. result.schema.json defines the final report.

All are JSON Schema Draft 2020-12 documents. The runtime validator intentionally implements the keyword subset used here: type, properties, required, additionalProperties, enum, const, pattern, min/maxLength, min/maxItems, uniqueItems, minimum/maximum and local $ref. It is not advertised as an unrestricted JSON Schema engine. Keep schemas within this subset or extend the validator in the same change.

Unknown request fields are rejected. Paths are additionally confined at runtime. Cross-field requirements such as task/target compatibility, executable tests and custom target files are checked by the actual runner pipeline.
