# 내 PC에 설치하기

> uEngine6 저장소를 받아 빌드하고, 인프라(PostgreSQL·Keycloak·Kafka)는 Docker로, 서비스 세 개와 웹 화면은 내 PC에서 직접 띄웁니다. 끝나면 `http://localhost:8288`에서 홍길동으로 로그인할 수 있습니다.

## 무엇을 · 왜

uEngine6 BPM은 서비스 세 개와 웹 화면 하나로 이루어져 있습니다. 브라우저는 언제나 **게이트웨이**(`keycloak-gateway`) 한 곳으로 들어오고, 게이트웨이가 Keycloak 로그인을 처리한 뒤 주소에 따라 요청을 각 서비스로 보냅니다.

```text
브라우저 ─▶ keycloak-gateway :8288 ─┬─ /definition/** /version(s)/**            → definition-service :9293
           (Keycloak :8280 로그인)  ├─ /instance/** /work-item/** /worklist/** … → process-service    :9294
                                    └─ 그 밖의 /**                                → 웹 화면(정적 빌드) :5373
process-service ─ PostgreSQL :5632 (엔진 저장소)
                └ Kafka :9092 (bpm-topic · bpm-brodcast — 외부 시스템 이벤트)
```

| 구성 | 포트 | 실행 방식 | 하는 일 |
|---|---|---|---|
| PostgreSQL 16 | 5632 | Docker | 인스턴스·업무 목록·이벤트 매핑 저장. 스키마는 기동할 때 Hibernate `ddl-auto: update`가 만듭니다 |
| Keycloak 26.6.1 | 8280 | Docker | 사용자·그룹·역할, 로그인 |
| Kafka 7.6.1 + ZooKeeper | 9092 · 22181 | Docker | 외부 시스템과 주고받는 이벤트 |
| process-service | 9294 | `java -jar` | 인스턴스 실행, 업무 목록, 이벤트 수신 |
| definition-service | 9293 | `java -jar` | 프로세스 정의·폼 저장 |
| keycloak-gateway | 8288 | `java -jar` | 브라우저 입구, 로그인, 라우팅 |
| 웹 화면(`process-gpt-vue3-hli`) | 5373 | 정적 빌드 + SPA 서버 | 모델러, 업무 목록, 관리자 화면 |

이 장은 uEngine6 저장소의 [로컬 설치 매뉴얼](https://github.com/uengine-oss/uEngine6-jdk21/blob/bmt/sds-process-test/docs/local-install-guide.md)(`docs/local-install-guide.md`)을 바탕으로, 이 튜토리얼의 영상 촬영에 사용한 로컬 스택의 실제 설치 과정을 담았습니다. 매뉴얼과 다른 점은 셋입니다.

- **Kafka 모드로 띄웁니다.** 이 브랜치의 process-service 기본 메시징 모드는 `polling`(DB inbox)이라 Kafka 없이도 동작합니다. 이 튜토리얼은 이벤트 장([외부 이벤트로 시작하기](message-start.html), [Kafka 연동](event-integration-kafka.html))과 산업 예제가 Kafka로 이벤트를 보내므로 처음부터 Kafka 모드로 띄웁니다.
- **설정 두 개를 덧붙입니다.** `uengine.messaging.require-event-actor: false`와 `esb.inbound-unwrap.enabled: true`입니다. 이유는 아래 「설정 레퍼런스」에 있습니다.
- **게이트웨이 라우트 네 개를 더합니다.** `/search/**`, `/iam/**`, `/business-rules/**`, `/events/**`가 저장소 설정에는 없어 요청이 웹 화면으로 전달됩니다(저장소 `docs/install-issues.md` #23).

!!! note "먼저 알아 둘 것"
    - 기준 브랜치는 uEngine6 `bmt/sds-process-test`(커밋 `0e163f07`), 웹 화면 `sooheon45/process-gpt-vue3-hli`의 같은 이름 브랜치(커밋 `58b5530`)입니다. 다른 브랜치에서는 포트·프로파일이 다를 수 있습니다.
    - **웹 화면 저장소 `sooheon45/process-gpt-vue3-hli`는 지금 비공개입니다.** 받으려면 저장소 접근 권한이 필요합니다. 공개 저장소 `uengine-oss/process-gpt-vue3`로 같은 화면이 나오는지는 확인하지 못했습니다.
    - 영상 촬영 스택은 macOS(Apple Silicon)·Docker Desktop·Homebrew에서 띄웠습니다. Windows에서는 확인하지 못했습니다.
    - 계정 `admin/admin`, `hong/1234`는 저장소 `realm-export.json`에 들어 있는 로컬 개발용 기본값입니다. 실제 설치에서는 바꾸세요.

## 따라 하기

<ol class="steps" markdown="1">
<li markdown="1">**준비물을 설치합니다.** JDK 21(`pom.xml`의 `<java.version>21</java.version>`, 17로는 빌드되지 않습니다), Maven 3.9, Docker, Node.js, Git, Python 3입니다. 영상 촬영 스택은 openjdk 21.0.12, Maven 3.9.12, Node v25.2.1이었습니다. 웹 화면 저장소 `package.json`에는 Node 버전 조건(`engines`)이 없어, 더 낮은 Node 버전에서 동작하는지는 확인하지 못했습니다.

```bash
brew install openjdk@21 maven node
export JAVA_HOME=/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home
export PATH="$JAVA_HOME/bin:$PATH"
java -version          # openjdk version "21.x"
```
</li>
<li markdown="1">**소스를 받습니다.** uEngine6와 웹 화면을 **나란히** 받습니다. 계정계 예제가 포함된 서브모듈도 받습니다(Kafka 설정 파일이 그 안에 있습니다).

```bash
git clone -b bmt/sds-process-test https://github.com/uengine-oss/uEngine6-jdk21.git
git clone -b bmt/sds-process-test https://github.com/sooheon45/process-gpt-vue3-hli.git
cd uEngine6-jdk21
git submodule update --init sample-apps/bpm-sample-app-banking
export UENGINE_HOME="$(pwd)"      # 아래 명령은 모두 이 폴더에서 실행합니다
```
</li>
<li markdown="1">**백엔드를 빌드합니다.** 게이트웨이는 루트 모듈이 아니므로 따로 빌드합니다. `-DskipTests`가 아니라 **`-Dmaven.test.skip=true`**를 쓰세요. `process-service`의 테스트 소스가 본 소스와 맞지 않아 컴파일되지 않습니다(`install-issues.md` #2).

```bash
mvn -B -Dmaven.test.skip=true install
mvn -B -Dmaven.test.skip=true -f keycloak-gateway/pom.xml package
```

`process-service/target/process-service-1.1-SNAPSHOT.jar`, `definition-service/target/definition-service-1.1-SNAPSHOT.jar`, `keycloak-gateway/target/gateway-0.0.1-SNAPSHOT.jar`가 생깁니다.
</li>
<li markdown="1">**PostgreSQL을 띄웁니다.** 저장소의 초기화 SQL(`infra/postgres/init/`의 이벤트 inbox·알림 테이블)을 함께 연결합니다. 이 튜토리얼에서는 다른 프로그램이 5432를 쓰고 있어 **5632**로 띄웠습니다. 5432가 비어 있으면 그대로 써도 되고, 그때는 아래 서비스 명령의 `POSTGRES_PORT`도 바꿉니다.

```bash
docker run -d --name uengine-postgres \
  -e POSTGRES_USER=uengine -e POSTGRES_PASSWORD=uengine -e POSTGRES_DB=uengine -e TZ=Asia/Seoul \
  -p 5632:5432 -v uengine6-pgdata:/var/lib/postgresql/data \
  -v "$UENGINE_HOME/infra/postgres/init:/docker-entrypoint-initdb.d:ro" \
  postgres:16-alpine
until docker exec uengine-postgres pg_isready -U uengine -d uengine; do sleep 2; done
```
</li>
<li markdown="1">**Keycloak을 띄우고 세 가지를 고칩니다.** realm `uengine`은 저장소의 `infra/keycloak/realm-export.json`에서 가져옵니다. `infra/docker-compose.yml`의 Keycloak 18로는 이 파일을 읽지 못하므로 **26.x**를 쓰세요(`install-issues.md` #7).

```bash
docker run -d --name uengine-keycloak -p 8280:8080 \
  -e KC_BOOTSTRAP_ADMIN_USERNAME=admin -e KC_BOOTSTRAP_ADMIN_PASSWORD=admin \
  -e KC_HTTP_ENABLED=true -e KC_HOSTNAME=http://localhost:8280 \
  -v "$UENGINE_HOME/infra/keycloak/realm-export.json:/opt/keycloak/data/import/realm-export.json:ro" \
  quay.io/keycloak/keycloak:26.6.1 start-dev --import-realm
until [ "$(curl -s -o /dev/null -w %{http_code} http://localhost:8280/realms/uengine)" = 200 ]; do sleep 3; done
```

처음 실행할 때는 빌드 단계가 있어 몇 분 걸릴 수 있습니다. 준비되면 `kcadm.sh`로 다음을 고칩니다.

1. **HTTP 허용.** realm 설정이 `sslRequired: external`이라 Docker를 거친 요청이 `HTTPS required`로 막힙니다. `uengine`과 `master` **둘 다** 제한을 해제합니다. `master`를 빠뜨리면 process-service의 Keycloak 관리 API 호출이 오류 표시 없이 실패해 프로세스 시작이 막힙니다.
2. **게이트웨이 주소를 리다이렉트 URI에 추가.** 이 브랜치의 `realm-export.json`에는 클라이언트 `uengine`의 리다이렉트 URI가 `http://localhost:5373/*`, `http://localhost:8088/*` 뿐입니다(커밋 `20e28361`에서 8288이 8088로 바뀜). 그대로 두면 8288 로그인이 `invalid_redirect_uri`로 막힙니다.

```bash
kc() { docker exec uengine-keycloak /opt/keycloak/bin/kcadm.sh "$@"; }
kc config credentials --server http://localhost:8080 --realm master --user admin --password admin
kc update realms/uengine -s sslRequired=NONE
kc update realms/master  -s sslRequired=NONE
CID=$(kc get clients -r uengine -q clientId=uengine --fields id | python3 -c 'import sys,json;print(json.load(sys.stdin)[0]["id"])')
kc update clients/$CID -r uengine \
  -s 'redirectUris=["http://localhost:5373/*","http://localhost:8088/*","http://localhost:8288/*"]'
```
</li>
<li markdown="1">**Kafka를 띄우고 토픽 두 개를 만듭니다.** 저장소의 `infra/docker-compose.infra.yml`에서 ZooKeeper와 Kafka만 올립니다(같은 파일의 Keycloak은 18이라 쓰지 않습니다). 영상 촬영 스택은 계정계 예제의 `sample-apps/bpm-sample-app-banking/docker-compose.yml`로 만든 컨테이너(이미지·리스너 설정이 같음)를 썼고, 아래 `infra/docker-compose.infra.yml` 명령 자체는 확인하지 못했습니다. Compose가 `all predefined address pools have been fully subnetted`로 네트워크를 만들지 못하면 쓰지 않는 Docker 네트워크를 정리합니다(`install-issues.md` #19).

```bash
docker compose -f infra/docker-compose.infra.yml up -d zookeeper kafka
KAFKA=$(docker compose -f infra/docker-compose.infra.yml ps -q kafka)
for t in bpm-topic bpm-brodcast; do
  docker exec $KAFKA kafka-topics --bootstrap-server localhost:9092 --create --if-not-exists --topic $t --partitions 1 --replication-factor 1
done
```

`bpm-topic`은 외부 시스템 → BPM 이벤트와 BPM이 내는 활동 이벤트, `bpm-brodcast`(철자 그대로)는 사람 작업 완료 방송입니다.
</li>
<li markdown="1">**process-service를 Kafka 모드로 띄웁니다.** 설정 파일 세 개를 순서대로 적용합니다. 저장소의 `docs/local/process-service.local.yml`(메일·`basePath`·SQL 함수 등록), 계정계 예제의 `config/process-service.kafka.yml`(Kafka 바인딩), 그리고 이 튜토리얼용 `process-service.tutorial.yml`(아래 「설정 레퍼런스」)입니다.

```bash
SPRING_PROFILES_ACTIVE=postgres,keycloak-installed \
UENGINE_MESSAGING_MODE=kafka KAFKA_BROKERS=localhost:9092 \
UENGINE_BASEPATH="$UENGINE_HOME" POSTGRES_PORT=5632 \
KEYCLOAK_URI=http://localhost:8280 KEYCLOAK_REALM=uengine \
KEYCLOAK_ADMIN_REALM=master KEYCLOAK_ADMIN_CLIENT_ID=admin-cli \
KEYCLOAK_ADMIN_USERNAME=admin KEYCLOAK_ADMIN_PASSWORD=admin \
PROCESS_SERVICE_URL=http://localhost:9294 \
java --add-opens java.base/java.util=ALL-UNNAMED --add-opens java.base/java.lang.reflect=ALL-UNNAMED \
     --add-opens java.base/java.text=ALL-UNNAMED --add-opens java.desktop/java.awt.font=ALL-UNNAMED \
     -Dfile.encoding=UTF-8 -jar process-service/target/process-service-1.1-SNAPSHOT.jar \
     --spring.config.additional-location=file:docs/local/process-service.local.yml,file:sample-apps/bpm-sample-app-banking/config/process-service.kafka.yml,file:process-service.tutorial.yml \
     --server.port=9294
```

- `--add-opens` 네 개가 없으면 작업을 완료할 때 XStream이 `Unable to make private void java.util.HashMap.readObject accessible`로 실패합니다(`install-issues.md` #10).
- `KEYCLOAK_REALM=uengine`을 꼭 설정합니다. 설정하지 않으면 사용자를 `master` realm에서 찾습니다(#12).
- 준비되면 로그에 `Startup definition metadata sync finished: … failed=0`이 기록됩니다. `definitions/`의 정의에서 이벤트 매핑을 읽어 DB에 저장한 것입니다.
</li>
<li markdown="1">**definition-service를 띄웁니다.** `PROCESS_SERVICE_URL`을 꼭 설정합니다. 정의를 저장하면 definition-service가 process-service의 `/definition-changes`를 호출하는데, 기본값이 Docker 서비스 이름(`http://process-service:9094`)이라 로컬에서는 실패합니다.

```bash
SPRING_PROFILES_ACTIVE=postgres,keycloak-installed \
UENGINE_BASEPATH="$UENGINE_HOME" POSTGRES_PORT=5632 \
KEYCLOAK_URI=http://localhost:8280 KEYCLOAK_REALM=uengine \
PROCESS_SERVICE_URL=http://localhost:9294 \
java -Dfile.encoding=UTF-8 -jar definition-service/target/definition-service-1.1-SNAPSHOT.jar \
     --spring.config.additional-location=file:docs/local/definition-service.local.yml \
     --server.port=9293
```

두 서비스의 `basePath`(= `UENGINE_BASEPATH`)는 같아야 합니다. 정의는 `definitions/<경로>.bpmn`에, 실행할 때 읽는 버전 사본은 `archive/<경로>.bpmn/<버전>.bpmn`에 둡니다.
</li>
<li markdown="1">**게이트웨이를 띄웁니다.** 프로파일 `keycloak-installed`를 꼭 설정합니다. 기본 프로파일에는 OAuth2 설정이 없어 로그인 없이 모두 통과합니다. 클라이언트 시크릿은 저장소의 `realm-export.json`에 있는 값을 읽어 전달합니다. 라우트 오버레이 `gateway.tutorial.yml`은 아래 「설정 레퍼런스」에 있습니다.

```bash
GW_SECRET=$(python3 -c 'import json;print(next(c["secret"] for c in json.load(open("infra/keycloak/realm-export.json"))["clients"] if c["clientId"]=="uengine"))')
SPRING_PROFILES_ACTIVE=keycloak-installed GATEWAY_URI=http://localhost:8288 \
KEYCLOAK_URI=http://localhost:8280 KEYCLOAK_REALM=uengine \
KEYCLOAK_CLIENT_ID=uengine KEYCLOAK_CLIENT_SECRET="$GW_SECRET" \
PROCESS_SERVICE_URI=http://localhost:9294 DEFINITION_SERVICE_URI=http://localhost:9293 \
FRONTEND_URI=http://localhost:5373 \
java -Dfile.encoding=UTF-8 -jar keycloak-gateway/target/gateway-0.0.1-SNAPSHOT.jar \
     --server.port=8288 --spring.config.additional-location=file:gateway.tutorial.yml
```
</li>
<li markdown="1">**웹 화면을 빌드해 5373에 띄웁니다.** 개발 서버(`npm run dev`)는 쓰지 않습니다. 프록시가 `/instance`로 시작하는 화면 주소까지 가로채고 대상 포트가 9093/9094로 고정돼 있습니다(`install-issues.md` #22).

```bash
cd ../process-gpt-vue3-hli
npm install --no-audit --no-fund --legacy-peer-deps
NODE_OPTIONS=--max-old-space-size=8192 npm run build
```

빌드한 `dist`에 런타임 주소를 넣습니다. **`index.html`과 `dist/static/config.js`를 둘 다** 고쳐야 합니다. `index.html`이 나중에 `static/config.js`를 `document.write`로 불러 `window._env_`를 8088/8080으로 덮어쓰기 때문입니다.

```bash
python3 - <<'PY'
import pathlib
env = {"VITE_KEYCLOAK_MODE": "installed", "VITE_KEYCLOAK_URL": "http://localhost:8280",
       "VITE_KEYCLOAK_REALM": "uengine", "VITE_KEYCLOAK_CLIENT_ID": "uengine",
       "VITE_GATEWAY_URL": "http://localhost:8288"}
p = pathlib.Path("dist/index.html"); s = p.read_text(encoding="utf-8")
if "window._env_ = {" not in s:
    block = "<script>\nwindow._env_ = {\n" + "".join(f'  {k}: "{v}",\n' for k, v in env.items()) + "};\n</script>\n"
    p.write_text(s.replace("<head>", "<head>\n" + block, 1), encoding="utf-8")
pathlib.Path("dist/static/config.js").write_text(
    "window._env_ = window._env_ || {};\n" + "".join(f"window._env_.{k} = '{v}';\n" for k, v in env.items()), encoding="utf-8")
PY
```

`dist`를 **SPA 폴백**(없는 경로는 `index.html`)이 있는 정적 서버로 5373에 띄웁니다. 저장소의 `server.js`는 CommonJS인데 `package.json`이 `"type": "module"`이라 그대로 실행되지 않습니다(#26). 영상 촬영 스택은 의존성 없는 작은 Node 정적 서버(history 폴백, `.bpmn`이 든 주소도 폴백)를 썼습니다. 저장소 매뉴얼은 `npx --yes serve -s dist -l 5373`을 안내하지만, 이 튜토리얼에서는 그 명령으로 확인하지 못했습니다.
</li>
<li markdown="1">**로그인해 봅니다.** 브라우저에서 **`http://localhost:8288`**을 엽니다(5373이 아닙니다). Keycloak 로그인 화면이 나오면 `hong` / `1234`로 들어갑니다. 업무 목록(`/todolist`)이 보이면 성공입니다.

로그인하지 않은 요청은 게이트웨이가 로그인 화면으로 돌려보냅니다.

```bash
curl -s -o /dev/null -w '%{http_code} %{redirect_url}\n' http://localhost:8288/
# 302 http://localhost:8288/oauth2/authorization/keycloak
```
</li>
<li markdown="1">**API로 정의 목록을 받아 봅니다.** Keycloak에서 토큰을 받아 `Authorization: Bearer`로 요청합니다.

```bash
TOKEN=$(curl -s -d client_id=uengine -d username=hong -d password=1234 \
             -d grant_type=password -d scope=openid \
             http://localhost:8280/realms/uengine/protocol/openid-connect/token \
        | python3 -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')
curl -s -H "Authorization: Bearer $TOKEN" http://localhost:8288/definition/
```

```json
{
  "_embedded" : {
    "definitions" : [ {
      "name" : "test",
      "directory" : true,
      "path" : "test",
      ...
```

`definitions/` 아래 폴더와 정의가 나오면 게이트웨이 → definition-service 연결이 된 것입니다.
</li>
<li markdown="1">**(선택) 가온가전 사용자를 만듭니다.** 저장소 realm에는 `hong`(관리자 역할 `manager`, 그룹 `IT부서`), `admin`, `유` 세 사용자만 있습니다. 이 튜토리얼의 최구매·윤팀장·김대표·이재고·정회계는 ERP 연동 예제의 `scripts/seed-keycloak.mjs`로 만들었습니다. 역할 5개(`purchase`, `purchase-lead`, `ceo`, `warehouse`, `accounting`), 그룹 5개(`경영진`, `구매팀`, `구매결재`, `물류팀`, `회계팀`), 사용자 6명(`kim`, `choi`, `yoon`, `lee`, `jung`, 연동 계정 `bpm-bridge`)을 Keycloak 관리 REST API로 만듭니다. ERP 연동 예제 저장소(`bpm-sample-app-erp`)는 공개 준비 중입니다. 그 전에는 [사용자·그룹·역할](security-keycloak.html) 장의 표대로 Keycloak 관리 콘솔에서 만들어도 됩니다. 화면으로 만드는 법은 [사용자·그룹·역할](security-keycloak.html) 장에 있습니다.

```bash
KEYCLOAK_URL=http://localhost:8280 KEYCLOAK_REALM=uengine \
KEYCLOAK_ADMIN=admin KEYCLOAK_ADMIN_PASSWORD=admin node scripts/seed-keycloak.mjs
```
</li>
</ol>

## 설정 레퍼런스

### 서비스별 환경 변수

| 변수 | 서비스 | 값(이 튜토리얼) | 없으면 |
|---|---|---|---|
| `SPRING_PROFILES_ACTIVE` | process · definition | `postgres,keycloak-installed` | 포트가 9094/9093, DataSource가 WAS JNDI(`dev`) |
| `SPRING_PROFILES_ACTIVE` | gateway | `keycloak-installed` | 로그인 없이 모두 통과 |
| `UENGINE_BASEPATH` | process · definition | 저장소 루트 | 정의를 못 찾음. 두 서비스가 같아야 함 |
| `POSTGRES_PORT` | process · definition | `5632` | `5432` |
| `KEYCLOAK_URI` · `KEYCLOAK_REALM` | process · definition · gateway | `http://localhost:8280` · `uengine` | process는 사용자를 `master`에서 찾음 |
| `KEYCLOAK_ADMIN_*` | process | `master` · `admin-cli` · `admin` · `admin` | 그룹·사용자 조회(관리 API) 실패 |
| `UENGINE_MESSAGING_MODE` · `KAFKA_BROKERS` | process | `kafka` · `localhost:9092` | `polling`(DB inbox) |
| `PROCESS_SERVICE_URL` | process · definition | `http://localhost:9294` | 정의 저장 뒤 `/definition-changes` 호출 실패 |
| `GATEWAY_URI` · `FRONTEND_URI` | gateway | `http://localhost:8288` · `http://localhost:5373` | 로그인 리다이렉트·화면 라우팅 실패 |
| `PROCESS_SERVICE_URI` · `DEFINITION_SERVICE_URI` | gateway | `:9294` · `:9293` | 기본값도 같음 |
| `KEYCLOAK_CLIENT_ID` · `KEYCLOAK_CLIENT_SECRET` | gateway | `uengine` · realm-export의 값 | 로그인 실패 |

### `process-service.tutorial.yml`

```yaml
uengine:
  messaging:
    require-event-actor: false   # 아래 패치가 있어야 효과가 있습니다
esb:
  inbound-unwrap:
    enabled: true
```

| 설정 | 왜 필요한가 |
|---|---|
| `uengine.messaging.require-event-actor: false` | 이 브랜치에 들어온 커밋 `9ee91cf3`(inbox 작업 소유자 검사) 이후, Kafka 이벤트로 사람 작업을 끝내려면 헤더 `emnb`(행위자)와 선점이 꼭 있어야 합니다. 계정계 예제처럼 **시스템이 행위자 없이** 이벤트를 보내는 연동은 첫 단계에서 `header.emnb is required to complete a work item`으로 멈춥니다. 이 스위치를 끄면 행위자 헤더가 **없는** 이벤트만 소유자 검사를 건너뜁니다. 헤더가 있으면 그대로 검사합니다. |
| `esb.inbound-unwrap.enabled: true` | 업무 목록의 「선택 N건 선점」(`POST /instance/multi-claim`)은 선점하는 사람·기관을 ESB 봉투 `{ "header": { "emnb", "belnOrgnCode" }, "payload": { … } }`로만 받습니다. 저장소 `application.yml`은 봉투를 푸는 기능이 꺼져 있어(`enabled: false`) 선점이 항상 `LBM050003`·`LBM050002`로 실패합니다. 봉투가 없는 본문은 그대로 통과하므로 다른 API에는 영향이 없습니다. |

!!! warning "`require-event-actor`는 저장소에 아직 없는 스위치입니다"
    `bmt/sds-process-test`의 `AsyncEventListener`에는 이 설정을 읽는 코드가 없습니다. 영상 촬영 스택은 아래 13줄을 더해 빌드했습니다(기본값 `true`라 설정하지 않으면 원래 동작과 같습니다). 행위자 없는 시스템 이벤트로 사람 작업을 끝내는 연동(계정계 예제)을 따라 하지 않는다면 이 패치와 설정은 없어도 됩니다.

```diff
--- a/process-service/src/main/java/org/uengine/five/service/AsyncEventListener.java
+++ b/process-service/src/main/java/org/uengine/five/service/AsyncEventListener.java
+import org.springframework.beans.factory.annotation.Value;
 ...
+    @Value("${uengine.messaging.require-event-actor:true}")
+    boolean requireEventActor = true;
 ...
         if (!UEngineUtil.isNotEmpty(actorEndpoint)) {
+            if (!requireEventActor) {
+                // 행위자 없는 시스템 이벤트: 소유자 검증 없이 완료 (onComplete 가 열린 워크아이템 1건을 닫는다)
+                return;
+            }
             throw new NonRetryableInboxException("header.emnb is required to complete a work item");
         }
```

### `gateway.tutorial.yml`

Spring은 `routes` 목록을 합치지 않고 통째로 바꾸므로, 저장소의 라우트를 모두 다시 적고 process-service 쪽에 네 경로를 더합니다. 웹 화면으로 가는 `/**`는 반드시 마지막에 둡니다.

```yaml
spring:
  config:
    activate:
      on-profile: keycloak-installed
  cloud:
    gateway:
      routes:
        - id: execution
          uri: ${EXECUTION_SERVICE_URI:http://localhost:8200}
          predicates:
            - Path=/complete/**, /vision-complete/**, /execution/**
          filters:
            - RewritePath=/execution/?(?<segment>.*), /$\{segment}
        - id: definition-servicce
          uri: ${DEFINITION_SERVICE_URI:http://localhost:9293}
          predicates:
            - Path=/definition/**, /version/**, /versions/**
        - id: instance-servicce
          uri: ${PROCESS_SERVICE_URI:http://localhost:9294}
          predicates:
            - Path=/worklist/**, /test/**, /instance/**, /work-item/** , /instances/**, /dry-run/**, /validate/**, /start-and-complete, /notifications/**, /sql-metadata/**, /rpa/**, /search/**, /iam/**, /business-rules/**, /events/**
        - id: analytics-service
          uri: ${ANALYTICS_SERVICE_URI:http://localhost:9295}
          predicates:
            - Path=/api/analytics/**
        - id: frontend
          uri: ${keycloak-client.frontend-uri}
          predicates:
            - Path=/**
```

[ERP 예제](industry-erp-purchase.html)를 따라 하려면 `frontend` 앞에 `/erp/**`·`/erp-bridge/**` 라우트를 더합니다.

### 웹 화면 수정 두 가지

영상 촬영 스택의 웹 화면은 저장소에서 아래 두 곳을 고친 뒤 빌드했습니다.

| 파일 | 고친 것 | 고치지 않으면 |
|---|---|---|
| `vite.config.ts` | `build.rollupOptions.external`에서 `'xlsx'`를 빼고, `globals`의 `xlsx`도 뺍니다 | `/definitions-tree`가 백지(`install-issues.md` #24) |
| `src/components/api/UEngineBackend.ts`, `src/components/apps/todolist/TodolistCard.vue` | 「선택 N건 선점」이 `POST /instance/multi-claim`을 봉투 `{ header: { emnb: <로그인 사용자>, belnOrgnCode: <작업의 그룹> }, payload: { dvsnVal, bswrList } }`로 보내고, 응답의 `payload`를 읽습니다 | 선점 버튼이 늘 실패(위 `esb.inbound-unwrap`와 한 쌍) |

### 다시 띄울 때와 정리

| 하고 싶은 것 | 명령 |
|---|---|
| 서비스만 내리기 | 각 `java -jar`와 정적 서버를 끕니다(`lsof -tiTCP:9294 -sTCP:LISTEN`으로 pid 확인) |
| 인프라 내리기 | `docker stop uengine-keycloak uengine-postgres` · `docker compose -f infra/docker-compose.infra.yml stop` |
| 처음 상태로 | `docker rm -f uengine-keycloak uengine-postgres && docker volume rm uengine6-pgdata` |

Kafka에 예전 메시지가 남은 상태에서 처음 연결하는 컨슈머 그룹(`bpm`)으로 접속하면, Spring Cloud Stream이 처음부터(`earliest`) 읽어 옛 이벤트를 다시 처리합니다. 예전 Kafka를 다시 쓴다면 process-service를 띄우기 전에 그룹의 읽기 위치를 최신으로 설정해 두세요.

```bash
docker exec $KAFKA kafka-consumer-groups --bootstrap-server localhost:9092 \
  --group bpm --topic bpm-topic --reset-offsets --to-latest --execute
```

## 알려진 제약

| 증상 | 원인·우회 |
|---|---|
| 업무 목록 「완료됨」 칸이 늘 비어 있음 | 이 브랜치의 결함(#30). 완료 여부는 관리자 화면(`/admin/<인스턴스>`)에서 봅니다 |
| 화면이 저절로 새로 고쳐지지 않음 | Kafka 모드에서는 `/events/stream`(SSE)이 404입니다. 업무 목록의 새로고침 아이콘을 누릅니다 |
| `/analytics` 백지, KPI 화면 오류 | 분석 서비스(`analytics`, :9295)를 띄우지 않았기 때문입니다. [분석과 KPI](analytics-kpi.html) 장 참고 |
| `GET /versions` 500 | `Range [10, 9) out of bounds`(#17). 버전 목록 화면은 쓰지 않습니다 |
| `oracle` 프로파일 기동 실패 | #4. 이 튜토리얼은 PostgreSQL만 씁니다 |
| 로그인·화면 이동이 수십 초 | 영상 촬영 PC는 다른 컨테이너로 Docker VM 부하가 높아 Keycloak이 간헐적으로 멈췄습니다. 부하가 낮을 때 처음부터 모두 띄우는 데 81초 걸렸습니다 |

!!! note "저장소 매뉴얼과 달라진 점"
    `docs/local-install-guide.md`(2026-08-19 검증)에는 「`roleMappings` 의 `endpoints` 는 이메일」, 「게이트웨이는 세션 쿠키와 Bearer 가 둘 다 필요」, 「업무 상세가 500」이라고 적혀 있습니다. 이 튜토리얼의 브랜치 상태에서는 셋 다 다릅니다. 사용자 ID는 토큰의 `preferred_username`(`hong`)이고(`SecurityAwareServletFilter`), 게이트웨이는 Bearer만으로도 통과하고, 업무 상세(`GET /work-item/<id>`)는 200입니다. 자세한 내용은 [API로 같은 일 하기](quickstart-api.html)에 있습니다.

## 확인 문제

<details class="answer" markdown="1"><summary>브라우저로 `http://localhost:5373`에 바로 들어가면 안 되나요?</summary>

안 됩니다. 5373은 웹 화면 파일만 제공하는 정적 서버입니다. 로그인과 API 요청의 라우팅은 게이트웨이(8288)가 처리하므로 늘 `http://localhost:8288`로 들어갑니다.
</details>

<details class="answer" markdown="1"><summary>process-service와 definition-service의 `UENGINE_BASEPATH`를 다르게 주면 어떻게 되나요?</summary>

모델러에서 저장한 정의는 definition-service의 `basePath` 아래 `definitions/`·`archive/`에 쓰입니다. process-service는 자신의 `basePath`에서 정의를 읽으므로, 다르면 저장한 정의를 찾지 못해 실행할 수 없습니다.
</details>

<details class="answer" markdown="1"><summary>로그인하면 Keycloak이 `invalid_redirect_uri`를 보여 줍니다. 무엇을 확인해야 하나요?</summary>

클라이언트 `uengine`의 리다이렉트 URI에 `http://localhost:8288/*`가 있는지 확인합니다. 이 브랜치의 `realm-export.json`에는 8088만 들어 있어 5단계의 `kcadm.sh update clients/…`로 더해야 합니다.
</details>
