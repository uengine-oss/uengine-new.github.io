# 6·7단계 유닛 나누기와 API 계약

> 컴포넌트를 따로 만들고 검증할 유닛으로 묶고 의존 그래프를 그린 뒤, 서비스 사이의 약속을 계약으로 정합니다. 계약은 첫 검토에서 NOT-READY였다가 고친 뒤 READY가 되었습니다.

## 6단계 유닛 나누기 (Units Generation)

### 무엇을 · 왜

| 정하는 것 | 뜻 |
|---|---|
| 유닛 | 독립적으로 설계·구현·검증할 수 있는 단위 (서비스, 화면, 스크립트) |
| 종류와 크기 | service · ui · packaging, S · M · L |
| 의존 그래프 | 만드는 순서의 근거 (DAG) |
| 스토리 맵 | 어느 스토리를 어느 유닛이 맡나 |

문서를 쓰기 전에 분할 계획을 먼저 보여 주고 승인을 받습니다. 답하고 승인하는 사람은 아키텍트입니다.

### 따라 하기

서비스를 3개로 묶도록 답했습니다(search = QueryParser+Recommendation, reservation = Reservation+Notification, payment = Payment). 모의 PG는 payment 안에 두고, 승인 결과는 자신의 웹훅을 HTTP로 비동기 호출해 전달하도록 했습니다. 화면은 Vite 프록시로 연결하도록 답했습니다. 분할 계획(유닛 5개)을 승인했습니다.

### 산출물과 바뀐 점

`inception/units-generation/`에 세 문서가 작성됩니다.

| 파일 | 내용 |
|---|---|
| `unit-of-work.md` | 유닛 5개(u1 search, u2 reservation, u3 payment, u4 web-ui, u5 local-run)와 담당 컴포넌트·스토리·종류·크기 |
| `unit-of-work-dependency.md` | 의존 DAG(mermaid: u2→u1, u3→u2, u4→u1·u2·u3, u5→전부, 순환 없음)와 연동 지점 표 |
| `unit-of-work-story-map.md` | 스토리 → 유닛. 예: US4.1은 u3(웹훅 수신), u2(확정과 푸시), u4(표시)가 1초를 나눠 사용합니다 |

## 7단계 API 계약 (Contract Design)

### 무엇을 · 왜

서비스 사이에서 누가 제공하고 누가 사용하는지, 요청·응답 형식(OpenAPI), 오류 형식, 제한 시간과 재시도, 세션·웹훅 서명 같은 보안 약속을 정합니다. 계약 테스트의 기준이 됩니다. 답하고 승인하는 사람은 아키텍트·개발 리드입니다.

### 따라 하기

세션 전달(`X-Session-Id` 헤더), 웹훅 위변조 방지(HMAC 서명 + 이벤트 ID), 호출 실패 시 재시도(2초 제한, 되돌릴 수 있는 호출만 재시도)를 제안대로 답했습니다. 첫 검토 판정이 NOT-READY여서 주요 문제 4건을 수정하도록 요청했습니다.

### 산출물과 바뀐 점

**① 첫 검토 NOT-READY → 재검토 READY** (`reviews/review-01.md` → `review-02.md`)

| 지적 | 내용 |
|---|---|
| R-01 | 이용 시간(`durationHours`)의 출처가 어느 계약에도 없음 |
| R-02 | 예약 생성이 시간 초과되면 재결제가 180초 동안 막힘(409) |
| R-03 | 브라우저 `EventSource`는 사용자 지정 헤더를 보낼 수 없음 |
| R-04 | 웹훅 반영 실패 시 응답 코드와 `eventId` 기록 시점이 없음 |

**② 최종 계약** `contract-summary.md`: 계약 6개(C1~C6)가 제공자·소비자·방식과 함께 표로 정리되고, 계약마다 OpenAPI 조각과 오류·제한 시간·재시도 표가 붙습니다.

```yaml
# C6 모의 PG 웹훅 (모의 PG → U3)
/api/payments/webhook:
  post:
    parameters:
      - name: X-Signature   # sha256=<hex>, 본문에 대한 HMAC-SHA256, 키는 환경 변수 PAYMENT_WEBHOOK_SECRET
```
