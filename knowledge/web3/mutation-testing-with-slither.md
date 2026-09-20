---
title: "Mutation Testing With Slither"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/blockchain/smart-contract-security/mutation-testing-with-slither.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web3
---

# Mutation Testing for Smart Contracts (slither-mutate, mewt, MuTON)

## Why coverage can deceive

Consider this simple threshold check:

```
function verifyMinimumDeposit(uint256 deposit) public returns (bool) {
    if (deposit >= 1 ether) {
        return true;
    } else {
        return false;
    }
}
```
Unit tests that only check a value below and a value above the threshold can reach 100% line/branch coverage while failing to assert the equality boundary (==). A refactor to `deposit >= 2 ether` would still pass such tests, silently breaking protocol logic.[\[2\]](#references)

Mutation testing exposes this gap by mutating the condition and verifying tests fail.

For smart contracts, surviving mutants frequently map to missing checks around:

- Authorization and role boundaries
- Accounting/value-transfer invariants
- Revert conditions and failure paths
- Boundary conditions (`==` , zero values, empty arrays, max/min values)

## Mutation operators with the highest security signal

Useful mutation classes for contract auditing:[\[1\]](#references)[\[2\]](#references)

- **High severity** : replace statements with`revert()` to expose unexecuted paths
- **Medium severity** : comment out lines / remove logic to reveal unverified side effects
- **Low severity** : subtle operator or constant swaps such as`>=` ->`>` or`+` ->`-`
- Other common edits: assignment replacement, boolean flips, condition negation, and type changes

Practical goal: kill all meaningful mutants, and explicitly justify survivors that are irrelevant or semantically equivalent.

## Why syntax-aware mutation is better than regex

Older mutation engines relied on regex or line-oriented rewrites. That works, but it has important limitations:[\[1\]](#references)

- Multi-line statements are hard to mutate safely
- Language structure is not understood, so comments/tokens can be targeted badly
- Generating every possible variant on a weak line wastes large amounts of runtime

AST- or Tree-sitter-based tooling improves this by targeting structured nodes instead of raw lines:[\[1\]](#references)

- **slither-mutate** uses Slither’s Solidity AST.<sup>[\[4\]](#references)</sup>
- **mewt** uses Tree-sitter as a language-agnostic core.<sup>[\[6\]](#references)</sup>
- **MuTON** builds on`mewt` and adds first-class support for TON languages such as FunC, Tolk, and Tact.<sup>[\[7\]](#references)</sup>

This makes multi-line constructs and expression-level mutations much more reliable than regex-only approaches.

## Running mutation testing with slither-mutate

Requirements: Slither v0.10.2+.

- List options and mutators:

```
slither-mutate --help
slither-mutate --list-mutators
```
- Foundry example (capture results and keep a full log):<sup>[\[2\]](#references)</sup>

```
slither-mutate ./src/contracts --test-cmd="forge test" &> >(tee mutation.results)
```
- If you don’t use Foundry, replace `--test-cmd` with how you run tests (e.g.,`npx hardhat test` ,`npm test` ).

Artifacts are stored in `./mutation_campaign` by default. Uncaught (surviving) mutants are copied there for inspection.[\[5\]](#references)

### Understanding the output

Report lines look like:

```
INFO:Slither-Mutate:Mutating contract ContractName
INFO:Slither-Mutate:[CR] Line 123: 'original line' ==> '//original line' --> UNCAUGHT
```
- The tag in brackets is the mutator alias (e.g., `CR` = Comment Replacement).
- `UNCAUGHT` means tests passed under the mutated behavior → missing assertion.

## Reducing runtime: prioritize impactful mutants

Mutation campaigns can take hours or days. Tips to reduce cost:[\[1\]](#references)[\[2\]](#references)

- Scope: Start with critical contracts/directories only, then expand.
- Prioritize mutators: If a high-priority mutant on a line survives (for example `revert()` or comment-out), skip lower-priority variants for that line.
- Use two-phase campaigns: run focused/fast tests first, then re-test only uncaught mutants with the full suite.
- Map mutation targets to specific test commands when possible (for example auth code -> auth tests).
- Restrict campaigns to high/medium severity mutants when time is tight.
- Parallelize tests if your runner allows it; cache dependencies/builds.
- Fail-fast: stop early when a change clearly demonstrates an assertion gap.

The runtime math is brutal: `1000 mutants x 5-minute tests ~= 83 hours`, so campaign design matters as much as the mutator itself.[\[1\]](#references)

## Persistent campaigns and triage at scale

One weakness of older workflows is dumping results only to `stdout`. For long campaigns, this makes pause/resume, filtering, and review harder.[\[1\]](#references)

`mewt`/`MuTON` improve this by storing mutants and outcomes in SQLite-backed campaigns. Benefits:[\[1\]](#references)

- Pause and resume long runs without losing progress
- Filter only uncaught mutants in a specific file or mutation class
- Export/translate results to SARIF for review tooling
- Give AI-assisted triage smaller, filtered result sets instead of raw terminal logs

Persistent results are especially useful when mutation testing becomes part of an audit pipeline instead of a one-off manual review.

## Triage workflow for surviving mutants

1.
Inspect the mutated line and behavior.
  - Reproduce locally by applying the mutated line and running a focused test.
2.
Strengthen tests to assert state, not only return values.
  - Add equality-boundary checks (e.g., test threshold `==` ).
  - Assert post-conditions: balances, total supply, authorization effects, and emitted events.
3. Add equality-boundary checks (e.g., test threshold
4.
Replace overly permissive mocks with realistic behavior.
  - Ensure mocks enforce transfers, failure paths, and event emissions that occur on-chain.
5.
Add invariants for fuzz tests.
  - E.g., conservation of value, non-negative balances, authorization invariants, monotonic supply where applicable.
6.
Separate true positives from semantic no-ops.
  - Example: `x > 0` ->`x != 0` is meaningless when`x` is unsigned.
7. Example:
8.
Re-run the campaign until survivors are killed or explicitly justified.

## Case study: revealing missing state assertions (Arkis protocol)

A mutation campaign during an audit of the Arkis DeFi protocol surfaced survivors like:[\[2\]](#references)[\[3\]](#references)

```
INFO:Slither-Mutate:[CR] Line 33: 'cmdsToExecute.last().value = _cmd.value' ==> '//cmdsToExecute.last().value = _cmd.value' --> UNCAUGHT
```
Commenting out the assignment didn’t break the tests, proving missing post-state assertions. Root cause: code trusted a user-controlled `_cmd.value` instead of validating actual token transfers. An attacker could desynchronize expected vs. actual transfers to drain funds. Result: high severity risk to protocol solvency.[\[2\]](#references)[\[3\]](#references)

Guidance: Treat survivors that affect value transfers, accounting, or access control as high-risk until killed.

## Do not blindly generate tests to kill every mutant

Mutation-driven test generation can backfire if the current implementation is wrong. Example: mutating `priority >= 2` to `priority > 2` changes behavior, but the right fix is not always “write a test for `priority == 2`”. That behavior may itself be the bug.[\[1\]](#references)

Safer workflow:

- Use surviving mutants to identify ambiguous requirements
- Validate expected behavior from specs, protocol docs, or reviewers
- Only then encode the behavior as a test/invariant

Otherwise, you risk hard-coding implementation accidents into the test suite and gaining false confidence.

## Practical checklist

- Run a targeted campaign:
  - `slither-mutate ./src/contracts --test-cmd="forge test"`
- Prefer syntax-aware mutators (AST/Tree-sitter) over regex-only mutation when available.
- Triage survivors and write tests/invariants that would fail under the mutated behavior.
- Assert balances, supply, authorizations, and events.
- Add boundary tests (`==` , overflows/underflows, zero-address, zero-amount, empty arrays).
- Replace unrealistic mocks; simulate failure modes.
- Persist results when the tooling supports it, and filter uncaught mutants before triage.
- Use two-phase or per-target campaigns to keep runtime manageable.
- Iterate until all mutants are killed or justified with comments and rationale.

## References

- [1] [Mutation testing for the agentic era](https://blog.trailofbits.com/2026/04/01/mutation-testing-for-the-agentic-era/)
- [2] [Use mutation testing to find the bugs your tests don’t catch (Trail of Bits)](https://blog.trailofbits.com/2025/09/18/use-mutation-testing-to-find-the-bugs-your-tests-dont-catch/)
- [3] [Arkis DeFi Prime Brokerage Security Review (Appendix C)](https://github.com/trailofbits/publications/blob/master/reviews/2024-12-arkis-defi-prime-brokerage-securityreview.pdf)
- [4] [Slither (GitHub)](https://github.com/crytic/slither)
- [5] [Slither Mutator documentation](https://github.com/crytic/slither/blob/master/docs/src/tools/Mutator.md)
- [6] [mewt](https://github.com/trailofbits/mewt)
- [7] [MuTON](https://github.com/trailofbits/muton)
