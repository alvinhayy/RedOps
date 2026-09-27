---
title: CI/CD - CircleCI
source_url: https://github.com/swisskyrepo/InternalAllTheThings/blob/203bb0c0b290bf7c9158c32d43523b8d66f292c1/docs/devops/cicd-circle-ci.md
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: devops
---
The configuration files for CircleCI builds are located in `.circleci/config.yml`\
By default - CircleCI pipelines don't build forked pull requests. It's an opt-in feature that should be enabled by the pipeline owners.

In order to run an OS command in a workflow that builds pull requests - simply add a `run` instruction to the step.

```yaml
jobs:
  build:
    docker:
     - image: cimg/base:2022.05
    steps:
        - run: echo "Say hello to YAML!"
```
