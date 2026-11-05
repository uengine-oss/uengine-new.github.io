# 시작하기

> Claude Code에 AWS Labs의 AI-DLC v2를 연결해, 음성으로 주차권을 찾고 예약하는 VoiceParking 프로토타입(Vue 3 + Spring Boot 마이크로서비스 3개)을 요구사항 인터뷰부터 동작하는 앱까지 만듭니다. 모든 화면은 실제로 실행한 결과입니다.

## 무엇을 만드나

사용자가 "강남역 근처 2시간 주차권 찾아줘"라고 말하면 가까운 주차권 세 개의 점수를 비교해 최적의 주차권 하나를 추천합니다. 모의 결제가 승인되면 예약을 확정합니다. 이 실습에서는 음성 대신 텍스트로 입력합니다. 실습을 마치면 다음 산출물이 남습니다.

| 산출물 | 어디에 | 누가 만드나 |
|---|---|---|
| 의도 문서, 이해관계자 표 | `aidlc/spaces/default/intents/<날짜>-voice-parking/ideation/` | AI-DLC가 질문하고 사람이 답한 뒤 작성 |
| 요구사항(FR·NFR, 합격 기준, 출처 표시) | `…/inception/requirements-analysis/requirements.md` | 〃 |
| 코드 생성 계획, 시험 지침, 추적표 | `…/construction/code-generation/` | 개발 에이전트 |
| 백엔드 서비스 3개(추천·결제·예약) | `backend/` | 개발 에이전트 |
| Vue 3 화면 | `frontend/` | 개발 에이전트 |
| 프로젝트 규칙(사람이 고쳐 준 것) | `aidlc/spaces/default/memory/project.md` | 학습 의식(learnings) |
| 감사 기록 | `…/audit/` | AI-DLC 훅이 자동 기록 |

## 원본 가이드와 실제가 다른 곳

이 튜토리얼은 「Claude Code 기반 AWS AI-DLC 실전 핸즈온 가이드」를 따라 하며 시작했습니다. 실습 중 여러 명령과 파일 이름이 가이드와 다르다는 점을 확인했습니다. 아래 표 오른쪽은 2026년 11월 5일 AI-DLC 2.11.2로 확인한 결과입니다.

| 가이드 | 실제 |
|---|---|
| `npm install -g @aws-labs/aidlc-cli` | 해당 npm 패키지는 없습니다. 공식 설치 명령은 `curl -fsSL https://github.com/awslabs/aidlc-workflows/releases/latest/download/install.sh \| sh`입니다 |
| `aidlc init --harness claude-code --scope workshop` | `aidlc config --harness claude`로 연결하고 `aidlc doctor`로 점검합니다. 스코프는 Claude Code에서 처음 요청할 때 고릅니다(`/aidlc workshop …`, `/aidlc poc …`) |
| workshop 스코프 25개 스테이지 | 실제 workshop은 33개 중 26개(Ideation 1.1~1.7 제외)입니다. 이 실습은 사용량을 줄이기 위해 가장 짧은 poc(초기화 3개 + 4개)를 사용했습니다 |
| `.claude/hooks/prompt-submit.sh` 하나 | 훅이 여러 개입니다. 단계 규칙을 다시 넣는 `deliver-stage-rules`, 사람의 답을 기록하는 `record-human-turn`, 감사 기록을 남기는 `write-audit-log` 등 13가지가 `.claude/settings.json`에 등록됩니다 |
| `aidlc/state/aidlc-state.md`, `CURRENT_STAGE=` | 작업마다 상태 파일이 `aidlc/spaces/default/intents/<날짜>-<이름>/aidlc-state.md`에 생성됩니다 |
| `01-requirements-questions.md` | 스테이지마다 질문 파일이 생성되고(`intent-capture-questions.md`, `requirements-analysis-questions.md`), 답하는 방법을 Guide me / 파일 편집 / Chat 가운데 고릅니다 |
| `/approve` | 스테이지가 끝날 때마다 Approve / Request Changes를 고르는 질문이 나옵니다 |
| "Contradiction Detected" 경고 | 그런 경고 문구는 없습니다. 대신 요구사항 분석 단계에서 서로 충돌하는 답을 찾아 **후속 질문**으로 되묻습니다(2장) |
| 모든 유닛에 TDD | poc 스코프의 기본 시험 방식은 구현 뒤 시험(test-after)입니다. 팀 규칙(`team.md`)에서 TDD로 바꿀 수 있습니다 |
| 피드백이 `aidlc/state/project.md`로 승격 | 수정 요청 뒤 "다음에도 기억할까요?"라는 학습 의식이 있고, 동의하면 `aidlc/spaces/default/memory/project.md`에 쌓입니다(3장) |
| 131개 정형 감사 이벤트 | 맞습니다. 이벤트 종류가 131가지이고, 이번 실행의 기록은 4장에서 확인합니다 |
| Express/TypeScript, Jest | 이 실습은 국내에서 많이 쓰는 **Vue 3 + Java Spring Boot**로 바꿨습니다. 모듈이 여럿이면 마이크로서비스로 나누라고 요청했습니다 |

## 준비물

- Claude Code (확인 버전 2.1.318). 로그인되어 있어야 합니다.
- Java 17, Maven 3.9, Node 20 이상.
- 외부 API 키나 DB는 필요 없습니다. 결제는 모의 결제로 처리하고, 주차장 정보는 샘플 데이터를 사용합니다.

## 실습 순서와 실제 걸린 시간

| 장 | 하는 일 | 이번 실행에서 걸린 시간 |
|---|---|---|
| **레벨 1 · poc** | 가장 짧은 경로로 동작하는 프로토타입까지 | |
| 1. 설치와 프로젝트 준비 | 설치, `aidlc config`, `aidlc doctor` | 약 2분 |
| 2. 의도 정리와 요구사항 | `/aidlc poc` 요청, 질문 두 묶음, 승인 게이트 두 번 | 약 13분 |
| 3. 코드 생성과 학습 | 서비스 3개와 화면 생성, 시험, 검토, 수정 요청과 학습 | 약 48분(검토와 수정 요청 포함) |
| 4. 동작 확인과 감사 기록 | 실행, 브라우저 시연, 402 응답, 감사 기록 | 약 10분 |
| **레벨 2 · classic** | 같은 요청을 스펙 → 설계 → TDD 구현으로 | |
| 5. 개념과 스펙킷 비교 | 스코프, 인텐트·유닛·볼트, 역할, 실패 루프 | 읽기 |
| 6. 스펙에서 볼트 계획까지 | 팀 규칙(TDD) → 요구사항 → 스토리 → 화면 → 도메인 설계 → 유닛 → 계약 → 볼트 | 약 55분(수정 요청 2번 포함) |
| 7. 유닛별 구현과 검증 | u1의 설계 → TDD 코드 → 검증 명령 (사용량 한도로 u1까지) | 약 52분 |
| 8. 산출물 지도 | 산출물 14가지를 하나씩: 내용, 쓰는 쪽·승인, 다음 쓰임, 스펙킷 대응 | 읽기 |

모델은 Claude Sonnet 5.5(노력 수준 medium)를 사용했습니다. AI-DLC가 권하는 모델은 Opus입니다. 모델이 작성하는 문장은 실행할 때마다 조금씩 달라지므로, 질문 수와 문구가 이 튜토리얼과 다를 수 있습니다.
