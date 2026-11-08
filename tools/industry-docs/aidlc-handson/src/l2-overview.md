# 레벨 2 개요와 1단계 팀 규칙

> 레벨 1과 같은 요청을 `classic` 스코프로 다시 만들며, 단계마다 무엇을 정하고 어떤 문서가 생기는지 봅니다. 이 장은 전체 흐름과 첫 단계인 팀 규칙을 다룹니다.

!!! tip "이 장의 산출물 · GitHub"
    실습을 실제로 실행한 결과가 공개 저장소 [uengine-oss/tutorial-aidlc-handson](https://github.com/uengine-oss/tutorial-aidlc-handson)의 `level2-classic/` 폴더에 있습니다. 본문의 파일 이름을 눌러도 해당 파일이 열립니다.

    - [`inception/practices-discovery/`](https://github.com/uengine-oss/tutorial-aidlc-handson/tree/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/practices-discovery) — 팀 규칙 질문·발견한 규칙·근거
    - [`memory/team.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/memory/team.md) — 승인된 팀 규칙
    - [`aidlc-state.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/aidlc-state.md) — 진행 상태

## 전체 흐름

`classic`은 AI-DLC v2(2.11.2) 안의 스코프 이름입니다. v1처럼 스테이지마다 사람이 승인하는 방식이라는 뜻이며, 버전 1을 가리키지는 않습니다.

| 부분 | 단계 |
|---|---|
| 설계 (Inception) | 팀 규칙 → 요구사항 → 유저 스토리 → 화면 → 도메인 설계 → 유닛 나누기 → API 계약 → 볼트 계획 |
| 구현 (Construction, 유닛마다 반복) | 기능 설계 → 품질 요구(NFR) → 코드 계획 승인 → 테스트 먼저(Red → Green → Refactor) → 유닛 검증 |
| 마지막 | 전체 빌드와 테스트 |

레벨 1의 `poc`는 이 중 요구사항과 코드, 테스트 단계만 거쳤습니다. 그래서 유저 스토리·설계 문서·유닛 분해가 없었고, 아키텍처는 코드 생성 계획서 안에서 한꺼번에 정해졌습니다.

## 모든 단계는 같은 다섯 걸음

1. **질문지**: AI가 이 단계에서 정할 내용을 질문으로 만듭니다 (`<단계>-questions.md`)
2. **사람이 답**: 보기를 고르거나 직접 답을 씁니다. 답은 질문지의 `[Answer]:` 칸에 남습니다
3. **문서 작성**: AI가 답만을 근거로 문서를 작성합니다. 문장마다 `[Q3]` 같은 출처가 붙습니다
4. **검토**: 검토 에이전트가 따로 문서를 읽고 판정(READY / NOT-READY)과 지적 사항을 남깁니다 (`reviews/review-*.md`)
5. **승인**: 사람이 승인해야 다음 단계로 넘어갑니다. 고칠 점이 있으면 수정을 요청하고 같은 단계를 반복합니다.

## 단계마다 답하는 사람

| 단계 | 답하고 승인하는 사람 |
|---|---|
| 팀 규칙 | 팀 리드 · 아키텍트 |
| 요구사항 · 유저 스토리 | PO · 기획 |
| 화면 | 디자이너 |
| 도메인 설계 · 유닛 · API 계약 | 아키텍트 |
| 볼트 계획 · 코드 계획 · 검증 | 개발 리드 · 개발자 |

## 산출물이 쌓이는 곳

```text
aidlc/spaces/default/
  memory/team.md                    팀 규칙 · 다음 작업에도 이어짐
  intents/261105-voice-parking/     이번 작업
    inception/<단계>/               설계 단계 문서
    construction/<유닛>/<단계>/     유닛별 구현 문서
    audit/                          누가 언제 무엇을 승인했나
services/                           코드
```

## 1단계 팀 규칙 (Practices Discovery)

### 무엇을 · 왜

팀이 일하는 방식을 먼저 정합니다. 이후 모든 단계에서 이 규칙을 참고합니다(훅이 단계마다 다시 넣어 줍니다). 예를 들어 테스트 방식을 TDD로 정하면 구현 단계의 코드 계획이 테스트를 먼저 쓰는 순서로 바뀝니다. 답하고 승인하는 사람은 팀 리드·아키텍트입니다.

**정할 범주는 5가지입니다.** [`team.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/memory/team.md)의 섹션과 하나씩 대응합니다.

| 범주 | 정하는 것 | 값 |
|---|---|---|
| Way of Working | 브랜치와 병합 | 자유 서술 |
| Walking Skeleton | 전체 흐름을 잇는 최소 기능을 먼저 만들지 | 자유 서술 |
| Testing Posture | 테스트 방식과 순서 | `Methodology`는 `tdd · bdd · atdd · test-after · custom` 중 하나, `Ordering`은 한 문장 |
| Deployment | 어디에, 어떻게 배포할지 | 자유 서술 |
| Code Style | 포매터와 린터 | 자유 서술 |

AI가 상황에 맞춰 질문의 보기를 만듭니다. 새 프로젝트라면 [`org.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/memory/org.md)의 기본값을 제안하고, 기존 코드가 있다면 코드에서 확인한 내용을 바탕으로 초안을 쓰고 확인하지 못한 것만 묻습니다. 사람이 "반드시/절대"라고 분명히 말한 규칙은 [`discovered-rules.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/practices-discovery/discovered-rules.md)에 `ALWAYS …` / `NEVER …`로 따로 남습니다.

### 따라 하기

<ol class="steps" markdown="1">
<li markdown="1">**요청.** 새 폴더를 `aidlc config --harness claude`로 연결하고, 레벨 1과 같은 요청에서 스코프와 깊이만 바꿉니다.

```text
/aidlc classic --depth minimal 사용자가 음성 텍스트('강남역 근처 2시간 주차권 찾아줘')를 보내면 …(레벨 1과 같은 요청)
```
</li>
<li markdown="1">**질문 4개에 답하기.** 워킹 스켈레톤은 "아니오(서비스별로 완성)", 테스트 방식은 **TDD**, 브랜치와 배포는 "trunk(main), 로컬 실행 스크립트만, Docker 없음", 코드 스타일은 "Java는 IDE 기본"으로 답하고 승인합니다.
</li>
</ol>

### 산출물과 바뀐 점

**① 질문지** [`inception/practices-discovery/practices-discovery-questions.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/practices-discovery/practices-discovery-questions.md): 질문마다 보기와 답 칸이 있고, 사람이 고른 답이 그대로 남습니다.

```markdown
## Q2. [품질] 테스트는 어떤 방식으로 작성할까요?
A. 구현 후 테스트 작성, 커버리지 80% 유지 (제안)
B. TDD (테스트 먼저)
…
[Answer]: B
```

**② 팀 방식 초안** [`inception/practices-discovery/team-practices.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/practices-discovery/team-practices.md): 답만을 근거로 다섯 범주를 작성합니다. classic 스코프의 최소 기준(커버리지 80%, 병합 전 CI)은 낮출 수 없으므로 함께 포함됩니다.

```markdown
## Testing Posture
- **Methodology**: tdd
- **Ordering**: 각 계층마다 실패하는 테스트를 먼저 작성한 뒤 그 테스트를 통과시키는 구현을 작성한다.
- `classic` 범위의 하한을 유지한다: 80% 라인 커버리지.
```

**③ 승인하면 [`memory/team.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/memory/team.md)가 바뀝니다.** 승인 전에는 섹션 제목만 있는 빈 틀이었고, 승인 뒤에는 위 내용이 들어갑니다. 이 내용을 옮기는 작업은 정해진 도구가 수행합니다. LLM이 직접 옮기지는 않습니다.

**④ 이 규칙이 쓰이는 곳.** 구현 단계에서 u1의 코드 계획이 계층마다 Red(실패하는 테스트 먼저) → Green → Refactor 순서로 잡혔습니다([7. 구현](l2-build.html)).

## 확인 문제

<details class="answer" markdown="1">
<summary>팀 규칙에서 시험 방식을 TDD로 정하면 이후 무엇이 달라지나요?</summary>

[`memory/team.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/memory/team.md)의 Testing Posture에 `Methodology: tdd`와 진행 순서(Ordering)가 들어갑니다. 구현 단계에서는 이 항목을 바탕으로 코드 계획을 세웁니다. 각 계층에서 실패하는 시험을 먼저 쓰는 Red, 시험을 통과시키는 Green, 코드를 정리하는 Refactor 순서로 진행합니다. u1의 `code-generation-plan.md`에서 Step 3·4(데이터 모델), Step 9·10(비즈니스 로직)이 이 순서를 따릅니다.
</details>

<details class="answer" markdown="1">
<summary>팀 규칙의 범주는 몇 가지이고, 마음대로 늘릴 수 있나요?</summary>

범주는 Way of Working, Walking Skeleton, Testing Posture, Deployment, Code Style 다섯 가지로 정해져 있습니다. 시험 방식은 `tdd`, `bdd`, `atdd`, `test-after`, `custom` 가운데 하나를 고릅니다. 각 항목의 내용은 답변에 맞춰 작성됩니다. 범주에 속하지 않는 약속은 `ALWAYS`·`NEVER` 규칙으로 따로 남습니다. 이번 실행에서는 "NEVER Docker를 도입하지 않는다", "ALWAYS 로컬 실행 스크립트를 제공한다"가 [`project.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/memory/project.md)에 들어갔습니다.
</details>

<details class="answer" markdown="1">
<summary>검토 에이전트가 NOT-READY를 내면 다음 단계로 갈 수 없나요?</summary>

판정은 의견이며, 최종 결정은 사람이 합니다. 요구사항 단계에서는 PO가 지적된 위험을 받아들이고 승인했습니다. 빠진 내용은 유저 스토리 단계에서 다시 질문했습니다. 도메인 설계와 API 계약 단계에서는 아키텍트가 수정을 요청했습니다. 수정 후 재검토에서 READY를 받았습니다.
</details>
