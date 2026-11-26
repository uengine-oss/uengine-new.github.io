# 골든 퀘스천 5개 묻기

> Neo4j MCP를 연결한 세션에서 골든 퀘스천 5개를 묻고, Claude가 호출한 도구와 Cypher, 답을 실제 기록으로 살펴봅니다. 답마다 근거 조문을 원문과 대조하고, 같은 질문을 15번 실행한 기록으로 호출 수·시간·오류를 측정합니다.

## 무엇을 · 왜

[5장](schema.html)에서 스키마를 설계할 때 출발점이었던 질문 다섯 개를 이제 실제로 묻습니다. [8장](mcp.html)에서 다시 연 세션은 앞선 설계·적재 대화가 없는 **새 세션**이고, Claude는 파일을 하나도 읽지 않고(Read·Bash 호출 0번) MCP 도구 두 개만으로 답했습니다. 이 장에서는 그래프가 답의 근거를 제대로 제공하는지 확인하고, 그 답을 검증하는 방법을 살펴봅니다.

아래 「질문별 기록」과 「같은 질문을 15번」은 원 교재(macOS, 법령 9개 그래프)의 실행 기록입니다. 다섯 질문의 근거 조문은 모두 위험물안전관리법 3종에 있어, 이 교재의 그래프에서도 같은 조문에 도달하는 것이 정상입니다. 다만 그래프가 작아 Claude가 받는 결과 행 수와 시간·비용은 원 교재보다 적게 나올 수 있습니다. 여러분의 답을 이 기록과 원문에 대조해 채점하세요.

!!! tip "시작하기 전에"
    8장에서 `/mcp`에 `✔ neo4j`가 보였어야 합니다. 질문의 답을 원문과 대조할 수 있도록 `pdf\` 폴더의 PDF 3개나 국가법령정보센터 화면을 옆에 열어 둡니다.

## 따라 하기

<ol class="steps" markdown="1">
<li markdown="block">**MCP가 연결된 세션을 엽니다.** 새 PowerShell 창이라면 8장처럼 `Set-Location C:\lab\law-graph; . .\env.ps1` 뒤 `claude`를 실행하고, `/mcp`에서 `✔ neo4j`를 확인합니다.

**왜 하나요?** 앞 장의 대화가 남아 있지 않은 새 세션에서 물어야 Claude가 그래프만 보고 답하는지 공정하게 평가할 수 있습니다.
</li>
<li markdown="block">**질문을 하나씩 붙여 넣습니다.** 골든 퀘스천 원문 뒤에 같은 문구 하나만 붙입니다. 그래프 구조에 대한 힌트는 주지 않습니다.

**왜 하나요?** 그래프 구조에 대한 힌트 없이 질문 원문만 주어야, 실제 사용자가 물었을 때와 같은 조건에서 그래프가 답의 근거를 제공하는지 볼 수 있습니다.

```text
제조소등에서 위치·구조·설비 변경 없이 저장·취급하는 위험물의 품명·수량(지정수량 배수)을 바꾸려면 언제까지 누구에게 신고해야 하는가? Neo4j 에서 찾아 근거 조문과 함께 답해 줘.
위험물안전관리자가 해임되거나 퇴직하면 관계인은 며칠 안에 다시 선임해야 하고, 선임한 뒤에는 어떤 절차를 밟아야 하는가? Neo4j 에서 찾아 근거 조문과 함께 답해 줘.
정기점검을 마친 제조소등의 관계인은 점검 결과를 언제까지 누구에게 제출해야 하는가? Neo4j 에서 찾아 근거 조문과 함께 답해 줘.
제조소등에서 위험물 유출 사고가 발생했을 때 관계인과 이를 발견한 사람은 각각 무엇을 해야 하며, 관계인이 응급조치를 하지 않으면 누가 명령할 수 있는가? Neo4j 에서 찾아 근거 조문과 함께 답해 줘.
안전관리자 선임 의무(제15조)나 정기점검 의무(제18조)를 지키지 않으면 어느 벌칙·과태료 조항이 적용되는가? Neo4j 에서 찾아 근거 조문과 함께 답해 줘.
```
</li>
<li markdown="block">**도구 호출을 펼쳐 봅니다.** 답 위에 `Called neo4j 3 times (ctrl+o to expand)`처럼 도구 호출 내역이 접힌 상태로 호출 수가 표시됩니다. ctrl+o로 펼치면 Claude가 작성한 Cypher와 반환된 결과를 볼 수 있습니다. 첫 호출 때 나오는 권한 요청에는 8장에서 본 대로 응답합니다.

**왜 하나요?** 답만 보면 맞았는지 우연인지 알 수 없습니다. Claude가 어떤 Cypher로 어떤 조문을 가져왔는지 보면 답의 근거를 추적할 수 있고, 틀렸을 때 원인(검색 조건, 그래프 데이터)을 찾을 수 있습니다.
</li>
<li markdown="block">**답의 근거 조문을 원문과 대조합니다.** 답에 인용된 조문 번호를 국가법령정보센터나 실습 폴더의 `pdf/`에서 찾아 문구를 대조합니다. 아래 「질문별 기록」의 판정은 이렇게 대조한 결과입니다.

**왜 하나요?** 법령 답변은 틀리면 실무에 그대로 피해가 갑니다. AI가 인용한 조문을 원문과 글자까지 맞춰 보는 것이 이 실습의 최종 검증입니다.
</li>
</ol>

## 질문별 기록

| Q | 호출 | 시간 | 답의 결론 | 원문 대조 |
|---|---|---|---|---|
| 1 | get-schema 1 + read-cypher 4 | 39.3초 | 변경하고자 하는 날의 1일 전까지 시ㆍ도지사에게 | 맞음 |
| 2 | read-cypher 3 | 25.3초 | 30일 이내 재선임, 14일 이내 소방본부장 또는 소방서장에게 신고 | 맞음 |
| 3 | read-cypher 4(오류 1) | 25.6초 | 점검을 한 날부터 30일 이내 시ㆍ도지사에게 | 맞음 |
| 4 | read-cypher 3 | 21.6초 | 관계인 즉시 응급조치, 발견자 즉시 통보, 소방본부장 또는 소방서장이 명령 | 맞음 + 데이터 오류 발견 |
| 5 | read-cypher 3 | 23.4초 | 9개 호(벌칙 6 · 과태료 3) | 맞음 |

시간은 질문을 입력한 시점부터 마지막 기록까지이며, 권한 요청에 대한 응답을 기다린 시간도 포함합니다. 모델이 작성하는 Cypher와 문장은 실행할 때마다 달라질 수 있습니다.

### 1번 — 품명·수량 변경 신고

Claude는 먼저 MCP 도구 정의를 불러오고(`ToolSearch`) `get-schema`로 스키마(9,111자)를 받은 뒤, 의미층(Norm)에서 「품명」을 찾았습니다.

```cypher
MATCH (n:Norm)-[:BASED_ON]->(p) WHERE n.object CONTAINS '품명' OR n.trigger CONTAINS '품명' OR n.action CONTAINS '품명' OR p.text CONTAINS '품명'
OPTIONAL MATCH (n)-[:HAS_SUBJECT]->(s:Actor) OPTIONAL MATCH (n)-[:ADDRESSED_TO]->(r:Actor)
RETURN n.normId, n.name, n.modality, n.trigger, n.action, n.object, n.deadlineText, n.deadlineKind, n.deadlineValue, n.deadlineUnit,
       n.subjectText, n.recipientText, n.reviewed, n.uncheckedFields, s.name, r.name, p.citation, p.pid, p.isCurrent, p.text LIMIT 30
```

이어서 조문 텍스트를 검색하고, `pid`로 시행령 제21조·법 제39조제1항·제6조제3항을 조회한 뒤 법령 판본을 확인했습니다. 답의 요지는 변경하고자 하는 날의 **1일 전까지 시ㆍ도지사**에게 신고(법 제6조제2항), 수리 권한은 소방서장에게 위임(시행령 제21조제2호)되어 실제 신고서는 별지 제19호서식으로 시ㆍ도지사 또는 소방서장에게 제출(시행규칙 제10조), 위반 시 500만원 이하의 과태료(법 제39조제1항제3호)였습니다.

**판정: 맞음.** 법 제6조제2항 「… 위험물의 품명ㆍ수량 또는 지정수량의 배수를 변경하고자 하는 자는 변경하고자 하는 날의 1일 전까지 행정안전부령이 정하는 바에 따라 시ㆍ도지사에게 신고하여야 한다.」, 시행령 제21조제2호 「법 제6조제2항의 규정에 의한 위험물의 품명ㆍ수량 또는 지정수량의 배수의 변경신고의 수리」.

### 2번 — 안전관리자 재선임과 신고

조문 텍스트 검색, Norm 검색, 하위법령 조회 순으로 세 번 질의했습니다(과정은 아래 「동작 과정 다시 보기」에 나옵니다). 답의 요지는 해임·퇴직한 날부터 **30일 이내** 재선임(법 제15조제2항), 선임한 날부터 **14일 이내** 소방본부장 또는 소방서장에게 신고(제15조제3항), 별지 제32호서식과 첨부서류(시행규칙 제53조제1항), 공백 기간의 대리자 지정과 30일 한도(제15조제5항), 미선임 1천500만원 이하의 벌금(제36조제6호), 선임신고 지연·허위 500만원 이하의 과태료(제39조제1항제5호)였습니다.

**판정: 맞음.** 법 제15조제2항 「… 해임하거나 퇴직한 날부터 30일 이내에 다시 안전관리자를 선임하여야 한다.」, 제3항 「… 선임한 날부터 14일 이내에 행정안전부령으로 정하는 바에 따라 소방본부장 또는 소방서장에게 신고하여야 한다.」

### 3번 — 정기점검 결과 제출: Cypher 오류를 스스로 고친 장면

첫 질의는 조문 텍스트·Sanction·Norm·Actor를 한 번에 연결하고 `collect`로 모은 뒤 `ORDER BY p.lawId`로 정렬하려다 실패했습니다.

```text
error during GetQueryType: Neo4jError: Neo.ClientError.Statement.SyntaxError (In a WITH/RETURN with DISTINCT or an aggregation, it is not possible to access variables declared before the WITH/RETURN: p (line 6, column 244 (offset: 571))
```

집계(`collect`)를 한 뒤에는 집계 전 변수(`p`)를 `ORDER BY`에 쓸 수 없다는 뜻입니다. Claude는 오류를 읽고 질의를 나눴습니다. 집계가 없는 질의로 법 제18조·제39조제1항, 시행규칙 제64조·제68조를 `pid`로 조회하고, Norm 하나만 따로 가져왔습니다.

```cypher
MATCH (n:Norm)-[:BASED_ON]->(p {pid:'위험물안전관리법:제18조:제2항'})
OPTIONAL MATCH (n)-[:ADDRESSED_TO]->(r:Actor) OPTIONAL MATCH (n)-[:HAS_SUBJECT]->(sj:Actor)
RETURN n.normId, n.action, n.object, n.trigger, n.deadlineText, n.deadlineValue, n.deadlineUnit, n.deadlineKind,
       n.reviewed, n.uncheckedFields, collect(DISTINCT sj.name) AS subj, collect(DISTINCT r.name) AS recip
```

```text
"n.deadlineText": "점검을 한 날부터 30일 이내", "n.deadlineValue": 30, "n.deadlineUnit": "일",
"n.reviewed": false, "recip": ["시ㆍ도지사"], "subj": ["관계인"], …
```

답의 요지는 점검을 한 날부터 **30일 이내 시ㆍ도지사**에게 제출(법 제18조제2항), 수리는 소방서장에게 위임(시행령 제21조제11호), 미제출 500만원 이하의 과태료(제39조제1항제7호의2)였고, 점검 대상(시행령 제16조)·연 1회 이상(시행규칙 제64조)·기록 보존(시행규칙 제68조)을 덧붙였습니다. 제출 서식을 정한 시행규칙 조문은 그래프에서 찾지 못해 답에 넣지 못했다는 한계도 밝혔습니다.

**판정: 맞음.** 법 제18조제2항 「제1항에 따라 정기점검을 한 제조소등의 관계인은 점검을 한 날부터 30일 이내에 점검결과를 시ㆍ도지사에게 제출하여야 한다.」, 시행령 제21조제11호 「법 제18조제2항에 따른 정기점검 결과의 수리」.

### 4번 — 유출 사고: 데이터 오류를 찾아낸 장면

Claude는 제27조의 Norm을 `WITH`로 먼저 모은 뒤 결과를 받았습니다(3번에서 발생한 오류를 피한 것으로 보입니다).

```cypher
MATCH (n:Norm)-[:BASED_ON]->(p) WHERE p.pid STARTS WITH '위험물안전관리법:제27조'
OPTIONAL MATCH (n)-[:ADDRESSED_TO]->(r:Actor) OPTIONAL MATCH (n)-[:HAS_SUBJECT]->(sj:Actor)
WITH n, p, collect(DISTINCT sj.name) AS subj, collect(DISTINCT r.name) AS recip
RETURN n.normId, n.modality, n.action, n.object, n.trigger, n.deadlineText, n.subjectText, n.recipientText,
       n.reviewed, n.uncheckedFields, subj, recip, p.citation ORDER BY n.normId
```

제2항에 해당하는 행에서 `"recip": ["경찰서", " 밖의 관계기관", "소방서"]`가 반환되었고, Claude는 답 끝에 이렇게 적었습니다.

```text
제27조제2항 Norm의 수신 Actor 중 하나가 이름이 " 밖의 관계기관"으로 저장되어 있습니다. "그 밖의 관계기관"에서 앞 글자
"그"가 잘린 추출 오류로 보입니다.
```

[7장](disambiguation.html)에서 묶음 이름을 쪼갤 때 생긴 오류(GL-14)입니다. Claude는 Norm이 `reviewed=false`라서 값만 믿지 않고 조문 원문과 대조했다고 밝혔고, 답의 결론은 원문에서 가져왔습니다.

**판정: 맞음.** 법 제27조제1항 「제조소등의 관계인은 당해 제조소등에서 위험물의 유출 그 밖의 사고가 발생한 때에는 즉시 그리고 지속적으로 … 응급조치를 강구하여야 한다.」, 제2항 「제1항의 사태를 발견한 자는 즉시 그 사실을 소방서, 경찰서 또는 그 밖의 관계기관에 통보하여야 한다.」, 제3항 「소방본부장 또는 소방서장은 제조소등의 관계인이 제1항의 응급조치를 강구하지 아니하였다고 인정하는 때에는 제1항의 응급조치를 강구하도록 명할 수 있다.」 명령 위반은 제36조제15호(1천500만원 이하의 벌금)에 해당합니다.

### 5번 — 벌칙·과태료: 여러 조문을 연결하는 질문

의무 조항(제15조·제18조)과 관련된 벌칙을 찾으려면 한 조문만으로는 답할 수 없습니다. 의무 조항 ←`PENALIZES`— 벌칙 호 ←`HAS_PART`— 벌칙 조 —`IMPOSES`→ 제재(Sanction)로 세 단계를 거쳐야 합니다. Claude의 첫 질의는 이 경로를 한 번에 탐색했습니다.

```cypher
MATCH (i)-[r:PENALIZES]->(t) WHERE t.lawId='위험물안전관리법' AND t.articleNo IN [15,18]
OPTIONAL MATCH (parent)-[:HAS_PART*1..2]->(i) WHERE (parent)-[:IMPOSES]->()
OPTIONAL MATCH (parent)-[:IMPOSES]->(s:Sanction)
RETURN i.pid, i.isCurrent, i.text, r.raw, t.pid, parent.pid, parent.text, s.type, s.text, s.maxFineWon, s.maxPrisonMonths ORDER BY i.order, t.pid
```

`PENALIZES` 10건(호 9개, 제36조제6호가 제15조 ①·② 두 항을 가리킴)이 반환되었습니다. [6장](ingest.html)에서 Neo4j Browser로 그린 것과 같은 경로입니다.

![Neo4j Browser: 제15조·제18조의 항 ←PENALIZES— 벌칙 호 ←HAS_PART— 벌칙 조·항 —IMPOSES→ 제재(금액). 노드 28 · 관계 32](img/gl-04b-penalty.webp)

![같은 경로를 테이블로: 의무 조항, 벌칙 조항, 제재 10행](img/gl-04b-penalty-table.webp)

Claude는 두 번째 질의로 벌칙 장과 제12조·제13조 원문에서 「제15조」「제18조」「안전관리자」「정기점검」을 문자열로 다시 찾아 `PENALIZES`에 빠진 호가 없는지 확인했고, 제12조의 허가취소·사용정지 사유도 덧붙였습니다. 양벌규정(제38조)은 「이번에 조회하지 않았다」고 밝혔습니다.

**판정: 맞음(9개 호 모두 원문과 일치).** 예: 제36조제6호 「제15조제1항 또는 제2항의 규정을 위반하여 안전관리자를 선임하지 아니한 관계인으로서 제6조제1항의 규정에 따른 허가를 받은 자」, 제39조제1항제7호의2 「제18조제2항을 위반하여 기간 이내에 점검결과를 제출하지 아니한 자」.

## 같은 질문을 15번

대화형 실행 한 번으로는 결과가 우연인지 판단할 수 없어, 녹화 없이 헤드리스(`claude -p`)로 질문마다 3번씩 실행했습니다. schema.md에 적어 둔 「기대 답」이 섞이지 않도록 `--tools ""`로 파일 읽기와 셸을 모두 끄고 Neo4j MCP 도구 두 개만 사용하게 했습니다.

원 교재의 bash 명령을 PowerShell 반복문으로 옮겼습니다(Windows PowerShell 5.1과 7 모두 동작). 질문은 5장에서 만든 `golden-questions.md`의 「1. …」 형식 줄에서 읽습니다. 질문 15개를 차례로 실행하므로 10분 안팎 걸리고, 구독 플랜의 사용 한도를 씁니다. 먼저 `$reps = 1`로 한 번씩만 돌려 보는 것을 권합니다.

```powershell
Set-Location C:\lab\law-graph
. .\env.ps1
New-Item -ItemType Directory -Force runs\graph | Out-Null
$qs = (Get-Content -Encoding utf8 golden-questions.md) -match '^\d+\. ' -replace '^\d+\. ', ''
$reps = 3
for ($n = 1; $n -le $qs.Count; $n++) {
  for ($m = 1; $m -le $reps; $m++) {
    claude -p "$($qs[$n-1]) Neo4j 에서 찾아 근거 조문과 함께 답해 줘." `
      --mcp-config .mcp.json --strict-mcp-config `
      --tools= --allowedTools "mcp__neo4j__get-schema,mcp__neo4j__read-cypher" `
      --output-format stream-json --verbose |
      Set-Content -Encoding utf8 "runs\graph\q$n-r$m.jsonl"
  }
}
```

| 원 교재(bash) | PowerShell | 이유 |
|---|---|---|
| 줄 끝 `\` | 줄 끝 `` ` ``(백틱), 파이프 `\|` 뒤에서는 그냥 줄바꿈 | PowerShell의 줄 잇기 문자 |
| `< /dev/null` | 생략 | PowerShell 창에서 실행한 `claude -p`는 입력을 기다리지 않습니다 |
| `> runs/graph/q<N>-r<M>.jsonl` | `\| Set-Content -Encoding utf8 "runs\graph\q$n-r$m.jsonl"` | 한글이 든 JSON을 UTF-8로 저장합니다. `>`는 5.1에서 UTF-16으로 저장해 다른 도구가 읽기 어렵습니다 |
| `--tools ""` | `--tools=` | Windows PowerShell 5.1은 빈 문자열 인자 `""`을 빼 버려 `--tools`가 다음 인자를 값으로 삼습니다. `--tools=`는 5.1과 7 모두 같은 뜻입니다 |

결과 파일마다 도구 호출 수, 걸린 시간, 비용을 모아 보는 명령입니다. `stream-json`의 마지막 `result` 줄에 시간(`duration_ms`)과 비용(`total_cost_usd`)이 들어 있습니다.

```powershell
Get-ChildItem runs\graph\*.jsonl | ForEach-Object {
  $ev = Get-Content -Encoding utf8 $_ | Where-Object { $_ } | ForEach-Object { $_ | ConvertFrom-Json }
  $res = $ev | Where-Object type -eq 'result' | Select-Object -Last 1
  $calls = @($ev | Where-Object type -eq 'assistant' | ForEach-Object { $_.message.content } |
             Where-Object { $_.type -eq 'tool_use' -and $_.name -like 'mcp__neo4j__*' }).Count
  [pscustomobject]@{ 파일 = $_.Name; 호출 = $calls; 초 = [math]::Round($res.duration_ms / 1000, 1); 비용 = $res.total_cost_usd }
} | Format-Table -AutoSize
```

원 교재 기록은 다음과 같습니다.

| 질문 | 평균 호출 | 평균 시간 | 평균 비용(API 환산) |
|---|---|---|---|
| 1 | 3.7 | 23.5초 | $0.447 |
| 2 | 6.7 | 31.3초 | $0.883 |
| 3 | 6.0 | 27.0초 | $0.692 |
| 4 | 7.3 | 33.6초 | $0.599 |
| 5 | 10.0 | 42.8초 | $0.820 |

15번의 총비용은 $10.32입니다. 모델은 `claude-fable-5-2`이고, 비용은 `claude -p`가 반환한 API 요금 환산치이므로 구독 로그인에서는 따로 청구되지 않습니다. 7장의 추출(haiku)보다 훨씬 비쌉니다. 헤드리스는 매번 새로 시작하므로 실행할 때마다 `get-schema` 1번 + `read-cypher` 2~10번을 호출했고, 대화형은 1번 질문에서만 스키마를 받고 그 뒤에는 문맥에 남은 스키마를 썼습니다.

- **답**: 15번 모두 결론이 원문과 맞았습니다. 질문별 핵심 사실(1일 전·시ㆍ도지사, 30일·14일, 즉시 응급조치·통보, 9개 호)이 모든 회차에 포함되었습니다.
- **컨텍스트**: 도구 결과를 모두 합치면 실행당 평균 약 5만 자(스키마 약 9천 자 포함)였습니다.
- **Cypher 오류**: 15번 중 10번에서 1~2건이 발생했고, 모두 모델이 수정해 다시 실행했습니다. 가장 흔한 첫 시도는 모든 속성을 문자열로 검색하는 `MATCH (n) WHERE any(k IN keys(n) WHERE toString(n[k]) CONTAINS '안전관리자') …`였고 `TypeError (Invalid input for function 'toString()': … got: StringArray[…])`로 실패했습니다(목록 속성 때문). 다음은 3번에서 본 집계 뒤 `ORDER BY` 오류였습니다.
- **그래프 구조를 틀리게 설명한 2건**: q4-r3은 「제36조제15호에서 제27조로 가는 `PENALIZES`·`REFERS_TO` 관계가 없습니다」라고 했지만 실제로는 `제36조제15호 -PENALIZES-> 제27조`가 있습니다. 모델이 조건에 `t.articleSub IS NULL`을 넣었는데 이 그래프는 가지번호가 없으면 0을 저장해 두므로 결과가 비었고, 모델은 이를 「관계가 없다」로 해석했습니다. q3-r1은 「제39조에는 Sanction 이 연결되어 있지 않다」고 했는데, 조 노드에는 없고 제39조제1항에 `IMPOSES`가 있어 반만 맞습니다. 두 회차 모두 벌칙 내용은 조문 텍스트에서 확인해 답 자체는 맞았습니다.

근거 조문을 얼마나 빠짐없이 가져왔는지(재현율)는 [10장](vector-vs-graph.html)에서 벡터 RAG와 같은 기준으로 측정합니다.

!!! warning "답의 근거 조문은 반드시 원문으로 확인하세요"
    15번 모두 결론이 맞았지만, 같은 실행 안에서도 그래프에 대한 설명은 틀릴 수 있었습니다. 빈 결과는 「없다」가 아니라 「이 조건으로는 안 나왔다」일 수 있습니다. 답에 인용된 조문 번호를 원문에서 찾아 문구를 대조하고, 그래프에 대한 주장(「관계가 없다」 등)은 직접 Cypher로 다시 확인하세요. 의미층 Norm은 아직 `reviewed=false`입니다.

## 동작 과정 다시 보기 — 2번 질문

[2장](how-graphrag.html)에서 본 질의 단계 이름에 따라 대화형 세션의 2번 질문을 실제 화면을 기준으로 살펴봅니다.

| 단계 | 이 세션의 실제 동작 |
|---|---|
| 엔티티 연결 | 7장의 별칭 노드(`normKeys`)를 거치지 않고, 「위험물안전관리자」 대신 더 짧은 문자열 「안전관리자」로 조문 텍스트를 찾았습니다(`p.text CONTAINS '안전관리자'`, 「선임」「신고」「해임」「퇴직」「대리자」도 같은 방식). 제15조는 `p.articleNo = 15`로 통째로 가져왔습니다. 「관계인」은 조건에 없었고, 반환된 Norm의 `HAS_SUBJECT`가 Actor 「관계인」이었습니다 |
| 스키마를 컨텍스트에 | `get-schema`를 다시 호출하지 않았습니다. 1번 질문 때 받은 스키마(9,111자)가 대화 문맥에 남아 있습니다 |
| Cypher 생성 | `read-cypher` 3번: 조문 텍스트 검색(14행) → Norm과 주체·상대방(14행) → `pid`로 시행규칙 제53조·제54조와 법 제12조·제36조·제39조제1항 조회(19행) |
| 실행 | 세 결과를 합쳐 13,876자가 모델에 전달되었습니다 |
| 답 | 30일 이내 재선임 → 14일 이내 신고 → 신고서·첨부서류 → 공백 기간 → 제재 순서로, 조문마다 원문 인용 |

두 번째 질의와 결과 일부입니다.

```cypher
MATCH (n:Norm)-[:BASED_ON]->(p) WHERE p.lawId STARTS WITH '위험물안전관리법' AND (p.text CONTAINS '안전관리자') AND (p.text CONTAINS '선임' OR p.text CONTAINS '해임')
OPTIONAL MATCH (n)-[:HAS_SUBJECT]->(s:Actor) OPTIONAL MATCH (n)-[:ADDRESSED_TO]->(r:Actor)
RETURN n.normId, n.modality, n.action, n.trigger, n.deadlineText, n.deadlineValue, n.deadlineUnit, n.deadlineKind, n.reviewed,
       collect(DISTINCT s.name) AS subj, collect(DISTINCT r.name) AS recip, p.citation LIMIT 40
```

```text
위험물안전관리법:제15조:제2항#1  subj ["관계인"]  deadlineText "해임하거나 퇴직한 날부터 30일 이내"
위험물안전관리법:제15조:제3항#1  subj ["관계인"]  recip ["소방본부장", "소방서장"]  deadlineText "선임한 날부터 14일 이내"
위험물안전관리법 시행규칙:제53조:제1항#1  subj ["관계인"]  recip ["소방본부장", "소방서장"]
…(14행 중 3행, 필드는 줄여 보임)
```

화면에는 이 과정이 한 줄로 접혀 나오고, 그 아래 답이 이어집니다.

```text
  Called neo4j 3 times (ctrl+o to expand)

⏺ 해임하거나 퇴직한 날부터 30일 이내에 다시 선임해야 하고, 선임한 날부터 14일 이내에 소방본부장 또는 소방서장에게 선임신고를
  해야 합니다.
```

질문의 「위험물안전관리자」에 「안전관리자」라는 문자열이 포함되어 있어 문자열 포함 여부만으로도 연결되었습니다. 문자열이 겹치지 않으면 상황이 다릅니다. 질문에 쓴 「시·도지사」(가운뎃점 ·)는 조문의 「시ㆍ도지사」(ㆍ)와 글자가 달라 문자열 포함 여부로는 일치하지 않지만, Term 「시ㆍ도지사」의 별칭 키(`normKeys`의 「시·도지사」)로는 일치합니다. 7장의 별칭과 전문 색인이 이런 역할을 합니다.

!!! warning "막히면"
    **다른 날 다시 열었더니 neo4j 도구가 없습니다 (GL-12).** 증상: `/mcp`에 neo4j가 연결되지 않고 질문해도 MCP 호출이 나오지 않습니다. 원인: `.mcp.json`의 `${NEO4J_PASSWORD}`는 claude를 실행한 셸의 환경변수 값으로 치환되는데, 새 터미널에는 그 변수가 없습니다. 조치: `Set-Location C:\lab\law-graph; . .\env.ps1` 뒤 `claude`를 다시 실행합니다(8장).

    **답에 `" 밖의 관계기관"` 같은 이상한 이름이 나옵니다 (GL-14).** 증상: 4번 질문에서 제27조제2항 Norm의 상대방 Actor 이름이 `" 밖의 관계기관"`입니다. 원인: 7장에서 묶음 이름을 쪼갤 때 「그 밖의」의 「그」를 접속어로 잘라냈습니다. 조치: 7장 「막히면」대로 쪼개기 규칙을 고치고 `uv run ingest_semantic.py --reset`을 실행합니다. 이 교재의 기록은 고치기 전 데이터입니다.

## 확인 문제

**1.** 헤드리스 q4-r3에서 Claude는 「제36조제15호에서 제27조로 가는 PENALIZES 관계가 없다」고 했지만 실제로는 있었습니다. 왜 이런 설명이 나왔고, 어떻게 확인하나요?

<details class="answer" markdown="1">
<summary>정답</summary>

모델이 쓴 질의에 `t.articleSub IS NULL` 조건이 들어 있었는데, 이 그래프는 가지번호가 없는 조에 `articleSub = 0`을 저장해 두므로 결과가 비었습니다. 모델은 빈 결과를 「관계가 없다」로 해석했습니다. `MATCH (i {pid:'위험물안전관리법:제36조:제15호'})-[r]->(t) RETURN type(r), t.pid`처럼 조건 없이 직접 질의하면 `PENALIZES → 위험물안전관리법:제27조`가 나옵니다.
</details>

**2.** 대화형 세션의 2~5번 질문에서는 `get-schema`를 호출하지 않았습니다. 그런데도 Cypher를 작성할 수 있었던 이유는 무엇인가요?

<details class="answer" markdown="1">
<summary>정답</summary>

1번 질문 때 받은 스키마(노드 레이블·관계 타입·속성, 9,111자)가 같은 대화의 문맥에 남아 있었기 때문입니다. 헤드리스 실행은 매번 새로 시작하므로 매번 `get-schema`를 먼저 호출했습니다.
</details>

**3.** 5번 질문(제15조·제18조 위반의 벌칙)은 한 조문 안에 답이 없습니다. 그래프에서 어떤 경로를 거쳐 답을 찾았나요?

<details class="answer" markdown="1">
<summary>정답</summary>

의무 조항(예: 제15조제3항) ←`PENALIZES`— 벌칙 호(제39조제1항제5호) ←`HAS_PART`— 벌칙 조·항(제39조제1항) —`IMPOSES`→ Sanction(500만원 이하의 과태료) 순서로 탐색했습니다. 그래프는 이렇게 여러 조문을 연결해야 하는 질문에 강하며, 10장에서 벡터 RAG와 비교합니다.
</details>
