# Mobile agent

RedOps includes a mobile-specific agent profile at
[`agents/mobile.md`](../agents/mobile.md). It adapts the upstream
[Mobile-ReverseSkill](https://github.com/alvinhayy/Mobile-ReverseSkill) to the
RedOps RAG and Exegol execution model.

## How to use it

Start an authorized engagement with an APK, AAB, IPA, or bundle in an isolated
workspace. Follow the pipeline in the profile:

```text
detect stack -> static analysis -> attack surface -> vuln hunt
             -> local Frida/Exegol confirmation -> optional offline fuzzing
```

The installed skills provide the detailed procedures:

- `reverse-engineer` for static-only APK/IPA/bundle analysis;
- `mobile-vuln-hunt` for signature scans, reachability triage, and finding output;
- `afl-fuzzing` for Android native-library fuzzing on a local emulator.

Static analysis must never execute the target app. Dynamic work is restricted to
the authorized local lab. Fuzzing must remain offline/local and must first pass a
positive harness reachability check.

## Expected outputs

Keep target-specific output outside the shared knowledge corpus unless it has been
reviewed and sanitized:

- `findings/vuln-classes-<slug>-<date>/vuln-classes.json`;
- `findings/<slug>/report.md`;
- `findings/<slug>/deception-analysis.{md,json}` when endpoint/secret deception is
  relevant;
- `static/` artifacts and `fuzz/` artifacts in the private engagement workspace.

Findings should include evidence locations, reachability, confirmation state,
impact, remediation, and source provenance. Do not commit production credentials,
session tokens, or unreviewed target data.

## Exegol example

```bash
export REDOPS_EXECUTION_BACKEND=exegol
export REDOPS_EXEGOL_CONTAINER=redops-mobile
redops exegol status
redops exegol exec -- frida --version
```

The runner uses an argv list and does not invoke a shell. Exegol setup and network
permissions remain the operator's responsibility and must match the written scope.
