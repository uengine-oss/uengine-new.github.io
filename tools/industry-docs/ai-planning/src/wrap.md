# 도구 선택과 적용 과제

> 보안 요건에 맞는 도구 조합, 단계별 승인 체크리스트, 자기 업무에 적용하는 과제를 정리합니다.

## 보안 요건이 도구를 가릅니다

보안 요건이 도구를 가릅니다. 외부 전송이 금지된 곳은 설치형을, 속도와 협업이 먼저인 곳은 SaaS를 씁니다. 주의할 점이 있습니다. 설치형이 곧 외부 전송 없음은 아닙니다. AI-DLC와 스킬은 내 컴퓨터에서 돌지만 클로드 코드를 쓰면 문서가 모델 제공자로 갑니다. 폐쇄망이라면 사내 모델 연결부터 검증합니다.

| 단계 | 외부 전송 금지 (금융, 방산, 공공) | 속도와 협업 우선 (스타트업, PoC) |
|---|---|---|
| 인터뷰 | AI-DLC + 사내 승인 모델 | ChatPRD 또는 AI-DLC |
| 모델링 | ddd-starter + 사내 승인 모델 | ddd-starter, Eraser |
| ERD | Mermaid CLI, Azimutt 자체 설치 | Mermaid Live, Eraser |
| 화면 | OpenUI, bolt.diy + Ollama | Uizard, Relume |

**"설치형"이 곧 "외부 전송 없음"은 아닙니다**

AI-DLC와 스킬은 내 컴퓨터에서 돌지만, Claude Code를 쓰면 문서가 모델 제공자로 갑니다. 폐쇄망에서는 사내 모델을 연결할 수 있는지 먼저 검증합니다. 이 교재에서는 그 구성을 실행하지 않았습니다.

## 오늘 우리 데이터는 어디로 갔습니까?

오늘 데이터가 어디로 갔는지 정리합니다. AI-DLC와 스킬은 클로드 코드의 모델 제공자로, 오픈유아이는 내 컴퓨터에만, 렐룸 같은 SaaS는 서비스 서버로 갔습니다. 실제 회사 문서를 넣기 전에 이 표를 자기 회사 기준으로 다시 씁니다. 오늘 주제가 가상의 회사인 이유입니다.

| 도구 | 모델과 처리 위치 | 확인할 점 |
|---|---|---|
| AI-DLC, ddd-starter | Claude Code의 모델 제공자 | 구상 글과 답변이 전송됩니다 |
| OpenUI + Ollama | 내 컴퓨터 127.0.0.1 | 프롬프트가 밖으로 나가지 않습니다 |
| Mermaid Live | 브라우저 화면 | 주소에 코드가 담기니 링크 공유 주의 |
| Azimutt 웹판 | 화면 문구: 내 컴퓨터에 머문다고 안내 | 민감하면 자체 설치, 정책 재확인 |
| Relume, ChatPRD 등 | 서비스 서버 | 입력은 외부로 갑니다. 약관 확인 |

실제 회사 문서를 넣기 전에 이 표를 자기 회사 기준으로 다시 씁니다. 오늘 주제가 가상의 회사인 이유입니다.

## 단계마다 사람이 확인할 일

단계마다 사람이 확인할 일입니다. 요구사항은 근거 없는 문장과 범위를, 모델은 핵심 규칙이 제약으로 있는지와 실패 경우를, 화면은 요구하지 않은 기능과 막아야 할 동작을 봅니다. 오늘 잡은 수령 기록, 반납일 당일, 잘못된 버튼 문제가 모두 이런 확인에서 나왔습니다.

**요구사항**

- 근거 표시 없는 문장이 있는가
- 범위 밖 목록이 맞는가
- 열린 질문의 담당자가 있는가

**모델과 DDL**

- 핵심 규칙이 제약으로 있는가
- 실패 경우까지 실제로 돌렸는가
- AI의 가정을 업무 담당자가 봤는가

**화면**

- 요구하지 않은 기능이 생겼는가
- 금지된 동작을 막고 있는가
- 예시 값을 실제 값으로 바꿨는가

오늘 잡은 문제 대부분은 이 질문들로 찾았습니다. 수령 기록, 반납일 당일, 잘못된 버튼, 눌리는 승인 버튼이 그랬습니다.

## 내 업무 하나로 다시 해 봅니다

마지막 15분은 자기 업무로 다시 해 봅니다. 엑셀과 메신저로 돌아가는 일을 다섯 줄로 쓰고, 실제 고객 정보는 뺍니다. 의도 정리까지 돌린 뒤, 절대 깨지면 안 되는 규칙을 한 문장으로 씁니다. 옆 사람과 바꿔 읽고 예외를 찾아 주면 수업이 끝납니다.

| 순서 | 할 일 | 결과 |
|---|---|---|
| 1 | 엑셀과 메신저로 돌아가는 일 하나를 다섯 줄로 씁니다. 실제 고객 정보는 뺍니다 | brief.md |
| 2 | /aidlc --scope poc 로 의도 정리까지 합니다 | 내가 정하지 않았던 것 3개 |
| 3 | "절대 깨지면 안 되는 규칙"을 한 문장으로 씁니다 | 불변식 1개 |
| 4 | 그 규칙이 깨지는 화면을 말로 설명합니다 | 정합성 표 1행 |

옆 사람과 불변식을 바꿔 읽고, 예외를 하나씩 찾아 줍니다.

## 공식 자료 (2026년 11월 4일 확인)

참고 자료입니다. 요금과 무료 한도는 자주 바뀌니 수업 전날 다시 확인합니다. 오늘 기억할 한 문장입니다. AI가 묻게 하고, 사람이 승인하고, 돌려 보고 믿습니다. 수고하셨습니다.

- [AI-DLC Workflows](https://github.com/awslabs/aidlc-workflows)
- [AI-DLC 문서](https://awslabs.github.io/aidlc-workflows/)
- [ddd-starter 스킬](https://github.com/uengine-oss/ddd-starter-skill-kor)
- [DDD Starter Modelling Process](https://github.com/ddd-crew/ddd-starter-modelling-process)
- [Mermaid Live Editor](https://mermaid.live/)
- [Mermaid (구 Mermaid Chart)](https://mermaid.ai/)
- [Azimutt](https://azimutt.app/)

- [Eraser DiagramGPT](https://www.eraser.io/diagramgpt)
- [ChatPRD 요금](https://www.chatprd.ai/pricing)
- [W&B OpenUI](https://github.com/wandb/openui)
- [Relume](https://www.relume.ai/)
- [Uizard 요금](https://uizard.io/pricing/)
- [bolt.diy](https://github.com/stackblitz-labs/bolt.diy)

요금, 무료 한도, 가입 조건은 자주 바뀝니다. 수업 전날 다시 확인합니다.

기억할 한 문장: AI가 묻게 하고, 사람이 승인하고, 돌려 보고 믿습니다.
