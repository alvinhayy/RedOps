---
title: Git repository
source_url: https://notes.incendium.rocks/pentesting-notes/web/git-repository
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: web
---

Found a .git folder? Good!

Download GitTools:&#x20;

***

## Dump Repository

We found a git directory , so we use a tool to dump the the git repository

```bash
gitdumper.sh http://blog-dev.travel.htb/.git/ ~/htb/travel/repo
```

## Extract Repository

We downloaded the repository, we also need to extract it using extractor.sh the command is given below:

```bash
extractor.sh ~/htb/travel/repo ~/htb/travel/repo-extract
```

## Git enumerating

After you dumped the repo, you can also use git commands to get more information:

```
git log
git diff <branch>
cat ./config
```
