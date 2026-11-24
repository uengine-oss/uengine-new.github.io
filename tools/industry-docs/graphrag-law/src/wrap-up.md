# 마무리

> 이 교재에서 수행한 작업을 장별로 정리하고, 정리 노트에서 꼽은 어려운 시나리오(스키마 구축 비용, 이력 데이터)와 실제 실행에서 드러난 한계(Cypher 오류, 큰 컨텍스트, LLM 추출 오류, PDF에 없는 별표)를 짚습니다. 이어서 혼자 해 볼 확장 과제와 참고 자료를 소개합니다.

## 한 일

| 장 | 한 일 | 결과 |
|---|---|---|
| 3 | Docker로 Neo4j 5.26 + APOC 실행하기 | 시작 4.6초, 메모리 926MiB / 상한 2GiB |
| 4 | Cypher 맛보기 | `MERGE`는 다시 실행해도 노드가 늘지 않음, 한국어 전문 색인은 `cjk` 분석기 |
| 5 | 골든 퀘스천에서 스키마 설계 | `schema.md`·`schema.cypher`. 사람이 검토한 뒤 두 가지를 수정하도록 함(표기 차이 → 별칭, 직접 작성한 Norm → LLM 추출로) |
| 6 | PDF 9종 → 조·항·호 → Neo4j | 노드 6,272 · 관계 17,537. 9개 법령 모두 현행 조 집합이 PDF와 일치 |
| 7 | 엔티티 추출과 엔티티 중의성 해소 | 이름 228가지 → Actor 136, Norm 410. 그래프 전체 노드 6,818 · 관계 18,643 |
| 8 | Neo4j MCP 서버를 읽기 전용으로 연결 | 도구 2개: `get-schema`, `read-cypher` |
| 9 | 골든 퀘스천 5개 묻기 | 대화형 5개, 헤드리스 15회 모두 답의 결론이 원문과 일치 |
| 10 | 같은 질문을 벡터 RAG로 | 그래프는 필수 조항 재현율 100%, 보충 포함 98%. 벡터와의 비교는 10장 |

한 문장으로 정리하면, **틀(온톨로지)은 골든 퀘스천에서 출발해 사람이 정하고, 인스턴스는 코드와 LLM이 채우고, 질의는 Claude Code가 MCP로 수행하고, 사람은 각 단계의 결과를 원문과 대조했습니다.**

## 한계와 어려운 점

### 노트가 꼽은 어려운 시나리오

**스키마 구축 비용.** 이 교재의 스키마는 Claude Code가 두 차례(4분 56초, 4분 36초)에 걸쳐 작성했지만, 그 사이에 사람이 PDF와 질문을 읽고 수정할 부분을 짚어야 했습니다. 첫 설계에는 골든 퀘스천용 의무 14건을 직접 작성한 표가 있었는데, 다른 법령으로 확장하기 어려워 LLM 추출 단계로 미뤘습니다. 또 이 틀은 다섯 질문에서 출발했으므로, 인허가나 개정 이력처럼 다른 종류의 질문에 답하려면 레이블과 관계를 다시 설계해야 합니다.

**이력 데이터를 보관할 수 있는가.** 국가법령정보센터 PDF에는 현행 조문 뒤에 같은 번호의 시행 예정 조문이 함께 실리는 경우가 있습니다. 이 교재의 9개 법령에서는 세 곳이었습니다. 조 번호만으로 `MERGE` 하면 뒤의 판본이 앞의 판본을 덮어쓰므로, 시행 예정 판본은 `pid`에 시행일을 붙여 따로 넣고 `isCurrent`를 `false`로 두었습니다([부록 GL-07](troubleshooting.html#gl-07)).

| `pid` | `effectiveFrom` | `isCurrent` |
|---|---|---|
| 폐기물관리법 시행규칙:제10조@20261210 | 2026-12-10 | false |
| 폐기물관리법:제13조의2@20270708 | 2027-07-08 | false |
| 폐기물관리법:제68조@20270108 | 2027-01-08 | false |

질문할 때는 `isCurrent`가 참인 조문만 조회합니다. 다만 이 방식은 PDF에 실린 두 판본(현행, 시행 예정)만 다룹니다. 이전 판본(연혁)은 그래프에 없고, 조문마다 개정 날짜 목록(`amendedOn`)만 속성으로 남아 있습니다. 「작년 이맘때는 기한이 며칠이었나」 같은 질문에는 답할 수 없습니다.

**memGPT와 비교.** memGPT는 LLM이 운영체제처럼 제한된 컨텍스트와 외부 기억 사이에서 내용을 스스로 옮기는 방식입니다. GraphRAG는 지식을 사람이 검토할 수 있는 구조로 LLM 바깥에 둡니다.

### 실제 실행에서 드러난 한계

**Cypher 오류와 재시도.** 헤드리스 15회 중 10회에서 Cypher 오류가 한두 번씩 발생했고, 모든 경우에 모델이 오류 문구를 읽고 Cypher를 수정했습니다. 가장 흔한 오류는 목록 속성에 `toString()`을 쓴 오류와 집계 뒤에 집계 전 변수를 `ORDER BY`에 쓴 오류였습니다. 또 답의 결론은 15회 모두 맞았지만, **그래프에 대한 설명이 틀린 곳**이 두 번 있었습니다. 한 번은 존재하는 `PENALIZES` 관계(제36조제15호 → 제27조)를 「없다」고 했고, 한 번은 형량이 조가 아닌 항에 연결된 것을 「연결되어 있지 않다」고 했습니다. 모델의 설명보다 답에 제시된 근거 조문을 원문으로 확인하는 습관이 필요합니다.

**큰 컨텍스트.** 그래프의 컨텍스트는 질문 한 번에 평균 약 5만 자였고, 그중 스키마가 약 9천 자입니다. 실행마다 19,139자에서 79,876자까지 달라졌습니다. 2장에서 본 골든 퀘스천 2번 실행에서는 법령 179개를 모두 조회한 호출 하나가 34,774자를 차지했습니다. 컨텍스트가 크면 비용도 늘어나, 질문 한 번에 API 요금 환산 $0.39~1.04가 들었습니다. 벡터 RAG는 k=5일 때 약 4천 자이므로, 같은 분량을 기준으로 한 비교는 10장에서 따로 합니다.

**LLM 추출 오류와 사람의 검토.** LLM이 추출한 의미층에는 사람이 수정해야 할 부분이 남아 있었습니다.

- 「표기 그대로」라는 지시에도 두 이름을 임의로 묶어 만든 이름 8가지(「기술원 또는 안전원」 등)가 있었습니다.
- 조건(`trigger`) 104건과 기한 6건이 조문 원문과 달라 값을 비우고 `uncheckedFields`에 표시했습니다.
- 엔티티 중의성 해소에서 관계인 = 관계자, 대리인 → 대리자처럼 잘못 통합한 사례가 있었습니다(검토로 찾아 수정, 7장).
- 「그 밖의 관계기관」을 나누다가 Actor 「 밖의 관계기관」이 생겼습니다(9장 질의 중 Claude가 발견, [부록 GL-14](troubleshooting.html#gl-14)).
- 주체가 아닌 「제조소등」「행정안전부령」 같은 이름이 Actor(종류 「기타」 51개)로 남았습니다.

그래서 Norm 410개는 모두 `reviewed: false`로 두었고, 9장의 답에서도 Claude는 Norm 값을 그대로 쓰지 않고 조문 원문과 대조했다고 밝혔습니다.

**PDF에 없는 별표.** 과태료 세부 금액처럼 별표·서식에 있는 내용은 이 교재에서 받은 PDF에 본문이 포함되어 있지 않습니다. 그래프에는 별표·서식을 가리키는 노드 349개가 있지만 모두 내용이 없는 자리표시(`inCorpus: false`)입니다. 그래서 과태료 금액을 물으면 시행령 제23조가 별표 9를 가리킨다는 것까지만 답할 수 있습니다.

**원문 대조의 범위.** 사람이 글자까지 대조한 것은 위험물안전관리법 3종의 표본 조문과 골든 퀘스천의 근거 조문입니다. 화학물질관리법·폐기물관리법의 벌칙 관계와 용어, 줄바꿈 위치의 띄어쓰기를 규칙으로 정하지 못한 약 9%는 전부 확인하지 못했습니다.

## 확장 과제

1. **다른 법령 넣기.** 국가법령정보센터에서 다른 법령(예: 소관 업무에 쓰는 다른 안전 법령)의 법률·시행령·시행규칙을 받아 같은 코드로 적재해 보세요. 6장처럼 그래프의 조 수와 PDF의 「제N조」 줄을 대조하고, 표본 조문 세 개를 글자까지 대조합니다. 의미층(Norm·Actor)을 9개 법령 전체로 확장하면, 위험물 3종의 실측값을 글자 수에 비례해 추산할 때 API 환산 비용은 약 $1.6이며, 동시 6개 처리 시 약 35분이 걸립니다(어림값이며 실측이 아닙니다).
2. **골든 퀘스천 세 개 더 쓰기.** 화학물질관리법이나 폐기물관리법에서 되도록 여러 조문을 살펴봐야 답을 찾을 수 있는 질문을 세 개 작성합니다. 먼저 원문을 읽고 모범 답과 근거 조항을 적은 뒤 Claude Code에 묻고, 답의 근거 조문을 원문과 대조하세요. 9장의 헤드리스 명령으로 세 번씩 실행하면 회차마다 달라지는 부분도 볼 수 있습니다.
3. **벡터 색인 섞기.** 조문 노드에 임베딩을 넣고 벡터 색인을 만든 뒤(2장의 문법), 벡터로 찾은 조문에서 `PENALIZES`·`IMPLEMENTS`를 따라 탐색 범위를 넓히는 질의를 만들어 보세요. 10장의 채점기는 `{qid, retrieved_text, answer}` 형식의 결과 파일만 읽으므로, 같은 기준으로 재현율과 컨텍스트 크기를 측정할 수 있습니다.
4. **개정 추적.** 이 교재의 출발점인 PBL 교재의 주제는 인허가 법령의 개정 추적이었습니다. 법령 노드의 번호·시행일(`lawNumber`, `effectiveOn`)을 판본별로 남기고, 새로 받은 PDF와 그래프의 조문 내용을 비교해 바뀐 조문과 그 조문을 가리키는 벌칙·위임 관계를 찾아보세요. 시행 예정 판본을 따로 둔 방식(`@시행일`, `isCurrent`)을 전체 판본에 적용하는 일입니다.
5. **질의 방법 안내.** 9장에서 Claude는 적재할 때 만든 전문 색인을 쓰지 않고 대부분 문자열 포함 조건(`CONTAINS`)과 조 번호 지정으로 찾았습니다. 「질문 낱말은 먼저 Term·Actor 의 별칭 열쇠로 찾아라」 같은 안내를 프롬프트나 프로젝트 지침에 넣고, 호출 수와 컨텍스트 크기가 어떻게 바뀌는지 비교해 보세요.

## 참고 자료

정리 노트 「Graph DB based RAG」에 있는 링크입니다.

- Knowledge Graphs & LLMs: Multi-Hop Question Answering — <https://medium.com/neo4j/knowledge-graphs-llms-multi-hop-question-answering-322113f53f51>
- Unifying LLMs & Knowledge Graphs for GenAI: Use Cases & Best Practices — <https://neo4j.com/blog/unifying-llm-knowledge-graph/>
- 노트의 「프롬프트」 항목(공유 대화) — <https://chat.openai.com/share/8a78ce53-4105-4aba-a380-cdf4ca53382a>
- Creating a Knowledge Graph From Video Transcripts With GPT-4 — <https://medium.com/neo4j/creating-a-knowledge-graph-from-video-transcripts-with-gpt-4-52d7c7b9f32c>
- ai graph db disambiguation (YouTube) — <https://youtu.be/eirBMLpAtcA>
- Constructing knowledge graphs from text using OpenAI functions — <https://bratanic-tomaz.medium.com/constructing-knowledge-graphs-from-text-using-openai-functions-096a6d010c17>
- LangChain Cypher 체인 코드 — <https://api.python.langchain.com/en/latest/_modules/langchain/chains/graph_qa/cypher.html>
- Vector search indexes — Cypher Manual — <https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/>
- Harnessing Large Language Models with Neo4j — <https://medium.com/neo4j/harnessing-large-language-models-with-neo4j-306ccbdd2867>
- neo4j/naLLM — <https://github.com/neo4j/naLLM>
- Multimodal RAG pipeline with LlamaIndex and Neo4j — <https://blog.llamaindex.ai/multimodal-rag-pipeline-with-llamaindex-and-neo4j-a2c542eb0206>
- Graph RAG: The New LLM Stack with Knowledge Graphs (NebulaGraph) — <https://medium.com/@nebulagraph/graph-rag-the-new-llm-stack-with-knowledge-graphs-e1e902c504ed>

노트의 「Graph DB 자체(neo4j)」 항목(Cypher 문법, Cypher 기본, Neo4j 학습 환경)에는 링크가 없어 공식 문서로 대신합니다.

- Neo4j Cypher Manual — <https://neo4j.com/docs/cypher-manual/current/>
- Neo4j Getting Started — <https://neo4j.com/docs/getting-started/>
- Neo4j GraphAcademy(무료 학습 과정) — <https://graphacademy.neo4j.com/>

이 교재에서 사용한 도구와 자료입니다.

- Neo4j MCP 서버(공식) — <https://github.com/neo4j/mcp>, 문서 <https://neo4j.com/docs/mcp/current/>
- Neo4j Docker 운영 문서 — <https://neo4j.com/docs/operations-manual/current/docker/>
- 국가법령정보센터 — <https://www.law.go.kr>
- MemGPT: Towards LLMs as Operating Systems — <https://arxiv.org/abs/2310.08560>

## 확인 문제

<details class="answer" markdown="1">
<summary>시행 예정 조문을 현행 조문과 같은 `pid`로 `MERGE` 하면 어떤 문제가 생기나요?</summary>

`MERGE`는 같은 키의 노드가 있으면 새로 만들지 않고 그 노드를 그대로 사용합니다. 그래서 이어지는 `SET`이 속성을 덮어써 PDF에서 뒤에 나오는 시행 예정 판본이 현행 조문을 덮어쓰거나, 두 판본의 항·호가 한 조 아래에 섞입니다. 이 교재는 시행 예정 판본의 `pid`에 `@시행일`을 붙여 다른 노드로 두고, `isCurrent`와 `effectiveFrom`으로 구분했습니다.
</details>

<details class="answer" markdown="1">
<summary>답의 결론이 15회 모두 맞았는데도 근거 조문을 원문으로 확인해야 하는 이유는 무엇인가요?</summary>

모델이 작성하는 Cypher와 문장은 실행할 때마다 달라지고, 실제로 그래프에 대한 설명이 틀린 경우가 두 번 있었습니다. 의미층의 Norm 값도 LLM이 추출한 것으로 사람이 검토하지 않은 상태(`reviewed: false`)입니다. 조문 원문은 그래프에 그대로 들어 있으므로, 답에 제시된 조문을 원문과 대조하는 것이 가장 확실한 검증입니다.
</details>

<details class="answer" markdown="1">
<summary>골든 퀘스천을 새로 쓸 때 모범 답을 먼저 원문에서 적어 두는 이유는 무엇인가요?</summary>

모델의 답을 본 뒤에 판단하면 그럴듯한 답에 영향을 받기 쉽습니다. 근거 조항과 핵심 사실(기한, 기관, 형량)을 먼저 적어 두면 답이 맞았는지, 어느 조항을 놓쳤는지를 같은 기준으로 평가할 수 있습니다. 10장의 재현율도 이렇게 미리 정한 정답 조항을 기준으로 측정합니다.
</details>
