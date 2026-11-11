# 형상관리와 볼트 진척 관리

> 여러 에이전트가 동시에 유닛을 만들면, 한 사람이 순서대로 진행하는 작업에 맞춰 설계된 Git 브랜치 방식이 병목이 됩니다. 이 장에서는 Git의 한계와 이를 보완하는 워크트리·Jujutsu, 데이터와 모델의 버전 관리, 그리고 시간 단위로 끝나는 볼트를 추적하는 방법을 다룹니다. AI-DLC 2.11.2가 실제로 어떻게 처리하는지도 함께 살펴봅니다.

## 에이전트가 여럿이면 Git의 어디가 막히나

| 제약 | 무슨 일이 생기나 |
|---|---|
| 하나의 인덱스와 작업 폴더 | Git은 저장소 하나에 `.git/index` 잠금과 작업 폴더 하나를 전제합니다. 에이전트 여럿이 동시에 쓰면 잠금을 기다리거나 서로의 파일을 덮어씁니다 |
| 충돌이 나면 멈춤 | 병합 중 충돌이 나면 충돌 표시가 파일에 들어가고 커밋·브랜치 전환이 막힙니다. 사람이 해결할 때까지 자동 실행이 멈춥니다 |
| 되돌리기가 어려움 | 에이전트가 재시도를 반복하다 잘못 고쳤을 때 reflog나 대화형 리베이스로 자동으로 되돌리기 어렵습니다 |
| 격리 비용 | 작업마다 저장소를 새로 복제하면 큰 모노레포에서는 디스크와 네트워크 비용이 커지고 작업 시작이 늦어집니다 |

## 워크트리와 Jujutsu

**Git 워크트리**는 저장소 하나에 작업 폴더를 여러 개 만들어 에이전트마다 따로 할당합니다. 폴더가 나뉘므로 병렬로 일할 수 있습니다. 하지만 브랜치 충돌과 잠금 방식은 Git 그대로입니다.

**Jujutsu(jj)**는 기존 Git 저장소와 원격 저장소를 그대로 쓰면서 형상관리의 핵심 동작을 다시 설계한 도구입니다.

- **작업 사본이 곧 커밋**입니다. `git add` 없이 수정이 바로 스냅샷으로 남습니다.
- **충돌도 커밋으로 남깁니다**(first-class conflicts). 두 에이전트가 같은 파일을 고쳐 충돌해도 작업이 멈추지 않고, 충돌을 커밋 그래프 안에 따로 남겨 나중에 해결합니다.
- **모든 변경 작업을 연산 기록(operation log)에 덧붙입니다.** 잘못된 리베이스도 `jj undo` 한 번으로 정확히 되돌립니다.
- 커밋을 합치거나 순서를 바꿔도 **바뀌지 않는 변경 ID**가 남고, 부모 커밋이 바뀌면 자식 커밋이 바뀐 부모 커밋 위에 자동으로 다시 적용됩니다.

Agentic Jujutsu는 jj에 MCP 서버와 구문 트리(AST) 분석을 붙여, 에이전트가 형상관리 명령을 직접 호출하고 변경 영향을 분석하게 한 확장입니다.

| 비교 | Git 브랜치 | Git 워크트리 | Jujutsu / Agentic Jujutsu |
|---|---|---|---|
| 여러 에이전트의 동시 작업 | 인덱스 잠금으로 제한 | 폴더를 나눠 병렬 가능 | 잠금 없이 병렬 커밋 |
| 충돌 | 작업 정지, 사람이 해소 | 작업 정지, 사람이 해소 | 충돌을 커밋으로 남기고 계속 진행 |
| 되돌리기 | reflog와 리셋 | 폴더 정리와 Git 복구 | 연산 기록으로 한 번에 되돌림 |
| 에이전트가 다루는 방법 | 셸 명령과 출력 해석 | 셸 명령과 경로 | MCP와 AST 기반 호출 |

!!! note "AI-DLC 2.11.2는 어떻게 하나"
    AI-DLC는 Jujutsu가 아니라 **Git 워크트리**를 씁니다. 구현 단계에서 볼트마다 워크트리와 브랜치를 만들고, 상태 파일·감사 기록·실행 그래프 조각을 그 워크트리용으로 따로 떼어 냅니다(fork). 볼트가 끝나면 이들을 다시 합치고, 브랜치는 `main`에 볼트 이름의 커밋 하나로 스쿼시 병합합니다(트렁크 기반). 감사 기록은 클론마다 다른 파일(`audit/<호스트>-<클론 ID>.md`)에 쓰므로 여러 사람이 동시에 기록해도 같은 파일에서 충돌하지 않습니다. 이 실습에서는 혼자 진행해 워크트리를 만들지 않았습니다. 상태 파일의 `Worktree Path`가 비어 있습니다.

## 데이터와 모델의 버전 관리

앱이 모델을 직접 미세 조정하거나 RAG 지식 베이스를 쓴다면, 코드뿐 아니라 원천 데이터와 모델 파일의 변경 이력과 서로의 관계도 함께 관리해야 합니다. Git은 큰 바이너리를 직접 다루지 못하므로 별도 계층을 둡니다.

| 도구 | 방식 | 잘 맞는 곳 |
|---|---|---|
| DVC | 실제 데이터는 S3·GCS 같은 객체 저장소에 두고, Git에는 해시를 담은 작은 포인터 파일(`.dvc`)만 커밋합니다. 파이프라인을 DAG로 정의해 실험을 재현합니다 | 개발자 중심의 ML 파이프라인 재현 |
| lakeFS | 객체 저장소 자체에 Git식 브랜치·커밋을 적용합니다. 큰 데이터 레이크를 복사하지 않고 몇 초 만에 가상 브랜치로 나눕니다 | 전사 데이터 레이크의 환경 분리와 거버넌스 |

흔히 권장하는 구성은 원천 데이터 레이크의 환경 분리는 lakeFS, 개별 ML 파이프라인과 코드 저장소의 연결은 DVC로 나누는 것입니다. 이 실습의 앱은 학습 데이터가 없으므로 해당하지 않습니다.

## 볼트 진척: 사람의 계획과 엔진의 실행 그래프는 따로 있다

볼트는 시간 단위로 끝나고 여러 에이전트가 병렬로 처리하므로, 사람 중심의 칸반 보드(Jira, Linear)만으로는 진행 상황을 실시간으로 관리하기 어렵습니다. 에이전트의 실행 상태, 승인 대기, 토큰 사용량, 의존 관계를 한 화면에서 확인하고 관리하는 관제가 필요합니다.

AI-DLC 안에서는 볼트 계획이 두 가지로 나뉩니다.

| | 사람이 읽는 계획 | 엔진이 실행하는 그래프 |
|---|---|---|
| 파일 | [`bolt-plan.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/delivery-planning/bolt-plan.md) | [`unit-of-work-dependency.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/units-generation/unit-of-work-dependency.md)의 `units` / `depends_on` 블록 |
| 만드는 단계 | 2.9 delivery-planning | 2.7 units-generation |
| 담는 것 | 볼트 순서와 이유, 완료 기준, 보여 줄 결과 | 유닛과 의존 관계 |
| 쓰임 | 릴리스 관점의 마일스톤 | 엔진이 이 블록을 컴파일해 병렬 실행 묶음(`bolt_dag.batches`)을 만듭니다 |

이렇게 나누면 한 유닛이 늦거나 실패해도, 그 유닛에 의존하지 않는 다른 묶음은 계속 진행할 수 있습니다. AI-DLC 2.11.2의 오케스트레이터 코드에도 "의존 문서가 있으면 그것이 기준이고, 컴파일된 묶음은 그 문서와 맞을 때만 받아들인다"고 적혀 있습니다. 공개 문서에서는 이 두 단계를 2.7과 2.8로 소개하기도 합니다. 2.11.2에서는 그 사이에 계약 설계(2.8)가 들어가서 볼트 계획이 2.9입니다.

이 실습의 의존 그래프는 한 줄로 이어집니다(u1 ← u2 ← u3 ← u4 ← u5). 그래서 실행 묶음도 다섯 개가 차례로 이어져, 병렬로 실행할 수 있는 유닛이 없었습니다. 예를 들어 화면(u4)이 검색(u1)에만 의존했다면, u2와 u4를 같은 묶음에서 동시에 만들 수 있었을 것입니다. 유닛을 나눌 때 의존 관계를 어떻게 정하느냐에 따라 병렬로 처리할 수 있는 정도가 달라집니다.

## 관제 도구

| 도구 | 하는 일 |
|---|---|
| Driftless Cascades Task Board | 백그라운드 데몬이 보드를 주기적으로 확인해 선행 조건을 충족한 작업을 코딩 에이전트에 보내고, 터미널 분할 화면에 로그·모델·토큰·비용을 보여 줍니다. 웹에서 에이전트를 원격으로 중지합니다 |
| nTra | 인터뷰로 비즈니스 의도를 파악해 작업과 사양으로 정리하고, Claude Code나 GitHub Copilot에 넘긴 뒤 결과를 풀 리퀘스트로 받습니다 |
| Linear | 키보드 중심의 빠른 이슈 관리와 주기(cycle) 관리를 지원합니다. 에이전트 게이트와 실행 기록은 외부 웹훅으로 연결해야 합니다 |
| Process GPT Lite (AI-DLC 팀 세션) | 저장소를 공유 폴더로 연결해 팀이 하나의 Claude Code 세션을 함께 사용합니다. 대기 중인 작업은 해당 역할 담당자의 홈 카드에서, 질문은 검토 보드에서 확인합니다. 진척은 의도 → 유닛 → 볼트 구조의 볼트 보드와 대시보드에서 확인합니다([19~21장](tools-team.html)) |
| AI-DLC 2.11.2 자체 | `/aidlc --status`(현재 단계와 가드), 상태 줄 표시, 팀 구현 현황 조회(`team-board`), 세션 비용(`/aidlc-session-cost`), 기록 재생(`/aidlc-replay`), 결과 묶음(`/aidlc-outcomes-pack`) |

이 실습에서는 따로 관제 도구를 쓰지 않고, 상태 파일 [`aidlc-state.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/aidlc-state.md)와 감사 기록으로 진행 상황을 확인했습니다.

## 확인 문제

<details class="answer" markdown="1">
<summary>볼트 계획 문서(`bolt-plan.md`)를 고치면 실행 순서도 바뀌나요?</summary>

AI-DLC 2.11.2에서는 바뀌지 않습니다. 엔진은 유닛 의존 문서(`unit-of-work-dependency.md`)의 `units` / `depends_on` 블록으로 실행 묶음을 계산합니다. 볼트 계획은 사람이 읽는 마일스톤 계획입니다. 실행 순서를 바꾸려면 유닛 단계의 의존 관계를 바꿔야 합니다.
</details>

<details class="answer" markdown="1">
<summary>이 실습에서는 왜 유닛이 병렬로 만들어지지 않았나요?</summary>

의존 그래프가 u1 ← u2 ← u3 ← u4 ← u5로 한 줄이라서, 각 묶음에 유닛이 하나씩만 들어갔기 때문입니다. 혼자 진행해 볼트 워크트리도 만들지 않았습니다.
</details>

<details class="answer" markdown="1">
<summary>Jujutsu의 「충돌도 커밋으로 남긴다」는 것이 에이전트에게 왜 중요한가요?</summary>

Git에서는 충돌이 나면 작업 폴더에서 진행하던 작업이 멈추고 사람이 충돌을 해결해야 다음 커밋을 할 수 있습니다. Jujutsu는 충돌 상태를 커밋으로 남기고 계속 진행하므로, 에이전트의 자동 실행이 충돌 하나로 멈추지 않습니다.
</details>

## 참고 자료

- Git Worktrees vs Jujutsu for AI Coding Agents: 2026 Decision Guide, <https://wavect.io/blog/git-worktrees-vs-jujutsu-ai-coding-agents/>
- agentic-jujutsu — npm, <https://www.npmjs.com/package/agentic-jujutsu>
- lakeFS vs DVC: Version Control Wants to Be a Filesystem, <https://sider.ai/blog/ai-tools/lakefs-vs-dvc-version-control-wants-to-be-a-filesystem>
- DVC Joins lakeFS: Your Questions Answered!, <https://dvc.org/blog/dvc-joins-lakefs-your-questions-answered/>
- Phases and Stages — AI-DLC Workflows, <https://awslabs.github.io/aidlc-workflows/guide/04-phases-and-stages/>
- [Bug]: bolt-plan.md is descriptive-only — awslabs/aidlc-workflows #985, <https://github.com/awslabs/aidlc-workflows/issues/985>
- AIDLC: AI Development Lifecycle & AI SDLC — driftless, <https://godriftless.ai/aidlc>
