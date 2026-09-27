---
name: toolbox
description: Select Exegol tools and precompiled binaries through the specialist policy.
---

Select tools from the role's `.opencode/tools.json` profile and run them inside the
approved Exegol workspace. Treat precompiled binaries as immutable resources supplied
by Exegol; do not download arbitrary binaries into the repository. If a required tool
or MCP is missing, report the capability gap and stop rather than silently substituting
an unapproved host tool.
