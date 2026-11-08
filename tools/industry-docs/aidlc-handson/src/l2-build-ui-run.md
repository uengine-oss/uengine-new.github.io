# 구현: 화면·실행 스크립트 (u4·u5)

> 화면 u4(Vue 3)와 실행 스크립트 u5를 만듭니다. 검토 에이전트가 화면 설계를 한 번 반려한 기록, 화면 시험까지 돌도록 사람이 승인해 바꾼 검증 명령, Docker 없이 네 서비스를 띄우는 스크립트의 비밀 값 처리를 차례로 봅니다.

## 무엇을 · 왜

| 유닛 | 하는 일 | 이 유닛에서 새로 정한 것 |
|---|---|---|
| u4 화면 (5173) | 입력 → 추천 카드 → 결제 → 예약 상태를 한 페이지에 표시하고 SSE로 갱신합니다 | 컴포넌트 7개와 상태를 한 곳에 두는 구조, Vite 프록시 규칙, 시연 설정 |
| u5 실행 스크립트 | Docker 없이 u1 → u2 → u3 → u4 순서로 띄우고 Ctrl-C로 정리합니다 | 비밀 값 생성과 전달, 준비 확인, 연동 스모크, 전체 검증 |

u5는 패키징 유닛이므로 기능 설계 단계가 없습니다. 보안·실행 설계가 그 역할을 맡습니다.

## 산출물과 바뀐 점

**① u4 컴포넌트** `u4-web-ui/functional-design/frontend-components.md`: 라우터나 상태 관리 라이브러리는 쓰지 않습니다. composable 하나(`useApp`)가 상태를 관리하고, 컴포넌트는 props와 이벤트로만 소통합니다.

```
App.vue
├─ QueryInput          입력창과 전송
├─ ErrorNotice         오류 안내
├─ ReservationStatus   결제 대기·완료·실패·취소
├─ RecommendationList  추천 카드 (최적 1 + 후보 최대 2)
├─ EmptyNotice         후보 없음
└─ ScenarioPanel       접힌 시연 설정 (모의 결제 결과, 지연 초)
```

**② u4 설계 검토** `u4-web-ui/functional-design/reviews/`: 첫 검토(`review-01.md`) 결과는 `NOT-READY`였으며, Major 지적은 6건이었습니다. 예를 들어 R-02는 다른 주차권으로 다시 결제하면 새 예약의 version이 처음부터 시작하는데, 화면이 하나의 version 기준만 쓰면 새 예약의 갱신을 모두 버린다는 지적입니다. 문서를 고친 뒤 두 번째 검토(`review-02.md`)에서는 "이전 Major 6건은 모두 고쳐졌고"라는 평가와 함께 `READY`를 받았습니다. 남은 지적은 Status 열에 `New`·`Unresolved`로 표시됩니다.

**③ 검증 명령** `aidlc-state.md`: u4를 만든 뒤 AI가 검증 명령 변경을 제안했습니다. 기존 `mvn -q verify`는 Java 서비스만 시험하므로 화면 시험도 실행하자는 제안입니다. 사람이 승인한 뒤 다음 명령이 기록되었습니다. 이후 모든 유닛의 체크포인트는 이 명령으로 기록됩니다.

```
- **Construction Verification Command**: mvn -q verify && npm --prefix services/u4-web-ui run verify
```

**④ u4 결과** `u4-web-ui/code-generation/code-summary.md`: 시험 374개(단위 351, 시간 4, 프록시 19)가 통과했습니다. 라인 커버리지는 98.29%입니다. 경과 시간 표시(틱) 시험이 부하가 높을 때 가끔 실패한다는 사실도 「미해결」로 적혀 있습니다.

**⑤ u5 보안·실행 설계** `u5-local-run/nfr-design/security-design.md`

| 설계 | 방식 |
|---|---|
| 비밀 값 | 웹훅 서명용 값은 실행마다 무작위 64자 이상으로 만들고, u3에만 환경 변수로 넘깁니다. 화면·로그·프로세스 인자에 쓰지 않고 파일에도 저장하지 않습니다 |
| 환경 구성 | 서비스마다 환경을 비운 뒤 필요한 변수만 전달합니다 |
| 준비 확인 | u1~u3은 `/actuator/health`가 UP인지 확인합니다. u4는 프록시를 거쳐 u1에 연결되는지(빈 요청에 400)로 판정합니다 |

**⑥ u5 결과** `u5-local-run/code-generation/code-summary.md`: 스크립트 세 개를 만듭니다. `run-local.sh`(네 서비스 기동과 정리), `smoke-local.sh`(화면 프록시를 거쳐 추천 → 결제 → 예약 완료 확인), `verify-all.sh`(전체 검증)입니다. bash 시험 79개(확인 439건)가 통과했습니다. 줄 커버리지는 100%입니다.

## 사람이 내린 결정

| 언제 | 질문 | 고른 것 |
|---|---|---|
| u4 구현 뒤 | 화면 시험까지 확인하도록 검증 명령을 바꿀까요? | **Approve** |
| u4 검증 | 부하가 오르내려 시간 시험(u2 2초 대기, u3 20ms, u4 틱 5ms) 결과가 계속 불안정합니다. 어떻게 할까요? | **계속 재시도** (시간 시험을 게이트에서 분리 / 호스트 한계로 기록하고 승인은 고르지 않음) |

"호스트 한계로 기록하고 승인"을 고르면 검증 명령이 실제로 통과하지 않아도 유닛이 승인됩니다. 그래서 기준을 그대로 두고 다시 시도했습니다. 감사 기록을 보면 u4 검증은 세 번 실패한 뒤 네 번째에 통과했고, u5는 첫 검증에서 통과했습니다.

## 확인 문제

<details class="answer" markdown="1">
<summary>검토 결과가 READY이면 지적이 하나도 없다는 뜻인가요?</summary>

아닙니다. u4의 두 번째 검토 결과는 READY였지만 새 Major 지적 2건과 Minor 지적이 남아 있었습니다. 검토자는 승인 전에 이를 반영하도록 권했습니다. READY는 다음 단계로 갈 수 있다는 판정입니다. 남은 지적은 Status 열에서 추적합니다.
</details>

<details class="answer" markdown="1">
<summary>검증 명령은 AI가 바꿀 수 있나요?</summary>

AI는 제안만 합니다. 검증 명령은 사람이 승인해야 상태 파일에 기록되며, 감사 기록에도 `VERIFICATION_COMMAND_RECORDED`로 남습니다.
</details>

<details class="answer" markdown="1">
<summary>u5 스크립트는 웹훅 비밀 값을 어디에 보관하나요?</summary>

보관하지 않습니다. 실행할 때마다 무작위로 만들고 u3 프로세스에만 환경 변수로 넘깁니다. 화면, 로그, 명령줄 인자, 파일 어디에도 값을 쓰지 않습니다.
</details>
