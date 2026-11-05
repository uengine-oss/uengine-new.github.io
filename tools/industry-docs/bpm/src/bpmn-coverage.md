# BPMN 지원 범위

> uEngine6 `bmt/sds-process-test` 브랜치에서 BPMN 요소를 각각 실제로 실행해 본 결과입니다. 그대로 되는 것(✅), 우회하면 되는 것(◐), 안 되는 것(✗)을 요소 분류별로 모으고, 우회 방법과 해당 장을 적었습니다.

## 무엇을 · 왜

모델러 팔레트에 있는 요소가 모두 엔진에서 실행되지는 않습니다. 이 페이지는 Camunda 문서의 「BPMN coverage」처럼, 이 브랜치에서 각 요소를 실행할 수 있는지 정리합니다.

- **기준.** uEngine6 `bmt/sds-process-test` 브랜치(시연 워크트리 `demo/bpm6-tutorial`, 커밋 `0e163f07`)와 그 프런트를 로컬 스택에서 실행해 확인했습니다. 다른 브랜치(`main` 등)에서는 결과가 다를 수 있습니다.
- **방법.** 정의를 화면 또는 BPMN XML로 만들어 배포하고, REST API·업무 목록·Kafka로 실행한 뒤, 작업 목록 표(`bpm_worklist`)·프로세스 변수·관리자 화면으로 결과를 확인했습니다. 「확인하지 못함」은 실행해 보지 않았다는 뜻입니다.
- **판정.** ✅ 그대로 됨 · ◐ 우회하면 됨(XML로 쓰기, API로 부르기 등) · ✗ 안 됨(엔진이나 화면을 고쳐야 함).

엔진은 BPMN 요소를 태그 이름으로 클래스에 대응시킵니다. 사람 작업은 `org.uengine.kernel.HumanActivity`, 스크립트 작업은 `org.uengine.kernel.ScriptActivity`, 그 밖의 요소는 `org.uengine.kernel.bpmn.<태그 이름>`(예: `ServiceTask`, `ExclusiveGateway`)입니다. 요소의 `<uengine:properties>` JSON 맨 위에 `_type`이 있으면 그 클래스로 바뀝니다(예: 서비스 작업을 `org.uengine.kernel.bpmn.SQLTask`로). 아래 표의 `_type` 칸은 이 값입니다. 자세한 규칙은 [엔진 확장하기](extend-engine.html)에 있습니다.

## 한눈에 보기

| 분류 | ✅ 그대로 | ◐ 우회 | ✗ 안 됨 |
|---|---|---|---|
| 작업 | 사람 작업, URL 작업, 스크립트, 규칙(DMN) | 폼 작업, REST 서비스 작업, SQL 작업, 콜 액티비티, REST 통지(보내기) | 보내기 작업(메일) |
| 게이트웨이 | 배타, 병렬, 포괄 | — | — (이벤트 기반·복합은 확인하지 못함) |
| 이벤트 | 시작·종료, 메시지 시작, 메시지 중간 대기, 오류 종료·오류 경계 | 메시지 경계, 보상 던지기, 이벤트 키 방송 | 타이머 전부, 신호, 에스컬레이션, 조건, terminate |
| 하위 프로세스 | — | 다중 생성(몸통 작업 1개) | 임베디드 서브프로세스 |
| 데이터 | 프로세스 변수, 데이터 매핑, 인스턴스 이름 패턴 | — | — (데이터 객체·저장소는 확인하지 못함) |

## 작업

| 요소 | `_type` | 판정 | 확인한 것 · 우회 | 장 |
|---|---|---|---|---|
| 사람 작업 | `org.uengine.kernel.HumanActivity` | ✅ | 아규먼트(입력 칸), 레인 배정, 업무 목록에서 완료 | [첫 프로세스](quickstart.html), [업무 목록](tasklist.html) |
| 폼 작업 | `org.uengine.kernel.FormActivity` (`tool: "formHandler:<폼 ID>"`) | ◐ | 실행·제출은 됩니다. 작업 패널 「폼」의 「폼 생성을 하시겠습니까?」에서 「예」를 눌러도 아무 동작이 없습니다 → 「아니오」를 누르고 미리 만든 폼을 고릅니다 | [폼 붙이기](forms.html) |
| URL 작업(외부 애플리케이션) | `org.uengine.kernel.URLActivity` | ✅ | 다른 앱 화면을 작업 화면 iframe으로 엽니다. URL은 게이트웨이와 같은 출처여야 합니다 | [다른 앱 화면을 작업으로](external-task-screen.html) |
| 서비스 작업(REST) | `org.uengine.kernel.bpmn.ServiceTask` | ◐ | GET·POST, 헤더·본문 템플릿, 응답 → 변수 매핑이 됩니다. ① 패널에서 저장하면 루트 `_type`이 지워져 배포가 실패합니다 → XML 보기에서 `_type`을 되살립니다 ② 본문에 `<%=변수%>`가 하나도 없으면 SpEL로 해석되어 오류가 납니다 ③ `skipIfNotFound`는 동작하지 않습니다 | [REST API 부르기](rest-service-task.html) |
| SQL 작업 | `org.uengine.kernel.bpmn.SQLTask` | ◐ | 직접 SQL(조회·갱신)은 패널에서 설정할 수 있습니다. 조회 결과 → 변수 매핑(`selectMappings`)과 데이터베이스 매핑 방식은 패널이 저장하지 못합니다 → XML로 씁니다 | [데이터베이스 읽고 쓰기](sql-task.html) |
| 스크립트 작업 | `org.uengine.kernel.ScriptActivity` | ✅ | JavaScript(Rhino, `language:"0"`)·Java(Janino, `language:"1"`) 모두 JDK 21에서 실행됩니다. Java는 `instance.get()`을 `try/catch`로 감쌉니다 | [스크립트로 값 계산](script-task.html) |
| 비즈니스 규칙 작업(DMN) | `org.uengine.kernel.bpmn.BusinessRuleTask` | ✅ | 규칙표 결과로 분기합니다. 결과는 `outcome` 하나뿐이고(고정 목록), 메모는 결과로 나오지 않습니다 | [결재선을 규칙표로](business-rule-dmn.html) |
| 콜 액티비티 | `org.uengine.kernel.bpmn.CallActivity` | ◐ | 하위 인스턴스 생성, 변수 in/out, 역할 전달이 됩니다. 패널에서 고친 값은 저장되지 않습니다 → 정의 선택·바인딩은 XML로 씁니다 | [공통 프로세스 불러 쓰기](call-activity.html) |
| 보내기 작업(메일) | `org.uengine.kernel.LocalEMailActivity` | ✗ | SMTP가 없으면 앞 작업 완료까지 실패합니다. `mail.enabled: false` 설정은 코드가 읽지 않습니다 | — |
| 보내기 작업(REST 통지) | `org.uengine.kernel.bpmn.SendTask` + `sendType:"rest_api"` | ◐ | XML로 작성하면 통지를 보내고 응답을 변수로 받습니다. 패널을 다시 열면 항상 「이메일 전송」이고, 그대로 저장하면 REST 칸이 지워집니다 → REST 서비스 작업으로 대신하세요 | [REST API 부르기](rest-service-task.html) |
| 수신 작업 · 수동 작업 · 일반 작업 | `ReceiveTask` · `DefaultActivity` | 확인하지 못함 | 코드상 수동 작업과 일반 작업은 `DefaultActivity`(바로 완료)이고, 수동 작업은 확장 JSON을 읽지 않습니다 | — |
| 작업의 다중 인스턴스·반복 표식 | (`multiInstanceLoopCharacteristics`) | 확인하지 못함 | 렌치 메뉴에 「병렬/순차 다중 인스턴스」「반복」이 있지만, 엔진 파서는 이 표식 요소를 읽지 않습니다(코드). 다중 생성은 아래 서브프로세스 방식으로 하세요 | [다중 인스턴스](multi-instance.html) |

## 게이트웨이

| 요소 | `_type` | 판정 | 확인한 것 · 우회 | 장 |
|---|---|---|---|---|
| 배타 게이트웨이 | `org.uengine.kernel.bpmn.ExclusiveGateway` | ✅ | 흐름 조건(`org.uengine.kernel.Evaluate`), 기본 흐름(`default` 속성), 우선순위 | [조건으로 갈라지기](exclusive-gateway.html) |
| 병렬 게이트웨이 | `org.uengine.kernel.bpmn.ParallelGateway` | ✅ | 분기 → 한쪽만 끝나면 대기 → 둘 다 끝나야 합류 | [동시에 진행하고 기다리기](parallel-inclusive-gateway.html) |
| 포괄 게이트웨이 | `org.uengine.kernel.bpmn.InclusiveGateway` | ✅ | 참인 갈래만 열리고, 열린 갈래가 모두 끝나야 합류 | [동시에 진행하고 기다리기](parallel-inclusive-gateway.html) |
| 이벤트 기반 게이트웨이 | `org.uengine.kernel.bpmn.EventBasedGateway` | 확인하지 못함 | 코드상 병렬 게이트웨이를 그대로 상속합니다(먼저 온 이벤트 하나만 고르는 동작이 따로 없음) | — |
| 복합 게이트웨이 | — | 확인하지 못함 | 엔진에 해당 클래스가 없습니다 | — |

## 이벤트

| 요소 | `_type` | 판정 | 확인한 것 · 우회 | 장 |
|---|---|---|---|---|
| 시작 · 종료 이벤트(none) | `StartEvent` · `EndEvent` | ✅ | — | [첫 프로세스](quickstart.html) |
| 메시지 시작 이벤트 | `org.uengine.kernel.bpmn.MessageStartEvent` | ✅ | Kafka `bpm-topic` 이벤트(헤더 `type`)로 인스턴스를 시작합니다. 상관 키가 중복되면 새로 만들지 않습니다. 직접 작성한 XML은 프로세스 JSON에 `definitionName`이 있어야 합니다(없으면 첫 사람 작업에서 NPE) | [외부 이벤트로 시작하기](message-start.html) |
| 이벤트 동기화 작업(이벤트로 작업 끝내기) | 작업 JSON의 `eventSynchronization` | ✅ | 이벤트 payload가 변수가 되고 작업이 끝납니다. 「기본」 사용자 작업 패널에는 이벤트 키 칸이 없습니다 → XML, 또는 URL 작업 패널 | [작업을 이벤트로 끝내기](event-completion.html) |
| 메시지 중간 대기(catch) | `org.uengine.kernel.bpmn.MessageIntermediateCatchEvent` | ✅ | 상관 키가 일치하는 인스턴스가 깨어납니다. 패널에 이벤트 키 칸이 없습니다 → XML | [작업을 이벤트로 끝내기](event-completion.html) |
| 이벤트 키 방송 | catch 이벤트의 `eventKey` | ◐ | 상관 키 **없이** 같은 이름의 이벤트를 보내면 그 이벤트를 기다리는 실행 중인 인스턴스가 **모두** 깹니다. 신호(signal) 대신 씁니다 | [작업을 이벤트로 끝내기](event-completion.html) |
| 메시지 경계 이벤트(중단) | `org.uengine.kernel.bpmn.MessageBoundaryEvent` | ◐ | `POST /work-item/{작업}/boundary-message/{경계 id}`로 부르면 작업이 취소되고 경계 쪽으로 진행합니다. 화면에 이 API를 부르는 버튼이 없습니다 → 외부 앱·curl | [작업을 이벤트로 끝내기](event-completion.html) |
| 오류 종료 · 오류 경계 | `ErrorEndEvent` · `ErrorBoundaryEvent` | ✅ | 서브프로세스 안 오류 종료 → 서브프로세스의 오류 경계, 실패한 서비스 작업 → 오류 경계 → 수기 처리 작업. **오류 코드 구분은 없습니다**(어떤 실패든 같은 경계로) | [실패 경로와 되돌리기](error-and-compensation.html) |
| 보상 던지기 | `org.uengine.kernel.bpmn.CompensateIntermediateThrowEvent` | ◐ | 지정한 작업까지 되돌립니다(지나온 작업 COMPENSATED, 그 작업이 새로 생김). BPMN의 보상 핸들러(취소 작업 실행)가 아니라 「지정 작업으로 되돌리기」입니다 | [실패 경로와 되돌리기](error-and-compensation.html), [되돌리기](back-to-here.html) |
| 타이머(시작·중간 대기·경계) | `TimerStartEvent` · `TimerIntermediateCatchEvent` · `TimerBoundaryEvent` | ✗ | 발화는 하지만 상태가 저장되지 않아, 발화로 생긴 작업을 완료하면 `500 Illegal completion`으로 인스턴스가 멈춥니다. 패널 기본값 `* * * * *`(5필드)는 시작부터 500 오류가 납니다 | — |
| 신호(시작·던지기·대기·경계) | `Signal*` | ✗ | `/instance/{id}/signal/{key}`에서 NPE가 발생합니다. 신호 던지기는 Kafka에 `type=ThrowEvent`로 나가 이벤트 키를 쓰지 않습니다 → 위 「이벤트 키 방송」으로 대신 | — |
| 에스컬레이션 | `Escalation*` | ✗ | 경계 쪽 작업은 생기지만 던진 이벤트가 끝나지 않아 서브프로세스 안 흐름이 멈춥니다 | — |
| 조건 이벤트 | `Conditional*` | ✗ | 조건이 참이어도 깨어나지 않습니다 | — |
| terminate 종료 | (`terminateEventDefinition`) | ✗ | 일반 종료로 처리되어 다른 갈래가 계속 실행됩니다 | — |

## 하위 프로세스

| 요소 | `_type` | 판정 | 확인한 것 · 우회 | 장 |
|---|---|---|---|---|
| 임베디드 서브프로세스 | `org.uengine.kernel.bpmn.SubProcess` | ✗ | 서브프로세스가 끝나도 다음 작업이 `Ready`로 남아 완료하면 `500 Illegal completion` 오류가 납니다. 묶어 쓰려면 콜 액티비티로 하세요 | [공통 프로세스 불러 쓰기](call-activity.html) |
| 다중 생성(변수 기반) | 서브프로세스 JSON `forEachVariable` | ◐ | 목록 변수(JSON 배열)의 항목마다 실행합니다. 병렬이 기본이고 루프는 `"multipleInstanceOption":"loop"`(XML). **몸통은 사람 작업 1개**여야 합니다(2단계 이상이면 첫 단계에서 끝난 것으로 처리합니다) | [다중 인스턴스](multi-instance.html) |
| 콜 액티비티 | `org.uengine.kernel.bpmn.CallActivity` | ◐ | 위 「작업」 표 참고 | [공통 프로세스 불러 쓰기](call-activity.html) |
| 이벤트 서브프로세스 · 트랜잭션 | — | 확인하지 못함 | — | — |

## 데이터와 사람

| 요소 · 기능 | 설정 | 판정 | 확인한 것 · 우회 | 장 |
|---|---|---|---|---|
| 프로세스 변수 | 프로세스 JSON의 `<uengine:variable>` (Text·Number·Date·Form) | ✅ | 시작 값, 작업 입력, 이벤트 payload가 변수로 | [프로세스 변수와 인스턴스 이름](process-data.html) |
| 인스턴스 이름 패턴 | `instanceNamePattern` (예: `구매_<%=instance.instanceId%>`) | ✅ | 인스턴스 목록·관리자 화면의 이름 | [프로세스 변수와 인스턴스 이름](process-data.html) |
| 데이터 매핑(작업 ↔ 변수) | `eventSynchronization.mappingContext` | ✅ | 매퍼에서 선을 이어 저장 | [작업 입력값과 데이터 매핑](arguments-and-mapping.html) |
| 데이터 객체 · 데이터 저장소 | `dataObjectReference` · `dataStoreReference` | 확인하지 못함 | 데이터는 프로세스 변수로 다루세요 | — |
| 레인 = 사람 직접 지정 | `DirectRoleResolutionContext` (`endpoint` = 사용자 이름) | ✅ | 화면 「사용자 직접 지정」은 이메일을 저장해 어느 업무 목록에도 표시되지 않습니다 → XML에서 사용자 이름으로 | [레인과 담당자](lanes-and-roles.html) |
| 레인 = 그룹·역할 + 선점 | `IAMRoleResolutionContext` (`groupName`·`scope`) + `dispatchingOption: 1` | ◐ | 실행은 됩니다. 레인 패널의 기관·권한 목록이 Keycloak이 아닌 고정값이므로 XML로 씁니다 | [레인과 담당자](lanes-and-roles.html), [Keycloak](security-keycloak.html) |
| 시작 레인 | 첫 레인 | ◐ | 첫 레인에 배분 설정이 있으면 화면 「실행」에서 500 오류가 납니다 → 첫 레인은 비워 둡니다 | [레인과 담당자](lanes-and-roles.html) |

## 작업 처리와 운영 기능

BPMN 요소는 아니지만 같은 기준으로 확인한 화면·API 기능입니다.

| 기능 | 판정 | 확인한 것 · 우회 | 장 |
|---|---|---|---|
| 업무 목록·선점(다중 선점 포함) | ✅ | 「완료됨」 칸은 비어 있습니다(완료 기록은 관리자 화면 히스토리) | [업무 목록에서 일하기](tasklist.html) |
| 중간 저장 | ◐ | 값은 변수로 가지만 다시 열면 칸이 비어 있습니다 | [업무 목록에서 일하기](tasklist.html) |
| 반송 · SKIP(작업 주인) | ✅ | 사유가 남으면 그 사람의 업무 목록에서 500 오류가 납니다 → 로컬 시연에서는 사유를 정리 | [반송과 SKIP](return-and-skip.html) |
| 위임 | ◐ | 단건 위임 API만 됩니다. 위임 화면·다중 위임은 ✗ | [REST API](rest-api.html) |
| 인스턴스 찾기·상세·변수 고치기 | ✅ | 변수 값은 JSON으로 해석합니다(문자열은 따옴표로 감쌉니다) | [인스턴스 찾고 살피기](instance-monitoring.html), [변수 고치기](fix-variables.html) |
| 되돌리기(Back To Here) | ✅ | 관리자 화면 「이 위치로 되돌리기」 | [되돌리기와 실패한 작업](back-to-here.html) |
| 관리자 SKIP(남의 작업) | ✗ | 403 `No permission to skip` → 작업 주인이 업무 화면에서 SKIP | [되돌리기와 실패한 작업](back-to-here.html) |
| 실패한 작업 표시 | ◐ | 서비스 작업이 실패하면 앞 작업의 완료가 거절될 뿐 실패 상태가 남지 않습니다 → 원인을 고쳐 다시 완료하거나 오류 경계를 붙입니다 | [되돌리기와 실패한 작업](back-to-here.html) |
| 정지 · 재개 | ✗ | API 응답은 200이지만 상태가 바뀌지 않습니다 | — |
| 시뮬레이션 · 단위 테스트 | ◐ | 「실행 테스트」 탭과 단위 테스트 케이스 작성까지. 「시나리오 테스트」는 준비 중 | [배포 전에 시험하기](test-before-deploy.html) |
| 버전 | ◐ | 화면 저장은 같은 버전을 덮어씁니다. 파일(archive)로 버전을 나누면 기존 인스턴스는 이전 버전으로 실행됩니다. 버전 관리자·버전 비교 화면은 ✗ | [버전과 배포](versions-and-deploy.html) |
| 분석·KPI | ◐ | 분석 서비스(analytics)를 따로 실행하고 ETL을 실행해야 합니다 | [분석과 KPI](analytics-kpi.html) |
| 조직도 화면 | ✗ | Keycloak과 이어지지 않습니다 → Keycloak 관리 콘솔 | [사용자·그룹·역할](security-keycloak.html) |
| 감사 기록 API(`/audit`) | ✗ | 감사 저장이 꺼져 있어 빈 목록입니다 | [REST API](rest-api.html) |

## 알려진 제약

!!! warning "이 표는 한 브랜치의 결과입니다"
    ✗ 로 적은 요소(임베디드 서브프로세스, 타이머, 신호·에스컬레이션·조건·terminate, 메일)는 이 튜토리얼의 따라 하기에 넣지 않았습니다. 엔진을 수정한 빌드에서는 결과가 달라지므로, 업그레이드할 때 이 페이지의 시험(`research/verify-scripts/B-*.mjs`와 같은 방식)을 다시 실행해 보세요.

- 모델러 팔레트·렌치 메뉴에는 위의 ✗ 요소도 모두 나옵니다. 그릴 수 있다고 실행되는 것은 아닙니다.
- 화면 패널이 일부 설정을 저장하지 못하는 요소(서비스·SQL·보내기·콜 액티비티·이벤트 키)는 XML 보기(`</>`)에서 직접 고칩니다. 고친 뒤 루트 `_type`이 남아 있는지 확인하세요.
- 시작자를 정적 필드에서 읽기 때문에, 동시에 여러 사용자가 시작하면 첫 작업 담당자가 바뀔 수 있습니다. API로 시작할 때는 `roleMappings`로 시작 레인 사람을 적어 주세요.

## 확인 문제

<details class="answer" markdown="1"><summary>결재가 사흘 안 끝나면 독촉 작업을 만들고 싶습니다. 타이머 경계 이벤트를 쓰면 되나요?</summary>

이 브랜치에서는 안 됩니다. 타이머는 발화하지만 발화로 생긴 작업을 완료할 수 없어 인스턴스가 멈춥니다. 외부 스케줄러가 기한을 넘긴 작업을 찾아 이벤트(Kafka)를 보내고, 그 이벤트를 메시지 경계·이벤트 동기화로 받는 식으로 우회합니다.
</details>

<details class="answer" markdown="1"><summary>「견적 입력 → 검토」 두 단계를 공급사마다 반복하려면 어떻게 그리나요?</summary>

다중 생성 서브프로세스의 몸통은 사람 작업 하나여야 합니다. 「견적 입력」만 다중 생성하고, 「검토」는 서브프로세스 뒤에 한 번 둡니다. 두 단계를 꼭 묶어야 하면 두 단계짜리 프로세스를 따로 만들어 콜 액티비티로 부르는 방법을 검토하세요(콜 액티비티의 다중 생성은 확인하지 못했습니다).
</details>

<details class="answer" markdown="1"><summary>서비스 작업 패널에서 URL을 고쳐 저장했더니 배포 실패 메시지가 나옵니다. 왜인가요?</summary>

패널이 저장하면서 서비스 작업 JSON 맨 위의 `_type`을 지우고, 헤더에는 `_type`을 남깁니다. 엔진은 JSON 어딘가에 `_type`이 있으면 맨 위에도 있어야 읽을 수 있습니다. XML 보기에서 `"_type":"org.uengine.kernel.bpmn.ServiceTask"`를 다시 넣고 저장하세요.
</details>
