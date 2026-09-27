---
name: toolbox
description: Select Exegol tools and precompiled binaries through the specialist policy.
---

Resolve the repository root first. Read the role's `.opencode/tools.json` profile.
Its `mcp` list is the allowed MCP
set; OpenCode agent permissions enforce the named server tool patterns. Check
connection health separately before use. Run authorized target tools inside the
approved Exegol workspace, not directly on the host unless the operator approves
a bounded exception.

Before using a file from `precompiled-binaries/`, require an entry in
`precompiled-binaries/MANIFEST.json` with its relative path and SHA-256 digest,
then verify that digest. An empty manifest means no local binaries are available;
use an Exegol-provided tool or report the gap. Do not download arbitrary binaries
into the repository. Record command, output, artifact provenance and cleanup in
`engagements/<name>/notes.md`. If a required tool or MCP is missing, report the
capability gap rather than silently substituting an unapproved tool.
