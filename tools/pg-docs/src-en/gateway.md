# Approve and reject — gateways and going back

> Create 「Sales Proposal Approval」, reject a proposal, and revise it for approval. Follow the branches chosen by the review result and the loop back to review.

!!! warning "Your installation needs these fixes"
    The run screens in this chapter were captured on an installation with the following fixes applied (2026-10-30). Installations from before these fixes reach the installation repository may stop partway through a run. This notice will be removed once the fixes are included.

    - Installation: [process-gpt-infra-docker #1](https://github.com/uengine-oss/process-gpt-infra-docker/pull/1) — missing columns in the task table; without them, the first submission stops.
    - Interface: [process-gpt-vue3 #234](https://github.com/uengine-oss/process-gpt-vue3/pull/234) — makes execution follow the first step and assigned role owners.
    - Interface: [process-gpt-vue3 #233](https://github.com/uengine-oss/process-gpt-vue3/pull/233) — preserves gateway conditions when saving in the editor.

## Add a decision to the flow

The process in Chapter 3 had no branches. This time, ask for approval and rejection from the start. You will create a new process, 「Sales Proposal Approval」.

The customer enters a request, and Minji writes a proposal. Jinyoung reviews it. If he rejects it, Minji revises it and sends it through review again. If he approves it, Minji handles the step for sending it to the customer.

## Try it 1 — Create the process through conversation

<ol class="steps" markdown="1">
<li markdown="1">Open a new conversation as in Chapter 3 and choose 「Basic Agent」.</li>
<li markdown="1">Enter the prompt below.</li>
<li markdown="1">When 「Shall I create the process from this draft?」 appears, choose 「Create the process as is」.</li>
</ol>

> Create a sales proposal approval process. The customer enters their request, then a sales representative writes a proposal and the sales team lead reviews it. If the sales team lead approves, the sales representative sends the proposal to the customer; if the lead rejects it, the sales representative reads the review comments and rewrites the proposal. Put a review result (approve or reject) and review comments in the team lead review form, and make an input form for each step.

![Process creation prompt — Basic Agent selected and the request for approval, rejection, and input forms](img/gw-prompt.webp)

When asking for a branch, say **who reviews**, **where approval leads**, and **where rejection leads**. Also ask for the form field that supplies the decision: 「Review Result」.

![Draft approval — the draft confirmation and Create the process as is choice](img/gw-draft-ok.webp)

After 「Created a work item to generate the process from the consultation.」, a progress indicator appears. Our run paused at 「waiting_for_user」 and 「72%」 for a confirmation.

## Try it 2 — Answer the single confirmation panel

This English run shows **one confirmation panel**. It asks whether to create a decision table (DMN) for the gateway. There are no separate skill or agent pages in this run.

The candidate is 「Proposal Approval Decision」 for 「Sales Proposal Approval」. It lists the approval and rejection branches.

![DMN confirmation — the Korean question, gateway candidate, optional text field, and disabled Submit response](img/gw-panel-1.webp)

<ol class="steps" markdown="1">
<li markdown="1">Leave the gateway candidate unselected. This exercise uses the BPMN branch conditions.</li>
<li markdown="1">Find 「Write your own (optional)」. Its placeholder is 「Type anything you'd like」.</li>
<li markdown="1">Enter `No decision table is needed — use the BPMN gateway conditions.`</li>
<li markdown="1">Click 「Submit response」 once it becomes enabled.</li>
</ol>

![Written confirmation response — No decision table is needed entered in the optional text field](img/gw-panel-2.webp)

「Submit response」 is disabled while nothing is selected or typed. Entering the response lets you continue without selecting a gateway for DMN conversion.

!!! note "This confirmation is still in Korean"
    The current version shows the DMN question and some generation progress text in Korean. 「DMN 의사결정 테이블을 어떤 게이트웨이에 만들까요?」 asks which gateways should become DMN decision tables. The submitted text bubble also starts with 「직접 입력:」, meaning direct input.

About ten seconds after submission, our run showed 「BPMN process generation complete」 and reported that one process had been created and saved.

![Generation complete — the completion message and Sales Proposal Approval result marked Saved](img/gw-generated.webp)

The result card is titled 「BPMN process generation result」 and includes 「Full graph」 and 「Saved」. The definition is saved automatically. There is no separate save button to click here.

## Read the gateway and the return arrow

The generated definition has three lanes: 「Customer」, 「Sales Representative」, and 「Sales Team Lead」.

The flow starts with 「Submit Sales Request」, then moves to 「Write Proposal」 and 「Review Proposal」.

![Approval flow — three lanes, Proposal Approval Decision, two conditional branches, and the rewrite loop](img/gw-bpmn.webp)

The diamond after review is 「Proposal Approval Decision」. An **X inside a diamond means an exclusive gateway**. The flow takes one outgoing branch whose condition matches.

| Condition beside the arrow | Next step | What follows |
|---|---|---|
| 「Review result is approve」 | 「Send Proposal to Customer」 | The process ends |
| 「Review result is reject」 | 「Read Comments & Rewrite Proposal」 | The flow returns to 「Review Proposal」 |

The arrow from rewriting back to review makes a loop. Rejection does not end this instance. Minji revises the proposal, and Jinyoung handles the same review step again.

!!! note "Check the names in your generated process"
    Generated step, form, and condition names can vary. This chapter uses the names from our run. Check that your approval path reaches customer sending and that your rejection path returns to review after revision.

## Try it 3 — Assign the lane owners

Use the same method as [Chapter 5](organization.html). In this definition's edit mode, the lanes are vertical columns with their names at the top.

<ol class="steps" markdown="1">
<li markdown="1">Open 「Sales Proposal Approval」 and click 「Edit」. Double-click the 「Sales Representative」 lane name.</li>
<li markdown="1">Choose 「Role Resolution By Direct user」 and select Minji Kim in 「User ID」. Save the panel.</li>
<li markdown="1">Double-click 「Sales Team Lead」. Use 「Role Resolution By Direct user」 to select Jinyoung Jang, then save and close the panel.</li>
<li markdown="1">Save the definition through 「Version Up」. Our version changes from v0.0 to v0.1.</li>
</ol>

![Sales team lead assignment — Sales Team Lead lane panel with Jinyoung Jang selected as the direct user](img/gwr-lane-manager.webp)

The automatic save after generation and this version save are separate. The version now includes the role owners. Jinyoung will also take the 「Customer」 role when opening the run.

!!! note "A breadcrumb still shown in Korean"
    The current version may show 「미분류 › 미분류」 in the definition breadcrumb. These are the uncategorized levels above the process.

## Try it 4 — Enter the customer request as Jinyoung

<ol class="steps" markdown="1">
<li markdown="1">As Jinyoung, click 「Execute」 for 「Sales Proposal Approval」.</li>
<li markdown="1">Check 「Role Mapping」: 「Customer」 is Jinyoung Jang, 「Sales Representative」 is Minji Kim, and 「Sales Team Lead」 is Jinyoung Jang.</li>
<li markdown="1">Enter the request below in 「Sales Request Details」, then click 「Submit Complete」.</li>
</ol>

> Hanbit Trading’s Daejeon branch is moving offices. It needs 30 work desks and 30 chairs, with a budget of KRW 20,000,000, installed before move-in in the first week of December.

![Filled run dialog — the three role owners and the Daejeon branch request](img/gwr-run-filled.webp)

Our instance name appears as 「Sales Proposal Approval · Hanbit Daejeon Office Fu…」. Use this instance name to find the right cards when switching between Jinyoung and Minji.

!!! note "A task tab still shown in Korean"
    The current version labels the similar-cases tab 「유사 사례」, even in English mode. Use 「Progress」 to view the process flow.

## Try it 5 — Write the proposal as Minji

In Minji's 「Task List」, open 「Write Proposal」 for this instance. 「Previous Activity Input」 includes 「Submit Sales Request · Jinyoung Jang」.

The current form is 「Write Proposal Layout」. Its 「Proposal Details」 field is a **plain text box**.

<ol class="steps" markdown="1">
<li markdown="1">Read Jinyoung's request in 「Previous Activity Input」.</li>
<li markdown="1">Enter the proposal below directly in 「Proposal Details」.</li>
<li markdown="1">Check the text, then click 「Submit Complete」.</li>
</ol>

> Daejeon branch move proposal: 30 work desks and 30 mesh chairs. Estimated about KRW 18,000,000 (VAT excluded).

![Filled proposal task — Previous Activity Input and the proposal in the plain Proposal Details text box](img/gwr-write-filled.webp)

There is no Report editor for this field. Type into the text box itself. In our run, 「Review Proposal」 reached Jinyoung about three seconds after submission.

## Try it 6 — Reject the proposal as Jinyoung

In Jinyoung's 「Task List」, open 「Review Proposal」. 「Previous Activity Input」 contains two entries: 「Submit Sales Request · Jinyoung Jang」 and 「Write Proposal · Minji Kim」.

The current form is 「Review Proposal Layout」.

<ol class="steps" markdown="1">
<li markdown="1">Read the request and proposal in 「Previous Activity Input」.</li>
<li markdown="1">Change 「Review Result」 from 「Approve」 to 「Reject」.</li>
<li markdown="1">Enter the comment below in 「Review Comments」.</li>
<li markdown="1">Check that 「Review Result」 is 「Reject」, then click 「Submit Complete」.</li>
</ol>

> The installation fee and schedule are missing. Please add the installation fee for the Daejeon area and an installation schedule before move-in, then rewrite it.

![Review ready for rejection — two previous inputs, Reject selected, and the installation-fee and schedule comment](img/gwr-review-reject-filled.webp)

!!! note "The first review defaults to Approve"
    Writing a rejection comment does not change the selected result. Change 「Review Result」 to 「Reject」 before submitting.

About eight seconds later, Minji received 「Read Comments & Rewrite Proposal」. 「Send Proposal to Customer」 did not open. The gateway took the rejection branch.

## Try it 7 — Revise the proposal as Minji

Open 「Read Comments & Rewrite Proposal」 as Minji. 「Previous Activity Input」 now includes the request, the first proposal, and Jinyoung's review.

The current form is 「Read Comments & Rewrite Proposal Layout」. It has two Report cards: 「Review Comments」 and 「Revised Proposal」.

![Rewrite task — three previous inputs and the Review Comments and Revised Proposal Report cards](img/gwr-rewrite.webp)

<ol class="steps" markdown="1">
<li markdown="1">Read the rejection comment in Jinyoung's 「Review Proposal」 entry under 「Previous Activity Input」.</li>
<li markdown="1">Open the 「Revised Proposal」 Report card for editing.</li>
<li markdown="1">Enter the revised proposal below in 「Content Editor」, then click 「Save」.</li>
<li markdown="1">Check the saved preview and click 「Submit Complete」.</li>
</ol>

> Revised Daejeon branch move proposal: 30 work desks and 30 mesh chairs, products about KRW 18,000,000 (VAT excluded). Includes the Daejeon installation fee; installed over two days in the first week of December, before move-in.

![Revised proposal editor — the proposal now includes the Daejeon installation fee and a two-day installation schedule](img/gwr-rewrite-report.webp)

!!! note "Read the comment in the previous input"
    The rewrite form's 「Review Comments」 Report card is empty. Jinyoung's comment is not copied into it automatically. Read his review under 「Previous Activity Input」.

About three seconds after submission, 「Review Proposal」 returned to Jinyoung. The flow followed the return arrow to the same review step.

## Try it 8 — Approve and record sending to the customer

Open 「Review Proposal」 again as Jinyoung. This time, the form **keeps the previous values**. It opens with 「Reject」 and the old comment already filled in.

![Reopened review before editing — Reject and the previous installation-fee and schedule comment remain filled in](img/gwr-review-approve.webp)

<ol class="steps" markdown="1">
<li markdown="1">Read Minji's revised proposal in the previous inputs.</li>
<li markdown="1">Change 「Review Result」 from 「Reject」 to 「Approve」.</li>
<li markdown="1">Replace 「Review Comments」 with `Good — the installation schedule is included. Please send it to the customer.`</li>
<li markdown="1">Check both values, then click 「Submit Complete」.</li>
<li markdown="1">Switch to Minji and open 「Send Proposal to Customer」 when it arrives.</li>
<li markdown="1">In 「Send Proposal to Customer Layout」, leave the 「Draft Proposal」 file field empty for this exercise. In the 「Review Result」 text field, enter `Approved — sent the revised proposal with the installation schedule`.</li>
<li markdown="1">Click 「Submit Complete」.</li>
</ol>

![Second review ready to submit — Approve selected and the old comment replaced with approval](img/gwr-review-approve-filled.webp)

The customer-sending task reached Minji about five seconds after approval in our run. This time, the gateway took the approval branch.

![Customer-sending task — empty Draft Proposal file field and the completed Review Result text](img/gwr-send-filled.webp)

This exercise records the sending step in a form. Submitting the text is not itself an email-sending action.

!!! note "Check retained values when a step returns"
    The first review defaulted to 「Approve」, but the reopened review retained 「Reject」. Do not assume a repeated step has reset its form. Check the result and replace the old comment before submitting.

## Try it 9 — Check that the instance is complete

<ol class="steps" markdown="1">
<li markdown="1">Check that the instance status is 「COMPLETED」.</li>
<li markdown="1">In Jinyoung's window, open 「Kanban Board」 and count the five cards under 「Done」.</li>
<li markdown="1">Check that there is only one 「Review Proposal」 card, even though Jinyoung reviewed twice.</li>
</ol>

![Completed instance — COMPLETED status and five cards in Done, including one Review Proposal card](img/gwr-done-kanban.webp)

The five cards are:

- 「Send Proposal to Customer」 — Minji Kim
- 「Read Comments & Rewrite Proposal」 — Minji Kim
- 「Review Proposal」 — 「My task」
- 「Write Proposal」 — Minji Kim
- 「Submit Sales Request」 — 「My task」

There is one review card because **the same step reopened**. A separate second review step was not created. The instance finished after rejection, revision, another review, and the final customer-sending submission.

## Next chapter

You followed a branch based on a review result and a loop that returned work for revision. You have now created and run processes handled by people.

In [Chapter 8](knowledge.html), you will upload company documents to the Knowledge Base so agents can use them as sources. In [Chapter 13](agent-steps.html), you will run an agent-assisted quote process whose approval path depends on whether the total is below KRW 30,000,000 or at least that amount.

!!! exercise "Check your understanding"
    1. Does a diamond with an X send work down every outgoing arrow?
    2. How does Jinyoung reject the proposal, and where does Minji read his comment?
    3. What must Jinyoung change when the review reopens?
    4. Why is there only one completed review card after two reviews?

<details class="answer" markdown="1"><summary>Answers</summary>

1. No. An exclusive gateway takes one branch whose condition matches. Here, rejection leads to rewriting and approval leads to customer sending.
2. He changes 「Review Result」 from 「Approve」 to 「Reject」 and enters 「Review Comments」. Minji reads his review under 「Previous Activity Input」.
3. The reopened form keeps 「Reject」 and the old comment. He must select 「Approve」 and replace the comment before submitting approval.
4. The same 「Review Proposal」 step reopened after revision. The process did not create a separate second review step.
</details>
