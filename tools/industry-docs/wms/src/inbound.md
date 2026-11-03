# 재보충에서 적치까지

> 부족한 재고 하나를 RFQ, 승인, PO, 도착, 입고, 품질 검사, 적치까지 역할을 바꿔 가며 채웁니다. 불합격 폐기와 감사 로그도 확인합니다.

## 무엇을 · 왜

재고가 최소 기준 아래로 내려가면 구매 담당자, 승인자, 입고 담당자, 품질 담당자가 차례로 같은 문서를 넘겨받습니다. 각 단계는 데이터베이스 함수(RPC) 하나이고, 함수가 역할과 문서 버전을 검사합니다. 받은 물건은 품질 검사를 통과하고 적치가 끝나야 가용 재고가 됩니다.

!!! note "샘플의 범위"
    - 화면 이름은 RFQ지만 **견적을 비교하는 화면은 없습니다.** RFQ를 만들면 바로 승인 대기(`TO_APPROVE`) 문서가 됩니다.
    - 도착, 입고, 품질, 적치는 사람이 누르는 대로 기록합니다. 스캐너나 실물 확인과 연결되어 있지 않습니다.
    - 값은 시드 데이터 그대로입니다. 앞 장의 역할 비교에서 문서를 만들었다면 `cd supabase && supabase db reset`으로 처음 상태로 되돌린 뒤 따라 하세요.

## 따라 하기

<ol class="steps" markdown="1">
<li markdown="1">**부족 확인.** `buyer-a@demo.local`로 로그인합니다. **Overview**에서 `SKU-A-001`은 Available 30, Reorder Min / Max 50 / 200, 상태 `BELOW MIN`입니다.

![Overview의 부족 재고](img/inbound-shortage.webp)
</li>
<li markdown="1">**RFQ 만들기.** **Replenishment**를 엽니다. 최소 기준 아래인 상품만 모여 있습니다. `SKU-A-001` 카드의 **Qty**를 비워 두면 최대 200에서 현재 30을 뺀 170이 들어갑니다. **Supplier**에서 `Acme Packaging Co.`를 고르고 **Create RFQ**를 누릅니다.

![Replenishment](img/inbound-replen.webp)
</li>
<li markdown="1">**문서 확인.** **Purchase Orders**에 `SKU-A-001`, Qty 170, `TO_APPROVE`, Version 1인 문서가 생깁니다. 구매 담당자에게는 승인 버튼이 없습니다.

![승인 대기 문서](img/inbound-po.webp)
</li>
<li markdown="1">**승인.** **Sign out**을 누른 뒤 `approver-a@demo.local`로 로그인해 **Purchase Orders**에서 **Approve**를 누릅니다. 상태는 `APPROVED`, Version은 2가 됩니다. 버전은 두 사람이 같은 문서를 동시에 고치는 일을 막습니다. 화면을 연 뒤 다른 사람이 먼저 고쳤다면 `CONFLICT` 오류가 납니다.

![승인됨](img/inbound-approve.webp)
</li>
<li markdown="1">**PO 확정.** `buyer-a@demo.local`로 다시 로그인해 **Confirm PO**를 누릅니다. 상태는 `CONFIRMED_PO`, Version 3입니다. 이때 입고 문서가 자동으로 만들어집니다.
</li>
<li markdown="1">**도착 등록.** `inbound-a@demo.local`로 로그인해 **Receiving**을 엽니다. Expected / Received는 170 / 0, 상태는 `EXPECTED`입니다. **Register Arrival**을 누르면 `ARRIVED`가 됩니다.

![도착 등록](img/inbound-arrival.webp)
</li>
<li markdown="1">**입고.** 수량 칸에 170을 넣고 **Receive**를 누릅니다. 비워 두면 예정 수량이 들어갑니다. 수량은 170 / 170, 상태는 `QC_PENDING`이 됩니다.
</li>
<li markdown="1">**품질 칸 확인.** **Overview**를 봅니다. `SKU-A-001`의 Available은 그대로 30, In QC가 170입니다. 받은 물건은 아직 가용 재고가 아니므로 상태도 `BELOW MIN` 그대로입니다.

![In QC 170](img/inbound-inqc.webp)
</li>
<li markdown="1">**합격 처리.** `quality-a@demo.local`로 로그인해 **Quality**에서 **Pass**를 누릅니다. `PUTAWAY_PENDING`으로 바뀝니다. 적치 버튼은 품질 담당자에게 보이지 않습니다.

![합격 처리](img/inbound-quality.webp)
</li>
<li markdown="1">**적치.** `inbound-a@demo.local`로 로그인해 **Quality**에서 **Putaway (→ Available)**를 누릅니다. 목록이 비면서 「대기 중인 검수/처분 건이 없습니다」가 보입니다.
</li>
<li markdown="1">**결과 확인.** **Overview**에서 `SKU-A-001`의 Available은 200, In QC는 0, 상태는 `OK`입니다.

![Available 200](img/inbound-ok.webp)
</li>
<li markdown="1">**불합격 처리.** `SKU-A-003`을 Qty 50으로 위와 같은 순서로 **Receive**까지 진행합니다. `quality-a@demo.local`로 로그인해 **Quality**에서 **Fail**을 누르면 `QC_COMPLETED`가 되고, 폐기 사유 코드(예: `DAMAGED`)를 넣어 **Scrap**을 누르면 끝납니다. **Overview**에서 `SKU-A-003`의 Available은 0 그대로입니다.

![폐기 뒤 Overview](img/inbound-scrap.webp)
</li>
<li markdown="1">**감사 로그.** `auditor-a@demo.local`로 로그인해 **Audit Log**를 엽니다. 위의 모든 단계가 시각, 행위자, 명령, 한국어 요약으로 남아 있습니다. 예를 들면 「입고 수량이 확정되었다 — 수령 50 / 예정 50, 상태 QC_PENDING.」입니다. 두 흐름을 끝까지 진행하면 14건이 남습니다.

![감사 로그](img/inbound-audit.webp)
</li>
</ol>

## 확인 문제

<details class="answer" markdown="1"><summary>입고 직후 Overview의 Available이 왜 늘지 않나요?</summary>
받은 수량은 품질 칸(In QC)에 표시됩니다. 품질 합격 뒤 적치가 끝나야 재고 원장에 가용 재고로 기록됩니다.
</details>

<details class="answer" markdown="1"><summary>구매 담당자가 자기가 만든 문서를 승인할 수 있나요?</summary>
할 수 없습니다. 승인은 `PURCHASE_APPROVER`나 `WMS_ADMIN`만 할 수 있습니다. 화면에 버튼이 없을 뿐 아니라 함수도 거부합니다.
</details>

<details class="answer" markdown="1"><summary>Fail을 누른 뒤 무엇을 더 해야 하나요?</summary>
문서는 `QC_COMPLETED`에 머뭅니다. 폐기 사유 코드를 넣고 **Scrap**을 눌러야 끝납니다. 사유 코드가 없으면 폐기할 수 없습니다.
</details>
