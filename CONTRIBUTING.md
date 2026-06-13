# Contributing

Thank you for your interest in FinSec-LLM-PostTraining. This project is an early-stage research and engineering repository for Korean financial-security and regulatory QA.

## Ways To Contribute

- Improve data conversion scripts for QA, law summaries, and security terminology.
- Add retrieval smoke tests with small public examples.
- Improve documentation for local model setup, indexing, training, and evaluation.
- Report reproducibility issues with environment details and the exact command used.
- Suggest evaluation cases for MCQ accuracy, short-answer similarity, keyword recall, retrieval hit rate, and answer faithfulness.

## Development Setup

Use Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For lightweight validation that does not require GPU model weights:

```bash
python -m unittest discover -s tests
```

GPU-heavy training and inference scripts should be validated separately with the smallest local dataset that reproduces the change.

## Pull Request Checklist

- Keep changes scoped to one behavior, script, or documentation area.
- Include the command used to validate the change.
- Do not commit model weights, private datasets, API keys, local paths, or generated outputs.
- Add or update a smoke test when changing data conversion, retrieval metadata, or evaluation behavior.
- Note any expected GPU, CUDA, or model-weight requirement in the PR description.

## Data And Security Notes

Only include data that is public and has a clear license or usage basis. If a sample may contain personal information, confidential regulatory material, private credentials, or institution-specific records, do not commit it.
