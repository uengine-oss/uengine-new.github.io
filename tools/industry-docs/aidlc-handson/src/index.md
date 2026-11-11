# 시작하기

> Claude Code에 AWS Labs의 AI-DLC v2를 연결해, 음성으로 주차권을 찾고 예약하는 VoiceParking 프로토타입(Vue 3 + Spring Boot 마이크로서비스 3개)을 요구사항 인터뷰부터 동작하는 앱까지 만듭니다. 모든 화면은 실제로 실행한 결과입니다.

!!! tip "실습 산출물 저장소 · GitHub"
    이 튜토리얼을 실제로 실행해 남은 파일 전부를 공개 저장소 [uengine-oss/tutorial-aidlc-handson](https://github.com/uengine-oss/tutorial-aidlc-handson)에 올려 두었습니다. 레벨 1은 [`level1-poc/`](https://github.com/uengine-oss/tutorial-aidlc-handson/tree/main/level1-poc), 레벨 2는 [`level2-classic/`](https://github.com/uengine-oss/tutorial-aidlc-handson/tree/main/level2-classic) 폴더입니다. 각 장 첫머리의 「이 장의 산출물」 상자와 본문의 파일 이름을 누르면 해당 파일이 바로 열립니다.

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
| "Contradiction Detected" 경고 | 그런 경고 문구는 없습니다. 대신 요구사항 분석 단계에서 서로 충돌하는 답을 찾아 **후속 질문**으로 되묻습니다(6장) |
| 모든 유닛에 TDD | poc 스코프의 기본 시험 방식은 구현 뒤 시험(test-after)입니다. 팀 규칙(`team.md`)에서 TDD로 바꿀 수 있습니다 |
| 피드백이 `aidlc/state/project.md`로 승격 | 수정 요청 뒤 "다음에도 기억할까요?"라는 학습 의식이 있고, 동의하면 `aidlc/spaces/default/memory/project.md`에 쌓입니다(7장) |
| 131개 정형 감사 이벤트 | 맞습니다. 이벤트 종류가 131가지이고, 이번 실행의 기록은 8장에서 확인합니다 |
| Express/TypeScript, Jest | 이 실습은 국내에서 많이 쓰는 **Vue 3 + Java Spring Boot**로 바꿨습니다. 모듈이 여럿이면 마이크로서비스로 나누라고 요청했습니다 |

## 준비물

- Claude Code (확인 버전 2.1.318). 로그인되어 있어야 합니다.
- Java 17, Maven 3.9, Node 20 이상.
- 외부 API 키나 DB는 필요 없습니다. 결제는 모의 결제로 처리하고, 주차장 정보는 샘플 데이터를 사용합니다.

## 순서와 실제 걸린 시간

이론 네 장으로 개념을 먼저 잡고, 이어서 실습으로 직접 만들어 봅니다. 마지막 부에서는 팀이 같은 과정을 함께 진행할 수 있도록 돕는 프로젝트 관리 도구를 살펴봅니다.

| 장 | 하는 일 | 이번 실행에서 걸린 시간 |
|---|---|---|
| **이론** | 실습 전에 개념과 용어를 잡습니다 | |
| 1. AI-DLC는 무엇이 다른가 | 실행과 통제의 전환, 볼트와 유닛, 몹 정교화, 결정론적 게이트 | 읽기 |
| 2. 사양 주도 개발과 검증 게이트 | 어셈블리 → C 논쟁과 지금의 AI 코딩, 조향 규칙의 층, 사양 게이트 세 가지, 프롬프트 회귀 시험 | 읽기 |
| 3. 형상관리와 볼트 진척 관리 | Git의 한계, 워크트리와 Jujutsu, DVC·lakeFS, 볼트 계획과 실행 그래프 | 읽기 |
| 4. 검증 피로를 막는 정책과 도입 순서 | 지정 승인자·검토 표준·의사결정 로그, 4계층 구조, 도입 4단계 | 읽기 |
| **실습 레벨 1 · poc** | 가장 짧은 경로로 동작하는 프로토타입까지 | |
| 5. 설치와 프로젝트 준비 | 설치, `aidlc config`, `aidlc doctor` | 약 2분 |
| 6. 의도 정리와 요구사항 | `/aidlc poc` 요청, 질문 두 묶음, 승인 게이트 두 번 | 약 13분 |
| 7. 코드 생성과 학습 | 서비스 3개와 화면 생성, 시험, 검토, 수정 요청과 학습 | 약 48분(검토와 수정 요청 포함) |
| 8. 동작 확인과 감사 기록 | 실행, 브라우저 시연, 402 응답, 감사 기록 | 약 10분 |
| **실습 레벨 2 · classic** | 같은 요청을 단계마다 문서로 (개념 → 터미널 → 산출물) | |
| 9. 개요와 1단계 팀 규칙 | 전체 흐름, 다섯 걸음, 답하는 사람, 팀 규칙(TDD) | 약 7분 |
| 10. 2단계 요구사항 | 질문 4 + 후속 3, FR·NFR, 검토 | 약 6분 |
| 11. 3·4단계 유저 스토리와 화면 | Given/When/Then 인수 조건, 화면 상태 8가지 | 약 9분 |
| 12. 5단계 도메인 설계 | 컴포넌트, ADR, 순환 의존 수정 요청 | 약 14분 |
| 13. 6·7단계 유닛과 API 계약 | 유닛 5개와 DAG, 계약 6개, NOT-READY → READY | 약 15분 |
| 14. 8단계 볼트 계획 | 볼트 5개와 완료 기준 | 약 4분 |
| 15. 구현: 유닛 u1 | 기능 설계 → NFR → TDD 코드 → 검증 명령 | 약 52분 |
| 16. 구현: 예약·결제 서비스(u2·u3) | 상태 머신과 180초 취소, 서명 웹훅과 중복 처리, 20ms 시험을 두고 사람이 내린 결정 | 약 3시간 20분(부하로 다시 돌린 시간 포함) |
| 17. 구현: 화면·실행 스크립트(u4·u5) | 컴포넌트, 설계 검토 반려와 통과, 검증 명령 변경, 비밀 값 처리 | 약 3시간(부하로 다시 돌린 시간 포함) |
| 18. 빌드·테스트와 앱 동작 | 연동 스모크, 브라우저 확인, 목표별 판정, 승인 | 약 7시간 50분(대부분 호스트 부하 대기) |
| **프로젝트 관리와 툴 지원** | 레벨 2를 팀으로 진행할 때 쓰는 도구 (Process GPT Lite) | |
| 19. 팀 세션 | 역할, 담당자에게 전달되는 카드, 결정 화면, 몹 회의, 코딩 중 개입 | 읽기 · 영상 |
| 20. 검토 보드 | 질문과 지적에 대한 팀의 공동 선택(플래닝 포커 방식), 의견이 갈린 카드만 논의 | 읽기 · 영상 |
| 21. 볼트 보드와 진척 | 의도 → 유닛 → 볼트, 되돌아온 볼트, AI 작업 시간과 사람 대기 시간 | 읽기 · 영상 |
| 산출물 찾아보기 | 레벨 2 산출물을 한곳에서 | 참고 |

모델은 Claude Sonnet 5.5(노력 수준 medium)를 사용했습니다. AI-DLC가 권하는 모델은 Opus입니다. 모델이 작성하는 문장은 실행할 때마다 조금씩 달라지므로, 질문 수와 문구가 이 튜토리얼과 다를 수 있습니다.
