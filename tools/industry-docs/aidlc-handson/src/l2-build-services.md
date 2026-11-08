# 구현: 예약·결제 서비스 (u2·u3)

> u1과 같은 순서로 예약 서비스 u2와 결제 서비스 u3를 만듭니다. 상태 머신과 180초 마감, 서명된 웹훅의 중복 처리, 1초를 여러 구간으로 나눈 성능 목표가 어떤 산출물에 담기는지 살펴봅니다. 호스트 부하로 20ms 시험 결과가 불안정할 때 사람이 내린 결정과 그 결정이 기록되는 곳도 확인합니다.

!!! tip "이 장의 산출물 · GitHub"
    실습을 실제로 실행한 결과가 공개 저장소 [uengine-oss/tutorial-aidlc-handson](https://github.com/uengine-oss/tutorial-aidlc-handson)의 `level2-classic/` 폴더에 있습니다. 본문의 파일 이름을 눌러도 해당 파일이 열립니다.

    - [`construction/u2-reservation-service/`](https://github.com/uengine-oss/tutorial-aidlc-handson/tree/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/construction/u2-reservation-service) — u2 예약 서비스 문서
    - [`construction/u3-payment-service/`](https://github.com/uengine-oss/tutorial-aidlc-handson/tree/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/construction/u3-payment-service) — u3 결제 서비스 문서
    - [`services/u2-reservation-service/`](https://github.com/uengine-oss/tutorial-aidlc-handson/tree/main/level2-classic/services/u2-reservation-service) — u2 코드
    - [`services/u3-payment-service/`](https://github.com/uengine-oss/tutorial-aidlc-handson/tree/main/level2-classic/services/u3-payment-service) — u3 코드

## 무엇을 · 왜

| 유닛 | 하는 일 | 이 유닛에서 새로 정한 것 |
|---|---|---|
| u2 예약 서비스 (8082) | 예약 상태를 확정하고 바뀐 상태를 SSE로 화면에 보냅니다 | 상태 머신, 180초 자동 취소, 다른 유닛에 넘길 계약 변경 |
| u3 결제 서비스 (8083) | 모의 PG에 결제를 요청하고, 서명된 결과 웹훅을 예약에 한 번만 반영합니다 | HMAC 서명 검증, 같은 이벤트 중복 처리, 1초 예산의 구간 목표 |

순서는 u1과 같습니다. 기능 설계 → 품질 요구(NFR 요구·설계) → 코드 계획 **승인** → 테스트 먼저(Red → Green → Refactor) → 검증 명령 → 체크포인트입니다. 자동 진행을 선택했으므로 일반 체크포인트는 넘어갑니다. 코드 계획과 실패 처리 방법은 사람이 정합니다.

## 산출물과 바뀐 점

모든 파일은 [`construction/<유닛>/`](https://github.com/uengine-oss/tutorial-aidlc-handson/tree/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/construction) 아래에 있습니다.

**① u2 기능 명세** [`u2-reservation-service/functional-design/functional-spec.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/construction/u2-reservation-service/functional-design/functional-spec.md): 예약의 상태 머신부터 정합니다.

| 지금 상태 | 사건 | 다음 상태 |
|---|---|---|
| (없음) | 예약 생성 | PENDING_PAYMENT (결제 대기) |
| PENDING_PAYMENT | 승인 결과, 마감 전 | CONFIRMED |
| PENDING_PAYMENT | 실패 결과, 마감 전 | PAYMENT_FAILED |
| PENDING_PAYMENT | 마감 시각 도달 | CANCELLED |

마감은 결제 요청 시각 + 180초입니다. 승인과 마감이 같은 시각이면 취소가 우선합니다(BR2.3). 상태마다 화면에 보일 안내 문구("예약이 완료되었습니다" 등)도 이 문서에서 정합니다.

**② u2 결과** [`u2-reservation-service/code-generation/code-summary.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/construction/u2-reservation-service/code-generation/code-summary.md): 코드 계획에서는 시험 약 35개를 예상했지만, 실제로는 145개가 통과했습니다. 라인 커버리지는 96.6%(564줄 중 545줄)입니다. 실제로 180초를 기다리는 취소 시험은 `-Pslow` 프로필로 따로 돌렸습니다(189.5초). 마지막 「다른 유닛에 넘기는 사항」에는 구독 연결 상한(32, 넘으면 503), 같은 요청을 다시 보냈을 때의 응답처럼 u3·u4·u5가 알아야 할 내용이 남습니다.

**③ u3 규칙** [`u3-payment-service/functional-design/rules.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/construction/u3-payment-service/functional-design/rules.md): 규칙은 웹훅에 집중되어 있습니다.

```yaml
- id: BR3.1
  statement: "웹훅은 출처와 무관하게 서명을 검증하고, 맞지 않으면 거부하며 상태를 바꾸지 않고 기록한다."
- id: BR3.4
  statement: "이미 처리한 이벤트 ID가 다시 오면 예약 서비스를 다시 부르지 않고 중복으로 알린다."
```

같은 eventId는 한 번에 하나씩 처리하므로 예약은 정확히 한 번 확정됩니다.

**④ u3 품질 요구** [`u3-payment-service/nfr-requirements/performance-requirements.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/construction/u3-payment-service/nfr-requirements/performance-requirements.md): "결제 승인 뒤 1초 안에 화면에 완료를 표시한다"는 요구를 구간으로 나눕니다. 웹훅 처리 150ms, 예약 반영과 푸시 150ms, 프록시와 화면 200ms, 여유 500ms입니다. 중복 웹훅과 서명 거부는 20ms 안에 응답한다는 하위 목표(NFR1.2, NFR1.3)도 이 단계에서 AI가 정했습니다.

**⑤ u3 결과** [`u3-payment-service/code-generation/code-summary.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/construction/u3-payment-service/code-generation/code-summary.md): 시험 229개 가운데 성능 시험을 뺀 223개가 통과했습니다. 라인 커버리지는 94.3%입니다. 「미해결」 항목에는 부하로 성능 시험 두 개의 결과가 얼마나 달라졌는지(중앙값 0.1~1ms, 최댓값 25~200ms) 적힙니다. 목표를 낮추지 않았다는 사실과 사람이 내린 결정도 함께 기록됩니다.

## 사람이 내린 결정

이 머신에서 다른 작업도 함께 실행되어 부하 평균이 100~250까지 올랐습니다(코어 16개). 이 때문에 20ms 성능 시험이 가끔 실패했습니다. AI-DLC는 실패를 어떻게 처리할지 사람에게 물었습니다.

| 질문 | 보기 | 고른 것 |
|---|---|---|
| 중복 웹훅 20ms, 서명 거부 20ms 시험이 부하에서 간헐적으로 실패합니다. 어떻게 할까요? | 부하가 낮을 때 다시 / 20ms → 50ms로 완화 / 성능 시험을 별도 실행으로 분리 | **부하가 낮을 때 다시** |

목표를 낮추거나 시험을 빼면 당장은 통과하지만 기준이 약해집니다. 그래서 목표를 그대로 두고 부하가 낮을 때 다시 돌렸습니다. 감사 기록을 보면 u3 검증은 두 번 실패(종료 코드 1)한 뒤 세 번째에 통과(종료 코드 0)했고, 이때 체크포인트가 기록되었습니다(`CHECKPOINT_VERIFICATION_RECORDED`). 질문과 답도 `QUESTION_REPLIED`로 남습니다.

설계 검토도 바로 통과하지는 않습니다. u2의 NFR 설계는 첫 검토에서 `NOT-READY`를 받았고, 고친 뒤 `READY`가 되었습니다([`nfr-design/reviews/review-01.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/construction/u2-reservation-service/nfr-design/reviews/review-01.md), [`review-02.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/construction/u2-reservation-service/nfr-design/reviews/review-02.md)).

## 확인 문제

<details class="answer" markdown="1">
<summary>결제 승인이 마감 시각과 같은 순간에 도착하면 예약은 어떻게 되나요?</summary>

취소됩니다. u2 기능 명세의 BR2.3이 "마감 시각과 같은 시각이면 취소가 이긴다"고 정했습니다. 마감 뒤에 도착한 승인은 예약을 확정하지 못하고 거부됩니다(REJECTED).
</details>

<details class="answer" markdown="1">
<summary>성능 시험이 부하 때문에 실패할 때 목표를 50ms로 올리면 안 되나요?</summary>

이번 실행에서는 그렇게 하지 않았습니다. 20ms는 AI가 NFR 단계에서 정한 하위 목표이므로 사람이 바꿀 수는 있습니다. 하지만 시험을 통과시키려고 기준을 낮추면 품질 목표가 약해집니다. 사람은 목표를 그대로 두고 부하가 낮을 때 다시 돌리기로 했고, 그 결정은 결과 문서와 감사 기록에 남았습니다.
</details>

<details class="answer" markdown="1">
<summary>「다른 유닛에 넘기는 사항」은 왜 필요한가요?</summary>

유닛을 각각 따로 만들기 때문입니다. u2를 만들며 정한 응답(구독 상한을 넘으면 503, 같은 요청을 다시 보냈을 때의 상태 등)을 u3·u4·u5가 알아야 합니다. 다음 유닛의 기능 설계에서는 이 결과 문서를 근거로 삼습니다.
</details>
