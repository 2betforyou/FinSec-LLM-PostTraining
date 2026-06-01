# Data Card

## Data Types

The original research workspace used a mixture of:

- Korean financial-security laws and enforcement decrees,
- regulatory and security guidelines,
- MITRE/security-related reference material,
- challenge-style QA pairs,
- generated or augmented QA examples for supervised fine-tuning.

This cleaned repository includes only small synthetic examples under [`examples/`](../examples). Full challenge data, generated submissions, model outputs, and any large/private raw documents are excluded.

## SFT Format

SFT examples use chat-message JSONL:

```json
{"messages":[{"role":"system","content":"..."},{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}
```

The training scripts convert each example into:

- `input_ids`: prompt tokens plus assistant-answer tokens,
- `labels`: `-100` for prompt tokens and answer token ids for assistant spans,
- `attention_mask`: standard causal LM attention mask.

This means the supervised loss is applied to the assistant answer, not to the system/user prompt.

## Retrieval Format

Retrieval documents are chunked into records with:

- chunk id,
- text,
- source path or source metadata,
- character offsets when available,
- optional extra metadata.

Embeddings are normalized and indexed with FAISS for cosine-style inner-product search. BM25 can be built as an additional lexical retrieval layer.

## Limitations

- The public repository intentionally omits full data and trained artifacts.
- Some source scripts assume local data paths from the original experiment workspace.
- Any external data should be checked for license compatibility before redistribution.
