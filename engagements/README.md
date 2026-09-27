# RedOps Engagements — Lifecycle Index

Authorized-pentest engagements run through the 8-phase RedOps graph. No active
phase may start until its gate is satisfied. Methodology reference:
[S1] knowledge/methodology/pentesting-methodology.md — https://hacktricks.wiki/generic-methodologies-and-resources/pentesting-methodology.html

## Current state

- `scope_confirmed = false`, `active_execution_enabled = false` — no engagement is authorized yet.
- Exegol container `redops` NOT found — no active execution runtime is available.
- Execution policy: **Exegol-first**. All active execution happens inside the
  Exegol runtime and belongs to the **approved phase specialist agent** for that
  phase. The scope_agent performs documentation only.

## Phase index

| # | Phase | Agent | Required artifacts | Gate | Status |
|---|-------|-------|--------------------|------|--------|
| 1 | pre_engagement | scope_agent | written_scope, target_inventory, rules_of_engagement | Written authorization + in-scope target are mandatory | ACTIVE (documentation only) — scope not yet confirmed |
| 2 | information_gathering | recon_agent | scope_reference, asset_inventory, service_or_artifact_evidence | scope_agent output delivered; rate limits accepted | PENDING gate |
| 3 | vulnerability_assessment | assessment_agent | recon_evidence, finding_hypotheses, severity_rationale | Recon evidence accepted from recon_agent | PENDING gate |
| 4 | exploitation | exploitation_agent | approved_finding, exploit_test_plan, rollback_plan | Written scope + exact per-phase approval | **BLOCKED** pending written scope + explicit approval |
| 5 | post_exploitation | post_exploitation_agent | validated_access, impact_evidence, cleanup_record | Written scope + exact per-phase approval | **BLOCKED** pending written scope + explicit approval |
| 6 | lateral_movement | lateral_movement_agent | movement_scope, source_access, destination_allowlist | Written scope + exact per-phase approval | **BLOCKED** pending written scope + explicit approval |
| 7 | proof_of_concept | poc_agent | reproduction_steps, sanitized_output, impact_statement | Validated findings from prior phases | PENDING gate |
| 8 | post_engagement | reporting_agent | finding_records, source_citations, remediation, cleanup_record | All prior phases closed with cleanup records | PENDING gate |

## Approval-gate design

1. **Phase 1 is the only entry point.** Every later phase consumes the previous
   phase's handoff; nothing downstream can start without written scope and an
   in-scope target.
2. **Active phases (4–6) are doubly gated**: written scope AND an explicit,
   dated approval line for that exact phase (see `ENGAGEMENT-TEMPLATE.md`).
   Prior approval for one phase never authorizes another.
3. **Runtime gate**: even an approved phase cannot execute while Exegol is down
   (`redops` container not found). Execution is Exegol-first and is performed
   only by the approved phase specialist.

## Handoff contract

Every phase-to-phase handoff MUST include:

- `phase_output` — the artifacts listed for the completed phase
- `source_citations` — grounded references for every claim
- `target_scope` — the exact in-scope identifiers the work applied to
- `open_questions` — unresolved items carried to the next phase

Every handoff MUST NOT include:

- credentials or tokens
- unscoped_targets
- unsupported_claims

## Start here

Copy `ENGAGEMENT-TEMPLATE.md`, complete it with the client/operator, and attach
written authorization. Until that packet is complete and signed, all phases
beyond pre_engagement remain closed.
