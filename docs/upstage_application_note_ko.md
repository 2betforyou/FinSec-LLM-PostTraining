# Upstage 지원서용 정리

## 한 줄 요약

금융보안/규제 QA를 위해 RAG 기반 근거 검색과 QLoRA 기반 SFT 도메인 적응을 결합한 LLM 파이프라인을 구축했습니다.

## 지원서 문구

FSI AI Challenge 프로젝트를 기반으로 한국어 금융보안 규제 QA를 위한 RAG + QLoRA SFT 파이프라인을 구축했습니다. QA 데이터를 SFT용 chat-message JSONL로 변환하고, EXAONE 계열 모델 및 금융 도메인 모델에 대해 4-bit QLoRA fine-tuning을 실험했습니다. 특히 assistant 응답 구간만 loss에 반영하도록 label masking을 구성하고, LoRA target module 설정, train/eval split, eval-loss 기반 checkpointing, PEFT adapter 저장까지 포함한 post-training의 기본 구성 요소를 직접 다뤘습니다.

이 경험은 RLHF/DPO 경험은 아니지만, LLM post-training에서 가장 기본적인 축인 supervised fine-tuning, domain adaptation, data formatting, evaluation-aware training pipeline과 연결됩니다. 또한 RAG와 graph-based retrieval 구조를 함께 다루며, 모델 출력만 보는 것이 아니라 검색 근거, 데이터 형식, 학습 loss, 평가 방식이 최종 답변 품질에 어떻게 연결되는지 실험했습니다.

## 면접에서 말하면 좋은 포인트

- retrieval 모듈을 fine-tuning한 것이 아니라, 금융보안 QA 파이프라인 안에서 사용하는 LLM adapter를 QLoRA로 SFT했습니다.
- 핵심은 "모델 하나를 돌렸다"가 아니라 데이터 변환, retrieval, label masking, LoRA 설정, eval loss 관리까지 end-to-end로 만진 경험입니다.
- Upstage의 LLM post-training internship과 연결할 때는 SFT/PEFT, data collection/cleaning, evaluation sensitivity, hypothesis-driven iteration을 강조하는 것이 좋습니다.

## 짧은 버전

한국어 금융보안 QA 데이터를 SFT용 chat-message JSONL로 변환하고, EXAONE 계열 모델에 대해 4-bit QLoRA 기반 supervised fine-tuning을 실험했습니다. assistant-only loss masking, LoRA target module 설정, eval-loss 기반 checkpointing, adapter 저장까지 포함한 post-training 파이프라인을 다뤘으며, RAG와 graph-based retrieval 기반 근거 검색과 결합해 금융보안/규제 QA 성능을 개선하는 방향으로 실험했습니다.
