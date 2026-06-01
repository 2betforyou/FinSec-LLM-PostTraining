# FinSec-LLM-PostTraining

RAG and QLoRA-based supervised post-training for Korean financial-security and regulatory QA.

This repository is a cleaned research/portfolio version of an FSI AI Challenge Track 1 prototype. It focuses on a practical question:

> How can we make an open-source Korean LLM answer financial-security and regulatory questions more accurately, more concisely, and with better evidence awareness?

## 1. Goal: What Problem Are We Tackling?

Financial-security QA is a difficult domain for general-purpose LLMs. The model must understand Korean legal/regulatory language, map questions to the right laws or guidelines, preserve answer format constraints, and avoid unsupported claims when evidence is weak.

In this project, we tackle **Korean financial-security and regulatory QA** as a combined retrieval and post-training problem.

The target setting includes:

- multiple-choice and short-answer financial-security questions,
- Korean laws, enforcement decrees, guidelines, and security references,
- domain-specific terminology that general LLMs may confuse,
- local model execution without relying on proprietary remote APIs,
- reproducible training and inference under limited GPU resources.

The practical goal is to build a pipeline where domain documents are not only retrieved at inference time, but also converted into supervised learning signals for lightweight LLM adaptation.

## 2. Existing Works: How Do Recent Prior Works Tackle This?

Recent work usually approaches this problem from one of four directions.

**Retrieval-Augmented Generation.**  
RAG combines a parametric language model with external retrieval so the model can use non-parametric memory at generation time. The original RAG formulation showed the value of retrieval for knowledge-intensive NLP tasks, and modern production systems commonly use dense retrieval, BM25, hybrid retrieval, and reranking to ground answers in external documents. See [Lewis et al., 2020](https://arxiv.org/abs/2005.11401).

**Graph-based retrieval.**  
Recent retrieval systems increasingly organize documents as graph structures instead of only flat chunks. This can help when the answer depends on relationships across entities, sections, clauses, or communities of documents. LightRAG is one representative example of this direction. See [LightRAG, 2024](https://arxiv.org/abs/2410.05779).

**Parameter-efficient fine-tuning.**  
QLoRA makes it possible to fine-tune large language models with 4-bit quantization and LoRA adapters, reducing memory requirements while preserving useful adaptation behavior. This is a natural fit when full fine-tuning is too expensive but domain adaptation is still needed. See [Dettmers et al., 2023](https://arxiv.org/abs/2305.14314).

**Domain financial LLMs and RAG evaluation.**  
Financial LLM projects such as FinGPT emphasize data-centric finance adaptation, while RAG evaluation frameworks such as RAGAS and ARES separate retrieval quality, answer relevance, and faithfulness. See [FinGPT, 2023](https://arxiv.org/abs/2306.06031), [RAGAS, 2023](https://arxiv.org/abs/2309.15217), and [ARES, 2023](https://arxiv.org/abs/2311.09476).

These works are strong, but they often solve only part of the financial-security QA pipeline.

## 3. Main Challenge: What Do Recent Works Still Fail To Solve?

The main challenge is the gap between **retrieving the right evidence** and **training the model to use that evidence in the right answer format**.

In Korean financial-security QA, a system can fail in several ways:

- retrieve a relevant law but miss the exact clause needed for the answer,
- retrieve the right clause but generate an over-general answer,
- answer multiple-choice questions in a format that breaks evaluation,
- produce fluent but unsupported regulatory explanations,
- memorize domain phrases during fine-tuning but fail to ground answers in evidence,
- improve average scores while hiding different failure modes across MCQ and short-answer tasks.

Pure RAG improves access to documents, but it does not necessarily teach the model the expected answer style, concision, refusal behavior, or task format. Pure fine-tuning can adapt the model to a domain, but it may still hallucinate or become stale without retrieval. Graph-based retrieval can improve context organization, but it still needs an evaluation-aware answer generation layer.

So the challenge is:

> How do we connect retrieval, domain data construction, supervised post-training, and evaluation so that financial-security QA improves as a whole system rather than as disconnected scripts?

## 4. Our Method: How Do We Solve The Main Challenge?

We build a **RAG + QLoRA supervised fine-tuning pipeline** for Korean financial-security QA.

The method has five parts.

**1. Domain document processing.**  
Financial-security laws, guidelines, and security references are cleaned, merged, and chunked into retrieval-friendly units. When useful, documents are parsed into graph-style structures so sections and cross-document relationships can be queried more explicitly.

**2. Hybrid retrieval.**  
The retrieval layer uses multilingual E5 embeddings with FAISS, optional BM25, and graph-style retrieval experiments. This gives the model both semantic retrieval and lexical/legal-term matching.

**3. SFT data construction.**  
Challenge-style QA data and domain references are converted into chat-message JSONL for supervised fine-tuning:

```json
{"messages":[{"role":"system","content":"..."},{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}
```

This makes the training data compatible with instruction-tuned causal LMs.

The fine-tuning data is not raw document text alone. It is a set of supervised examples derived from three sources:

- **law and regulation QA/summary data** built from Korean financial-security laws and related statutes, including examples such as electronic financial transactions, credit information, privacy, electronic signatures, real-name financial transactions, telecommunications network, and electronic commerce laws,
- **security terminology data** built from Korean security glossary/standard material, where term-definition pairs are converted into concise instruction-output examples,
- **security framework reference data** built from MITRE-style security descriptions translated/cleaned into Korean, used for security concept explanation and retrieval-aware QA.

Raw laws and security documents are mainly used for retrieval indexing. The supervised fine-tuning scripts train on converted JSONL datasets such as `train.jsonl`, `val.jsonl`, `train_plus_TTA.jsonl`, `val_plus_TTA.jsonl`, and `tta_mitre_sft_plus_ko*.jsonl`.

**4. Assistant-only QLoRA SFT.**  
The training scripts apply 4-bit QLoRA and mask prompt tokens with `-100`, so the model learns from assistant answer spans rather than simply learning to reproduce user prompts. The pipeline includes LoRA target module configuration, train/eval splits, constant-length packing, eval-loss checkpointing, early stopping, and PEFT adapter saving.

**5. Evaluation-aware iteration.**  
The system is designed to compare baseline LLM, RAG-only, QLoRA-only, and RAG+QLoRA variants. The goal is not only to report one score, but to identify which failure modes are reduced by retrieval, which are reduced by supervised adaptation, and which still require better data or reward/evaluation signals.

## Why This Method Targets The Challenge

The key idea is that financial-security QA requires both **external evidence** and **learned answer behavior**.

RAG supplies the evidence. QLoRA SFT adapts the model to the domain-specific output style and task format. Assistant-only label masking makes the learning signal focus on answer behavior. Graph-style retrieval helps when a question depends on relationships across legal sections or security concepts. Evaluation-aware ablations prevent the system from hiding retrieval failures behind generation quality or hiding generation failures behind good retrieval.

In short:

```text
retrieval finds the evidence
SFT teaches answer behavior
evaluation separates failure modes
```

## 5. Expected Experimental Results: How Do We Show It Works?

The expected experiments compare the following systems:

| System | Retrieval | Fine-tuning | Expected Role |
| --- | --- | --- | --- |
| Base LLM | No | No | Measures the raw model's domain knowledge |
| RAG-only | Yes | No | Tests whether evidence retrieval improves factual grounding |
| QLoRA-only | No | Yes | Tests whether SFT improves format and domain response style |
| RAG + QLoRA | Yes | Yes | Tests whether evidence and learned answer behavior are complementary |
| Relational RAG + QLoRA | Graph-style | Yes | Tests whether relational document structure helps harder regulatory questions |

Evaluation should include:

- **MCQ accuracy** for multiple-choice questions,
- **short-answer similarity** and **keyword recall** for descriptive answers,
- **retrieval hit rate** for whether the needed clause/reference is retrieved,
- **answer faithfulness** for whether the generated answer is supported by retrieved context,
- **format validity** for whether the model follows required answer schemas,
- **failure taxonomy** such as `retrieval_miss`, `wrong_clause`, `unsupported_answer`, `over_answering`, `format_error`, and `domain_term_confusion`.

The expected pattern is:

- RAG-only should reduce unsupported answers but may still be verbose or format-unstable.
- QLoRA-only should improve answer style and task format but may still miss evidence.
- RAG + QLoRA should improve both grounding and answer behavior.
- Graph-style retrieval should help most when the question depends on relationships across clauses, definitions, or security frameworks.

## Repository Map

```text
src/
  data/          data conversion, augmentation, and law merging scripts
  training/      QLoRA SFT and adapter training scripts
  retrieval/     FAISS/BM25 retrieval and RAG generation scripts
  graph_retrieval/ graph-based retrieval experiments
  inference/     challenge-style inference prototype
  evaluation/    answer evaluation helpers
configs/         example training and retrieval configs
docs/            project notes, data card, and portfolio summary
examples/        small synthetic examples only
```

Representative files:

- [`src/data/make_sft_from_csv.py`](src/data/make_sft_from_csv.py): convert QA CSV rows into chat-message JSONL
- [`src/training/train_qlora_exaone.py`](src/training/train_qlora_exaone.py): QLoRA SFT for EXAONE-style instruction models
- [`src/training/train_qlora_fin_term.py`](src/training/train_qlora_fin_term.py): QLoRA SFT with label-preserving packing and early stopping
- [`src/retrieval/build_index.py`](src/retrieval/build_index.py): build FAISS/BM25 retrieval index
- [`src/retrieval/ask_rag.py`](src/retrieval/ask_rag.py): retrieve evidence and generate answers
- [`src/graph_retrieval/`](src/graph_retrieval): graph-based document retrieval experiments

## Quick Start

Install dependencies:

```bash
pip install -r requirements.txt
```

Convert a QA CSV file into SFT chat-message JSONL:

```bash
python src/data/make_sft_from_csv.py examples/qa_sample.csv data/sft/train.jsonl
```

Build a retrieval index:

```bash
PYTHONPATH=src python src/retrieval/build_index.py \
  --sources "data/docs/*.txt" \
  --index-dir "data/index/finsec_e5" \
  --embedding-model "intfloat/multilingual-e5-base" \
  --chunk-chars 900 \
  --chunk-overlap 200 \
  --bm25
```

Run QLoRA supervised fine-tuning:

```bash
PYTHONPATH=src python src/training/train_qlora_exaone.py
```

The scripts assume local model execution and local datasets. Model weights, trained adapters, full challenge data, and generated submissions are intentionally not included.

## FinSec-LLM-PostTraining

이 레포는 한국어 금융보안 및 규제 질의응답을 위해 RAG와 QLoRA 기반 supervised post-training을 결합한 프로젝트입니다. FSI AI Challenge Track 1에서 진행한 실험형 프로토타입을 포트폴리오용으로 정리했으며, 핵심 질문은 다음과 같습니다.

> 오픈소스 한국어 LLM이 금융보안/규제 질문에 더 정확하고, 더 간결하며, 더 근거 있게 답하도록 만들려면 어떤 retrieval 및 post-training 파이프라인이 필요한가?

### 1. 목표: 어떤 문제를 풀고자 하는가?

금융보안 QA는 일반 LLM에게 까다로운 문제입니다. 모델은 한국어 법령과 규제 문장을 이해해야 하고, 질문과 관련된 법령/지침을 찾아야 하며, 객관식과 주관식처럼 서로 다른 답변 형식도 지켜야 합니다. 또한 근거가 부족할 때 그럴듯한 답변을 만들어내는 것이 아니라, 불확실성을 드러내거나 unsupported claim을 피해야 합니다.

이 프로젝트는 한국어 금융보안/규제 QA를 단순 생성 문제가 아니라 **retrieval과 post-training이 함께 필요한 문제**로 봅니다. 목표는 도메인 문서를 inference-time context로만 사용하는 데서 그치지 않고, supervised fine-tuning에 사용할 수 있는 학습 신호로도 변환하는 것입니다.

### 2. 기존 연구: 최근 연구들은 이 문제를 어떻게 다루는가?

최근 연구들은 대체로 네 가지 방향에서 이 문제를 다룹니다.

**Retrieval-Augmented Generation.**  
RAG는 LLM이 생성 과정에서 외부 문서를 검색해 사용할 수 있도록 합니다. 원래의 RAG 연구는 knowledge-intensive NLP task에서 retrieval의 효과를 보였고, 이후 실제 시스템에서는 dense retrieval, BM25, hybrid retrieval, reranking 등을 조합해 답변을 외부 문서에 grounding하는 방식이 널리 쓰이고 있습니다. See [Lewis et al., 2020](https://arxiv.org/abs/2005.11401).

**Graph-based retrieval.**  
최근 retrieval 시스템은 문서를 단순 chunk 목록이 아니라 entity, section, clause, relation 등의 graph 구조로 다루는 방향으로도 발전하고 있습니다. 이는 답변이 여러 조항, 개념, 문서 간 관계에 의존할 때 도움이 될 수 있습니다. LightRAG가 이 방향의 대표적인 예입니다. See [LightRAG, 2024](https://arxiv.org/abs/2410.05779).

**Parameter-efficient fine-tuning.**  
QLoRA는 4-bit quantization과 LoRA adapter를 사용해 제한된 GPU 자원에서도 큰 언어모델을 효율적으로 fine-tuning할 수 있게 합니다. 전체 모델을 업데이트하기 어렵지만 특정 도메인에 맞춘 adaptation이 필요한 상황에 적합합니다. See [Dettmers et al., 2023](https://arxiv.org/abs/2305.14314).

**Domain financial LLMs and RAG evaluation.**  
FinGPT 같은 금융 도메인 LLM 연구는 data-centric한 금융 특화 adaptation을 강조하고, RAGAS나 ARES 같은 RAG 평가 프레임워크는 retrieval quality, answer relevance, faithfulness를 분리해 평가하려고 합니다. See [FinGPT, 2023](https://arxiv.org/abs/2306.06031), [RAGAS, 2023](https://arxiv.org/abs/2309.15217), and [ARES, 2023](https://arxiv.org/abs/2311.09476).

이 연구들은 각각 중요한 축을 다루지만, 금융보안 QA 전체 파이프라인을 하나로 연결하는 데에는 여전히 빈틈이 있습니다.

### 3. 핵심 도전: 최근 연구들이 아직 충분히 해결하지 못한 지점은 무엇인가?

핵심 도전은 **올바른 근거를 검색하는 것**과 **모델이 그 근거를 올바른 답변 형식으로 사용하도록 학습시키는 것** 사이의 간극입니다.

한국어 금융보안 QA에서는 다음과 같은 실패가 발생할 수 있습니다.

- 관련 법령은 검색했지만 실제 정답에 필요한 조항을 놓치는 경우
- 맞는 조항을 검색했지만 답변이 너무 일반적이거나 장황해지는 경우
- 객관식 문제에서 평가 형식에 맞지 않는 답변을 생성하는 경우
- 근거가 부족한데도 그럴듯한 규제 설명을 만들어내는 경우
- fine-tuning으로 도메인 표현은 익혔지만 retrieval context에 충실하지 못한 경우
- 평균 점수는 올라갔지만 MCQ와 주관식에서 서로 다른 failure mode가 가려지는 경우

순수 RAG는 문서 접근성을 높이지만, 모델이 기대하는 답변 스타일, 간결성, 거절/불확실성 표현, 형식 준수를 자동으로 학습시키지는 않습니다. 반대로 순수 fine-tuning은 도메인 적응에는 도움이 되지만, retrieval 없이 최신성이나 근거성을 확보하기 어렵습니다. Graph-based retrieval 역시 문서 구조를 더 잘 제공할 수는 있지만, 최종 답변 생성과 평가 구조가 함께 설계되지 않으면 효과가 제한됩니다.

따라서 이 프로젝트의 핵심 질문은 다음과 같습니다.

> retrieval, domain data construction, supervised post-training, evaluation을 어떻게 연결해야 금융보안 QA가 개별 스크립트가 아니라 하나의 시스템으로 개선될 수 있는가?

### 4. 제안 방법: 위 도전을 어떻게 해결하는가?

이 프로젝트는 한국어 금융보안 QA를 위해 **RAG + QLoRA supervised fine-tuning pipeline**을 구성합니다.

방법은 다섯 단계로 이루어집니다.

**1. 도메인 문서 처리.**  
금융보안 관련 법령, 지침, 보안 참고자료를 정제하고 병합한 뒤 retrieval에 적합한 단위로 chunking합니다. 필요한 경우 문서를 graph-style 구조로 파싱해 조항 간 관계나 문서 간 연결을 더 명시적으로 탐색할 수 있게 합니다.

**2. Hybrid retrieval.**  
검색 단계에서는 multilingual E5 embedding과 FAISS를 사용하고, 선택적으로 BM25와 graph-style retrieval을 결합합니다. 이를 통해 의미 기반 검색과 법령/보안 용어 중심의 lexical matching을 함께 활용합니다.

**3. SFT 데이터 구성.**  
대회형 QA 데이터와 도메인 reference를 supervised fine-tuning에 사용할 수 있는 chat-message JSONL 형식으로 변환합니다.

```json
{"messages":[{"role":"system","content":"..."},{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}
```

이 형식은 instruction-tuned causal LM에 바로 사용할 수 있습니다.

fine-tuning에 사용한 자료는 법령 원문 전체를 그대로 넣은 것이 아니라, 원문과 참고자료를 바탕으로 만든 supervised example입니다. 크게 세 종류입니다.

- **법령/규제 QA 및 요약 데이터**: 전자금융거래법, 신용정보법, 개인정보보호법, 전자서명법, 금융실명법, 정보통신망법, 전자거래기본법 등 금융보안 관련 법령과 조항을 바탕으로 만든 질의응답/요약 데이터
- **보안 용어 데이터**: 한국어 보안 용어집/표준 자료에서 용어-정의 쌍을 뽑아 간결한 instruction-output 형식으로 만든 데이터
- **보안 프레임워크 참고 데이터**: MITRE 계열 보안 설명 자료를 한국어로 정제해 보안 개념 설명과 retrieval-aware QA에 활용할 수 있게 만든 데이터

즉, raw 법령과 보안 문서는 주로 retrieval index 구축에 쓰이고, QLoRA SFT는 `train.jsonl`, `val.jsonl`, `train_plus_TTA.jsonl`, `val_plus_TTA.jsonl`, `tta_mitre_sft_plus_ko*.jsonl`처럼 변환된 JSONL supervised dataset을 대상으로 수행합니다.

**4. Assistant-only QLoRA SFT.**  
학습 단계에서는 4-bit QLoRA를 적용하고, prompt token에는 `-100` label mask를 부여해 assistant 답변 구간만 loss에 반영합니다. 이를 통해 모델이 사용자 prompt를 복사하는 것이 아니라 실제 답변 행동을 학습하도록 합니다. 또한 LoRA target module 설정, train/eval split, constant-length packing, eval-loss checkpointing, early stopping, PEFT adapter 저장을 포함합니다.

**5. Evaluation-aware iteration.**  
실험은 baseline LLM, RAG-only, QLoRA-only, RAG+QLoRA, Relational RAG+QLoRA를 비교하도록 설계합니다. 목표는 하나의 최종 점수만 보고 끝내는 것이 아니라, retrieval로 줄어드는 실패와 supervised adaptation으로 줄어드는 실패를 분리해 보는 것입니다.

핵심 아이디어는 간단합니다.

```text
retrieval finds the evidence
SFT teaches answer behavior
evaluation separates failure modes
```

### 5. 예상 실험 결과: 방법이 실제로 문제를 해결하는지 어떻게 보일 것인가?

예상 실험은 다음 시스템들을 비교합니다.

| System | Retrieval | Fine-tuning | Expected Role |
| --- | --- | --- | --- |
| Base LLM | No | No | 기본 모델의 금융보안 도메인 지식 측정 |
| RAG-only | Yes | No | 근거 검색이 factual grounding을 개선하는지 확인 |
| QLoRA-only | No | Yes | SFT가 답변 형식과 도메인 응답 스타일을 개선하는지 확인 |
| RAG + QLoRA | Yes | Yes | 근거 검색과 학습된 답변 행동이 상호 보완적인지 확인 |
| Relational RAG + QLoRA | Graph-style | Yes | 조항/개념 간 관계가 중요한 문제에서 graph 구조가 도움이 되는지 확인 |

평가는 다음 항목을 포함할 수 있습니다.

- 객관식 문제의 MCQ accuracy
- 주관식 답변의 semantic similarity와 keyword recall
- 필요한 조항이나 reference가 검색되었는지 보는 retrieval hit rate
- 생성 답변이 검색된 context에 의해 뒷받침되는지 보는 answer faithfulness
- 요구된 답변 형식을 지키는지 보는 format validity
- `retrieval_miss`, `wrong_clause`, `unsupported_answer`, `over_answering`, `format_error`, `domain_term_confusion` 같은 failure taxonomy

예상되는 결과는 다음과 같습니다.

- RAG-only는 unsupported answer를 줄일 수 있지만, 답변이 장황하거나 형식이 불안정할 수 있습니다.
- QLoRA-only는 답변 스타일과 task format을 개선할 수 있지만, 근거 문서 접근이 부족할 수 있습니다.
- RAG + QLoRA는 grounding과 answer behavior를 함께 개선할 가능성이 큽니다.
- Graph-style retrieval은 여러 조항, 정의, 보안 framework 간 관계가 필요한 문제에서 특히 도움이 될 수 있습니다.

이 레포의 fine-tuning 대상은 retrieval 모듈이 아니라, 금융보안 QA에 맞게 적응한 LLM adapter입니다. 프로젝트의 핵심은 retrieval, SFT data construction, assistant-only QLoRA training, evaluation-aware ablation을 하나의 금융보안 QA 파이프라인으로 연결하는 것입니다.

## Notes

- This is a cleaned research/portfolio repository, not the full raw competition workspace.
- Full datasets, model weights, trained adapters, and generated submissions are excluded.
- Some scripts preserve experimental paths from the original workspace and may need path updates for a new environment.
