# 엔진 확장하기

> 새 작업 종류(사용자 정의 액티비티), 담당자를 정하는 규칙(역할 해석), 모든 작업의 실행 전후 훅(액티비티 필터), 배포 훅, 사용자 정보(IAM), 이벤트 발행을 Java로 바꿔 끼우는 방법입니다. 클래스·인터페이스 이름은 이 브랜치 코드에서 확인했습니다.

## 무엇을 · 왜

모델러 패널에 없는 동작이 필요할 때가 있습니다. 사내 신용 조회 시스템을 호출하는 작업, 「요청자의 팀장」처럼 조직도를 따라 담당자를 찾는 규칙, 모든 작업의 완료를 사내 감사 시스템에 기록하는 일 등이 있습니다.
uEngine6은 이런 동작을 **process-service의 Java 클래스**로 구현할 수 있습니다. 정의 파일은 그 클래스를 이름으로 가리키기만 합니다.

| 바꾸고 싶은 것 | 확장 지점 | 정의·설정에서 가리키는 법 | 등록 |
|---|---|---|---|
| 작업이 하는 일 | `org.uengine.kernel.Activity` 하위 클래스 | 작업 JSON의 `_type` | process-service 클래스패스에 두기만 하면 됨 |
| 담당자를 정하는 규칙 | `org.uengine.kernel.RoleResolutionContext` 하위 클래스 | 레인 JSON의 `roleResolutionContext._type` | 위와 같음 |
| 모든 작업의 실행 전후 | `org.uengine.kernel.ActivityFilter` | — | Spring 빈 |
| 작업 완료(커밋 뒤) 알림 | `org.uengine.kernel.IActivityCompletionListener` | — | Spring 빈 |
| 정의 배포 때 | `org.uengine.kernel.DeployFilter` | — | Spring 빈 |
| 사용자·그룹·역할 조회 | `org.uengine.five.service.IAMService` | 환경 변수 `IAM_PROVIDER` | `IAMServiceFactory.register(...)` |
| 이벤트 내보내기 | `org.uengine.five.messaging.EventPublisher` | `uengine.messaging.mode` | Spring 빈(Kafka/폴링 구현이 이미 있음) |

**`_type`의 뜻.** 엔진(`org.uengine.five.serializers.BpmnXMLParser`)은 BPMN 태그 이름으로 기본 클래스를 정합니다. `userTask`는 `org.uengine.kernel.HumanActivity`, `scriptTask`는 `org.uengine.kernel.ScriptActivity`, `task`·`manualTask`는 `org.uengine.kernel.DefaultActivity`, 나머지는 `org.uengine.kernel.bpmn.<태그 이름>`(예: `ServiceTask`)입니다. 그다음 요소의 `<uengine:properties>` JSON을 Jackson으로 읽습니다. JSON에 `_type`이 있으면 **그 클래스 이름으로** 객체를 만듭니다. 그래서 서비스 작업은 `_type`에 따라 REST 호출(`ServiceTask`)도, SQL(`SQLTask`)도, RPA(`org.uengine.five.rpa.RPAActivity`)도 됩니다.

```java
// BpmnXMLParser.createTypedJsonObjectMapper() — 이 브랜치 코드
objectMapper.setVisibilityChecker(... .withFieldVisibility(JsonAutoDetect.Visibility.ANY)
                                      .withGetterVisibility(JsonAutoDetect.Visibility.NONE)
                                      .withSetterVisibility(JsonAutoDetect.Visibility.NONE) ...);
objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
objectMapper.enableDefaultTypingAsProperty(ObjectMapper.DefaultTyping.OBJECT_AND_NON_CONCRETE, "_type");
```

이 코드에서 알 수 있는 점은 세 가지입니다.

- JSON은 **필드에 바로** 들어갑니다(setter를 거치지 않음). 클래스에는 인자 없는 public 생성자가 있어야 하고, 필드 이름이 곧 JSON 속성 이름입니다.
- 알 수 없는 속성은 무시합니다. 철자가 틀려도 오류 없이 빈 값이 됩니다.
- JSON 어딘가(헤더·역할 등)에 `_type`이 있으면 맨 위에도 `_type`이 있어야 합니다. 파서가 이때 맨 위를 추상 `Activity`로 읽기 때문입니다([REST API 부르기](rest-service-task.html)의 「패널 저장 후 `_type` 확인」과 같은 이유).

!!! note "이 장은 글만 있습니다"
    확장은 process-service를 다시 빌드하고 실행해야 하므로, 여러 사람이 함께 쓰는 시연 스택에서는 실행해 보지 않았습니다. 클래스·인터페이스·메서드 이름과 등록 방식은 이 브랜치(`bmt/sds-process-test`) 코드에서 확인했습니다. **아래 예제 코드(`com.gaon…`)는 컴파일·실행해 보지 않았습니다.** 이미 있는 구현(`RPAActivity`, `DirectRoleResolutionContext`, `InstanceNameFilter` 등)을 본보기로 쓰세요.

## 따라 하기

<ol class="steps" markdown="1">
<li markdown="1">**사용자 정의 액티비티 — 동기 작업.** 바로 끝나는 작업은 `org.uengine.kernel.DefaultActivity`를 상속해 `executeActivity`를 구현하고, 끝에 `fireComplete(instance)`를 호출합니다. 변수는 `instance.get("", "<이름>")`으로 읽고, 결과는 `ProcessVariable` 필드의 `set(instance, "", 값)`으로 씁니다(`ScriptActivity`와 같은 방식).

```java
package com.gaon.bpm;

import java.io.Serializable;
import org.uengine.kernel.DefaultActivity;
import org.uengine.kernel.ProcessInstance;
import org.uengine.kernel.ProcessVariable;

/** 공급사 신용 등급 조회(예제). 정의에서는 "_type":"com.gaon.bpm.CreditCheckActivity" */
public class CreditCheckActivity extends DefaultActivity {
    String supplierVariable;   // JSON "supplierVariable": "공급사"
    ProcessVariable out;       // JSON "out": {"name": "신용등급"}

    public CreditCheckActivity() { setName("신용 조회"); }

    @Override
    protected void executeActivity(ProcessInstance instance) throws Exception {
        Serializable supplier = instance.get("", supplierVariable);
        String grade = lookup(String.valueOf(supplier));      // 사내 시스템 호출
        if (out != null) out.set(instance, "", grade);
        fireComplete(instance);                               // 부르지 않으면 작업이 끝나지 않는다
    }

    String lookup(String supplier) { return "A"; }
}
```

실패할 때는 예외를 던집니다. 이 브랜치에서는 서비스 작업과 같이 앞선 사람 작업의 완료 요청 전체가 거절되고, 오류 경계를 붙였으면 그쪽으로 진행합니다([되돌리기와 실패한 작업 다루기](back-to-here.html), [실패 경로와 되돌리기](error-and-compensation.html)).
</li>
<li markdown="1">**정의에서 가리키기.** 모델러에는 이 클래스의 패널이 없으므로 「XML 보기」(`</>`)에서 서비스 작업의 JSON을 바꿉니다. 태그는 `serviceTask`든 `task`든 상관없고, `_type`이 클래스를 정합니다.

```xml
<bpmn:serviceTask id="Credit" name="신용 조회">
  <bpmn:extensionElements><uengine:properties><uengine:json>
    {"_type":"com.gaon.bpm.CreditCheckActivity","supplierVariable":"공급사","out":{"name":"신용등급"}}
  </uengine:json></uengine:properties></bpmn:extensionElements>
</bpmn:serviceTask>
```

클래스가 process-service 클래스패스에 없으면 배포(`POST /definition-changes`)가 실패합니다. definition-service는 BPMN 원문만 저장하므로 해당 서비스에는 클래스가 없어도 됩니다.
</li>
<li markdown="1">**사용자 정의 액티비티 — 오래 걸리는 작업.** 외부 작업이 끝날 때까지 기다려야 하면 `org.uengine.kernel.ReceiveActivity`를 상속하고, `executeActivity`에서는 작업을 맡기기만 하고 `fireComplete`를 호출하지 않습니다. 결과가 오면 `fireComplete(instance)`(실패하면 `fireFault(instance, e)`)를 부릅니다. 이 브랜치의 `org.uengine.five.rpa.RPAActivity`가 이 방식입니다. `executeActivity`에서 RPA 작업을 큐에 넣고, 워커가 결과를 REST로 보고하면 `onJobResult(ProcessInstance, Map)`이 결과를 변수에 매핑한 뒤 `fireComplete`를 호출합니다.

사람이 화면에서 끝내는 작업을 만들려면 `org.uengine.kernel.HumanActivity`를 상속하고 `getTool(ProcessInstance)`를 바꿉니다. `FormActivity`는 `"formHandler:<폼 ID>"`, `URLActivity`는 `"urlHandler:<URL>"`, 기본은 `"defaultHandler"`를 반환합니다. 이 문자열은 업무 목록 행의 `tool` 칸에 저장될 뿐이고, **어떤 화면을 표시할지는 프런트가 정합니다**(`WorkItem.vue`가 `urlHandler`·`formHandler`·그 밖으로 나눔). 서버에 폼 핸들러를 추가하는 인터페이스는 없습니다(`org.uengine.kernel.ITool`은 있지만 쓰는 곳이 없음). 새 작업 화면은 [URL 작업](external-task-screen.html)으로 다른 앱 화면을 여는 편이 쉽습니다.
</li>
<li markdown="1">**담당자 규칙 — 역할 해석.** 레인의 담당자는 `org.uengine.kernel.RoleResolutionContext`가 정합니다. 추상 메서드는 둘입니다.

```java
abstract public RoleMapping getActualMapping(ProcessDefinition pd, ProcessInstance instance,
                                             String tracingTag, Map options) throws Exception;
abstract public String getDisplayName();
```

사람 한 명을 정하는 규칙이면 `DirectRoleResolutionContext`처럼 `RoleMapping`에 사용자 이름을 넣어 반환합니다.

```java
package com.gaon.bpm;

import java.util.Map;
import org.uengine.kernel.*;

/** 금액이 기준 이상이면 above, 아니면 below 가 결재(예제). */
public class AmountBasedApprover extends RoleResolutionContext {
    String amountVariable = "금액";
    long threshold = 10_000_000L;
    String below = "yoon";
    String above = "kim";

    @Override
    public RoleMapping getActualMapping(ProcessDefinition pd, ProcessInstance instance,
                                        String tracingTag, Map options) throws Exception {
        Object v = instance.get("", amountVariable);
        long amount = v instanceof Number ? ((Number) v).longValue() : 0L;
        RoleMapping rm = RoleMapping.create();
        rm.setEndpoint(amount >= threshold ? above : below);   // 엔드포인트 = Keycloak 사용자 이름
        rm.setAssignType(Role.ASSIGNTYPE_USER);
        return rm;
    }

    @Override
    public String getDisplayName() { return "금액 기준 결재자"; }
}
```

```json
{"roleResolutionContext": {"_type": "com.gaon.bpm.AmountBasedApprover", "threshold": 5000000}}
```

엔드포인트는 이메일이 아니라 **토큰의 `preferred_username`**(예: `yoon`)이어야 그 사람의 업무 목록에 표시됩니다([사용자·그룹·역할](security-keycloak.html)).

그룹·역할로 배정하는 기본 구현 `org.uengine.five.overriding.IAMRoleResolutionContext`(필드 `groupName`·`scope`)는 사용자를 나열하지 않습니다. `RoleMapping`에 그룹·역할과 배정 종류(`ASSIGNTYPE_GROUP`=3, `ASSIGNTYPE_ROLE`=4, `ASSIGNTYPE_GROUP_ROLE`=5)만 넣습니다. 작업을 볼 수 있는 사람은 업무 목록 조회(`findToDo`)가 토큰의 `groups`·`realm_access.roles`와 비교해 정합니다. 「이 사람이 담당자인가」 검사가 필요하면 `org.uengine.kernel.IContainsMapping`(`boolean containsMapping(ProcessInstance, RoleMapping)`)을 함께 구현합니다. 고객사 패키지 `org.uengine.hwlife.overriding`의 `BoundRoleResolutionContext`(다른 규칙 + 변수 바인딩), `RuleBasedRoleResolutionContext`(정책 규칙)도 참고할 수 있습니다.
</li>
<li markdown="1">**모든 작업에 훅 걸기 — 액티비티 필터.** `org.uengine.kernel.ActivityFilter`를 구현한 Spring 빈은 **모든 정의의 모든 작업**에 적용됩니다. 엔진(`ProcessDefinition.getActivityFilters()`)이 `GlobalContext.getComponents(ActivityFilter.class)`, 즉 Spring의 `getBeansOfType`으로 필터를 모읍니다.

```java
public interface ActivityFilter extends java.io.Serializable {
    void beforeExecute(Activity activity, ProcessInstance instance) throws Exception;
    void afterExecute(Activity activity, ProcessInstance instance) throws Exception;
    void afterComplete(Activity activity, ProcessInstance instance) throws Exception;
    void afterFault(Activity activity, ProcessInstance instance, FaultContext faultContext) throws Exception;
    void onPropertyChange(Activity activity, ProcessInstance instance, String propertyName, Object changedValue) throws Exception;
    void onDeploy(ProcessDefinition definition) throws Exception;
}
```

호출 순서는 `beforeExecute → executeActivity → afterExecute → fireComplete → (onEvent) → afterComplete`입니다(`Activity.java` 주석과 코드). `org.uengine.kernel.SensitiveActivityFilter`는 `onEvent(Activity, ProcessInstance, String eventName, Object payload)`를 더합니다. 등록은 `@Bean`이 확실합니다.

```java
@Configuration
public class GaonFilters {
    @Bean
    public ActivityFilter gaonAuditFilter() {
        return new ActivityFilter() {
            public void afterComplete(Activity a, ProcessInstance i) throws Exception {
                if (a instanceof HumanActivity) log("완료", i.getInstanceId(), a.getTracingTag());
            }
            public void beforeExecute(Activity a, ProcessInstance i) {}
            public void afterExecute(Activity a, ProcessInstance i) {}
            public void afterFault(Activity a, ProcessInstance i, FaultContext f) {}
            public void onPropertyChange(Activity a, ProcessInstance i, String p, Object v) {}
            public void onDeploy(ProcessDefinition d) {}
        };
    }
    static void log(Object... x) { /* 사내 감사 시스템으로 */ }
}
```

이 브랜치에서 실제로 적용된 필터는 `InstanceNameFilter`(인스턴스 이름 패턴 적용)와 `InstanceDataAppendingActivityFilter`(서비스·스크립트 작업을 업무 목록 행으로 남기고, 실패하면 Failed 행)입니다. 둘 다 `@Bean`으로 등록돼 있습니다. `PayloadFilter`는 설정 `filter.payload.enabled: false`로 꺼져 있고, `AuditActivityFilter`는 빈 등록이 주석 처리돼 있습니다.
</li>
<li markdown="1">**완료 알림 — 커밋 뒤.** 필터는 엔진 트랜잭션 안에서 실행됩니다. 외부로 메시지를 보낼 때는 커밋이 끝난 뒤 호출되는 `org.uengine.kernel.IActivityCompletionListener`(`void onActivityCompleted(ProcessInstance instance, Activity activity)`)가 안전합니다. 이 브랜치의 `ActivityCompletionBrodcastListener`(`@Component`)가 이 방식으로 사람 작업이 끝날 때마다 `EventPublisher.send("bpm-brodcast", …, Map.of("type", "TASK_COMPLETED"))`를 보냅니다([이벤트로 시스템 잇기](event-integration-kafka.html)).
</li>
<li markdown="1">**배포 훅.** `org.uengine.kernel.DeployFilter`(`beforeDeploy(ProcessDefinition, ProcessTransactionContext, String folder, boolean isNew)`)를 구현한 Spring 빈은 정의가 배포될 때(`POST /definition-changes`, 시작 시 정의 동기화) 호출됩니다. `EventMappingDeployFilter`가 이때 시작 이벤트·이벤트 동기화 작업을 `BPM_EVENT_MAPPING` 표에 등록합니다. 정의 검사(「서비스 작업에 URL 이 없으면 거절」 같은)를 추가할 수 있는 지점입니다.
</li>
<li markdown="1">**사용자 정보(IAM).** 그룹·역할 확인과 사용자 이름 조회는 `org.uengine.five.service.IAMService`를 거칩니다. 메서드는 `getUserById`, `getUsersByGroup`, `getUsersByRole`, `getUserScopes`, `getUserGroups`, 기본 구현 `hasScope`·`isInGroup`입니다. 구현은 `KeycloakIAMService`(Keycloak 관리 REST)와 고객사용 `ExternalIAMService`가 있고, `ProcessServiceApplication`이 `IAMServiceFactory.register("keycloak", …)`·`register("external", …)`로 등록합니다. 어떤 구현을 쓸지는 환경 변수 `IAM_PROVIDER`(또는 속성 `iam.provider`)로 고릅니다. LDAP·사내 인사 시스템을 붙이려면 이 인터페이스를 구현해 같은 방식으로 등록합니다.
</li>
<li markdown="1">**이벤트.** 들어오는 이벤트는 `BpmMessageDispatcher.dispatch`가 헤더 `type`·`corrKey`·`emnb`를 읽어 `AsyncEventListener.wheneverEvent(eventBody, typeHeader, inboxCorrKey, actorEndpoint)`로 넘깁니다. `BPM_EVENT_MAPPING`에서 이벤트 이름으로 정의·작업을 찾아 시작하거나 작업을 끝냅니다. 여기에 추가하는 사용자 정의 핸들러 인터페이스는 **없습니다**. 다른 처리가 필요하면 그 이벤트를 받는 작업을 `ReceiveActivity` 하위 클래스로 만들거나(3단계), 폴링 모드의 진입점 `POST /inbox`를 `org.uengine.five.messaging.EventInboxProvider`(`getProviderId()`, `receiveEvent(String requestBodyJson)`) 구현으로 바꿉니다(설정 `event-inbox.provider`). 나가는 이벤트는 `EventPublisher.send(String channel, Object payload, Map<String,Object> headers)` 하나로 보냅니다. 구현은 Kafka 모드 `KafkaEventPublisher`, 폴링 모드 `InboxEventPublisher`입니다.
</li>
</ol>

## 설정 레퍼런스

### 확장 인터페이스 요약

| 형식 | 이름(패키지) | 꼭 구현할 것 | 이 브랜치의 예 |
|---|---|---|---|
| 클래스 | `org.uengine.kernel.Activity` / `DefaultActivity` | `protected void executeActivity(ProcessInstance)` → `fireComplete(instance)` | `ScriptActivity`, `bpmn.ServiceTask`, `bpmn.SQLTask` |
| 클래스 | `org.uengine.kernel.ReceiveActivity` | `executeActivity`에서 맡기기만, 나중에 `fireComplete`/`fireFault` | `org.uengine.five.rpa.RPAActivity` |
| 클래스 | `org.uengine.kernel.HumanActivity` | `public String getTool(ProcessInstance)` | `FormActivity`, `URLActivity` |
| 클래스 | `org.uengine.kernel.RoleResolutionContext` | `getActualMapping(...)`, `getDisplayName()` | `DirectRoleResolutionContext`, `five.overriding.IAMRoleResolutionContext` |
| 인터페이스 | `org.uengine.kernel.IContainsMapping` | `containsMapping(ProcessInstance, RoleMapping)` | `IAMRoleResolutionContext` |
| 인터페이스 | `org.uengine.kernel.ActivityFilter` / `SensitiveActivityFilter` | 6개(+`onEvent`) | `five.overriding.InstanceNameFilter`, `InstanceDataAppendingActivityFilter` |
| 인터페이스 | `org.uengine.kernel.IActivityCompletionListener` | `onActivityCompleted(ProcessInstance, Activity)` | `five.overriding.ActivityCompletionBrodcastListener` |
| 인터페이스 | `org.uengine.kernel.DeployFilter` | `beforeDeploy(...)` | `EventMappingDeployFilter`, `ServiceRegisterDeployFilter` |
| 인터페이스 | `org.uengine.five.service.IAMService` | 조회 메서드 5개 | `KeycloakIAMService` |
| 인터페이스 | `org.uengine.five.messaging.EventPublisher` | `send(channel, payload, headers)` | `KafkaEventPublisher`, `InboxEventPublisher` |
| 인터페이스 | `org.uengine.five.messaging.EventInboxProvider` | `getProviderId()`, `receiveEvent(String)` | `DefaultEventInboxServiceImpl` |

### 어디에 두고 어떻게 띄우나

- 모듈: 루트 `pom.xml`의 `uengine-commons`, `uengine-resource-manager`, `uengine-core`, `uengine-five-api`, `definition-service`, `process-service`, `analytics`. 엔진 확장은 **process-service 실행 jar 안**에 있어야 합니다. 가장 쉬운 방법은 `RPAActivity`처럼 process-service 모듈에 두는 것이고, 따로 jar로 만들면 `process-service/pom.xml`의 의존성으로 넣습니다(이 저장소에는 `loader.path` 같은 외부 jar 로딩 설정이 없습니다).
- Spring 빈 스캔: `ProcessServiceApplication`의 `@ComponentScan(basePackages = {"org.uengine.kernel.bpmn", "org.uengine.five", "org.uengine.hwlife"})`. 다른 패키지(`com.gaon…`)에 `@Component`를 붙이면 스캔되지 않습니다. `@Bean`으로 등록하거나 스캔 대상에 넣으세요. `spring.main.allow-bean-definition-overriding: true`라서 같은 이름의 빈으로 기본 빈을 교체할 수도 있습니다.
- `_type`으로만 쓰는 클래스(액티비티·역할 해석)는 빈 등록이 필요 없습니다. Jackson이 클래스 이름으로 찾습니다.
- 빌드·실행(저장소 문서 `docs/local-install-guide.md` 5-1):

```bash
mvn -B -Dmaven.test.skip=true install          # 저장소 루트
SPRING_PROFILES_ACTIVE=postgres,keycloak-installed UENGINE_BASEPATH="$(pwd)" \
KEYCLOAK_URI=http://localhost:8280 KEYCLOAK_REALM=uengine ... \
java --add-opens java.base/java.util=ALL-UNNAMED ... \
     -jar process-service/target/process-service-1.1-SNAPSHOT.jar \
     --spring.config.additional-location=file:docs/local/process-service.local.yml
```

### 정의 JSON에서 쓸 수 있는 이름

| 쓰는 곳 | 이름 | 뜻 |
|---|---|---|
| 스크립트 작업(JavaScript·Java) | `instance`, `activity`, `definition`, `util` | 실행 중 인스턴스, 이 작업, 정의, 도우미([스크립트로 값 계산](script-task.html)) |
| 템플릿(서비스 작업 URL·본문, 인스턴스 이름) | `<%=변수%>`, `<%=instance.instanceId%>`, `<%=instance.corrkey%>` | 변수·인스턴스 속성 치환 |
| 프로세스 변수 형식 | `Text`, `Number`, `Date`, `Form` | 파서(`convertToJavaType`)가 받는 형식. 그 밖은 오류 |

## 알려진 제약

- **패널이 없습니다.** 사용자 정의 `_type`은 모델러의 「XML 보기」에서 직접 씁니다. 그 요소의 패널을 열어 저장하면 패널이 아는 속성만 남을 수 있으니, 저장한 뒤 XML을 다시 확인하세요.
- **`_type`은 클래스패스의 어떤 클래스든 가리킬 수 있습니다.** 파서가 Jackson 기본 타입 지정을 쓰고, 허용 패키지 목록(`PolymorphicTypeValidator`)이 코드에 없습니다. 정의를 배포할 수 있는 사람은 서버 코드를 고를 수 있는 사람이라고 보고, 배포 권한을 제한하세요.
- 폼·업무 화면 종류는 서버에서 늘릴 수 없습니다(프런트 `WorkItem.vue`가 정함).
- 들어오는 이벤트에 추가하는 핸들러 인터페이스는 없습니다(위 8단계의 두 우회 방법).
- 확인하지 못함: `ActivityFilter.onDeploy`를 부르는 곳을 이 브랜치 코드에서 찾지 못했습니다. 배포 훅은 `DeployFilter`를 쓰세요. 프런트 레인 패널이 가리키는 `org.uengine.five.overriding.GroupRoleResolutionContext`, `org.uengine.kernel.ExternalCustomerRoleResolutionContext`는 백엔드 소스에 없습니다(그 선택지로 배포해 보지는 않았습니다).
- 이 장의 예제 코드는 빌드·실행하지 않았습니다.

## 확인 문제

<details class="answer" markdown="1"><summary>사용자 정의 액티비티를 만들었는데 정의를 배포하면 실패합니다. 무엇부터 확인하나요?</summary>

① 그 클래스가 process-service 실행 jar 안에 있는지(다른 모듈이면 `process-service/pom.xml` 의존성), ② JSON의 `_type`이 패키지까지 맞는지, ③ 인자 없는 public 생성자가 있는지 확인합니다. 정의 저장(definition-service)은 원문만 저장하므로 성공해도, process-service가 읽을 때 실패할 수 있습니다.
</details>

<details class="answer" markdown="1"><summary>모든 사람 작업 완료를 사내 감사 시스템에 보내려면 ActivityFilter와 IActivityCompletionListener 중 무엇을 쓰나요?</summary>

`IActivityCompletionListener`입니다. 커밋이 끝난 뒤 호출되므로, 엔진 트랜잭션이 되돌려진 작업의 완료 알림을 외부로 보내는 일이 없습니다. 필터는 트랜잭션 안에서 실행되므로 같은 DB 내 기록이나 검사에 적합합니다.
</details>

<details class="answer" markdown="1"><summary>「요청자의 팀장」에게 결재를 보내는 레인을 만들려면 어디를 고치나요?</summary>

`RoleResolutionContext` 하위 클래스를 만들어 `getActualMapping`에서 요청자(시작한 사람)의 팀장을 사내 조직도나 `IAMService`로 찾아 `RoleMapping`의 엔드포인트(사용자 이름)로 돌려주고, 레인 JSON의 `roleResolutionContext._type`에 그 클래스 이름을 적습니다.
</details>
