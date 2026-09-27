---
title: CI/CD - Drone CI
source_url: https://github.com/swisskyrepo/InternalAllTheThings/blob/203bb0c0b290bf7c9158c32d43523b8d66f292c1/docs/devops/cicd-drone-ci.md
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: devops
---
The configuration files for Drone builds are located in `.drone.yml`\
Drone build are often self-hosted, this means that you may gain excessive privileges to the kubernetes cluster that runs the runners, or to the hosting cloud environment.

In order to run an OS command in a workflow that builds pull requests - simply add a `commands` instruction to the step.

```yaml
steps:
  - name: do-something
    image: some-image:3.9
    commands:
      - {Payload}
```
