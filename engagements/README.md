# Engagements

Create one private `engagements/<name>/` directory per authorized target. Start with the fields in `ENGAGEMENT-TEMPLATE.md` and keep a `notes.md` ledger for scope, phase approvals, commands, evidence, source citations, findings, and cleanup. The RedOps orchestrator passes this exact ledger path to every specialist; agents hand off through it using their `.opencode/tools.json` profile.

The directories are ignored by Git. Never commit credentials, VPN configuration, target loot, or raw exports. No target is authorized merely because its directory exists.
