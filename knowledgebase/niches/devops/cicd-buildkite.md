---
title: CI/CD - BuildKite
source_url: https://github.com/swisskyrepo/InternalAllTheThings/blob/203bb0c0b290bf7c9158c32d43523b8d66f292c1/docs/devops/cicd-buildkite.md
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: devops
---
The configuration files for BuildKite builds are located in `.buildkite/*.yml`\
BuildKite build are often self-hosted, this means that you may gain excessive privileges to the kubernetes cluster that runs the runners, or to the hosting cloud environment.

In order to run an OS command in a workflow that builds pull requests - simply add a `command` instruction to the step.

```yaml
steps:
  - label: "Example Test"
    command: echo "Hello!"
```
