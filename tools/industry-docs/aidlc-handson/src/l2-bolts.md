# 8단계 볼트 계획

> 만들 순서와 "다 됐다"의 기준을 정합니다. 볼트마다 완료 기준이 유저 스토리의 인수 조건 번호와 계약 시험, 커버리지로 적혀, 앞에서 정한 스펙이 그대로 구현의 합격선이 됩니다.

!!! tip "이 장의 산출물 · GitHub"
    실습을 실제로 실행한 결과가 공개 저장소 [uengine-oss/tutorial-aidlc-handson](https://github.com/uengine-oss/tutorial-aidlc-handson)의 `level2-classic/` 폴더에 있습니다. 본문의 파일 이름을 눌러도 해당 파일이 열립니다.

    - [`inception/delivery-planning/`](https://github.com/uengine-oss/tutorial-aidlc-handson/tree/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/delivery-planning) — 볼트 계획·팀 배정·위험과 순서·외부 의존

## 무엇을 · 왜

| 정하는 것 | 뜻 |
|---|---|
| 볼트 | 유닛 하나 이상을 묶어 실제로 작동하는 결과물을 만드는 작업 단위(AI-DLC 2.11.2의 볼트 계획). 원문은 볼트를 유닛을 만드는 한 차례의 반복으로 정의하므로, 하나의 유닛이 여러 볼트를 거치기도 합니다([21장](tools-bolts.html)) |
| 순서 | 유닛 의존 그래프를 따릅니다 |
| 완료 기준 (DoD) | 인수 조건 번호 · 계약 테스트 · 커버리지 |
| 확인할 가설 | 가장 우려되는 사항을 먼저 확인 |
| 검증 명령 | 유닛마다 실행할 명령 (첫 볼트에서 사람이 승인) |

답하고 승인하는 사람은 개발 리드입니다. 결과는 [`inception/delivery-planning/bolt-plan.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/delivery-planning/bolt-plan.md)(같은 폴더에 [`team-allocation.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/delivery-planning/team-allocation.md), [`risk-and-sequencing-rationale.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/delivery-planning/risk-and-sequencing-rationale.md), [`external-dependency-map.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/delivery-planning/external-dependency-map.md))입니다.

## 따라 하기

볼트 크기는 유닛마다 하나(5개), 가장 우려되는 점은 "승인 후 1초 안 화면 표시"로 답하고 승인했습니다.

## 산출물과 바뀐 점

[`bolt-plan.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/delivery-planning/bolt-plan.md)에 볼트 5개의 순서와 이유, 볼트별 완료 기준·가설·보여 줄 결과가 적힙니다.

| 볼트 | 유닛 | 순서의 이유 |
|---|---|---|
| B1 | u1 search | 의존 대상이 없음 |
| B2 | u2 reservation | u1에 의존 |
| B3 | u3 payment | u2에 의존 |
| B4 | u4 web-ui | u1~u3에 의존 |
| B5 | u5 local-run | u1~u4에 의존 |

```markdown
## B2 u2-reservation-service
- Definition of Done: AC3.1.3, AC4.1.1(서버 측 시간 측정), AC4.1.4, AC4.1.5, AC4.2.1~AC4.2.4가 시험으로 통과하고,
  C3, C5 계약 시험과 `applyPaymentResult` 경합 시험이 통과한다. 80% 라인 커버리지.
- Confidence hypothesis: 결제 결과 반영과 180초 자동 취소가 같은 순간 겹쳐도 하나만 확정되고,
  승인 후 서버 안에서 SSE 푸시가 150ms 안에 나간다.
```

완료 기준의 `AC4.1.1`은 [3단계 유저 스토리](l2-stories.html)에서 PO와 정한 인수 조건과 같습니다. 아직 실행할 코드가 없으므로 검증 명령은 첫 볼트를 마칠 때 묻도록 했습니다.

## 확인 문제

<details class="answer" markdown="1">
<summary>볼트 순서는 어떻게 정해졌나요?</summary>

유닛 의존 그래프를 따릅니다. 다른 유닛에 의존하지 않는 u1 검색 서비스부터 시작합니다. 그다음은 u2 → u3 → u4 → u5 순서입니다. 팀 규칙에서 워킹 스켈레톤을 쓰지 않기로 했습니다. 따라서 작은 end-to-end 조각을 먼저 만들지 않고 서비스를 하나씩 완성합니다.
</details>

<details class="answer" markdown="1">
<summary>검증 명령은 왜 볼트 계획에서 정하지 않았나요?</summary>

이 시점에는 실행할 코드가 없기 때문입니다. 첫 유닛인 u1의 구현을 마친 뒤 에이전트가 `mvn -q verify`를 제안했고, 사람이 승인했습니다. 이 명령은 [`aidlc-state.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/aidlc-state.md)에 기록되어 이후 유닛의 체크포인트에서 사용됩니다.
</details>
