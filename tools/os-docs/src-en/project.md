# Capstone Project — Build a Quality Incident Response App

> This project brings together everything you have learned. Around a quality incident, you connect source data, build an ontology, run queries and actions, and turn the whole process into one app. It is a team project (2–3 people) of about 2–3 hours.

## The situation

On Monday morning, Tokyo Devices, a customer in Tokyo, files a “PCB soldering defect” claim (T-3). The quality team lead asks:

1. Which supplier did this defective PCB come from, and how much of that supplier's **quantity has not arrived yet**?
2. What **open orders from other customers** use the same PCB?
3. Put that supplier's open purchase orders **on hold** until the investigation is done, and send a **notice** to the affected customers.
4. Turn all of this into **one screen** to check every day.

## Tasks

### Step 1 — Connect the data (Chapters 5–6)

- Expose `erp.po_line` as the `PoLine` virtual node and create the `IN_ORDER` and `OF_ITEM` relationships (if you did this in Chapter 6, reuse it).
- **Deliverable**: a screenshot of the `SHOW VIRTUAL RELATIONSHIPS` result

### Step 2 — Answer with Cypher (Chapters 7–9)

In the portal (graph `sample`), write Cypher that answers questions 1 and 2.

- Question 1: claim → sales order → item ← purchase order line → purchase order → supplier, plus the shipments carrying those purchase orders that are not `DELIVERED`.
- Question 2: sales orders for the same item with `status = 'OPEN'`, and their customers.
- Use `EXPLAIN FABRIC` to see how many sources the query touches.
- **Deliverables**: the two Cypher queries, the result tables, the EXPLAIN FABRIC output

### Step 3 — Extend the ontology (Chapters 11–13)

The sample ontology has no purchase order lines. Run an **additional ingestion** into **Supply Chain Operations (Sample)** to add them.

- Source: the `erp` data source
- Add a Golden Question: “Which supplier supplied the item in the PCB soldering defect claim, and how much of that supplier's quantity has not arrived yet?”
- After the build, ask this question in the Ask & Act tab and check that it gives the same answer as your Cypher from step 2.
- **Deliverables**: a screenshot of the build report, and a comparison of the answer with your step 2 results

### Step 4 — Take action (Chapters 14–16)

- In the Ask & Act tab, give the commands “Put all of that supplier's open purchase orders on hold (reason: investigating the PCB soldering defect)” and “Send a remediation notice to the affected customers”.
- Record what each plan card allowed and denied, and why. After you approve and execute, check in the Data Sources tab that `erp.purchase_order` and `crm.notice` have changed.
- Finally, **cancel everything** to restore the original state, and explain the order of the compensation history.
- **Deliverables**: screenshots of the plan cards, execution results, source checks and compensation history, with your explanation

### Step 5 — Build the app (Chapters 17–20)

- A code app called **Quality Incident Response**: a claim summary at the top, the affected supplier and its not-yet-arrived quantity in the middle, and the affected customers' open orders at the bottom.
- Edit it in plain words at least twice, and compare one query in `app.js` with your Cypher from step 2.
- (0.1.1 and later) A **Put purchase order on hold** button on supplier rows and a **Send notice** button on customer rows.
- **Deliverables**: a screenshot of the app, and the query part of `app.js`

## Grading criteria (example)

| Item | Criteria | Points |
|---|---|---|
| Data connection | Virtual nodes and relationships are joined on the right keys | 15 |
| Cypher | Correct answers to questions 1 and 2, correct labels and directions, EXPLAIN interpreted | 25 |
| Build | Golden Questions are specific, and the query answers match the Cypher results | 20 |
| Actions | Policy denial reasons explained; execution, source check and compensation order explained | 20 |
| App | Real data, handling of empty results and errors, the editing process | 20 |

## Things to think about

- What was the same, and what was different, between the Cypher you wrote in step 2 and the agent's answer in step 3?
- If you really used “Send notice” from step 4 in production, what conditions should the policy add? (For example: at most once a day per customer)
- Using the EXPLAIN FABRIC result from step 2 as evidence, explain the pros and cons of not copying the source databases (the data fabric approach).
