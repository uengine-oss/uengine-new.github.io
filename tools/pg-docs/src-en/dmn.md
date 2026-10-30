# Business rules (DMN) — let a table make the decision

> Describe the price list's volume discount in words to make a **decision table (DMN)**, save it as a version, and test it in inference mode. Then ask **Hanbit Office Quote Advisor**, which has the rule attached, and it answers with the discount rate from that rule.

## Why a decision table

When a rule like “20–49 of the same product get 5%, 50–99 get 8% …” sits in a document as text, people and AI have to reread and interpret it every time. A **decision table** puts such rules into rows of “condition (When) → result (Then)”. The standard name is DMN (Decision Model and Notation), and Process GPT calls it a **business rule**.

| Rule written as text | Decision table |
|---|---|
| Each reader may interpret it differently | Each condition has exactly one result row |
| Hard to find what changed after an edit | Saved as versions you can compare |
| The agent has to find and read the document | The agent finds the rule and uses it directly |

## Try it 1 — Make a decision table by describing it

<ol class="steps" markdown="1">
<li markdown="1">Under **Agent Colleagues** in the sidebar, open **Hanbit Office Quote Advisor** ([Chapter 10](agent-chat.html)).</li>
<li markdown="1">At the very bottom of the profile on the left, click **＋ next to Business Rule**. The DMN editor and a chat box open on the right, and the mode at the bottom left of the chat box is **Creation**.</li>
<li markdown="1">Type the following and send it.</li>
</ol>

![Business Rule ＋ — “Business Rule ＋” below the agent profile, the DMN editor (DRD) open on the right with an empty “New Decision” box, and the chat box in Creation mode](img/dmn-editor.webp)

```text
Make the Hanbit Office volume discount rule as a decision table. Input: order quantity of the same product (number). Output: discount (%). 1–19 → 0%, 20–49 → 5%, 50–99 → 8%, 100 or more → 12%.
```

In our run, after about 12 seconds the decision box was renamed **Hanbit Office Volume Discount**, and the chat below the editor said: “Created a Hanbit Office volume discount decision table: input is order quantity (number), output is discount (%). The table includes four rules covering all specified quantity ranges.”, followed by a list of the changes it made. Scroll down below the editor to see the chat. Decision and input/output names can differ between runs.

![After sending — the decision box in the DRD is now named “Hanbit Office Volume Discount”](img/dmn-generated.webp)

## Try it 2 — Open the table

Click the blue table icon at the top left of the decision box to open the decision table.

![Decision table — name “Hanbit Office Volume Discount”, Hit policy “Unique”, When “order_quantity” (number), Then “discount” (number), 4 rule rows](img/dmn-table.webp)

| # | When order_quantity | Then discount |
|---|---|---|
| 1 | `>= 1 and <= 19` | 0 |
| 2 | `>= 20 and <= 49` | 5 |
| 3 | `>= 50 and <= 99` | 8 |
| 4 | `>= 100` | 12 |

Expressions can also differ: for example, `>= 20 and < 50` covers the same whole-number order quantities as `>= 20 and <= 49`. Check that the quantity bands and discount rates match.

Hit policy **Unique** means exactly one row must match any input. Check in the table that the ranges don't overlap. You can click a cell to edit it, and add a row with the ＋ below the table. Go back with **‹** (View DRD) at the top left.

## Try it 3 — Save as a version

<ol class="steps" markdown="1">
<li markdown="1">Click 💾 next to **New DMN Decision** at the top right of the editor. The **Save DMN** dialog opens.</li>
<li markdown="1">Enter `Hanbit Office Volume Discount` in **Name**, and in **Description** write what the rule is for (for example, `Price list "2. Volume discount" — discount by quantity of the same product`). Leave **Version Tag** at **Minor Update** ("Current Version : v0.0 -> Next Version : v0.1").</li>
<li markdown="1">Click **Save**. “Saved successfully.” appears, the editor's title changes from **New DMN Decision** to **Hanbit Office Volume Discount**, and the rule shows up under **Business Rule** in the profile.</li>
</ol>

![Save DMN dialog — Name “Hanbit Office Volume Discount”, Version Tag Minor Update (v0.0 to v0.1), and the Description of the rule](img/dmn-save.webp)

!!! note "You need a name to save"
    If **Name** is empty, you can't click **Save**. As with process definitions ([Chapter 4](definition.html)), the version goes up one step each time you save.

## Try it 4 — Test it in inference mode

Switch the mode at the bottom left of the chat box from **Creation** to **Inference**, then ask:

```text
What is the discount for an order quantity of 40?
```

In our run, after about 12 seconds the answer came back. It first walked through the table and its hit policy, then gave a **Final Result**: “For an order quantity of 40, the discount applied is 5%.”, a small table (Order Quantity 40, Discount Rate 5%), “This is because 40 falls within the range 20–49, as specified by Rule 2.”, a practical note and a summary. Another run may simply give the 5% result without the explanation.

![Inference mode — mode Inference and “5. Final Result”: for an order quantity of 40 the discount is 5%, matched by Rule 2, with a practical note and a summary](img/dmn-infer.webp)

!!! tip "Test with boundary values"
    Ask about quantities where the range changes, such as 19 and 20, 49 and 50, or 99 and 100. You'll quickly see whether the table's range boundaries work as intended.

## Try it 5 — Ask the agent using the rule

Open the agent again, and **Hanbit Office Volume Discount** appears under **Business Rule** in the profile (scroll the profile down to see it). Ask in **New Chat** on the right.

![The agent opened again — the profile on the left down to “Business Rule ＋”, and an empty New Chat on the right](img/dmn-listed.webp)

```text
Find the registered business rule "Hanbit Office Volume Discount" and tell me the discount rate for an order of 60 Mesh Chair Air.
```

In our run, after about 25 seconds it answered from the rule: it showed the rule's four ranges as a table (1–19 → 0, 20–49 → 5, 50–99 → 8, 100 or more → 12), then “Order Quantity: 60 — Applicable Discount Rate: 8%” and “If you order 60 Mesh Chair Air, you will receive an 8% discount according to the "Hanbit Office Volume Discount" business rule.” It finds the rule and answers even though you didn't pick the price list from the Knowledge Base.

![The agent's answer — the Hanbit Office Volume Discount rules table and “Applicable Discount Rate: 8%” for an order of 60](img/dmn-agent-answer.webp)

## Next chapter

The decision table now handles the discount rate. Approval rules in the quote approval policy, such as “under KRW 30,000,000 the sales team lead approves; at KRW 30,000,000 or more the finance officer approves too”, can be made into a table the same way. Next, you'll look at the lead time and bottlenecks of the work you've run, on the analytics screens ([Chapter 16](analytics.html)).

!!! exercise "Check your understanding"
    1. What does the decision table's hit policy **Unique** mean?
    2. If you ask in inference mode “What if the quantity is 50?”, what percentage should you get? Which quantity band is it?
    3. If you turned the approver rule in Article 5 of the quote approval policy into a decision table, what would the input and output be?

<details class="answer" markdown="1"><summary>Answers</summary>

1. Exactly one row must match any input. The ranges must not overlap.
2. 8%, the 50–99 quantity band. 50 is outside the 20–49 band.
3. The input is “quote total (excluding VAT, number)” and the output is “approver” (e.g. `sales team lead`, `sales team lead + finance officer`). The rows are `< 30000000` → sales team lead and `>= 30000000` → sales team lead + finance officer.
</details>
