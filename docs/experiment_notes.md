# Experiment Notes

## Base Models

The experimental scripts include variants for:

- `LGAI-EXAONE/EXAONE-3.5-7.8B-Instruct`
- `taetae030/fin-term-model`

The cleaned repository keeps these as transparent experiment references. They can be changed in the training scripts or moved into config-driven training if needed.

## QLoRA Setup

Common configuration:

- 4-bit quantization with NF4,
- bfloat16 compute,
- LoRA rank 16,
- LoRA alpha 32,
- dropout 0.05,
- target modules around attention and MLP projections.

The most important implementation detail is assistant-only label masking. Without it, a model can waste loss on reproducing prompts rather than learning answer behavior.

## Evaluation Direction

The original task setting contained both multiple-choice and short-answer examples. The cleaned project frames evaluation around:

- exact match for multiple-choice outputs,
- semantic similarity and keyword recall for short-answer outputs,
- qualitative checks for evidence-groundedness and over-answering.

## Portfolio Interpretation

The appropriate way to describe this project is:

> QLoRA-based supervised fine-tuning and RAG pipeline for Korean financial-security QA.

Avoid saying:

> Fine-tuned the retrieval module.

Retrieval is the evidence layer. The fine-tuned component is the language model adapter used in the QA pipeline.
