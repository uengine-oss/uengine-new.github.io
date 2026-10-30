# Strategy board and KPIs

> Add completed-count, duration, and satisfaction KPIs to 「Grow bulk order revenue」. Complete another process, answer its surveys, and compare the refreshed measurements.

!!! warning "Your installation needs these fixes"
    The run screens in this chapter were captured on an installation with the following fix applied (2026-10-30). Before this fix reaches the installation repository, the strategy service may fail to connect. This notice will be removed once the fix is included.

    - Installation: [process-gpt-infra-docker #1](https://github.com/uengine-oss/process-gpt-infra-docker/pull/1) — fixes the strategy service's graph database connection.

## Connect execution records to an objective

In [Chapter 16](analytics.html), you read execution times and bottlenecks. Now you will create a strategic objective and connect process records and survey responses to its KPIs.

Jinyoung Jang creates the objective and KPIs as the admin. Minji Kim completes another sales proposal and answers a survey. Jinyoung also answers, then refreshes the measurements.

The objective is 「Grow bulk order revenue」. Its KPIs count completed proposals, measure approval time, and collect proposal satisfaction. This exercise does not measure revenue itself. Keep the objective's name separate from what its KPIs actually measure.

## Try it 1 — Explore the strategy board

<ol class="steps" markdown="1">
<li markdown="1">Open 「Strategy Board」.</li>
<li markdown="1">Read 「BSC strategy map · KPIs · initiatives」.</li>
<li markdown="1">Find 「Financial」, 「Customer」, 「Internal Process」, and 「Learning & Growth」.</li>
</ol>

![Empty strategy board — four perspectives and the board controls](img/st-board.webp)

Each empty perspective shows 「No objectives in this perspective yet」. The controls include 「Import legacy map」, 「Refresh Metrics」, 「AI Edit」, and 「Add Objective」.

Two buttons remain in Korean: 「전략 정합성 검사」 means strategy consistency check, and 「온톨로지 뷰」 means ontology view.

This exercise adds one objective under 「Financial」. You do not need to fill all four perspectives to test KPI measurements.

## Try it 2 — Add the strategic objective

<ol class="steps" markdown="1">
<li markdown="1">Click 「Add Objective」.</li>
<li markdown="1">Set 「Name」 to 「Grow bulk order revenue」.</li>
<li markdown="1">Set 「Description」 to 「Grow revenue from bulk orders (20 or more pieces of office furniture)」.</li>
<li markdown="1">Choose 「Financial」 in 「Perspective」.</li>
<li markdown="1">Keep 「Strategic importance」 at 3 and click 「Save」.</li>
</ol>

![Add Objective dialog — the revenue objective, description, Financial perspective, and importance 3](img/st-obj-dialog.webp)

The dialog also has 「Parent objectives」. This is the first objective on the board, so no parent is needed for the exercise.

「Strategic importance」 includes the explanation 「1 (low) – 5 (high) — used as the weight for contribution aggregation」.

The description's “20 or more” threshold describes the objective. It does not automatically filter the completed-count KPI by order quantity. That KPI will count completions of a linked process definition.

![Saved objective — Grow bulk order revenue with 0 KPI, 0 initiatives, and Not measured](img/st-obj-saved.webp)

The card initially shows 「0 KPI · 0 initiatives · Not measured」. A Korean 「전략맵 초기화」 button also appears after the first objective; it means reset strategy map.

## Try it 3 — Add the proposal-count KPI

<ol class="steps" markdown="1">
<li markdown="1">Open the 「Grow bulk order revenue」 card.</li>
<li markdown="1">Choose the 「KPI」 tab and click 「Add KPI」.</li>
<li markdown="1">Enter the settings below.</li>
<li markdown="1">Check the linked process, unit, baseline, target, and direction, then save.</li>
</ol>

![Objective panel — KPI, Initiatives, Contribution, and Add KPI](img/st-obj-panel.webp)

The panel has 「KPI」, 「Initiatives」, and 「Contribution」 tabs. This exercise adds KPIs only.

| Field | Value |
|---|---|
| 「Name」 | 「Sales proposals sent」 |
| 「Measure type」 | 「Completed count」 |
| 「Linked process definition」 | 「Sales Proposal Submission」 |
| 「Unit」 | cases |
| 「Baseline」 | 0 |
| 「Target」 | 10 |
| 「Direction」 | 「Higher is better」 |

For 「Description」, explain that this KPI counts completed sales proposal processes. This makes its scope clear.

![Completed-count KPI — Sales Proposal Submission linked to Sales proposals sent, with target 10](img/st-kpi1-filled.webp)

The dialog also includes 「AI Suggest」, 「Strategic importance」, 「Period start」, and 「Period end」. This chapter enters the measured KPI types and targets directly.

The KPI name says proposals sent, but the selected measure is 「Completed count」. It counts completion records for the linked process. It does not read an email system to verify messages sent.

## Try it 4 — Add the approval-time KPI

<ol class="steps" markdown="1">
<li markdown="1">Click 「Add KPI」 again.</li>
<li markdown="1">Enter the settings below for 「Proposal approval time」.</li>
<li markdown="1">Check that the baseline and target use hours.</li>
<li markdown="1">Choose 「Lower is better」 and save.</li>
</ol>

| Field | Value |
|---|---|
| 「Name」 | 「Proposal approval time」 |
| 「Measure type」 | 「Avg duration」 |
| 「Linked process definition」 | 「Sales Proposal Approval」 |
| 「Unit」 | hours |
| 「Baseline」 | 48 |
| 「Target」 | 24 |
| 「Direction」 | 「Lower is better」 |

Use 「Description」 to explain that this measures average elapsed time from the customer request through sending the approved proposal.

![Duration KPI — Proposal approval time with baseline 48 hours, target 24 hours, and Lower is better](img/st-kpi2-filled.webp)

The count KPI improves as its value rises. The duration KPI improves as its value falls. Do not enter a number of minutes or seconds into a target expressed in hours.

This chapter uses 「Completed count」, 「Avg duration」, and 「Survey score」. It does not connect an external revenue system.

## Try it 5 — Refresh the first measurements

<ol class="steps" markdown="1">
<li markdown="1">Click 「Refresh Metrics」 on the board.</li>
<li markdown="1">Check the objective card.</li>
<li markdown="1">Open the objective panel and read both KPI values.</li>
</ol>

![First measurement board — the objective after refreshing its two process-based KPIs](img/st-measured-board.webp)

The panel shows:

| KPI | Current / target | Achievement shown |
|---|---|---:|
| 「Sales proposals sent」 | 「1 / 10 cases」 | 10% |
| 「Proposal approval time」 | 「0.04 / 24 hours」 | 150% |

![First KPI measurements — Sales proposals sent at 1/10 and Proposal approval time at 0.04/24](img/st-measured-panel.webp)

The duration KPI appears as 「Avg duration (h)」 in the measured panel. It is set to 「Lower is better」. The practice runs were much shorter than the 24-hour target, so the displayed achievement reached the 150% cap.

!!! note "150% is not a time-saving percentage"
    Read 150% as the displayed KPI achievement. It does not mean elapsed time fell by 150%. Read it together with the current value of 0.04 hours, the 24-hour target, and 「Lower is better」.

## Try it 6 — Add a satisfaction survey KPI

<ol class="steps" markdown="1">
<li markdown="1">Click 「Add KPI」 in the objective panel.</li>
<li markdown="1">Set 「Name」 to 「Proposal satisfaction」. Use 「Description」 to explain that it measures participants' satisfaction after the proposal process.</li>
<li markdown="1">Choose 「Survey score」 in 「Measure type」 and 「Sales Proposal Submission」 in 「Linked process definition」.</li>
<li markdown="1">Set 「Unit」 to points and 「Target」 to 4.5.</li>
<li markdown="1">Under 「Survey questions (auto-sent on process completion)」, click 「Add question」.</li>
<li markdown="1">Enter 「How satisfied were you with this proposal?」 for Q1, then save.</li>
</ol>

![Survey KPI — Proposal satisfaction linked to Sales Proposal Submission, with target 4.5 and the survey question](img/st-survey-kpi.webp)

The dialog explains: 「When the linked process completes, a survey workitem is issued to participants/requesters automatically.」

Entering a target of 4.5 does not create a measured score of 4.5. Responses must be collected first.

This exercise surveys process participants. It does not demonstrate a survey sent to an external customer. In the captured run, Minji and Jinyoung received the survey workitems.

## Try it 7 — Complete another proposal process

After saving the survey KPI, run 「Sales Proposal Submission」 again using the method from [Chapter 6](process-run.html).

<ol class="steps" markdown="1">
<li markdown="1">As Jinyoung, run 「Sales Proposal Submission」.</li>
<li markdown="1">Enter the customer request below.</li>
<li markdown="1">As Minji, complete the proposal task with the response below and click 「Submit Complete」.</li>
<li markdown="1">Check that the process is 「COMPLETED」.</li>
<li markdown="1">Find 「설문: Proposal satisfaction」 in Minji's 「Task List」.</li>
</ol>

Customer request:

> Hanbit Trading needs 8 standing desks for its Pangyo office, with a budget of KRW 8,000,000, installed in mid-December.

Minji's proposal:

> Pangyo office proposal: 8 standing desks, about KRW 7,200,000 (VAT excluded), installed in the 3rd week of December.

Both Minji and Jinyoung received survey workitems after completion.

![Survey workitem — the task titled 설문: Proposal satisfaction](img/st-survey-list.webp)

The generated workitem still has the Korean prefix 「설문:」, meaning survey. Its description also contains 「완료에 따른 KPI 설문」, meaning a KPI survey following completion. Check the instance named in that description.

!!! note "The objective description does not filter the KPI"
    The objective describes orders of 20 or more pieces. This new order has only eight desks, but completing the linked process still increases the count. The quantity condition in the objective description is not automatically applied to the KPI.

## Try it 8 — Answer the surveys as Minji and Jinyoung

<ol class="steps" markdown="1">
<li markdown="1">Open Minji's 「설문: Proposal satisfaction」 workitem.</li>
<li markdown="1">Read the completed process name and 「How satisfied were you with this proposal?」.</li>
<li markdown="1">Choose five stars.</li>
<li markdown="1">Enter the comment below and click 「Submit」.</li>
<li markdown="1">Check for 「Thank you for your response!」.</li>
<li markdown="1">Open Jinyoung's survey for the same instance, choose four stars, and submit it.</li>
</ol>

> The request was clear, so I could send the proposal quickly.

![Survey form — Proposal satisfaction, Process Satisfaction Survey, the completed process name, and the question](img/st-survey-open.webp)

The screen is titled 「Proposal satisfaction」 and 「Process Satisfaction Survey」. It says:

> The process 'Sales Proposal Submission · Hanbit Trading standin' has completed. Please answer the questions below.

Read the process name before responding so that the rating applies to the intended execution.

![Minji's survey response — five stars and the comment about sending the proposal quickly](img/st-survey-filled.webp)

Minji gave 5 points, and Jinyoung gave 4. These are practice values used to demonstrate measurement. They are not the correct satisfaction ratings for every execution.

![Survey submitted — Thank you for your response! and Back to todolist](img/st-survey-done.webp)

After submission, the screen offers 「Back to todolist」. Submitting responses and refreshing the strategy measurements are separate actions.

## Try it 9 — Compare the second measurements

<ol class="steps" markdown="1">
<li markdown="1">As Jinyoung, return to 「Strategy Board」.</li>
<li markdown="1">Click 「Refresh Metrics」.</li>
<li markdown="1">Open 「Grow bulk order revenue」 and read all three KPIs.</li>
<li markdown="1">Compare them with the first measurements.</li>
</ol>

![Second measurement — proposal count 2/10, approval time 0.04/24, and satisfaction 4.50/4.50](img/st-measured2.webp)

| KPI | Second measurement | Achievement shown |
|---|---|---:|
| 「Sales proposals sent」 | 「2 / 10 cases」 | 20% |
| 「Proposal approval time」 | 「0.04 / 24 hours」 | 150% |
| 「Proposal satisfaction」 | 「4.50 / 4.50 points」 | 100% |

The proposal count rose from 1 to 2. Satisfaction now shows 4.50, matching the average of the two responses: `(5 + 4) ÷ 2 = 4.5`.

Approval time stayed at 0.04 hours. The new execution was 「Sales Proposal Submission」. The duration KPI is linked to 「Sales Proposal Approval」, a different process definition.

![Final strategy board — Grow bulk order revenue with 3 KPI, 0 initiatives, and 90%](img/st-board-final.webp)

The objective card shows 「3 KPI · 0 initiatives · 90%」. This summarizes the configured KPIs. It is not a measurement of actual revenue.

## Try it 10 — Check overall progress and the ontology

<ol class="steps" markdown="1">
<li markdown="1">Open 「KPI & Progress」 and read overall strategy achievement.</li>
<li markdown="1">Read the lower KPI and process-pipeline sections separately.</li>
<li markdown="1">Return to the board and open 「온톨로지 뷰」 to inspect the ontology.</li>
</ol>

![KPI and progress — Strategy Achievement Overall 90% and the separate empty pipeline sections](img/st-kpi-progress.webp)

The top shows 「Strategy Achievement Overall 90%」 and 「Grow bulk order revenue 90% Financial」.

The lower 「KPI Achievement」 section shows 「At Risk 0%」, 「Target 0」, and 「Current Published 0」. 「Process Pipeline」 shows 0 for 「Draft」, 「Review」, and 「Published」.

The explanation says 「Only processes published after review are counted toward KPI targets」. 「Weekly Deployment Velocity」 shows 「No data available」.

!!! note "These sections do not measure the same thing"
    Overall achievement is 90%, while another section shows 「At Risk 0%」. Pipeline counts of 0 do not mean no process instances were completed. Keep each value with its section name and explanation. The captured evidence does not establish every relationship between these aggregates.

The ontology page remains almost entirely Korean in English mode. Its heading is 「기업 운영 온톨로지」, meaning enterprise operations ontology. Its subtitle describes four layers: strategy, process, resources, and knowledge.

![Ontology — the Korean interface with 71 nodes, 66 relationships, and the English legend](img/st-ontology.webp)

The run shows 「노드 71」 and 「관계 66」: 71 nodes and 66 relationships.

The tabs include 「온톨로지 그래프」, 「영향도 분석」, and 「전략 개선점」, meaning ontology graph, impact analysis, and strategy improvements. 「전략보드에서 편집」 means edit in the strategy board.

The English legend includes Strategy, KPI, Initiative, Process, Task, User, Agent, Team, and Skill. This view helps inspect connections. Node and relationship counts do not prove that a strategy is appropriate.

## Next chapter

You attached three KPIs to an objective and refreshed their measurements after another completion and two survey responses. You separated the objective description, measurement scope, and displayed achievement.

In [Chapter 18](settings.html), you will review settings. In [Chapter 19](project.html), you will combine these skills in a final project.

!!! exercise "Check your understanding"
    1. Which direction did you choose for proposal count and approval time?
    2. What produced the satisfaction score of 4.50?
    3. Does the objective's 90% mean Hanbit Office achieved 90% of a revenue target?

<details class="answer" markdown="1"><summary>Answers</summary>

1. 「Higher is better」 for proposal count, with a target of 10 cases. 「Lower is better」 for approval time, with a target of 24 hours.
2. After adding the survey KPI, another 「Sales Proposal Submission」 instance completed. Minji answered 5 and Jinyoung answered 4. Jinyoung then clicked 「Refresh Metrics」.
3. No. This exercise measured process completions, duration, and participant satisfaction, not revenue. The objective's quantity threshold also did not automatically filter the completed-count KPI.
</details>
