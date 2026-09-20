---
title: AWS - Service - DynamoDB
source_url: https://github.com/swisskyrepo/InternalAllTheThings/blob/203bb0c0b290bf7c9158c32d43523b8d66f292c1/docs/cloud/aws/aws-dynamodb.md
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---

> Amazon DynamoDB is a key-value and document database that delivers single-digit millisecond performance at any scale. It's a fully managed, multi-region, multi-active, durable database with built-in security, backup and restore, and in-memory caching for internet-scale applications. DynamoDB can handle more than 10 trillion requests per day and can support peaks of more than 20 million requests per second.

## List Tables

```bash
$ aws --endpoint-url http://s3.bucket.htb dynamodb list-tables

{
    "TableNames": [
        "users"
    ]
}
```

## Enumerate Table Content

```bash
$ aws --endpoint-url http://s3.bucket.htb dynamodb scan --table-name users | jq -r '.Items[]'

{
  "password": {
    "S": "Management@#1@#"
  },
  "username": {
    "S": "Mgmt"
  }
}
```

## References

* [Amazon DynamoDB Documentation - AWS](https://docs.aws.amazon.com/dynamodb/)
