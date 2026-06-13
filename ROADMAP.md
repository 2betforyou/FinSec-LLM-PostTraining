# Roadmap

This roadmap tracks the next public-maintenance steps for FinSec-LLM-PostTraining.

## v0.1: Public Baseline

- Add an explicit open-source license.
- Keep small public examples under `examples/`.
- Add lightweight smoke tests for data conversion.
- Document reproducible quick-start commands.
- Publish an initial GitHub release once the baseline docs and tests are in place.

## v0.2: Retrieval Reproducibility

- Add a tiny public document fixture for retrieval indexing tests.
- Add a CPU-only retrieval metadata smoke test.
- Document FAISS/BM25 index artifacts and expected output files.
- Clarify data-source assumptions in `docs/data_card.md`.

## v0.3: Evaluation Harness

- Add sample MCQ and short-answer evaluation fixtures.
- Report format-validity checks separately from answer-quality metrics.
- Add a minimal baseline-vs-RAG comparison script for public examples.

## v0.4: Contributor Workflow

- Add issue templates for bugs, reproducibility reports, and feature requests.
- Add pull request templates with validation-command fields.
- Expand security guidance for secrets, private datasets, and generated artifacts.
