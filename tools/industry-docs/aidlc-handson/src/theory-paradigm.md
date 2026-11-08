# AI-DLC는 무엇이 다른가

> AI 주도 개발 생애주기(AI-DLC)에서는 AI 에이전트가 분석·설계·코드 작성·시험을 수행하고, 사람은 맥락을 검토하고 승인합니다. 실행과 통제의 역할이 뒤바뀌면 반복 주기는 스프린트에서 볼트로 짧아지고, 병목은 코드 작성에서 검증과 승인으로 옮겨 갑니다. 이 장에서는 실습의 실제 기록을 바탕으로 그 변화를 설명합니다.

!!! note "이론 장을 읽는 순서"
    이론 네 장은 실습 전에 읽어도 되고, 실습을 마친 뒤 내용을 정리하며 읽어도 됩니다. 각 장의 「이 실습에서는」 칸은 레벨 2(classic) 실행 기록을 바탕으로 설명합니다. 기록은 [공개 저장소](https://github.com/uengine-oss/tutorial-aidlc-handson)에서 직접 열어 볼 수 있습니다.

## 실행과 통제가 뒤바뀐다

전통적인 개발 생애주기(SDLC)에서 자동화 도구와 컴파일러는 사람의 판단과 코드 작성을 돕는 수단이었습니다. AI-DLC에서는 AI 에이전트가 요구사항 분석, 설계, 코드 생성, 시험 작성을 맡고 사람은 비즈니스 맥락을 검토해 승인합니다. 일을 하는 쪽과 일을 통제하는 쪽이 바뀌는 것입니다.

| 비교 항목 | 전통적 SDLC (스크럼·애자일) | AI-DLC | 이 실습에서는 |
|---|---|---|---|
| 일을 실행하는 주체 | 사람 엔지니어 (AI는 보조) | AI 에이전트 (사람은 검토·승인) | 에이전트 11종이 단계마다 문서와 코드를 쓰고, 사람은 승인 게이트에서 18번 승인하고 3번 반려했습니다 |
| 기본 반복 단위 | 2~4주 스프린트 | 몇 시간~1~2일 볼트(Bolt) | 볼트 5개이며, u1 하나에 약 52분이 걸렸습니다 |
| 요구사항을 나누는 단위 | 에픽과 사용자 스토리 | 유닛(Unit of Work)과 계약 | 유닛 5개, API 계약 6개 |
| 주된 병목 | 코드 구현 속도 | 사양 검증·승인에 사람이 쏟을 수 있는 주의력 | 코드 생성보다 검토와 재시험에 시간이 오래 걸렸습니다 |
| 팀 협업 방식 | 일일 스탠드업, 스프린트 회의 | 몹 정교화(Mob Elaboration), 몹 구축(Mob Construction) | 한 사람이 답했습니다. 유저 스토리 단계는 몹 방식으로 설계되어 있습니다 |
| 형상관리 대상 | 소스 코드, 설정 파일 | 코드 + 프롬프트·조향 규칙·감사 기록 | `aidlc/` 폴더 전체를 저장소에 저장합니다 |

「이 실습에서는」 칸의 수치는 레벨 2 [감사 기록](https://github.com/uengine-oss/tutorial-aidlc-handson/tree/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/audit)에서 집계한 값입니다. 기록된 사건은 1,577건이며, 종류는 50가지입니다.

## 볼트와 유닛

**유닛**은 독립적으로 만들고 검증할 수 있는 작업 단위입니다. 큰 에픽을 유닛으로 나누고, 유닛 사이의 의존 관계를 그래프(DAG)로 그립니다. 이 실습에서는 [`unit-of-work.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/units-generation/unit-of-work.md)가 유닛 5개(u1 검색, u2 예약, u3 결제, u4 화면, u5 실행 스크립트)를 정했습니다.

**볼트**는 유닛 하나(또는 의존 관계로 연결된 작은 유닛 묶음)에 구현 단계 3.1~3.5(기능 설계 → NFR 요구 → NFR 설계 → 인프라 설계 → 코드 생성)를 한 번 실행하는 단위입니다. 스프린트가 사람 사이의 조율 비용 때문에 2~4주였다면, 볼트는 에이전트가 실행하므로 몇 시간 안에 끝납니다. 기획부터 통합 검증까지의 피드백 주기도 그만큼 짧아집니다.

| 단위 | 정의 | 이 실습의 파일 |
|---|---|---|
| 유닛 | 독립적으로 만들고 검증할 작업 단위 | [`unit-of-work.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/units-generation/unit-of-work.md), [`unit-of-work-dependency.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/units-generation/unit-of-work-dependency.md) |
| 볼트 | 유닛 하나에 3.1~3.5를 한 번 실행 | [`bolt-plan.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/delivery-planning/bolt-plan.md) (B1~B5) |
| 체크포인트 | 볼트가 끝날 때 검증 명령을 실행하고 결과를 기록 | 감사 기록의 `CHECKPOINT_VERIFICATION_RECORDED` 10건 |

## 생산성의 역설

코드를 만드는 비용이 거의 0에 가까워지면, 조직의 병목은 코드를 쓰는 속도에서 **사양을 검증하고 승인하는 데 쓸 수 있는 시간과 집중력**으로 옮겨 갑니다. 사양을 명확히 정하지 않고 코딩 도우미만 도입하면, 모델이 맥락 없이 지어낸 코드를 숙련자가 디버깅하느라 시간이 더 드는 역설이 생깁니다.

이 실습에서도 시간이 많이 든 작업은 코드 생성이 아니었습니다. u3 결제 서비스의 20ms 성능 시험이 호스트 부하로 결과가 불안정해지자, AI-DLC는 목표를 낮출지 다시 실행할지 사람에게 물었습니다(12장). u4 화면 설계는 검토 에이전트가 Major 6건을 지적하며 반려했습니다(13장). 빌드·테스트 단계의 판정표를 승인하기 전에 사람이 브라우저에서 앱을 직접 확인해야 했습니다(14장). 이런 판단이 사람의 몫으로 남습니다.

## 몹 정교화와 몹 구축

팀 단위 AI-DLC에서는 개발자마다 따로 프롬프트를 넣는 방식을 피합니다. 대신 팀이 함께 에이전트의 계획과 설계 제안을 실시간으로 검증합니다(**몹 정교화**). 구현 단계의 기술적 결정도 함께 조율합니다(**몹 구축**).

AI-DLC 2.11.2는 이 방식을 에이전트 구성에도 적용했습니다. 좁은 분야만 맡는 전문가 수십 개 대신 여러 업무를 맡는 에이전트 11종을 두고, 각 에이전트가 여러 단계에 참여합니다. 작업을 순서대로 넘기는 과정이 다시 폭포수 방식처럼 길어지는 일을 막으려는 것입니다. 단계마다 실행 방식도 정해져 있습니다. 2.4 유저 스토리는 `mob` 방식으로, 제품 에이전트가 이끌고 디자인·개발·품질 에이전트가 함께 참여합니다. 2.2 팀 규칙 찾기와 3.5 코드 생성은 별도 에이전트에게 맡기는 `subagent` 방식입니다.

이 실습에서는 한 사람이 모든 질문에 답했습니다. 팀으로 진행한다면 질문 파일(`*-questions.md`)과 승인 게이트를 함께 보는 자리가 몹 정교화가 됩니다.

## 결정론적 검증 게이트

개인의 프롬프트 숙련도와 관계없이 산출물의 최소 품질 수준을 지키려면, 단계 사이에 **결정론적 게이트**가 있어야 합니다. 같은 입력이면 같은 판정을 내리는 검사입니다. AI-DLC에서는 세 가지가 이 역할을 합니다.

| 게이트 | 하는 일 | 이 실습의 기록 |
|---|---|---|
| 센서 | 문서를 작성할 때 필수 절, 출처 표시, 상위 문서 반영, 추적 여부를 자동 검사 | `SENSOR_FIRED` 218건, 실패 7건 |
| 검토 에이전트 | 산출물을 읽고 `READY` / `NOT-READY` 판정과 Major·Minor 지적 | `REVIEW_REQUESTED` 32건 |
| 승인 게이트 | 사람이 Approve 또는 Request Changes 선택 | `GATE_APPROVED` 18건, `GATE_REJECTED` 3건 |

다음 장에서는 이 게이트들이 사양의 품질을 어떻게 지키는지 자세히 살펴봅니다.

## 확인 문제

<details class="answer" markdown="1">
<summary>볼트와 스프린트의 가장 큰 차이는 무엇인가요?</summary>

진행 기간과 실행 주체입니다. 스프린트는 사람 사이의 조율 비용 때문에 2~4주 단위입니다. 볼트는 에이전트가 유닛 하나의 구현 단계(3.1~3.5)를 실행하는 단위라 몇 시간 안에 끝납니다. 이 실습의 u1 볼트는 약 52분 걸렸습니다.
</details>

<details class="answer" markdown="1">
<summary>코드를 거의 공짜로 만들 수 있는데 왜 개발이 빨라지지 않을 수 있나요?</summary>

병목이 검증과 승인으로 옮겨 가기 때문입니다. 사양이 명확하지 않으면 AI가 만든 코드를 사람이 디버깅하는 시간이 늘어납니다. 그래서 AI-DLC는 코드보다 먼저 요구사항·설계·계약을 문서로 정하고, 단계마다 검증 게이트를 둡니다.
</details>

<details class="answer" markdown="1">
<summary>이 실습에서 사람이 판단해야 했던 일을 두 가지 들어 보세요.</summary>

예를 들어 u3의 20ms 성능 시험이 부하로 결과가 불안정할 때 목표를 유지하고 다시 실행하기로 한 결정(12장)과, 판정표를 승인하기 전에 브라우저에서 앱을 직접 확인한 일(14장)이 있습니다. 설계 검토에서 나온 반려 의견을 받아들여 수정을 승인한 것도 사람입니다.
</details>

## 참고 자료

- AI-DLC 방법론이란 무엇인가? — 스마일샤크, <https://www.smileshark.kr/post/what-is-ai-dlc-ai-driven-development-lifecycle>
- What Is AIDLC (AI-DLC)? The AI-Driven Development Lifecycle — nTra, <https://ntra.ai/ai-dlc>
- AI-Driven Development Lifecycle (AI-DLC) 란 무엇인가?, <https://dogfootsleep.tistory.com/entry/AI-Driven-Development-Lifecycle-AI-DLC-%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80>
- Understand the 3 Phases and Bolt / Mob Elaboration in 10 Minutes, <https://note.com/cc_works_cl/n/n673726233c57?hl=en>
- awslabs/aidlc-workflows, <https://github.com/awslabs/aidlc-workflows>
