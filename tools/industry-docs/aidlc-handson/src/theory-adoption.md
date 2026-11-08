# 검증 피로를 막는 정책과 도입 순서

> 볼트가 시간 단위로 짧아지면 검토자가 산출물을 제대로 읽지 못하고 승인만 누르기 쉽습니다. 이 장에서는 이를 막는 세 가지 정책, 조직에 적용할 4계층 참조 구조, 단계적 도입 순서를 설명합니다. 이 실습의 승인 기록이 그 정책을 얼마나 충족하는지도 확인합니다.

## 고무도장 승인

볼트 주기가 시간 단위로 줄면, 사람이 에이전트가 만든 많은 산출물을 꼼꼼히 살피지 못하고 승인 단추만 누르는 **고무도장(rubber-stamping)**식 승인이 생깁니다. 그러면 운영 결함이 늘어납니다. 이를 막으려면 다음 세 가지 정책을 글로 정해 두어야 합니다.

| 정책 | 내용 | 이 실습의 기록 |
|---|---|---|
| 지정 승인자(Named Approver) | 프롬프트를 입력해 에이전트를 실행한 사람이 아닌 동료가 승인자가 되고, 승인한 사람의 신원을 감사 기록에 남깁니다 | **충족하지 못했습니다.** 같은 사람이 요청하고 승인했습니다. 승인 기록에 승인자 이름 칸이 없습니다 |
| 검토 표준(Review Standard) | 직관 대신 체크리스트를 기준으로 검토합니다. 데이터 스키마의 영향 범위, 되돌리기 경로, 조향 규칙의 보안 규약을 확인합니다 | **일부 충족합니다.** 검토 에이전트가 단계마다 같은 형식(`READY`·`NOT-READY` 판정과 Major·Minor 지적)으로 검토하고, 체크포인트마다 사람이 정한 검증 명령을 실행합니다 |
| 의사결정 로그(Decision Log) | 승인 당시의 사양 버전, 적용된 규칙의 해시, 승인자, 시각을 묶어 바꿀 수 없는 기록으로 남깁니다 | **대부분 충족합니다.** 시각, 단계, 사람의 답이 남고, 일부 사건에는 검증 근거의 해시(sha256)가 붙습니다. 승인자 신원은 없습니다 |

이 실습의 실제 승인 기록 하나입니다([감사 기록](https://github.com/uengine-oss/tutorial-aidlc-handson/tree/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/audit)).

```
## Gate Approved
**Timestamp**: 2026-11-05T09:01:16Z
**Event**: GATE_APPROVED
**Stage**: practices-discovery
**User Input**: Approve
**Person Reply**: Approve
**Message Id**: 415cdb26
**Brief Digest**: none
```

언제, 어느 단계를, 어떤 답으로 승인했는지는 남지만 누가 승인했는지는 남지 않습니다. 감사 기록 파일 이름으로 기록을 남긴 컴퓨터와 클론을 알 수 있을 뿐입니다. 팀으로 쓰려면 승인자 지정과 신원 기록을 풀 리퀘스트 승인 같은 외부 절차로 보완해야 합니다.

## 4계층 참조 구조

조직에 AI-DLC를 도입할 때는 사양 수립, 작업 편성, 에이전트 실행, 형상관리, 품질 검증이 끊기지 않고 이어져야 합니다. 역할에 따라 네 계층으로 나눌 수 있습니다.

| 계층 | 하는 일 | 쓰는 도구의 예 | 이 실습에서 다룬 것 |
|---|---|---|---|
| ① 사양과 조향 | 비즈니스 목표를 검증된 요구사항과 기술 사양으로 바꾸고, 구현 전에 사양 게이트로 모순을 걸러 냅니다. 프롬프트는 레지스트리에서 환경별로 관리합니다 | AI-DLC 조향 규칙, Driftless Spec Gates, Langfuse | 요구사항·스토리·도메인 설계·계약(6~9장), 규칙 파일(5장) |
| ② 작업 편성과 관제 | 승인된 사양을 유닛으로 나누고 의존 DAG를 만든 뒤 볼트 계획으로 구체화합니다. 의존 조건을 충족한 작업을 에이전트에 할당합니다 | AI-DLC 유닛·볼트 계획, Driftless Task Board, Linear | 유닛 5개와 볼트 5개(9~10장) |
| ③ 실행과 형상관리 | Kiro, Claude Code, Cursor 같은 에이전트가 유닛을 병렬로 구현합니다. 작업 트리와 데이터를 따로 관리합니다 | Git 워크트리, Jujutsu, lakeFS, DVC | Claude Code 한 세션에서 유닛을 차례로 구현했습니다(11~13장) |
| ④ 품질과 운영 피드백 | 단위 시험 뒤 풀 리퀘스트로 제출합니다. CI에서 프롬프트 회귀 평가를 수행하고, 지정 승인자가 감사 기록을 보고 병합을 승인합니다. 운영 기록을 사양에 다시 반영합니다 | Promptfoo, CI, Langfuse | 체크포인트 검증과 빌드·테스트 판정표(14장). CI와 운영 단계는 이번 실습 범위에 포함하지 않습니다 |

## 단계적 도입 순서

갑자기 프로세스를 바꾸면 혼란이 생기므로 단계를 나누어 도입합니다.

1. **영향이 작은 내부 서비스로 시범 운영합니다.** 결제·인증 같은 핵심 시스템이 아니라 내부 배치나 백오피스 API에 볼트 1~2회를 먼저 적용하고, 검증 피로와 도구 사이의 병목을 수치로 측정합니다. 이 실습도 외부 연동 없이 모의 결제를 쓰는 프로토타입으로 시작했습니다.
2. **첫 볼트 전에 승인 정책을 글로 정합니다.** 유닛별 지정 승인자, 표준 검토 체크리스트, 의사결정 로그 보존 규칙을 먼저 정하지 않으면, 속도가 빨라진 뒤 승인이 형식적인 절차로 바뀝니다. AI-DLC에서는 팀 규칙(`team.md`)과 프로젝트 규칙(`project.md`)이 이 정책을 적는 곳입니다.
3. **착수(Inception) 단계에서 인수 시험을 먼저 씁니다.** 사양을 정할 때 Given/When/Then 인수 조건을 적고, 사람이 승인해야 구현(Construction)으로 넘어가게 합니다. 이 실습의 스토리에는 `AC4.1.1` 같은 인수 조건 ID가 붙어 있고, 팀 규칙에서 TDD를 정했으므로 구현할 때는 실패하는 시험부터 작성했습니다.
4. **속도 지표와 함께 결함 유출률을 측정합니다.** 개발 속도가 몇 배로 빨라져도 운영 환경까지 넘어간 결함이 늘었다면, 효율이 오른 것이 아니라 검증 책임을 운영에 떠넘긴 것입니다. 배포 빈도, 변경 리드 타임과 함께 **결함 유출률(Defect Escape Rate)**을 핵심 지표로 봅니다.

## 정리

AI-DLC는 코드를 빨리 쓰게 하는 기법이 아니라, 개발의 중심을 코드 구현에서 **사양 설계와 검증 통제**로 옮기는 방식입니다. 실행 비용이 낮아질수록 팀의 경쟁력은 명확한 사양, 결정론적 품질 게이트, 에이전트 산출물을 안전하게 조율하는 거버넌스에서 나옵니다. 레벨 2 실습의 판정표가 목표 22개 가운데 3개를 Not Met으로 남기고 목표를 낮추지 않은 것도 같은 원칙입니다([`build-and-test-summary.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/construction/build-and-test/build-and-test-summary.md)).

## 확인 문제

<details class="answer" markdown="1">
<summary>AI-DLC의 승인 기록만으로 「지정 승인자」 정책을 지킬 수 있나요?</summary>

이 실습의 2.11.2 기록만으로는 어렵습니다. 승인 기록에는 시각, 단계, 답이 남지만 승인자 신원은 남지 않습니다. 같은 사람이 요청하고 승인해도 구분되지 않습니다. 풀 리퀘스트 승인 같은 외부 절차로 승인자를 지정하고 기록해야 합니다.
</details>

<details class="answer" markdown="1">
<summary>개발 속도가 세 배 빨라졌는데 결함 유출률도 올랐습니다. 성공인가요?</summary>

아닙니다. 검증 책임을 운영 환경으로 떠넘긴 것입니다. 속도 지표와 결함 유출률을 함께 봐야 합니다.
</details>

<details class="answer" markdown="1">
<summary>첫 볼트를 돌리기 전에 정해 두어야 할 것은 무엇인가요?</summary>

유닛별 승인자, 표준 검토 체크리스트, 의사결정 로그의 보존 기간입니다. 이를 먼저 정하지 않으면 속도가 붙은 뒤 승인이 형식적인 절차로 바뀝니다.
</details>

## 참고 자료

- AI-DLC Explained: AWS's AI-Driven Development Lifecycle, <https://www.exploreagentic.ai/insights/ai-dlc/>
- AIDLC: AI Development Lifecycle & AI SDLC — driftless, <https://godriftless.ai/aidlc>
- AI-DLC in Practice: Running AWS's AI-Driven Lifecycle, <https://orchestrator.dev/blog/2026-10-03-ai-dlc-in-practice/>
- [AWS Summit Seoul 2026] 생성형 AI 시대의 새로운 개발 방법론, <https://tech.cloud.nongshim.co.kr/blog/aws/ai/3930/>
- AI-DLC를 활용한 업무용 툴 개발기, <https://suzuworld.tistory.com/476>
