# Security Policy

FinSec-LLM-PostTraining handles financial-security and regulatory QA workflows, so the repository is maintained with extra care around data provenance, secrets, and generated artifacts.

## Supported Versions

This is an early-stage research repository. Security fixes are applied to the `main` branch.

## Reporting A Vulnerability

Please open a GitHub issue if the report can be public and does not expose sensitive details. For reports involving secrets, private data, or an exploitable vulnerability, contact the maintainer privately before posting details publicly.

When reporting, include:

- the affected file or script,
- the command or workflow that exposes the issue,
- the expected impact,
- a minimal reproduction when safe to share.

## Sensitive Data

Do not commit:

- API keys, tokens, cookies, or credentials,
- private financial records or personal information,
- non-public regulatory or institution-specific documents,
- model weights, adapters, logs, or generated datasets that may contain private data.

Use small public fixtures under `examples/` for tests and documentation.
