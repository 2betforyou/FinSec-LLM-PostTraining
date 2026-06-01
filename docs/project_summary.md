# Project Summary

## One-Line Description

RAG and QLoRA-based supervised fine-tuning pipeline for Korean financial-security and regulatory QA.

## Problem

General-purpose LLMs often fail on financial-security QA because the domain requires precise terminology, regulatory evidence, and strict answer formats. A model may produce fluent text while still missing the relevant law, confusing similar concepts, or over-answering beyond available evidence.

## Research/Engineering Question

How can Korean financial-security documents and QA examples be converted into useful post-training and retrieval signals?

This project approaches the question through:

- evidence retrieval over law, guideline, and security documents,
- supervised fine-tuning examples in chat-message format,
- assistant-only loss masking for answer-focused learning,
- lightweight LoRA adapters for domain adaptation,
- evaluation utilities for multiple-choice and short-answer tasks.

## Technical Scope

The project includes:

- document preprocessing and law merging,
- CSV/JSONL conversion into SFT examples,
- FAISS/BM25 retrieval index construction,
- RAG-based answer generation,
- QLoRA SFT over Korean financial-security QA data,
- adapter saving through PEFT.

The project does not claim RLHF, DPO, or production-grade deployment. Its post-training scope is supervised fine-tuning and PEFT-based domain adaptation.

## Main Takeaway

The strongest portfolio signal is not "I fine-tuned a model" in isolation. The stronger signal is that the project connects data construction, retrieval, supervised post-training, and evaluation into one domain QA pipeline.
