# 사양 주도 개발과 검증 게이트

> AI-DLC에서 엔지니어링의 출발점은 코드가 아니라, 기계가 읽을 수 있는 사양과 에이전트를 이끄는 조향 규칙입니다. 이 장에서는 규칙이 어떤 계층으로 쌓이는지, 사양의 결함을 구현 전에 막는 게이트가 무엇을 검사하는지, 프롬프트 변경이 기존 동작에 문제를 일으키는지 확인하는 회귀 시험(regression testing)을 어떻게 수행하는지 설명합니다.

## 조향 규칙은 층으로 쌓인다

에이전트가 비즈니스 맥락에서 벗어나거나 설계를 마음대로 바꾸지 못하게 하려면, 에이전트의 실행을 제어하는 환경인 하네스(harness)에 작업 지침을 넣어야 합니다. 이를 **조향 규칙(steering rules)**이라고 합니다. AWS AI-DLC는 Kiro에서는 `.kiro/steering/`, Claude Code에서는 `.claude/CLAUDE.md`를 통해 규칙을 적용합니다.

이 실습에서 확인한 Claude Code 연결 방식은 다음과 같습니다. `.claude/CLAUDE.md`가 규칙 파일들을 불러오고, 규칙은 다섯 계층에 걸쳐 더해집니다. 적용 범위가 좁은 계층은 넓은 계층의 규칙을 보완할 수만 있고 뒤집을 수는 없습니다.

| 층 | 파일 | 이 실습의 예 |
|---|---|---|
| 조직 | `org.md` | 테스트를 핵심 산출물로 다룹니다. classic 범위에서는 라인 커버리지 하한이 80%입니다 |
| 팀 | `team.md` | 테스트 방식은 TDD이며, Vue 3 + Spring Boot를 사용하고 Docker는 쓰지 않습니다 |
| 프로젝트 | `project.md` | "NEVER Docker를 도입하지 않는다" 같은 금지·의무 규칙 |
| 단계 | `phases/inception.md` 등 | 인수 조건은 Given/When/Then, ADR에는 대안 두 개 이상 |
| 스테이지 | 스테이지 파일(프레임워크 안) | 스테이지마다 만들 문서와 질문 |

레벨 2의 규칙 파일은 [`memory/`](https://github.com/uengine-oss/tutorial-aidlc-handson/tree/main/level2-classic/aidlc/spaces/default/memory) 폴더에 있습니다. 팀 규칙은 사람이 직접 작성하는 대신 1단계(팀 규칙 찾기)의 질문에 답한 뒤 결과를 승인해 만들었습니다(9장).

!!! warning "문서마다 다르게 적힌 산출물 위치"
    여러 소개 글은 요구사항과 설계 결정이 `aidlc-docs/` 폴더에 쌓인다고 설명합니다. AI-DLC 1판의 구조입니다. 이 실습에서 쓴 2.11.2는 작업마다 `aidlc/spaces/default/intents/<날짜>-<이름>/` 폴더를 만들고 그 아래에 산출물을 단계별로 저장합니다. 프레임워크와 함께 설치되는 원칙 문서(`ai-dlc-principles.md`)에는 아직 `aidlc-docs/`라는 옛 표현이 남아 있습니다. 어느 쪽이든 세션을 다시 시작해도 맥락이 사라지지 않게 문서로 남긴다는 원칙은 같습니다.

## 사양 게이트: 구현 전에 사양의 결함을 막는다

**사양 게이트(Spec Gates)**는 코드를 만들기 전에 사양 자체의 구조적 결함을 걸러 내는 검사입니다. Driftless Cascades 같은 도구는 요구사항 정의서(PRD)와 기술 사양서가 세 가지 게이트를 통과해야 구현으로 넘어가게 합니다. AI-DLC는 같은 이름의 게이트를 쓰지 않습니다. 대신 센서, 검토 에이전트, 후속 질문, 승인 게이트로 비슷한 검사를 나눠 맡깁니다.

| 게이트 | 검사하는 것 | 불합격이면 | AI-DLC 2.11.2에서 비슷한 일을 하는 것 | 이 실습의 예 |
|---|---|---|---|---|
| 무결성(Integrity) | PRD 절과 기술 사양의 1:1 대응, 사양마다 구현 작업이 있는지, Given/When/Then 인수 조건 | 구현 단계 진입 차단 | 센서 `required-sections`·`claim-sources`·`upstream-coverage`·`traceability`, 단계 규칙의 Given/When/Then | 요구사항 문서 맨 위의 출처 목록(`[desc]`, `[Q3]`)과 가정 표시(`[assumption]`), [`traceability.json`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/requirements-analysis/traceability.json) |
| 충돌(Collisions) | 사양 절끼리의 모순, 인접한 기능과의 계약 충돌, 비즈니스 사양에 섞인 기술적 세부 사항 | 사양 자동 재작성 | 요구사항 분석의 **후속 질문**, 검토 에이전트의 `NOT-READY` | 답만으로 정할 수 없거나 서로 모순되는 부분을 후속 질문 3개로 다시 물었습니다(10장). 도메인 설계 첫 검토에서는 순환 의존을 찾았습니다(12장) |
| 결과(Consequences) | 의존 그래프의 끊긴 곳, 빠진 작업, 공유 자원의 영향 범위 | 의존과 작업을 보완할 때까지 대기 | 유닛 의존 그래프, 계약 설계, 볼트 계획의 위험·외부 의존 문서 | [`unit-of-work-dependency.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/units-generation/unit-of-work-dependency.md), [`risk-and-sequencing-rationale.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/delivery-planning/risk-and-sequencing-rationale.md) |

AI-DLC의 센서에는 경고만 하는 것(advisory)과 승인을 막는 것(blocking)이 있습니다. 승인을 막는 센서가 실패하면 검사 결과를 무시한다는 명시적 결정(override)을 감사 기록에 남겨야 게이트가 열립니다. 이 실습에서는 센서가 218번 실행되었고 7번 실패했습니다. 3건은 문서를 고친 뒤 다시 통과했습니다. 나머지 4건은 u4·u5 문서의 상위 문서 반영 검사(`upstream-coverage`)였습니다. 이 검사는 기본적으로 경고용이므로, 다시 통과한 기록 없이 다음 단계로 넘어갔습니다. 경고용 센서가 실패해도 다음 단계로 넘어갈지는 사람이 판단해야 합니다.

## 사양을 이렇게 쓰면 게이트를 통과한다

게이트가 검사하기 쉬운 사양에는 공통점이 있습니다. 이 실습의 문서에서도 확인할 수 있습니다.

1. **근거가 적혀 있습니다.** 요구사항 문서 맨 위 `## Sources`에 `[desc]`(처음 요청), `[Q3]`(세 번째 질문의 답) 같은 근거 목록이 있고, 사람에게 확인받지 않은 가정에는 `[assumption]`이 붙습니다. 센서가 이 표시를 검사하므로 근거 없는 요구사항이 슬며시 끼어들기 어렵습니다([`requirements.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/requirements-analysis/requirements.md)).
2. **합격 기준을 측정할 수 있습니다.** "빠르게" 대신 "결제 승인 뒤 1초 안에 완료 표시"처럼 씁니다. 이 1초는 구현 단계에서 웹훅 150ms, 예약 반영 150ms처럼 구간별로 나뉘었습니다(16장).
3. **ID로 연결됩니다.** 스토리의 인수 조건 ID(`AC4.1.1`)가 볼트 계획의 완료 기준과 코드 계획의 시험 순서(Red 단계)까지 이어지고, 추적표가 그 ID를 구현 파일과 시험 파일에 연결합니다([`stories.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/user-stories/stories.md)).
4. **결정에는 대안이 있습니다.** 도메인 설계의 결정 기록(ADR)은 맥락, 결정, 결과, 채택하지 않은 대안을 함께 적습니다([`decisions.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/domain-design/decisions.md)).

## 프롬프트도 배포 산출물이다

애플리케이션 코드 안에 프롬프트와 에이전트 지침을 직접 넣으면 버전을 추적하기 어렵고, 도메인 전문가나 기획자가 함께 고치기도 어렵습니다. 그래서 프롬프트를 독립된 산출물로 다루는 도구가 쓰입니다.

| 도구 | 하는 일 | 쓰는 곳 |
|---|---|---|
| Langfuse | 프롬프트 버전과 릴리스 레이블 관리, 실행 기록(trace) 연결 | 운영 중인 AI 기능의 프롬프트를 재배포 없이 바꾸고 추적 |
| Promptfoo | YAML로 입력·기대 출력·안전 제약을 정의하고, PR마다 자동 평가해 기준 미달이면 병합 차단 | 프롬프트나 모델을 바꿀 때 회귀 시험 |
| AI-DLC 조향 규칙 | 단계별 규칙을 마크다운으로 넣고, 산출물과 함께 Git에 저장 | 개발 에이전트가 지침을 벗어나지 않도록 방지 |

이 실습에서는 개발 에이전트의 규칙만 다뤘으므로 Langfuse와 Promptfoo는 쓰지 않았습니다. 만든 앱 안에 LLM 기능이 들어간다면, 이런 평가 도구로 해당 프롬프트의 회귀 시험을 수행하는 것이 좋습니다.

## 확인 문제

<details class="answer" markdown="1">
<summary>팀 규칙에 "Docker를 쓴다"고 쓰면 조직 규칙과 충돌하지 않나요?</summary>

규칙은 조직 → 팀 → 프로젝트 → 단계 → 스테이지 순서로 더해지고, 적용 범위가 좁은 계층은 넓은 계층의 규칙을 뒤집을 수 없습니다. 적용 범위가 넓은 계층과 모순되는 규칙은 학습 단계의 승인 검사에서 거절됩니다. 이 실습의 조직 규칙은 Docker에 대해 아무것도 정하지 않았으므로, 팀이 "Docker를 쓰지 않는다"고 정할 수 있었습니다.
</details>

<details class="answer" markdown="1">
<summary>답변끼리 모순되면 AI-DLC는 어떻게 하나요?</summary>

"모순 감지" 경고 문구를 띄우는 대신, 요구사항 분석 단계에서 서로 충돌하는 답을 찾아 후속 질문으로 다시 묻습니다. 이 실습에서는 질문 4개에 답한 뒤 후속 질문 3개가 나왔습니다. 시간 적합도 점수 계산, 웹훅 승인 뒤 화면에 결과를 전달하는 방식, 180초를 세는 시점처럼 답만으로는 정할 수 없던 부분이었습니다(10장).
</details>

<details class="answer" markdown="1">
<summary>요구사항 문서의 `[Q3]`, `[assumption]` 같은 표시는 왜 필요한가요?</summary>

요구사항이 어디서 왔는지 보여 줍니다. `[Q3]`은 세 번째 질문의 답이 근거라는 뜻이고, `[assumption]`은 아직 사람에게 확인받지 않은 가정이라는 뜻입니다. 센서가 이 표시를 검사하므로 근거 없는 요구사항이 끼어들기 어렵고, 나중에 요구사항이 왜 생겼는지 거꾸로 추적할 때도 씁니다.
</details>

## 참고 자료

- AIDLC: AI Development Lifecycle & AI SDLC — driftless, <https://godriftless.ai/aidlc>
- What Is Spec-Driven Development? Tools and Specs — re:cinq, <https://re-cinq.com/topics/spec-driven-development>
- Open Source Prompt Management — Langfuse, <https://langfuse.com/docs/prompt-management/overview>
- Promptfoo Review 2026 for LLM Regression Testing — PE Collective, <https://pecollective.com/tools/promptfoo/>
- CJ올리브영의 AI 협업 개발 프로세스 구축, AI-DLC 실전 도입 사례 — AWS 기술 블로그, <https://aws.amazon.com/ko/blogs/tech/cj-oliveyoung-aidlc-tech-blog/>
