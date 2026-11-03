# 플러그인과 REST·MCP 연동

> 코어를 고치지 않고 SQL 파일 하나로 포인트 플러그인을 붙입니다. 연동 키를 만들어 REST 를 호출하고 MCP 클라이언트로 도구를 부릅니다.

## 무엇을 · 왜

플러그인도 모듈과 같은 방식으로 이벤트를 구독합니다. 판매 모듈은 플러그인이 있는지 모릅니다.

| 길 | 주소 | 인증 | 하는 일 |
|---|---|---|---|
| REST | `/rest/v1/erp_api_<유형>` | 구성원의 로그인 토큰 | 유형마다 자동으로 생기는 자원. 한 요청에 한 건 |
| MCP | `/rest/v1/rpc/erp_mcp` | 연동 키(`x-erp-key`) | 도구 4개로 켜져 있는 모듈의 문서를 다룸 |
| 이벤트 | `erp_event_feed` | 로그인 토큰 | 원장을 순서대로 읽기 |

!!! note "먼저 알아 둘 것"
    - 가온가전은 가상 회사이고, 수치는 모두 가상 회사의 것입니다. 화면은 로컬 Supabase 로 찍었습니다.
    - **에이전트 제품에 실제로 붙여 찍지 않았습니다.** 여기서는 공식 SDK 로 만든 MCP 클라이언트로 호출했습니다.
    - 플러그인은 코어와 같은 데이터베이스 권한으로 돕니다. 권한 격리는 코드 검토에 달려 있으니, 믿을 수 있는 SQL 만 실행하세요.
    - 저장소 링크는 공개된 뒤에 열립니다. 대시보드의 SQL Editor 로 플러그인을 넣는 단계는 아직 클라우드에서 확인하지 못했습니다. 무료 플랜의 속도도 재지 않았습니다.

## 따라 하기

[앞 장](whatif.html)과 같은 가상 회사에 관리자로 로그인합니다. 플러그인 파일은 저장소의 [`plugins/points.sql`](https://github.com/uengine-oss/uengine-erp/blob/main/plugins/points.sql)(38줄)과 [`plugins/points-uninstall.sql`](https://github.com/uengine-oss/uengine-erp/blob/main/plugins/points-uninstall.sql) 입니다.

<ol class="steps" markdown="1">
<li markdown="1">**플러그인 파일 읽기.** 포인트 유형을 등록하고, `SalesOrderConfirmed` 와 `SalesOrderCancelled` 를 구독하는 처리기를 둡니다.

![플러그인 파일](img/connect-file.webp)
</li>
<li markdown="1">**설치.** SQL Editor 에 붙여 넣어 실행합니다. 녹화에서는 로컬 데이터베이스에 바로 실행했습니다.

```bash
docker exec -i supabase_db_uengine-erp psql -q -U postgres -d postgres < plugins/points.sql
```

![설치](img/connect-install.webp)
</li>
<li markdown="1">**켜기.** 앱을 새로 고치고 **설정 → 모듈** 에서 포인트 카드의 **켜기** 를 누릅니다. 메뉴에 **포인트** 가 생깁니다.

![포인트 카드](img/connect-card.webp)
</li>
<li markdown="1">**주문 확정.** 고객 `가온마트 본점`, 창고 `수도권 창고`, 제습기 1개로 주문을 확정합니다. 공급가액은 289,000 입니다.
</li>
<li markdown="1">**포인트 확인.** **포인트** 화면에 그 주문의 포인트 2,890 이 있습니다. 공급가액의 1/100 입니다.

![포인트](img/connect-points.webp)
</li>
<li markdown="1">**되돌리기.** 주문의 이력에서 `주문 확정` 의 **이 작업 되돌리기** 를 누릅니다. 미리보기에 `모듈이 달라도 함께 되돌아갑니다 (판매, 포인트, 재고)` 가 나옵니다. 사유를 적고 실행하면 포인트 목록이 비어 있습니다.

![미리보기](img/connect-preview.webp)
</li>
<li markdown="1">**제거.** `plugins/points-uninstall.sql` 을 실행합니다. 플러그인의 함수와 자원이 사라지고, `PointsEarned` 이벤트는 일어난 일로 원장에 남습니다.

```bash
docker exec -i supabase_db_uengine-erp psql -q -U postgres -d postgres < plugins/points-uninstall.sql
```

![제거](img/connect-remove.webp)
</li>
<li markdown="1">**코어 확인.** 앱을 새로 고치면 포인트 메뉴와 카드가 없습니다. 다섯 모듈은 그대로 켜져 있고 주문도 그대로입니다.
</li>
<li markdown="1">**연동 키 만들기.** **설정 → 연동 → 연동 키 만들기** 에서 이름을 적고, **이 구성원의 권한으로 동작** 에서 구성원을 고릅니다. 이 키로 하는 모든 일은 그 구성원이 한 것으로 원장에 남고, 그 구성원의 역할만큼만 할 수 있습니다. 필요한 역할만 가진 구성원을 따로 만들어 쓰세요.

![연동 키 만들기](img/connect-key.webp)
</li>
<li markdown="1">**키 복사.** 키는 한 번만 보여 줍니다. 화면을 떠나면 다시 볼 수 없고, 데이터베이스에는 해시만 남습니다. 표에는 앞자리만 보입니다. 아래 그림은 키와 공개 키를 가렸습니다.

![키는 한 번만](img/connect-once.webp)
</li>
<li markdown="1">**REST 호출.** 거래처를 읽고, 하나 만들고, 원장의 출처를 봅니다. 환경 변수 `API_URL`, `ANON_KEY`, `TOKEN`(구성원의 로그인 토큰)을 먼저 정합니다.

```bash
curl -s "$API_URL/rest/v1/erp_api_partner?select=name,region&region=eq.호남&limit=2" \
  -H "apikey: $ANON_KEY" -H "Authorization: Bearer $TOKEN"
curl -s -X POST "$API_URL/rest/v1/erp_api_partner" \
  -H "apikey: $ANON_KEY" -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" -H "Prefer: return=representation" \
  -d '{"name":"REST 거래처","region":"수도권"}'
curl -s "$API_URL/rest/v1/erp_events?select=event_type,source&order=seq.desc&limit=1" \
  -H "apikey: $ANON_KEY" -H "Authorization: Bearer $TOKEN"
```

녹화에서는 호남 거래처 2곳을 읽고, `REST 거래처` 를 버전 1 로 만들고, 원장에서 `{"event_type":"PartnerCreated","source":"api"}` 를 확인했습니다.

![REST](img/connect-rest.webp)
</li>
<li markdown="1">**MCP 호출.** 로그인 없이 연동 키만 씁니다. 연동 화면의 예시를 그대로 쓰면 도구 목록을 받습니다.

```bash
curl -s "$API_URL/rest/v1/rpc/erp_mcp" -H "apikey: $ANON_KEY" -H "x-erp-key: $ERP_KEY" \
  -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

녹화에서는 공식 MCP SDK(`@modelcontextprotocol/sdk`)로 만든 작은 클라이언트로 불렀습니다. 도구는 `erp_read, erp_create, erp_update, erp_delete` 4개입니다. 박영업의 키로 거래처를 읽고 만들면 원장의 출처가 `mcp` 로 남고, 박영업의 권한 밖인 전표 쓰기는 `ERP_FORBIDDEN` 으로 거부됩니다.

![MCP](img/connect-mcp.webp)
</li>
<li markdown="1">**키 폐기.** 키 줄의 **폐기** 를 누릅니다. 되살릴 수 없습니다. 같은 클라이언트를 다시 실행하면 연결을 거부당합니다.

![폐기 뒤](img/connect-revoked.webp)
</li>
</ol>

## 확인 문제

<details class="answer" markdown="1"><summary>플러그인을 지우면 그동안 쌓인 포인트 이벤트도 사라지나요?</summary>
사라지지 않습니다. 함수와 자원만 지웁니다. 이벤트는 일어난 일로 원장에 남습니다.
</details>

<details class="answer" markdown="1"><summary>REST 와 MCP 의 인증이 다른 이유는 무엇인가요?</summary>
로그인 토큰은 1시간이면 만료되므로 오래 도는 에이전트에 맞지 않습니다. MCP 는 구성원에 묶인 장기 연동 키를 쓰고, REST 는 구성원의 로그인 토큰으로 부릅니다.
</details>

<details class="answer" markdown="1"><summary>연동 키가 유출되면 어떻게 하나요?</summary>
키 줄에서 폐기합니다. 데이터베이스에는 해시만 있고, 키는 그 구성원의 권한을 넘지 못합니다. 그래서 필요한 역할만 가진 구성원을 따로 만들어 키를 묶는 것이 좋습니다.
</details>
