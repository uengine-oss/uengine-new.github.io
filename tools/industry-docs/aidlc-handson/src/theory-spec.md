# 사양 주도 개발과 검증 게이트

> AI-DLC에서 엔지니어링의 출발점은 코드가 아니라, 기계가 읽을 수 있는 사양과 에이전트를 이끄는 조향 규칙입니다. 이 장에서는 먼저 어셈블리에서 C로 넘어가던 때의 논쟁에 견주어 왜 사양이 중심이 되는지 보고, 이어서 규칙이 어떤 계층으로 쌓이는지, 사양의 결함을 구현 전에 막는 게이트가 무엇을 검사하는지, 프롬프트 변경이 기존 동작에 문제를 일으키는지 확인하는 회귀 시험(regression testing)을 어떻게 수행하는지 설명합니다.

## 왜 사양이 중심이 되나: 어셈블리에서 C로 넘어갈 때와 같은 논쟁

지금의 AI 코딩(바이브 코딩) 논쟁은 1970~80년대 C 언어가 등장했을 때의 논쟁과 놀라울 만큼 겹칩니다. 그때도 똑같은 반발과 회의론이 있었습니다.

### 당시 어셈블리 개발자들의 반발

C 언어가 운영체제(Unix)와 시스템 개발에 도입되던 당시, 베테랑 프로그래머들은 강하게 반발했습니다.

- **"컴파일러가 사람의 최적화를 따라올 수 없다."** 어셈블리를 쓰면 CPU 레지스터를 몇 개 사용할지, 메모리 사이클에 몇 클록을 쓸지 프로그래머가 완전히 제어할 수 있었습니다. 반면 컴파일러가 번역한 기계어는 쓸데없는 분기와 오버헤드가 많아 비효율적이고 무겁다는 비판을 받았습니다.
- **"결국 디버깅하려면 어셈블리를 알아야 한다."** C로 추상화해 봤자 프로그램이 비정상 종료되거나 버그가 나면 결국 메모리 덤프와 어셈블리 코드를 들여다봐야 합니다. 어셈블리를 모른 채 C만 쓰면 문제를 해결하지 못하는 반쪽짜리 개발자가 된다는 논리였습니다.
- **"하드웨어 제어권을 잃는다."** 포인터 같은 개념이 있어도 특정 주소의 미세한 타이밍을 제어하거나 하드웨어 전용 인터럽트를 다루는 일은 C로 완벽히 해낼 수 없다는 비판이 지배적이었습니다.

### 역사가 내린 결론

이 논쟁은 두 단계를 거쳐 정리되었습니다.

1. **컴파일러의 진화와 생산성의 승리.** 최적화 기술(옵티마이저)이 발전하면서 사람이 짠 어셈블리보다 컴파일러가 만든 코드가 더 효율적인 영역이 점점 넓어졌습니다. 게다가 하드웨어 성능이 급격히 좋아지면서 성능을 몇 퍼센트 더 높이는 것보다 개발 속도와 이식성이 훨씬 더 중요해졌습니다.
2. **영역의 분리.** 어셈블리가 완전히 사라진 것은 아닙니다. 부트로더, 운영체제 커널의 초기화 코드, 실시간 임베디드 칩처럼 아주 좁고 깊은 영역에는 어셈블리가 남았습니다. 하지만 산업 전반에서는 대부분 C와 그보다 추상화 수준이 높은 언어(C++, Java, Python)로 넘어갔습니다.

### 지금의 논쟁과 나란히 놓으면

지금의 AI 코딩 논쟁은 추상화 계층이 한 단계 더 올라가는 과정에서 같은 논쟁이 되풀이되는 모습입니다.

| 구분 | 1970~80년대 (어셈블리 → C) | 지금 (직접 코딩 → 바이브 코딩·AI) |
|---|---|---|
| 추상화 단위 | 하드웨어 레지스터·명령어 → 문법·함수 | 문법·함수·로직 → 자연어 사양·프롬프트 |
| 비판하는 쪽 | "어셈블리를 모르면 메모리 누수와 성능 저하를 못 잡는다." | "AI가 짠 코드의 내부 로직을 한 줄씩 검증하지 않으면 사고가 난다." |
| 낙관하는 쪽 | "알고리즘 구조와 설계만 C로 짜면 컴파일러가 알아서 한다." | "입출력 명세와 시험 하네스(사양)만 정교하면 내부는 상관없다." |

앞으로의 흐름도 이전과 비슷할 가능성이 높습니다.

- **사양과 검증 자동화의 승리.** AI가 만드는 코드의 품질이 높아지고, 이를 검증하는 자동화 수단(TDD, E2E 시험, 정적 분석 도구)이 정교해질수록 사람이 코드를 한 줄씩 읽는 비용은 감당하기 어려워집니다.
- **영역의 분리.** 시스템 코어, 보안 취약점 점검, 고성능 최적화 영역에서는 여전히 전통적인 방식으로 코드 수준에서 검증하는 사람이 필요합니다. 하지만 대부분의 비즈니스 로직과 서비스 개발에서는 「사양을 정교하게 정하고 검증 환경을 설계하는 엔지니어링」으로 무게중심이 옮겨 가고 있습니다.

"어셈블리를 직접 다룰 줄 알아야 진짜 엔지니어인가?"라는 옛 질문이 지금은 "코드를 직접 치고 한 줄씩 읽어야 진짜 개발자인가?"라는 질문으로 옷만 갈아입고 되풀이되고 있습니다. 사양 주도 개발은 이 질문에 대한 답입니다. 사람의 일을 코드 작성에서 사양 정의와 검증 설계로 옮깁니다.

이 튜토리얼의 실습도 같은 방향을 따릅니다. 승인자는 AI가 만든 코드를 한 줄씩 읽지 않았습니다. 대신 요구사항과 인수 조건, 검증 명령을 정해 승인하고, 결과는 자동 시험 886개와 목표별 판정표로 확인했습니다(18장). 성능 목표(20ms)와 비밀 값 처리처럼 좁고 깊은 영역은 별도의 시험과 설계 검토로 확인했습니다(16·17장).

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
<summary>"AI가 짠 코드를 한 줄씩 읽지 않으면 위험하다"는 주장은 역사 속 어떤 주장과 닮았나요?</summary>

1970~80년대의 "결국 디버깅하려면 어셈블리를 알아야 한다", "컴파일러가 사람의 최적화를 따라올 수 없다"는 주장과 닮았습니다. 당시 논쟁은 두 가지로 정리되었습니다. 컴파일러와 검증 도구가 발전하면서 대부분의 개발은 추상화 수준이 한 단계 높은 언어로 옮겨 갔고, 부트로더나 커널 초기화 같은 좁고 깊은 영역에만 어셈블리가 남았습니다. 지금도 대부분의 서비스 개발은 사양 정의와 검증 설계로 옮겨 가고, 시스템 코어·보안·고성능 영역에는 코드 수준의 검증이 남을 가능성이 높습니다.
</details>

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
