---
title: "State Divergence Default Value Authorization Bypasses"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/blockchain/blockchain-and-crypto-currencies/state-divergence-default-value-authorization-bypasses.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web3
---

# State Divergence and Default-Value Authorization Bypasses

## Audit duplicated state as an authorization boundary

For every value used by a permission check, enumerate **all representations**: canonical module state, object fields, cached aggregates, indexes, snapshots, bridge records, and off-chain mirrors. Then trace every create, mint, burn, transfer, reset, migration, and synchronization path to determine which copy is updated in each object mode. A field may be authoritative for one mode and informational for another.[\[1\]](#references)

A practical review workflow is:[\[1\]](#references)

1. Locate protected actions and reduce each authorization branch to a boolean predicate.
2. For every operand, record its store, update paths, lifecycle states, and source of truth.
3. Generate transitions that update only one representation, then compare all copies.
4. Attempt the protected action from a fresh account after each transition.
5. Continue beyond the bypass: if the action edits an ACL, self-grant persistent roles and invoke normal privileged APIs.

Suspicious patterns include `cachedSupply == balance`, `metadataOwner == caller`, or `snapshotShares == currentShares` when the two sides have different synchronization rules. Querying an authoritative value for one operand does not make the comparison safe when the other operand is stale.[\[1\]](#references)

## Default-value equality bypass

An equality predicate is also unsafe when both operands can independently take the same default value. The check below grants “full supply control” to any empty account when `supply` is zero, regardless of whether zero results from stale metadata or a legitimately unfunded object.[\[1\]](#references)[\[3\]](#references)

```
balance := bank.GetBalance(ctx, caller, denom)
supply := marker.GetSupply() // duplicate or stale representation
return balance.Amount.Equal(supply.Amount) // 0 == 0 -> true
```
Switching to the canonical store fixes divergence but **not** the empty-object case. The security property must include an independent validity condition; the Provenance patch uses live bank supply and rejects nil or zero supply before comparing the caller balance.[\[1\]](#references)[\[2\]](#references)[\[3\]](#references)

```
supply := bank.GetSupply(ctx, denom)
if supply.Amount.IsNil() || supply.Amount.IsZero() {
    return false
}
balance := bank.GetBalance(ctx, caller, denom)
return supply.Equal(NewCoin(denom, balance.Amount))
```
Apply the same reasoning to quorum counts, ownership percentages, debt, collateral, epochs, nonces, timestamps, and counters: `callerValue == protectedValue` must not authorize a caller until the protected value is independently valid and belongs to the expected domain.[\[1\]](#references)

## ACL takeover to legitimate privileged operations

A bypass in an ACL-editing operation is a durable privilege-escalation primitive. In the Provenance case, an unprivileged account with zero tokens could pass the stale `0 == 0` supply test, grant itself administrative, mint, and withdrawal permissions, and then use ordinary message handlers to mint assets or withdraw escrow. The exploit therefore required no second vulnerability after the ACL change.[\[1\]](#references)

General exploitation sequence:[\[1\]](#references)

1. Find an object whose non-authoritative field differs from live state, or whose protected value is the default.
2. Use a new/empty identity so its local value matches that stale/default value.
3. Call the role-management, ownership-transfer, or policy-update endpoint and self-grant durable capabilities.
4. Confirm persistence by reading the ACL from canonical state.
5. Invoke the legitimate high-impact operation (mint, withdraw, upgrade, transfer ownership, or change policy).

When triaging impact, inspect every capability reachable from the new role rather than stopping at the authorization bypass. Escrow-like accounts may custody assets unrelated to the object whose stale metadata enabled the takeover.[\[1\]](#references)

## Invariant and stateful-fuzzing targets

Specify authorization independently from the implementation. For a full-supply shortcut, the minimal invariant is:[\[1\]](#references)[\[2\]](#references)

```
controlsAllSupply(caller, asset) == true
    => authoritativeSupply(asset) > 0
    && authoritativeBalance(caller, asset) == authoritativeSupply(asset)
```
Use a model/state-machine fuzzer to generate sequences—not isolated calls—covering creation, zero-value initialization, activation/finalization, minting, burning, transfers, resets, migrations, sync calls, and ACL changes. After every transition, compare duplicated representations and assert that a fresh account cannot perform any protected action. Seed explicit cases for zero, one unit, partial ownership, full ownership, stale-low, and stale-high values.[\[1\]](#references)[\[2\]](#references)

High-signal regression properties are:[\[1\]](#references)[\[2\]](#references)

- Zero authoritative supply never implies ownership or administration.
- Partial holders cannot become administrators when a duplicate supply equals their balance.
- A true full holder retains the intended shortcut when live supply is positive.
- Failed self-grants do not mutate the ACL or enable downstream privileged calls.
- Mode changes cannot silently change which representation an authorization check treats as authoritative.

## References

- [1] [State divergence enables unauthorized access (Trail of Bits)](https://blog.trailofbits.com/2026/08/25/state-divergence-enables-unauthorized-access/)
- [2] [Provenance PR #2734 - Fix stale supply checks](https://github.com/provenance-io/provenance/pull/2734)
- [3] [Provenance commit c81fd65 - Reject zero supply in the total-supply authorization shortcut](https://github.com/provenance-io/provenance/commit/c81fd65f8ad48de42d5a6d68e761a0851c7e72c4)
