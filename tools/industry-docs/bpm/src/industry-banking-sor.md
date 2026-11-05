# 금융: 계정계와 이벤트로만 잇기

> 은행 계정계(System of Record)가 업무를 처리하고 uEngine6 BPM이 흐름을 통제합니다. 둘은 Kafka 이벤트로만 연결하고, 서로의 API·DB를 부르지 않습니다. 「일반계좌신규」를 신규고객·기존고객 두 경우로 끝까지 실행합니다.

## 무엇을 · 왜

계정계는 고객·계좌·서류 원장을 관리하는 시스템입니다. 창구에서 어떤 순서로 무엇을 확인하는지는 규정이 바뀔 때마다 달라집니다.
그 순서를 BPM에 두면 계정계를 고치지 않고 흐름을 바꿀 수 있습니다. 어느 신청이 어디서 멈췄는지도 한곳에서 확인합니다.

**핵심 원칙 — 업무는 계정계가, 흐름 통제는 BPM이.** 계정계가 한 단계를 처리하면 도메인 이벤트를 발행합니다.
BPM은 그 이벤트를 해당 작업의 `eventSynchronization`으로 받아 완료 처리하고 다음 단계를 큐에 올립니다.

| 토픽 | 방향 | 무엇 |
|---|---|---|
| `bpm-topic` | 계정계 → BPM | 도메인 이벤트. 헤더 `type`(이벤트 이름)·`corrKey`(신청 번호) |
| `bpm-brodcast` | BPM → 누구나 | 진행 상황(`TASK_COMPLETED`). 계정계는 화면 표시에만 씁니다 |

!!! note "먼저 알아 둘 것"
    - 예제 저장소: [uengine-oss/bpm-sample-app-banking](https://github.com/uengine-oss/bpm-sample-app-banking) (uEngine6 저장소의 `sample-apps/` 서브모듈).
    - 이 튜토리얼의 시연 스택(`bmt/sds-process-test` 브랜치)에서는 이벤트로 사람 작업을 끝낼 때 행위자 헤더(`emnb`)를 요구하는 검사가 있습니다. 계정계 예제는 행위자 없이 보내므로, 시연 스택은 `uengine.messaging.require-event-actor: false`로 띄웠습니다.
    - 아래 영상 넷은 예제를 만들 때 촬영해 목소리와 화면 해상도가 이 튜토리얼의 다른 장과 다릅니다.

## 따라 하기

<ol class="steps" markdown="1">
<li markdown="1">**스택 띄우기.** [내 PC에 설치하기](install-local.html)의 스택에 계정계를 더합니다. Kafka·계정계 DB는 예제의 `docker-compose.yml`로, process-service는 예제의 `config/process-service.kafka.yml`을 추가해 Kafka 모드로 띄웁니다.

```bash
cd sample-apps/bpm-sample-app-banking
docker compose up -d                      # PostgreSQL(5434) · Zookeeper · Kafka(9092)
UENGINE_HOME=../.. bash deploy-definitions.sh   # definitions/계정계 연동/ 에 정의 2개
```
</li>
<li markdown="1">**신청 접수.** 디지털창구(`:5174`)에서 고객 이름·휴대폰·초입금으로 계좌 개설을 신청합니다. 계정계가 `AccountOpeningRequested`를 발행하면 BPM의 메시지 시작 이벤트가 인스턴스를 만듭니다(상관 키 = 신청 번호).
</li>
<li markdown="1">**단계 처리.** 상담 → 서류 징구 → 스캔 → 실명확인 → 개인정보 동의를 창구 화면에서 차례로 처리합니다. 단계마다 계정계가 이벤트를 발행합니다. 그러면 BPM 업무 목록에서 해당 작업이 끝나고 다음 작업이 생깁니다.
</li>
<li markdown="1">**분기.** 개인정보 동의 이벤트에 `NewCustomer`가 실려 와 프로세스 변수가 됩니다. 게이트웨이 「신규고객여부」가 `Y`면 고객정보등록/KYC로, `N`이면 계좌신규 등록으로 바로 갑니다.
</li>
<li markdown="1">**끝.** 계좌 개설 → 통장 교부 → 휴대폰 본인인증까지 처리하면 인스턴스가 완료됩니다. 시연 스택에서 신규고객은 작업 9건, 기존고객은 8건으로 끝났습니다.
</li>
<li markdown="1">**되돌리기.** 관리자 화면에서 완료된 단계를 골라 **Back To Here**로 다시 처리하게 할 수 있습니다. 업무 데이터의 보상(이미 만든 계좌 취소 등)은 계정계가 처리하고, BPM은 경로만 되돌립니다.
</li>
</ol>

## 영상으로 더 보기

빌드타임(무엇을 어떻게 설정했나), 런타임(업무함·알림·딥링크와 되돌리기), 관리자 콘솔을 각각 촬영한 영상입니다.

<div class="video"><iframe src="https://www.youtube.com/embed/Vut_yoM1w_w" title="빌드타임 · 프로세스 설정 — 3:16" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>

<div class="video"><iframe src="https://www.youtube.com/embed/wda06hMN4mc" title="런타임 · 업무함과 되돌리기 — 3:02" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>

<div class="video"><iframe src="https://www.youtube.com/embed/K9bex0NLM6s" title="BPM 관리자 콘솔 — 2:44" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>

## 어떻게 설정했나

일반계좌신규의 단계와 이벤트(상관 키 `applicationNo`):

| BPM 작업 | 이벤트 `type` | 계정계가 하는 일 |
|---|---|---|
| 시작 이벤트 | `AccountOpeningRequested` | 신청 원장 생성 |
| 상담/권유 | `ConsultationCompleted` | 상담 기록 |
| 필요 서류 조회 및 징구 | `DocumentsCollected` | 서류 상태 → 징구완료 |
| 서류 스캔 | `DocumentsScanned` | 전자문서 번호 부여 |
| 실명확인 및 고객확인 | `IdentityVerified` | 신분증 진위확인 |
| 개인정보 이용동의서 | `PrivacyConsentSigned` | 동의 기록 + `NewCustomer` 판정 |
| 고객정보등록/KYC | `CustomerRegistered` | 고객 원장 채번 |
| 계좌신규 등록 | `AccountOpened` | 계좌 원장 개설 |
| 발급통장 및 계약서류 교부 | `PassbookIssued` | 통장 발행 |
| 문자교부 시 휴대폰 본인인증 | `MobileAuthConfirmed` | 수령 확인 |

작업마다 URL 작업으로 계정계 화면을 연결하고(`url`에 `<%instance.corrkey%>`), `eventSynchronizations`에 이벤트 이름과 상관 키 속성(`isCorrKey`)을 답니다.
payload의 모든 필드는 프로세스 변수가 되므로, 게이트웨이는 `NewCustomer == 'Y'`처럼 이벤트 값을 바로 봅니다.

계정계는 BPM이 만든 작업을 `GET /worklist`로 주기적으로 읽어 역할별 업무함을 만들고, 작업의 `tool`(URL)로 화면을 엽니다.
같은 방식을 ERP에 적용하면서 업무함을 BPM 쪽에 두고 ERP 화면을 BPM 안에 띄운 것이 [다음 장](industry-erp-purchase.html)입니다.

## 확인 문제

<details class="answer" markdown="1"><summary>계정계가 BPM의 REST API를 한 번도 부르지 않는데, 작업은 어떻게 끝나나요?</summary>

계정계가 Kafka `bpm-topic`에 도메인 이벤트를 보내면, process-service가 이벤트 이름(`type`)과 상관 키(`corrKey`)로 현재 대기 중인 작업을 찾아 완료합니다. 매핑은 정의를 배포할 때 `BPM_EVENT_MAPPING`에 등록됩니다.
</details>

<details class="answer" markdown="1"><summary>기존고객이면 KYC 단계를 건너뛰는 판단은 누가 하나요?</summary>

계정계가 개인정보 동의 이벤트에 `NewCustomer`를 실어 보내고, BPM 게이트웨이가 그 값으로 경로를 고릅니다. 판정 규칙은 계정계에, 경로는 BPM에 있습니다.
</details>
