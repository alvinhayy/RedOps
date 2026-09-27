# Engagement Packet — Pre-Engagement Scope Document

Complete every field with the client/operator BEFORE any active phase begins.
An active phase may start only when this packet is fully signed and its
phase-specific approval line is filled. Methodology framing follows:
[S1] knowledge/methodology/pentesting-methodology.md — https://hacktricks.wiki/generic-methodologies-and-resources/pentesting-methodology.html

> Secret policy: this packet contains NO credential fields. Credentials and
> tokens are exchanged out-of-band only and never stored in engagement
> artifacts or phase handoffs.

## 1. Engagement metadata

- Engagement name: ______
- Operator (orchestrator): ______
- Client organization: ______
- Packet version / date: ______

## 2. Written authorization

Authorization for this engagement is granted as follows:

- Authorizing signatory (name, role): ______
- Signature: ______
- Date: ______
- Authorization reference / contract number: ______
- Scope of authority (what this signature covers): ______

## 3. Target inventory (explicit allowlist)

Only rows marked IN SCOPE may be touched by any phase. Everything else is
out of scope by default.

| # | Identifier (exact IP/host/app/URL) | Type | Location/ENV | Owner | In scope? (YES/no) | Notes |
|---|-----------------------------------|------|--------------|-------|--------------------|-------|
| 1 | ______ | ______ | ______ | ______ | ______ | ______ |
| 2 | ______ | ______ | ______ | ______ | ______ | ______ |
| 3 | ______ | ______ | ______ | ______ | ______ | ______ |

## 4. Exclusions

- Explicitly excluded systems/networks/accounts: ______
- Blacklisted times or conditions: ______
- Data types that must not be touched/exfiltrated: ______

## 5. Test window & rate limits

- Test window (dates/times, timezone): ______
- Max concurrent requests per target: ______
- Requests per second/minute cap: ______
- Bandwidth or load ceilings: ______
- No-test periods (backups, peak hours): ______

## 6. Rules of engagement

- Permitted techniques: ______
- Prohibited techniques (e.g., DoS, physical, social engineering of third parties): ______
- Evidence handling (capture, storage, retention, encryption at rest): ______
- Client escalation contacts (name, phone, email, hours): ______
- Operator escalation contacts: ______
- Stop conditions (what halts the engagement immediately): ______
- Rollback expectations (system restoration, artifact removal, verification): ______

## 7. Phase-by-phase approvals

Each active phase requires its own explicit, dated approval line. Approval of
one phase does NOT authorize any other phase.

| Phase | Approved? (YES/no) | Approved by | Date | Exact targets covered |
|-------|--------------------|-------------|------|------------------------|
| information_gathering | ______ | ______ | ______ | ______ |
| vulnerability_assessment | ______ | ______ | ______ | ______ |
| exploitation | ______ | ______ | ______ | ______ |
| post_exploitation | ______ | ______ | ______ | ______ |
| lateral_movement | ______ | ______ | ______ | ______ |
| proof_of_concept | ______ | ______ | ______ | ______ |
| post_engagement | ______ | ______ | ______ | ______ |

## 8. Open questions

- ______
- ______

## 9. Completion checklist

- [ ] All target inventory rows have explicit in-scope markings
- [ ] Written authorization block signed and dated
- [ ] Rate limits accepted by recon phase owner
- [ ] Every active phase has its own approval line
- [ ] No credentials recorded anywhere in this packet
