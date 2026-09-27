---
title: "AI Security"
source: hacktricks.wiki
source_url: https://hacktricks.wiki/AI/index.html
fetched_at: 2026-09-20T09:50:19Z
license: unspecified
category: misc
---

# AI in Cybersecurity

## Main Machine Learning Algorithms

The best starting point to learn about AI is to understand how the main machine learning algorithms work. This will help you to understand how AI works, how to use it and how to attack it:

[AI Supervised Learning Algorithms](./AI-Supervised-Learning-Algorithms.html)

[AI Unsupervised Learning Algorithms](./AI-Unsupervised-Learning-Algorithms.html)

[AI Reinforcement Learning Algorithms](./AI-Reinforcement-Learning-Algorithms.html)

### LLMs Architecture

In the following page you will find the basics of each component to build a basic LLM using transformers:

## AI Security

### AI Risk Frameworks

Two useful starting frameworks for assessing AI-system risk are the OWASP Machine Learning Security Top 10 and Google’s Secure AI Framework (SAIF). They are complementary rather than an exhaustive list of AI risk frameworks.[\[1\]](#references)[\[2\]](#references)

### AI Prompts Security

LLMs have made the use of AI explode in the last years, but they are not perfect and can be tricked by adversarial prompts. This is a very important topic to understand how to use AI safely and how to attack it:

### AI Models RCE

It’s very common to developers and companies to run models downloaded from the Internet, however just loading a model might be enough to execute arbitrary code on the system. This is a very important topic to understand how to use AI safely and how to attack it:

### AI-Assisted KYC Bypass

Generative video can be combined with virtual-camera injection and camera API manipulation to bypass weak KYC, age-verification, and biometric liveness workflows:

### AI Model Context Protocol

MCP (Model Context Protocol) is an open protocol for connecting AI applications to tools and data sources. Because MCP servers can expose data and actions, assessments must include authorization, consent, tool-input validation, and trust-boundary review.[\[3\]](#references)

### AI-Assisted Fuzzing & Automated Vulnerability Discovery

[Ai Assisted Fuzzing And Vulnerability Discovery](AI-Assisted-Fuzzing-and-Vulnerability-Discovery.html)

### Web Black-Box AI Pentester Bots

LLM-powered agents can automate long-running black-box web pentesting workflows when they are supported by observability, orchestration, authenticated session handling, and adversarial validation:

[Web Black-Box AI Pentester Bots](Web-Black-Box-AI-Pentester-Bots.html)

## References

- [1] [OWASP Machine Learning Security Top 10](https://owasp.org/www-project-machine-learning-security-top-10/)
- [2] [Google — Secure AI Framework (SAIF)](https://saif.google/)
- [3] [Model Context Protocol — Introduction](https://modelcontextprotocol.io/docs/getting-started/intro)
