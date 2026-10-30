# Final project — Hanbit Office A/S intake

> Read Hanbit Office's after-sales service policy and build a process that connects an agent's warranty assessment with human approval. Complete one free-service case and one paid-service case, then review the work through KPIs and execution analytics.

## Complete the project yourself

You are Jinyoung Jang, Hanbit Office's sales team lead and service lead. You want to handle customer after-sales service requests from intake through the completion report.

Minji Kim handles intake, paid-service quotes, and repair-result records. Seoyeon Park, the finance officer, checks costs at or above the policy's approval threshold.

This chapter is a project in **reading a policy, building a definition, and verifying it through execution**. It does not ask you to reproduce a fixed set of screens. Generated names and form layouts may differ from the examples. The policy conditions, owners, and order of work must be correct.

Finish the required work first. Then add a decision table, skill, or MCP tool as optional work. Even without the optional tasks, complete both instances, measure the KPI, and review the analytics.

## Prepare the policy and expected flow

Download [Hanbit Office A/S policy (PDF)](files/Hanbit-Office-AS-Policy.pdf). Read Articles 1–7. Check that you can use Minji Kim's and Seoyeon Park's accounts.

The definition needs a branch between **free and paid service** and a branch that decides whether **paid repair costs of KRW 500,000 or more** need a finance check. Include approval, rejection, and the return path for a revised quote.

| Part | Flow required by the policy |
|---|---|
| Intake and warranty assessment | Minji records the request → agent assesses warranty coverage |
| Free service | On-site repair → completion report |
| Paid service below KRW 500,000 | Paid-service quote → Jinyoung approves → on-site repair → completion report |
| Paid service of KRW 500,000 or more | Paid-service quote → Jinyoung approves → Seoyeon checks costs → on-site repair → completion report |
| Rejection | Record the reason → return to the paid-service quote → follow approval rules for the revised amount |

!!! note "Check both business conditions"
    The two conditions are free versus paid service and the cost threshold. The diagram may need more than two diamonds to represent approval and rejection. Do not remove a rejection path just to match a gateway count.

## Task 1 — Upload the policy to the Knowledge Base

Reference: [Chapter 8](knowledge.html).

<ol class="steps" markdown="1">
<li markdown="1">Upload the practice PDF to 「Knowledge Base」.</li>
<li markdown="1">Find the warranty period, user-caused damage conditions, visit fees, approval threshold, and visit deadline.</li>
<li markdown="1">Select the policy in a conversation and ask about warranty coverage and approval rules. Compare the answer with the original document.</li>
</ol>

Free service requires both conditions: the product is within two years of purchase, and the problem is not caused by user fault.

Paid repair cost includes the visit fee as well as parts. Explain these two rules in your own words before continuing.

## Task 2 — Create the process with Deep Agent

Reference: [Chapter 12](document-process.html).

<ol class="steps" markdown="1">
<li markdown="1">In the conversation with the policy selected, ask 「Deep Agent」 to create the process. Use the prompt below as a starting point.</li>
<li markdown="1">Check that an agent handles warranty assessment while people handle approval and cost checking.</li>
<li markdown="1">Review the draft and continue generation. If an agent-selection confirmation appears, select the agent needed for warranty assessment.</li>
</ol>

> Create an “A/S Intake” process that follows the selected Hanbit Office A/S policy. Minji Kim records requests and prepares paid-service quotes. An agent should assess warranty coverage from the policy and record both the result and its reasons. Send free-service cases to on-site repair and paid-service cases to quotation and approval. Jinyoung Jang approves paid repair costs. If the total is KRW 500,000 or more, Seoyeon Park checks the costs after Jinyoung's approval. On rejection, record the reason and return to the paid-service quote. Minji records the on-site repair result. Include the service date, work performed, and billed amount in the completion report. Also reflect the requirement to visit within 5 business days of intake.

The intake form needs the customer company, product name, purchase date, symptoms, and preferred visit date. The intake date, user-fault status, and visit region must also be available for warranty assessment and quotation.

Do not let the agent guess missing facts.

## Task 3 — Compare the definition with the policy

Reference: [Chapter 12](document-process.html).

A generation-complete message does not finish the task. Put the policy and definition side by side and check the following.

<ol class="steps" markdown="1">
<li markdown="1">Confirm that free service requires purchase within two years and no user fault.</li>
<li markdown="1">Check that the visit fee is KRW 30,000 for Seoul and Gyeonggi, and KRW 50,000 for other regions.</li>
<li markdown="1">Check that a cost of exactly KRW 500,000 goes to Seoyeon's cost check after Jinyoung's approval.</li>
<li markdown="1">Find the rejection-reason field and the return path to the paid-service quote.</li>
<li markdown="1">Check the completion-report fields and the visit deadline of 5 business days after intake. Request specific corrections for any mismatch.</li>
</ol>

For example, if the finance check comes before the team lead's approval, ask:

> This differs from Article 5. If paid repair costs are KRW 500,000 or more, Jinyoung Jang must approve first, then Seoyeon Park must check the costs. Correct that order. On rejection, record the reason and return to the paid-service quote.

Check the same conditions again after the change. Writing a deadline into the definition does not prove that it will be met. Compare the intake date and visit date during execution too.

## Task 4 — Assign the lane owners

Reference: [Chapter 5](organization.html).

<ol class="steps" markdown="1">
<li markdown="1">Edit the definition. For each human lane, use 「Role Resolution By Direct user」 to assign the owner below.</li>
<li markdown="1">Check that the selected agent owns the warranty-assessment step.</li>
<li markdown="1">Save a version of the definition with these assignments.</li>
</ol>

| Role | Owner |
|---|---|
| Intake, paid-service quotation, repair-result recording, completion report | Minji Kim |
| Sales team lead and service lead | Jinyoung Jang |
| Finance officer and cost check | Seoyeon Park |
| Warranty assessment | An agent that uses the policy |

Record a practice repair result in the on-site repair step. You do not need to add a separate repair-technician account.

## Task 5 — Complete both cases

References: [Chapter 6](process-run.html) · [Chapter 7](gateway.html) · Chapter 13 (coming soon).

Run the following cases separately. Choose practice customer names and intake dates. Set the purchase dates to one year and three years before the corresponding intake date. Choose preferred visit dates within 5 business days of intake.

| Input | Case A — broken chair caster | Case B — standing-desk motor replacement |
|---|---|---|
| Purchase date | One year before intake | Three years before intake |
| Symptoms | Chair caster broke during normal use | Standing-desk motor failure |
| User fault | No | No |
| Visit region | Seoul | Busan |
| Parts cost | Not billed for this free-service case | KRW 600,000 |
| Expected policy path | Free service → on-site repair | Paid service → team lead approval → finance check → on-site repair |
| Expected billed amount | KRW 0 | KRW 650,000 |

A broken caster alone does not establish free-service eligibility. This case explicitly has **no user fault**.

The desk is outside the warranty period even though there is no user fault. Add the Busan visit fee of KRW 50,000 to its parts cost.

<ol class="steps" markdown="1">
<li markdown="1">As Jinyoung, open 「Execute」 and check the owners in 「Role Mapping」.</li>
<li markdown="1">Complete Minji's intake task. Continue through each owner's 「Task List」.</li>
<li markdown="1">Read the agent's warranty result and reasons. Compare the purchase date, intake date, and user-fault status with the inputs.</li>
<li markdown="1">For the paid case, have Minji prepare the quote. Complete Jinyoung's approval, then Seoyeon's cost check. Check each form before clicking 「Submit Complete」.</li>
<li markdown="1">Record the repair result and completion report for both cases. Include the service date, work performed, and billed amount.</li>
<li markdown="1">Check that both instances are 「COMPLETED」 and review their completed tasks in 「Kanban Board」.</li>
</ol>

The paid case's “two approvals” in the submission checklist mean **Jinyoung's approval and Seoyeon's cost check**. Verify both records and their order. Card counts alone do not establish how many approvals occurred.

!!! note "Separate expected results from observed results"
    The table gives amounts and paths derived from the policy. You must verify the path actually taken during execution. If it differs, inspect the inputs, agent result, and branch conditions. Do not submit an unfinished instance as completed.

## Task 6 — Make a warranty decision table〔Optional〕

Reference: [Chapter 15](dmn.html).

<ol class="steps" markdown="1">
<li markdown="1">Create a decision table with warranty-period eligibility and user-fault status as inputs, and free or paid service as the output.</li>
<li markdown="1">Test within two years with no user fault, within two years with user fault, and over two years. Also test exactly two years.</li>
<li markdown="1">Attach the rule to the agent. Ask about the same conditions and compare the answers with the decision table.</li>
</ol>

Submit the decision table, test inputs, and actual answers together. Meeting the warranty-period condition alone must not produce free service.

## Task 7 — Measure the KPI and find bottlenecks

References: [Chapter 17](strategy.html) · [Chapter 16](analytics.html).

<ol class="steps" markdown="1">
<li markdown="1">Create an objective for improving A/S handling in 「Strategy Board」.</li>
<li markdown="1">Use 「Add KPI」 to add an “Average A/S handling time” KPI. Set 「Measure type」 to 「Avg duration」 and link the A/S process in 「Linked process definition」. Measure from intake through the completion report and state the unit clearly.</li>
<li markdown="1">Prepare the measurement settings using the method from Chapter 17, then click 「Refresh Metrics」. Record the displayed value, unit, measurement time, and number of cases.</li>
<li markdown="1">Inspect this process in the analytics dashboard and process heatmap. Look for steps that took longer.</li>
<li markdown="1">Record the observed step and a proposed improvement. If two cases are insufficient, explain which additional execution records you need.</li>
</ol>

Average handling time and the requirement to visit within 5 business days measure different things. The first ends at the completion report. The second is a visit deadline. An average alone cannot show that every case met that deadline.

Fast practice runs may not represent real waiting time. Separate what the screen shows from what you still need to investigate.

## Task 8 — Reuse the completion report〔Optional〕

References: [Chapter 11](skills.html) · [Chapter 14](mcp-hub.html).

<ol class="steps" markdown="1">
<li markdown="1">Create a completion-report skill that requires the service date, work performed, and billed amount. Upload it and attach it to the agent.</li>
<li markdown="1">Check the 「office」 registration in settings under 「MCP Servers」 and the agent's 「Tools」 connection, as in Chapter 14.</li>
<li markdown="1">Use the MCP tool to create a completion-report document from a completed case. Open the document and compare it with the original records.</li>
</ol>

Check that the agent has not added repair work absent from the records. Submit only the skill behavior and document results you actually verified.

## Deliverables and completion checklist

Use this table as your checklist. Record whether each requirement is met and where its evidence can be found. Mark optional work “Not done” if you did not attempt it.

| Type | Deliverable or criterion | Status |
|---|---|---|
| Required | Definition checked against the policy: free/paid branches, KRW 500,000 threshold, and return to quotation after rejection | □ Met □ Needs work |
| Required | Lane owners: Minji Kim, Jinyoung Jang, Seoyeon Park, and the warranty-assessment agent | □ Met □ Needs work |
| Required | Both instances are COMPLETED, with records of both approval stages for the paid case | □ Met □ Needs work |
| Required | A person checked both agents' warranty results and reasons against the policy and inputs | □ Met □ Needs work |
| Required | Completion reports include service date, work performed, and billed amount; visit deadlines were checked | □ Met □ Needs work |
| Required | Actual average A/S handling time, unit, measurement time, and case count | □ Met □ Needs work |
| Required | Analytics screen and a bottleneck observation, or a reason further evidence is needed | □ Met □ Needs work |
| Optional | Warranty decision table and test results, including boundary cases | □ Met □ Needs work □ Not done |
| Optional | Completion-report skill and its observed application | □ Met □ Needs work □ Not done |
| Optional | MCP-generated completion report compared with the original records | □ Met □ Needs work □ Not done |

## Common pitfalls

| Situation | What to check |
|---|---|
| Every run owner appears as Jinyoung. | Unassigned lanes may default to the person starting the run. Check 「Role Resolution By Direct user」 and the owners in the run dialog. [Chapter 5](organization.html) |
| Saving shows 「A gateway requires at least 2 branches」. | Read the validation message and use 「Save Anyway」 to save. Then check that the required conditions and paths exist; saving does not repair the gateway. Chapter 13 (coming soon) |
| The next form is empty. | Previous values do not automatically fill the next form. Read 「Previous Activity Input」 and enter the needed values. [Chapter 6](process-run.html) |
| The process approves even though a rejection comment was entered. | The review choice may initially be 「Approve」. Change it to 「Reject」 before submitting. [Chapter 7](gateway.html) |
| The agent's calculation or dates look wrong. | Compare the output with the policy and inputs. Do not submit unchecked calculations or dates. Chapter 13 (coming soon) |
| Deep Agent holds generation or produces a different draft. | Generation can vary. State the required conditions precisely and request a correction. [Chapter 12](document-process.html) |
| Generation seems stuck at a confirmation panel. | Complete every required confirmation. If there are several pages, advance through them and submit the final response. In the Chapter 7 English run, the single panel used 「Submit response」 after a choice or written response. [Chapter 7](gateway.html) |
| A task remains after closing the run dialog. | Opening and closing the dialog can leave a first-step task behind. Check 「Task List」 before starting another run. [Chapter 5](organization.html) |

## Next chapter

You have practiced describing recurring work, checking and correcting a definition, and running it with people and agents. This final project asks you to verify that a document's rules appear correctly in the flow, assignments, and execution records.

For a new workflow, follow the same order: read the policy, check the draft, assign owners, verify execution, and measure the result.

Use the [cheatsheet](cheatsheet.html) to find features and steps again. Use the [FAQ](faq.html) when you get stuck.

!!! exercise "Check your understanding"
    1. Besides the purchase date, what must you check before classifying the chair case as free service? Why record the assessment reasons?
    2. What amount determines the approval path for the Busan motor replacement, and where does rejection lead?
    3. If both instances finish and average handling time is short, does that prove the A/S process has improved enough?

<details class="answer" markdown="1"><summary>Answers</summary>

1. Check that there is no user fault. Recording the reasons lets a person compare the result with the policy and inputs, and investigate an incorrect assessment.
2. Use KRW 650,000: KRW 600,000 for parts plus the KRW 50,000 Busan visit fee. Jinyoung approves first, then Seoyeon checks the costs. Rejection records a reason and returns to the paid-service quote.
3. No. Two practice cases are insufficient. Check measurement scope and units, visit deadlines, and waiting at each step. Gather more real execution records before judging the improvement.
</details>
