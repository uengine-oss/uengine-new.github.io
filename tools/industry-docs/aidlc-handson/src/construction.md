# 코드 생성과 학습

> 개발 에이전트가 계획을 쓰고 Spring Boot 서비스 3개와 Vue 화면을 만든 뒤 시험을 돌립니다. 검토 에이전트의 지적을 보고 "결제 오류 응답은 HTTP 402로 통일"이라는 수정을 요청하면, 그 규칙이 프로젝트 기억(`project.md`)에 저장됩니다.

## 무엇을 · 왜

코드 생성(3.5)은 **계획 → 구현 → 시험 → 검토 → 승인** 순서로 진행합니다. poc 스코프는 계획 승인(plan approval)이 꺼져 있어, 계획을 작성한 뒤 한 줄로 알리고 바로 구현을 시작합니다. 원하면 언제든 계획을 같이 보자고 할 수 있습니다.

사람의 수정 요청은 이후 작업에도 반영됩니다. AI-DLC의 **학습 의식(learnings)**은 수정 요청을 규칙 후보로 보고, 사람이 동의하면 `aidlc/spaces/default/memory/project.md`의 `## Corrections`에 한 줄로 저장합니다. 다음 단계와 다음 작업은 물론 다른 팀원의 도구에서도 이 파일을 읽습니다.

## 따라 하기

<ol class="steps" markdown="1">
<li markdown="1">**계획.** 요구사항 승인 직후 개발 에이전트가 Java·Maven·Node 버전을 확인하고(명령을 실행하므로 허락을 묻습니다) 계획 `code-generation-plan.md`를 작성합니다. 이번 실행의 계획에서 정한 내용은 다음과 같습니다.

| 결정 | 내용 |
|---|---|
| 서비스 분해 | `recommendation-service`(8081), `payment-service`(8082), `reservation-service`(8083) — 요청대로 모듈이 여럿이라 마이크로서비스 |
| 화면 | Vue 3 + Vite(5173), 개발 서버 프록시로 각 서비스에 연결 |
| 저장소 | 서비스마다 메모리(`ConcurrentHashMap`). 프로토타입이라 DB 없음 |
| 흐름 | 추천 → 예약 `PENDING` → 결제 `PENDING` → 모의 PG가 비동기 웹훅 → 결제 서비스가 예약 확정 요청 → 예약 서비스가 SSE로 화면에 `CONFIRMED` |
| 180초 | 예약 서비스 스케줄러가 `CANCELLED`로 변경. 정확히 180초가 되어도 취소 |
| 점수 환산 | 가격·거리는 후보 중 최솟값 대비 비율, 이용 시간은 1시간 어긋날 때마다 50점 감점. 동점이면 가격이 낮은 쪽 |
| "근처" | 반경 1,000m. 후보가 3개 미만이면 있는 만큼 보여 주고 안내 |
| 시험 방식 | 구현 뒤 시험(test-after). poc의 기본값입니다 |

![계획을 쓰고 개발 에이전트에 넘기는 장면](img/cons-plan.webp)
</li>
<li markdown="1">**구현과 시험.** 개발 에이전트가 서비스마다 코드를 작성하고 `mvn test`를 실행합니다. 프런트에서는 `npm install`·`vitest`·`vite build`를 실행합니다. 마지막으로 서비스 셋을 실행하고 `curl`로 전체 흐름을 확인하는 스모크 시험을 진행합니다. acceptEdits 모드라 명령마다 허락을 묻습니다. 같은 명령을 계속 쓰면 「Yes, and don't ask again」을 골라도 됩니다.

![시험 명령 실행 허락](img/cons-perm.webp)

Java·Vue·JS 파일 61개와 시험 클래스 9개가 생성되었습니다. 수정 요청까지 반영한 뒤의 시험 수는 다음과 같습니다.

| 시험 | 수 | 결과 |
|---|---|---|
| recommendation-service (JUnit) | 18 | 통과 |
| reservation-service (JUnit) | 19 | 통과 |
| payment-service (JUnit) | 19 | 통과 |
| frontend (vitest) | 16 | 통과 |
</li>
<li markdown="1">**검토 에이전트.** 구현이 끝나면 설계 검토 에이전트(`aidlc-architecture-reviewer-agent`)가 계획·코드·시험을 다시 읽고 시험도 직접 실행합니다. 이번 판정은 READY였고, 6건을 짚었습니다. 가장 큰 지적(R-01, Major)은 결제 후 화면에 예약 완료를 표시하는 `App.vue`의 SSE·폴링 연결을 검증하지 않았다는 점입니다. 자동 시험도, 실제 브라우저 확인도 없었습니다. 이 확인은 4장에서 직접 합니다.

![검토 결과와 코드 생성 승인 게이트](img/cons-review.webp)
</li>
<li markdown="1">**수정 요청(Request Changes).** 게이트에서 Request Changes를 고르면 어떤 지적 사항을 수정할지 묻습니다. 여기서는 Type something을 골라 원본 가이드의 리뷰어 피드백을 그대로 넣었습니다.

```text
R-01은 제가 브라우저로 직접 확인할게요. 대신 결제 실패·오류 응답은 모두 HTTP 402 Payment Required와
표준 에러 객체(code, message)로 통일해 주세요. 앞으로 결제 관련 예외는 모두 이 규칙을 따라 주세요.
```

![수정 요청 입력](img/cons-fix.webp)
</li>
<li markdown="1">**규칙이 기억에 저장됨.** 개발 에이전트가 결제 서비스의 공통 예외 처리기를 고치고(코드 `PAYMENT_VALIDATION_FAILED`, `PAYMENT_NOT_FOUND`, `PAYMENT_ALREADY_APPROVED`, `RESERVATION_UNAVAILABLE`, `PAYMENT_INTERNAL_ERROR`), 프런트에서 결제 화면에 `code`·`message`를 표시하도록 바꿉니다. 그리고 "말씀하신 결제 오류 규칙은 프로젝트 메모리에 저장해 두었습니다"라고 알립니다. 요청에 "앞으로"라고 분명히 적었기 때문에 따로 "기억할까요?"를 묻지 않고 저장했습니다. 감사 기록에는 `RULE_LEARNED`(출처 `user_addition`)가 남습니다.

```markdown
## Corrections
- 결제 관련 실패·오류 응답은 모두 HTTP 402 Payment Required와 표준 에러 객체 { code, message }로
  통일하고, 앞으로 추가하는 결제 관련 예외도 같은 규칙을 따른다. (learned 2026-11-05)
```

개발 에이전트는 규칙을 적용하지 않은 부분도 설명했습니다. 모의 PG의 실패 통지 웹훅은 200을 유지합니다(402로 바꾸면 웹훅 멱등 처리가 깨지기 때문). 재검토에서는 "없는 경로도 402가 된다" 같은 사소한 문제 5건(R-07~R-11)을 짚었고, Approve를 선택했습니다.

![규칙을 프로젝트 기억에 저장했다는 알림](img/cons-rule.webp)
</li>
<li markdown="1">**빌드와 테스트(3.6).** 품질 에이전트가 백엔드 jar 3개와 프런트 번들을 다시 만들고 시험 72개(추천 18, 결제 19, 예약 19, 프런트 16)를 모두 실행합니다. 요구사항 13개가 시험과 연결되는지 확인하는 추적표(`cross-unit-traceability.md`)도 작성합니다. 이어서 서비스 셋을 실행하고, 승인 웹훅을 받은 뒤 확정 알림(SSE)이 도착하기까지 걸린 시간을 10번 측정했습니다. 10번 모두 1초 안(5~114ms)이었습니다. 이 단계에서도 브라우저에서 화면을 확인하는 일을 남은 작업으로 기록했습니다. Approve를 고르면 워크플로가 끝나고 상태줄이 `COMPLETE`로 바뀝니다.

| 확인 | 기대 | 실제 | 판정 |
|---|---|---|---|
| NFR1 | 승인 웹훅 수신부터 1초 이내 | 서버 → 클라이언트 5~114ms, 10회 | 충족(화면 표시는 4장에서 확인) |
| NFR2 | 180초 대기, 넘으면 자동 취소 | 179초 대기, 180초 정확히 취소, 취소 뒤 승인 무시 | 충족 |
| 시험 묶음 | 기존 시험 모두 통과 | 72개 통과, 실패 0 | 충족 |

![빌드와 테스트 결과](img/cons-build.webp)
</li>
</ol>

## 센서는 무엇을 봤나

가이드는 코드를 쓰는 즉시 `tsc`·Jest 같은 센서가 실행되고 실패하면 스스로 고친다고 설명합니다. 실제 AI-DLC 2.11.2의 코드 센서(`linter`, `type-check`)는 TypeScript·JavaScript 파일을 대상으로 하고, 이번 실행에서는 문서 센서 4종(`claim-sources`, `required-sections`, `traceability`, `upstream-coverage`)만 실행되었습니다. 모두 통과했습니다. Java 코드의 빌드와 시험은 개발 에이전트와 검토 에이전트가 `mvn test`로 직접 실행했습니다. Java 프로젝트에서 센서로 오류를 차단하려면 `.claude/sensors/`에 센서를 더해야 합니다.

## 확인 문제

<details class="answer" markdown="1">
<summary>수정 요청 뒤 규칙이 저장되지 않게 하려면 어떻게 하나요?</summary>

"다음에도 기억할까요?"라는 질문이 나오면 아니라고 답합니다. 처음부터 학습 의식을 끄려면 요청에 `--learnings off`를 붙입니다. 이미 `project.md`에 있는 규칙은 계속 읽힙니다.
</details>

<details class="answer" markdown="1">
<summary>계획을 구현 전에 보고 싶다면요?</summary>

poc·express는 계획 승인이 꺼져 있습니다. 계획이 작성될 때 "계획을 보여 줘"라고 하거나, 처음부터 `/aidlc --plan-approval on`으로 켭니다. classic·workshop은 기본으로 계획 승인을 묻습니다.
</details>
