# 구현: 유닛 u1

> 유닛마다 기능 설계 → 품질 요구 → 코드 계획 승인 → 테스트 먼저 → 검증 명령 → 체크포인트를 반복합니다. 첫 유닛 u1(검색 서비스)의 산출물이 어떻게 이어지는지 봅니다. 나머지 유닛은 다음 장에서 이어집니다.

!!! tip "이 장의 산출물 · GitHub"
    실습을 실제로 실행한 결과가 공개 저장소 [uengine-oss/tutorial-aidlc-handson](https://github.com/uengine-oss/tutorial-aidlc-handson)의 `level2-classic/` 폴더에 있습니다. 본문의 파일 이름을 눌러도 해당 파일이 열립니다.

    - [`construction/u1-search-service/`](https://github.com/uengine-oss/tutorial-aidlc-handson/tree/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/construction/u1-search-service) — u1 기능 설계·NFR·코드 계획·결과
    - [`services/u1-search-service/`](https://github.com/uengine-oss/tutorial-aidlc-handson/tree/main/level2-classic/services/u1-search-service) — u1 코드와 시험

## 무엇을 · 왜

| 순서 | 하는 일 | 산출물 | 사람 |
|---|---|---|---|
| 기능 설계 | 엔티티·규칙·워크플로 | [`entities.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/construction/u1-search-service/functional-design/entities.md), [`rules.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/construction/u1-search-service/functional-design/rules.md), [`functional-spec.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/construction/u1-search-service/functional-design/functional-spec.md) | 따로 멈추지 않음 |
| 품질 요구(NFR) | 성능·보안·신뢰성과 측정 방법 | `nfr-requirements/*`, `nfr-design/*` | 따로 멈추지 않음 |
| 코드 계획 | 팀 규칙대로 Red → Green → Refactor 단계 | [`code-generation-plan.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/construction/u1-search-service/code-generation/code-generation-plan.md) | **승인** |
| 구현 | 테스트 먼저, 그다음 코드 | 코드, `traceability.json`, [`code-summary.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/construction/u1-search-service/code-generation/code-summary.md) | 명령 실행 허가 |
| 검증 | 사람이 승인한 명령으로 확인 | 상태 파일·감사 기록의 체크포인트 | 첫 유닛에서 **명령 승인** |

시작할 때 한 번, 누가 만들지(이 세션 혼자 / 여러 팀이 유닛을 나눠 맡기)와 진행 방식(일반 체크포인트 자동 / 단계마다 확인)을 정합니다. 이번에는 혼자, 자동 진행을 골랐습니다. 자동 진행이어도 코드 계획과 검증 명령은 사람이 승인하며, 실패하면 사람에게 확인을 요청합니다.

## 산출물과 바뀐 점

모든 파일은 [`construction/u1-search-service/`](https://github.com/uengine-oss/tutorial-aidlc-handson/tree/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/construction/u1-search-service) 아래에 있습니다.

**① 기능 명세** [`functional-design/functional-spec.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/construction/u1-search-service/functional-design/functional-spec.md): "강남역 근처 2시간" 요청의 점수 계산 예시가 테스트 기준값으로 들어갑니다.

| passId | 총액 | 거리 | 종합 | 순위 |
|---|---|---|---|---|
| gangnam-public-1 | 6,000 | 120 | 62 | BEST |
| yeoksam-bldg-1 | 7,000 | 80 | 60 | CANDIDATE |
| teheran-1 | 5,000 | 300 | 50 | CANDIDATE |

**② 품질 요구** [`nfr-requirements/performance-requirements.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/construction/u1-search-service/nfr-requirements/performance-requirements.md): 측정 방법이 함께 적힙니다. `NFR3.1`은 추천 요청을 100회 반복했을 때 응답 시간의 최댓값이 2초 이하여야 한다는 요구입니다.

**③ 코드 계획** [`code-generation/code-generation-plan.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/construction/u1-search-service/code-generation/code-generation-plan.md): 팀 규칙(TDD)대로 계층마다 실패하는 테스트를 먼저 작성합니다. 아래 스토리 추적 표는 인수 조건과 코드 계획을 연결합니다.

```markdown
- [ ] Step 9: 비즈니스 로직 - Red. 시험을 먼저 쓴다: QueryParser(…), 점수 계산(AC2.2.1의 92·72·0 입력 예시, 계산 예시 표의 62·60·50·40과 순위, …)
- [ ] Step 10: 비즈니스 로직 - Green. QueryParser, RecommendationService, ReasonFormatter, PassLookupService를 구현한다.
```

**④ 결과** [`code-generation/code-summary.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/construction/u1-search-service/code-generation/code-summary.md): 테스트 65개가 통과했고, 라인 커버리지는 95.8%입니다(313줄 중 300줄, 하한 80%). `traceability.json`에는 u1이 맡은 ID 44개(AC·NFR·BR)마다 구현·테스트 파일이 기록됩니다.

**⑤ 검증 명령** [`aidlc-state.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/aidlc-state.md): 사람이 승인한 `mvn -q verify`가 기록되고, 유닛마다 이 명령으로 체크포인트를 기록합니다(감사 기록 `CHECKPOINT_VERIFICATION_RECORDED`, 종료 코드 0).

## 다음 유닛과 마지막 빌드·테스트

남은 유닛 u2 → u5도 같은 순서로 이어지고, 모든 유닛이 끝나면 전체 빌드와 테스트로 한 번 확인합니다. 실패하면 정해진 순서로 처리합니다.

1. 단계 안에서 수정합니다(테스트 설정·스크립트·환경). 최대 2번 시도합니다.
2. 원인을 분류하고 영향을 추정합니다.
3. 자동 진행이면 원인 유닛의 코드 생성 단계부터 다시 실행합니다. 최대 3번 시도합니다.
4. 그래도 해결되지 않으면 멈추고 사람에게 후보와 영향을 제시하며 묻습니다

품질 목표(커버리지 하한 등)를 낮춰 통과시키는 것은 수정으로 인정하지 않습니다. u1 한 바퀴에 주간 사용량의 약 3%를 썼습니다. 이번 실행은 사용량 한도로 u2 직전에 한 번 멈췄고, 같은 폴더에서 `claude` → `/aidlc`로 다시 시작해 이어 갔습니다([u2·u3](l2-build-services.html), [u4·u5](l2-build-ui-run.html)).

## 확인 문제

<details class="answer" markdown="1">
<summary>"Continue automatically"를 고르면 사람은 아무것도 확인하지 않나요?</summary>

자동으로 진행되는 것은 일반 체크포인트 승인뿐입니다. 코드 계획 승인, 요약 확인, 검증 명령 선택, 실패 처리 때는 여전히 진행을 멈추고 사람에게 묻습니다. 이번 실행에서도 u1의 코드 계획과 `mvn -q verify`는 사람이 승인했습니다.
</details>

<details class="answer" markdown="1">
<summary>시험을 통과하지 못했을 때 커버리지 하한을 낮춰서 통과시켜도 되나요?</summary>

안 됩니다. classic 스코프의 80% 라인 커버리지 하한과 팀이 정한 품질 목표는 낮출 수 없습니다. 이를 낮춰서 통과시켜도 수정으로 인정하지 않습니다. 실패하면 먼저 현재 단계에서 고칩니다. 해결되지 않으면 원인이 된 유닛으로 돌아갑니다. 그래도 해결되지 않으면 사람에게 묻습니다.
</details>
