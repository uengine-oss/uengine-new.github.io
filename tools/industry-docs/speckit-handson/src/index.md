# 시작하기

> GitHub Spec Kit을 Claude Code에 연결해, 한 문장으로 전국 주차장을 찾아 추천받고 모의 결제로 예약하는 앱을 만듭니다. 헌법 → 명세 → 명확화 → 계획 → 품질 점검 → 작업 목록 → 구현 → 수렴의 각 단계에서 어떤 문서가 생기고, 문서를 어떤 기준으로 검토하는지 실제 실행 결과로 확인합니다.

!!! tip "실습 산출물 저장소 · GitHub"
    이 튜토리얼을 실제로 실행해 남은 파일과 기록을 공개 저장소 [uengine-oss/tutorial-speckit-handson](https://github.com/uengine-oss/tutorial-speckit-handson)에 올려 두었습니다. 단계마다 커밋이 하나씩 있고, 장마다 태그(`step-04-specify` 등)가 붙어 있어 그 장이 끝났을 때의 파일을 그대로 열어 볼 수 있습니다. 각 장 첫머리의 「이 장의 산출물」 상자와 본문의 파일 이름을 누르면 해당 파일이 열립니다.

## 무엇을 · 왜

AX School의 AI-PMO 과정에서 이 교재는 두 교재를 잇는 단계입니다.

| 순서 | 교재 | 사양을 다루는 방식 |
|---|---|---|
| 1 | [디자인 → MVP → 실제 구현](../ai-planning/index.html) | 화면 시안과 동작하는 MVP를 Claude Code에 넘기고, 계획 모드에서 바로 구현합니다 |
| 2 | **Claude Code × Spec Kit 핸즈온 (이 교재)** | 구현 전에 사양을 문서로 정리하고, 모호한 부분을 정해진 기준으로 묻고, 작업을 나눠 에이전트에게 맡깁니다 |
| 3 | [Claude Code × AI-DLC 핸즈온](../aidlc-handson/index.html) | 팀 규칙, 승인 게이트, 유닛과 볼트, 검토 에이전트까지 갖춘 개발 수명주기로 확장합니다 |

1번 교재에서는 화면을 보고 바로 만들었습니다. 그 방식은 빠르지만, 무엇을 만들기로 했는지가 대화 속에만 남습니다. 3번 교재의 AI-DLC는 그 결정을 모두 문서와 게이트로 남기지만, 단계가 많고 처음 접하기에는 부담스럽습니다.

Spec Kit은 그 중간 단계입니다. 프로젝트마다 원칙 문서(헌법) 하나를 두고, 기능마다 `spec.md` → `plan.md` → `tasks.md`를 차례로 만든 뒤 구현합니다. 명령은 `/speckit-`로 시작하는 Claude Code 스킬 아홉 개가 전부입니다. 이 교재에서 사양 주도 개발(SDD)의 기본 흐름을 익히면, AI-DLC에서 무엇이 더해지는지 훨씬 쉽게 이해할 수 있습니다.

## 예제: 전국 주차장 검색·예약

AI-DLC 핸즈온의 VoiceParking에서 다룬 문제를 조금 확장했습니다.

- 운전자가 "강남역 근처 2시간 주차"처럼 한 문장을 입력합니다.
- 서울·부산·대구·대전·광주의 샘플 주차장 가운데 조건에 맞는 곳을 찾아 추천 1곳과 비교 후보 2곳을 이유와 함께 보여 줍니다.
- 한 곳을 골라 모의 결제를 하고, 승인되면 예약 번호를 받습니다. 실패하면 사유를 보고 다시 시도합니다.

AI-DLC 핸즈온은 같은 문제를 Spring Boot 마이크로서비스 3개로 만들었습니다. 이 교재는 헌법의 「단순함」 원칙에 따라 Spring Boot 서비스 1개와 Vue 3 화면 1개로 만듭니다.

## 누가 어디부터 보면 좋은가

| 독자 | 시작할 곳 | 이유 |
|---|---|---|
| 기획자·PM | [명세](specify.html) → [명확화](clarify.html) → [요구사항 품질 점검](checklist.html) | 요구사항을 어떤 문장으로 쓰고, 모호함을 어떤 기준으로 찾아내는지가 기획 업무와 같습니다 |
| 개발 리더 | [계획](plan.html) → [작업 목록](tasks.html) → [구현과 병렬 에이전트](implement.html) | 사양이 설계 문서와 작업으로 나뉘고, 에이전트 여럿에게 나뉘는 방식을 봅니다 |
| 처음 보는 사람 | [스펙 주도 개발과 BDD](concepts.html)부터 순서대로 | 개념 → 설치 → 단계별 실습 순서입니다 |

## 장 목록

| 장 | 하는 일 | 명령 |
|---|---|---|
| [시작하기](index.html) | 교재의 위치와 예제 | |
| [스펙 주도 개발과 BDD](concepts.html) | 사양이 원본이 되는 이유, Given/When/Then, Spec Kit과 AI-DLC | |
| [설치와 프로젝트 준비](setup.html) | uv로 설치, `specify init`, 만들어지는 파일 | `uv tool install specify-cli` |
| [헌법: 프로젝트 원칙](constitution.html) | 모든 기능이 지켜야 할 원칙 네 개 | `/speckit-constitution` |
| [명세: spec.md](specify.html) | 사용자 이야기·인수 시나리오·요구사항·성공 기준 | `/speckit-specify` |
| [명확화: 모호함을 재는 기준](clarify.html) | 열 가지 범주로 빈 부분을 찾고 다섯 번 묻기 | `/speckit-clarify` |
| [계획: plan.md와 설계 문서](plan.html) | 기술 선택, 헌법 점검, 데이터 모델, API 계약 | `/speckit-plan` |
| [요구사항 품질 점검](checklist.html) | "요구사항을 위한 단위 시험"으로 사양과 계획의 어긋남 찾기 | `/speckit-checklist` |
| [작업 목록과 일관성 분석](tasks.html) | `T001 [P] [US1]` 형식, 단계, 병렬 표시, 세 문서 대조 | `/speckit-tasks` · `/speckit-analyze` |
| [구현과 병렬 에이전트](implement.html) | 체크리스트 관문, `[P]` 작업을 서브에이전트에 나눠 맡기기 | `/speckit-implement` |
| [수렴과 동작 확인](converge.html) | 사양 대비 남은 일 찾기, 실제 앱 실행 | `/speckit-converge` |
| [TDD와 랄프 루프](tdd-loop.html) | 시나리오가 JUnit·Vitest 시험이 되는 과정, 같은 지시를 수렴까지 되풀이하는 루프 | `./ralph.sh` |
| [확장: 업무 매뉴얼과 시연 영상](extension.html) | 구현 뒤 사양대로 화면을 녹화하고 업무 매뉴얼을 쓰는 확장을 만들어 `after_implement` 훅에 연결 | `specify extension add` · `/speckit-manual-create` |

## 준비물

| 구분 | 준비할 것 |
|---|---|
| Spec Kit | Python 3.11 이상, [uv](https://docs.astral.sh/uv/), Git |
| 에이전트 | 로그인된 Claude Code |
| 예제 앱 | Java 17, Maven 3.9, Node.js 20 이상 |

화면과 결과는 2026년 11월 13일 Spec Kit 1.4.0, Claude Code 2.1.323(Sonnet 5.5, 노력 수준 medium)으로 실행해 얻었습니다. 권한 모드는 자동 모드(auto mode)였습니다. 모델이 쓰는 문장과 질문은 실행할 때마다 달라질 수 있습니다. 화면 문구가 조금 다르더라도 같은 단계에서 같은 종류의 문서가 생기는지를 기준으로 비교하세요.

먼저 [스펙 주도 개발과 BDD](concepts.html)에서 이 교재의 바탕이 되는 두 개념을 간단히 살펴봅니다.
