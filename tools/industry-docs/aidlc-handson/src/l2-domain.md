# 5단계 도메인 설계

> 책임과 데이터 소유로 컴포넌트를 나누고, 중요한 결정을 ADR로 기록합니다. 첫 검토에서 나온 순환 의존을 아키텍트가 수정 요청으로 고치고, 결정 기록이 어떻게 바뀌었는지 봅니다.

!!! tip "이 장의 산출물 · GitHub"
    실습을 실제로 실행한 결과가 공개 저장소 [uengine-oss/tutorial-aidlc-handson](https://github.com/uengine-oss/tutorial-aidlc-handson)의 `level2-classic/` 폴더에 있습니다. 본문의 파일 이름을 눌러도 해당 파일이 열립니다.

    - [`inception/domain-design/`](https://github.com/uengine-oss/tutorial-aidlc-handson/tree/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/domain-design) — 컴포넌트·결정(ADR)·검토

## 무엇을 · 왜

| 정하는 것 | 뜻 |
|---|---|
| 컴포넌트 | 변경 이유에 따라 나눈 구성 요소 |
| 데이터 소유 | 어떤 데이터를 누가 갖나 |
| 의존 방향 | 누가 누구를 부르나 |
| ADR | 결정(Decision)과 근거(Context), 결과(Consequences), 채택하지 않은 대안(Alternatives Rejected) |

단계 규칙에서 "결정마다 대안을 2개 이상 적을 것"을 요구합니다. 답하고 승인하는 사람은 아키텍트입니다. 결과 문서는 [`inception/domain-design/components.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/domain-design/components.md), [`decisions.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/domain-design/decisions.md)입니다.

## 따라 하기

<ol class="steps" markdown="1">
<li markdown="1">**컴포넌트 개수 정하기.** 에이전트가 5개 안(QueryParser, Recommendation, Reservation, Payment, Notification)과 3개 안의 장단점을 제시했고, 5개 안을 골랐습니다.
</li>
<li markdown="1">**첫 검토와 수정 요청.** 주요 문제 2건이 나왔습니다. 아키텍트는 승인 대신 **Request Changes**를 고르고 두 문제를 함께 해결하는 안을 선택했습니다.
</li>
<li markdown="1">**재검토 후 승인.** 두 문제가 해결되었음을 확인하고 승인했습니다.
</li>
</ol>

## 산출물과 바뀐 점

**① 컴포넌트와 데이터 소유** [`components.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/domain-design/components.md): 컴포넌트 구조도(mermaid)와 데이터 소유 표가 있습니다.

| Entity | Owning Component |
|---|---|
| ParkingLot · ParkingPass | Recommendation |
| Reservation | Reservation |
| Payment · WebhookEvent | Payment |
| Subscription | Notification |

**② 첫 검토** [`reviews/review-01.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/domain-design/reviews/review-01.md): 알림이 예약을 조회하면 예약 → 알림 이벤트와 맞물려 순환 의존이 생깁니다(R-01). 예약 상태를 확정하는 주체도 ADR마다 다릅니다(R-02).

**③ 고친 결정** [`decisions.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/domain-design/decisions.md): 상태 확정은 Reservation에서만 원자 연산으로 처리하도록 바뀌었습니다(ADR-002). 호출 방향은 Payment → Reservation → Notification으로 통일되었습니다(ADR-003).

```markdown
## ADR-003: 호출 방향을 Payment에서 Reservation으로 둔다
- Decision: Payment가 Reservation을 호출한다. Reservation은 Payment를 호출하지 않는다. Reservation은 Notification에
  상태 스냅샷을 이벤트로 밀어 넣고 Notification은 Reservation을 호출하지 않는다.
- Alternatives Rejected: Reservation이 Payment를 호출하는 방식은 결과 반영에서 순환이 생겨 선택하지 않았다.
```

**④ 재검토** [`reviews/review-02.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/intents/261105-voice-parking/inception/domain-design/reviews/review-02.md): R-01, R-02 해결로 기록되었습니다.

**⑤ 다음에 쓰이는 곳.** 이 컴포넌트와 의존 방향이 다음 단계에서 유닛(서비스)을 묶는 기준이 됩니다.

## 확인 문제

<details class="answer" markdown="1">
<summary>첫 검토에서 지적된 순환 의존은 왜 문제인가요?</summary>

알림이 예약을 조회하고 예약이 알림에 이벤트를 보내면 두 컴포넌트가 서로를 호출하는 고리가 생깁니다. 그러면 각각 시험하거나 배포하기 어렵습니다. 한쪽을 바꾸면 다른 쪽에 문제가 생기기 쉽습니다. 고친 뒤에는 호출이 Payment → Reservation → Notification 한 방향으로만 흐릅니다(ADR-003).
</details>

<details class="answer" markdown="1">
<summary>ADR에 채택하지 않은 대안까지 적는 이유는 무엇인가요?</summary>

나중에 같은 논의를 되풀이하지 않기 위해서입니다. 조건이 바뀌었을 때 무엇을 다시 검토해야 하는지도 알 수 있습니다. 이 프로젝트의 단계 규칙([`phases/inception.md`](https://github.com/uengine-oss/tutorial-aidlc-handson/blob/main/level2-classic/aidlc/spaces/default/memory/phases/inception.md))도 ADR마다 Context, Decision, Consequences, Alternatives Rejected를 적도록 요구합니다. 대안도 2개 이상 검토해야 합니다.
</details>
