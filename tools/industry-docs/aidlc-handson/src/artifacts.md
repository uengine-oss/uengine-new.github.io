# 산출물 지도

> 레벨 2(`classic`)에서 실제로 만들어진 산출물 14가지를 하나씩 봅니다. 산출물마다 무엇이 들어 있는지(실제 발췌), 누가 쓰고 누가 승인하는지, 다음 단계에서 어떻게 쓰이는지, 스펙킷의 무엇에 해당하는지를 정리합니다.

## 산출물이 이어지는 실

산출물은 번호(ID)로 서로 연결됩니다. 이번 실행에서 "승인 후 1초 안에 예약 완료 표시"라는 요구 하나가 어떻게 이어졌는지 따라가면 다음과 같습니다.

| 단계 | 산출물 | 이어지는 ID |
|---|---|---|
| 요구사항 | `requirements.md` | `FR6` 예약 완료 즉시 표시, `NFR1` 웹훅 수신부터 1초 |
| 유저 스토리 | `stories.md` | `US4.1` → 인수 조건 `AC4.1.1` (Given/When/Then) |
| 유닛 | `unit-of-work-story-map.md` | `US4.1` → u3 payment(웹훅 수신), u2 reservation(확정과 푸시), u4 web-ui(표시)가 1초를 나눠 씀 |
| 계약 | `contract-summary.md` | `C3` 예약 조회와 실시간 알림(SSE) |
| 볼트 | `bolt-plan.md` | B2 완료 기준에 `AC4.1.1`(서버 쪽), B4 완료 기준에 `AC4.1.1`(화면까지 100건 최대 1초) |
| 코드 계획 | `code-generation-plan.md` | 스토리 추적 표: AC → 계획 단계(Red/Green) |
| 추적표 | `traceability.json` | AC·NFR·BR → 구현 파일 + 시험 파일, 상태 OK |

모든 산출물은 실습 폴더의 `aidlc/spaces/default/intents/261105-voice-parking/` 아래에 쌓입니다. 팀 규칙만 작업 바깥(`aidlc/spaces/default/memory/`)에 있어 다음 작업에도 이어집니다.

## 1. 팀 규칙 · `memory/team.md`

| 항목 | 내용 |
|---|---|
| 스펙킷 | constitution |
| 쓰는 쪽 · 승인 | pipeline-deploy 에이전트가 초안, 품질·개발·보안 에이전트가 따로 점검 → **팀 리드·아키텍트** 승인 시 승격 |
| 다음에 쓰임 | 모든 스테이지. 훅(`deliver-stage-rules`)이 도구를 부를 때마다 이 파일과 단계 규칙을 다시 넣음 |

이번에 확정된 내용은 TDD(테스트 먼저), 커버리지 80%, trunk 기반, 로컬 실행 스크립트(Docker 없음)입니다. 커버리지 하한은 classic 스코프가 정한 최소 기준이라 낮출 수 없었습니다. 같은 폴더의 `org.md`(프레임워크 기본값), `project.md`(이 프로젝트 규칙, 학습), `phases/*.md`(단계 규칙)와 함께 계층을 이루며 읽힙니다.

## 2. 요구사항 · `inception/requirements-analysis/requirements.md`

| 항목 | 내용 |
|---|---|
| 스펙킷 | specify (`spec.md`) |
| 쓰는 쪽 · 승인 | product 에이전트 → **PO·기획** |
| 다음에 쓰임 | 유저 스토리, 도메인 설계, NFR, 시험 기준 |

맨 위 `## Sources`에 출처(처음 요청 `[desc]`, 질문 답 `[Q3]` 등)가 있고, 기능 요구사항 FR1~FR8과 비기능 요구사항이 합격 기준과 함께 적힙니다. 레벨 1과 달리 처음부터 PO가 웹훅·1초·180초를 직접 적었고, 후속 질문으로 시간 적합도 점수, SSE, 180초를 세는 시점이 정해졌습니다.

## 3. 유저 스토리 · `inception/user-stories/stories.md`

| 항목 | 내용 |
|---|---|
| 스펙킷 | specify (user scenarios) |
| 쓰는 쪽 · 승인 | product 에이전트 → **PO·기획** |
| 다음에 쓰임 | 유닛 스토리 맵, 볼트 완료 기준, 시험 |

스토리 9개가 사용자 흐름 순서로 나뉘고, 인수 조건이 단계 규칙대로 Given/When/Then 형식으로 작성되며 `AC<그룹>.<순번>.<조건>` 번호가 붙습니다.

```markdown
- AC4.1.1 Given 예약이 결제 대기이고 화면이 서버 푸시(SSE)로 연결돼 있을 때, When 모의 PG의 승인 웹훅이 오면,
  Then 웹훅 수신 시각부터 1초 이내에 화면에 예약 완료(주차장, 이용 시간, 결제 금액)가 표시된다.
- AC4.1.2 Given 같은 승인 웹훅이 3번 도착해도, When 처리하면, Then 예약 확정은 정확히 1회이다.
```

## 4. 화면 · `inception/refined-mockups/mockups.md`

| 항목 | 내용 |
|---|---|
| 스펙킷 | specify 보조 (화면) |
| 쓰는 쪽 · 승인 | design 에이전트 → **디자이너·PO** |
| 다음에 쓰임 | u4 화면 유닛의 설계와 시험(S1~S8 동작이 완료 기준) |

화면 상태 8가지(S1 입력 대기, S2 해석 오류, S3 추천 결과, S4 후보 없음, S5 결제 승인 대기, S6 예약 완료, S7 결제 실패, S8 자동 취소)가 스토리 번호와 함께 정리되고, 상호작용 규칙(`interaction-spec.md`)과 접근성 체크리스트가 따로 생깁니다.

## 5. 도메인 설계 · `inception/domain-design/components.md`, `decisions.md`

| 항목 | 내용 |
|---|---|
| 스펙킷 | plan (아키텍처) |
| 쓰는 쪽 · 승인 | architect 에이전트 → **아키텍트** |
| 다음에 쓰임 | 유닛 분해, 계약 설계 |

`components.md`에는 컴포넌트 다섯 개와 그림, 각 엔티티를 소유하는 컴포넌트가 정리되어 있습니다.

| Entity | Owning Component | Identifier |
|---|---|---|
| ParkingLot · ParkingPass | Recommendation | lotId · passId |
| Reservation | Reservation | reservationId |
| Payment · WebhookEvent | Payment | paymentId · eventId |
| Subscription | Notification | subscriptionId |

`decisions.md`에는 ADR 5개가 Context / Decision / Consequences / Alternatives Rejected 형식으로 정리되어 있습니다. ADR-002(상태 확정은 Reservation 한 곳)와 ADR-003(호출은 Payment → Reservation → Notification 한 방향)은 검토에서 순환 의존이 지적되어 아키텍트가 수정을 요청한 결정입니다.

## 6. 유닛 · `inception/units-generation/unit-of-work*.md`

| 항목 | 내용 |
|---|---|
| 스펙킷 | 없음 (AI-DLC 고유) |
| 쓰는 쪽 · 승인 | architect 에이전트 → **아키텍트** (분할 계획도 먼저 승인) |
| 다음에 쓰임 | 볼트 계획, Construction 순서, 팀 분담 |

`unit-of-work.md`에는 유닛 5개(search, reservation, payment 서비스, web-ui, local-run)가 각각 맡는 컴포넌트·스토리·종류·크기를 적습니다. `unit-of-work-dependency.md`에는 의존 DAG(mermaid)와 연동 지점 표(누가 누구를 어떤 방식으로 부르는지)를 적습니다. `unit-of-work-story-map.md`에는 스토리 → 유닛 연결을 적습니다.

## 7. API 계약 · `inception/contract-design/contract-summary.md`

| 항목 | 내용 |
|---|---|
| 스펙킷 | plan (`contracts/`) |
| 쓰는 쪽 · 승인 | architect 에이전트 → **아키텍트·개발 리드** |
| 다음에 쓰임 | 계약 시험, 유닛별 API 구현 |

계약 6개(C1~C6)가 제공자·소비자·방식과 함께 표로 정리되고, 계약마다 OpenAPI 조각이 붙습니다. 공통 규칙(세션 헤더, 오류 형식)과 오류·제한 시간·재시도 표도 있습니다.

```yaml
# C6 모의 PG 웹훅 (모의 PG → U3)
/api/payments/webhook:
  post:
    parameters:
      - name: X-Signature   # sha256=<hex>. 본문에 대한 HMAC-SHA256, 키는 환경 변수 PAYMENT_WEBHOOK_SECRET
```

초안의 검토 결과는 NOT-READY였습니다(이용 시간 값의 출처 없음, 예약 생성 시간 초과 시 재결제 180초 막힘, 브라우저 `EventSource`는 헤더를 못 보냄, 웹훅 반영 실패 응답 없음). 고친 뒤 승인했습니다.

## 8. 볼트 계획 · `inception/delivery-planning/bolt-plan.md`

| 항목 | 내용 |
|---|---|
| 스펙킷 | tasks (묶음과 완료 기준) |
| 쓰는 쪽 · 승인 | delivery 에이전트 → **개발 리드** |
| 다음에 쓰임 | Construction 순서, 볼트별 완료 판정, 검증 명령 |

볼트 5개(B1~B5)의 순서와 이유, 볼트마다 완료 기준(Definition of Done)·확인할 가설·보여 줄 결과가 있습니다. 핵심은 완료 기준을 인수 조건 ID와 계약 시험, 커버리지로 명시한다는 점입니다. 같은 폴더의 `team-allocation.md`, `risk-and-sequencing-rationale.md`, `external-dependency-map.md`도 이 스테이지 산출물입니다.

## 9. 기능 설계 (유닛마다) · `construction/<유닛>/functional-design/`

| 항목 | 내용 |
|---|---|
| 스펙킷 | plan (`data-model.md`) |
| 쓰는 쪽 · 승인 | architect 에이전트 → 코드 계획과 함께 **개발 리드** |
| 다음에 쓰임 | 코드 생성 계획, 시험 기준값 |

`entities.md`는 엔티티의 속성, 제약, 관계를 YAML로 적은 데이터 모델입니다. `rules.md`에는 비즈니스 규칙(BR)을, `functional-spec.md`에는 워크플로와 오류 응답을 적습니다. u1의 기능 명세에는 시험 기준값이 될 계산 예시가 들어갔습니다.

| passId | 총액 | 거리 | 가격 점수 | 거리 점수 | 시간 적합도 | 종합 | 순위 |
|---|---|---|---|---|---|---|---|
| gangnam-public-1 | 6,000 | 120 | 29.4 | 89.2 | 75.0 | 62 | BEST |
| yeoksam-bldg-1 | 7,000 | 80 | 0.0 | 100.0 | 100.0 | 60 | CANDIDATE |
| teheran-1 | 5,000 | 300 | 58.8 | 40.5 | 50.0 | 50 | CANDIDATE |

## 10. NFR 요구사항·설계 (유닛마다) · `construction/<유닛>/nfr-requirements/`, `nfr-design/`

| 항목 | 내용 |
|---|---|
| 스펙킷 | plan (`research.md`, 기술 선택) |
| 쓰는 쪽 · 승인 | architect 에이전트 → **개발 리드** |
| 다음에 쓰임 | 성능·보안 시험, 기술 스택 |

성능·보안·신뢰성·확장성·관측 요구사항을 측정 방법과 함께 유닛별로 정리하고(예: `NFR3.1` 추천 요청 2초 이내, 100회 반복 최댓값으로 측정), 설계 문서와 `tech-stack-decisions.md`가 뒤따릅니다.

## 11. 코드 생성 계획 (유닛마다) · `construction/<유닛>/code-generation/code-generation-plan.md`

| 항목 | 내용 |
|---|---|
| 스펙킷 | `tasks.md` |
| 쓰는 쪽 · 승인 | developer 에이전트 → **개발자 (Plan Approval)** |
| 다음에 쓰임 | 구현과 시험 |

팀 규칙이 TDD라서 계층마다 Red → Green → Refactor 순서로 계획했습니다(데이터 모델, 저장소, 비즈니스 로직, API). 비즈니스 로직의 Red 단계는 `AC2.2.1`의 숫자 예시부터 시험으로 작성합니다. 아래 `## 스토리 추적` 표가 인수 조건과 계획 단계를 연결하고, 시험 실행 방법은 `unit-test-instructions.md`에 따로 있습니다.

## 12. 추적표 · `construction/<유닛>/code-generation/traceability.json`

| 항목 | 내용 |
|---|---|
| 스펙킷 | analyze (일관성 확인) |
| 쓰는 쪽 · 승인 | developer 에이전트, `traceability` 센서가 검사 |
| 다음에 쓰임 | Build and Test의 요구사항 대비 검증표 |

u1이 맡은 ID 44개(AC, NFR, BR)마다 구현 파일과 시험 파일, 상태가 기록됩니다.

```json
{ "id": "AC2.2.1", "status": "OK", "target": "…/service/Ratio.java, …/service/RecommendationServiceTest.java" }
{ "id": "NFR3.1", "status": "OK", "target": "…/PerformanceTest.java" }
```

## 13. 코드 요약 · `construction/<유닛>/code-generation/code-summary.md`

| 항목 | 내용 |
|---|---|
| 스펙킷 | implement (결과 보고) |
| 쓰는 쪽 · 승인 | developer 에이전트 → 검증 명령(`mvn -q verify`) 통과로 유닛 체크포인트 |
| 다음에 쓰임 | 다음 유닛, Build and Test |

만든 파일, 실행 방법, 핵심 구현 결정, 시험 결과, 실행하지 않은 시험, 계획과 다른 점, 후속 작업을 적습니다. u1은 시험 65개 통과, 라인 커버리지 95.8%(313줄 중 300줄)였습니다.

## 14. 상태와 감사 기록 · `aidlc-state.md`, `audit/*.md`

| 항목 | 내용 |
|---|---|
| 스펙킷 | 없음 (AI-DLC 고유) |
| 쓰는 쪽 · 승인 | AI-DLC 엔진과 훅이 자동 기록 |
| 다음에 쓰임 | 세션 재개, 감사, git으로 팀 공유 |

상태 파일에는 스코프·깊이·실행할 스테이지, 사람이 승인한 검증 명령(`mvn -q verify`), 진행 방식(`autonomous`)이 남습니다. 감사 기록에는 질문과 답, 승인(`GATE_APPROVED`), 수정 요청(`GATE_REJECTED`), 센서 실행, 유닛 검증(`CHECKPOINT_VERIFICATION_RECORDED`, 종료 코드 0) 같은 이벤트가 시각과 함께 쌓입니다.

## 확인 문제

<details class="answer" markdown="1">
<summary>스펙킷의 plan.md 하나에 해당하는 내용이 AI-DLC에서는 왜 여러 파일로 나뉘나요?</summary>

아키텍처(도메인 설계), 분할 단위(유닛), 서비스 사이 약속(계약), 유닛 안의 데이터와 규칙(기능 설계), 품질 특성(NFR)을 각기 다른 시점에 다른 사람이 승인하기 때문입니다. 유닛 안의 설계는 유닛마다 따로 생깁니다.
</details>

<details class="answer" markdown="1">
<summary>시험이 스펙을 기준으로 쓰였는지 어떻게 확인하나요?</summary>

볼트 계획의 완료 기준에는 인수 조건 ID가 적혀 있습니다. 코드 계획의 스토리 추적 표는 그 ID와 Red 단계를 연결하고, `traceability.json`은 ID마다 시험 파일을 기록합니다. 세 파일에서 같은 ID(예: `AC2.2.1`)를 따라가면 됩니다.
</details>
