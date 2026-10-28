# Ontological Studio Tutorial

> A hands-on, step-by-step guide. You start with what an ontology is, then connect source databases, query data with Cypher, build an ontology with an agent, run actions on business systems, and finally build apps on top of it all.

## What you will do in this tutorial

Ontological Studio is a desktop program for **building ontologies, running queries and actions, and building business apps**. A single installer includes a graph database (Ontological DB), a data fabric, an ontology-building agent, an action executor and sample business systems, so you can do every exercise from start to finish on one laptop.

This tutorial follows the **supply chain operations** of one company. The company's data is spread across three systems.

| System | Data | Example |
|---|---|---|
| Purchasing ERP (`erp`) | Suppliers, items, purchase orders, order lines | We ordered 2,000 PCB boards from Shenzhen Goldline PCB |
| Logistics WMS (`wms`) | Inbound shipments, daily stock | A shipment for that order has been held at customs for 9 days |
| Customer CRM (`crm`) | Customers, sales orders, claims | A customer in Tokyo filed a PCB soldering defect claim |

To answer “Which inbound shipments are more than 3 days late, and which supplier and purchase order are they for?”, you have to connect data from all three systems. By the end of the tutorial you will answer this question with a graph query, carry out the instruction “Expedite those shipments” on the real systems after an approval step, and build a business app that brings all of this together on one screen.

## Learning path

<div class="cards" markdown="0">
<a href="install.html"><b>1 · Getting started</b><span>Install, first run, a tour of the app</span></a>
<a href="ontology-basics.html"><b>2 · Ontology concepts</b><span>Classes, properties, relationships, instances; how the app is built</span></a>
<a href="datasource.html"><b>3 · Connecting data</b><span>Source databases as virtual nodes, without copying</span></a>
<a href="cypher-basics.html"><b>4 · Learning Cypher</b><span>From MATCH to aggregation, diagnostics and time travel</span></a>
<a href="golden.html"><b>5 · Building the ontology</b><span>Golden Questions and Golden Commands, building from documents, querying</span></a>
<a href="systems.html"><b>6 · Actions</b><span>Registering systems, creating actions, approve, execute, cancel</span></a>
<a href="dashboard.html"><b>7 · Applications</b><span>Dashboards, code apps, the SDK, action buttons</span></a>
<a href="project.html"><b>8 · Final project</b><span>A hands-on project that uses everything you learned</span></a>
</div>

Each chapter goes **concept → Try it → Check yourself**. The answers to the Check yourself questions are folded, so try them on your own first, then open the answers.

## Who this tutorial is for

- If you have learned SQL `SELECT` and `JOIN` in a university database course, you are ready.
- You don't need to know graph databases or Cypher. Part 4 teaches them from scratch.
- You need a little programming only in Part 7 (code apps). Even there the agent writes the code, so being able to read it is enough.

## What you need

| Item | Details |
|---|---|
| Computer | macOS (Apple Silicon M1 or later, or Intel) or Windows 10/11 (x64), 8 GB of memory recommended |
| Disk | At least 2 GB free |
| Coding agent | [Claude Code](https://claude.com/claude-code) or Codex CLI. If you install one and sign in, the build and query agents work without an API key. Without one, you can still do Parts 3 and 4 (connecting data, Cypher) as written. |
| Network | Needed only to download the installer and to use the agent (LLM). All databases run on your own computer. |

!!! tip "Prefer to watch first?"
    The [product page](https://www.uengine.org/en/contents/ontologystudio.html#demo) has demo videos of building from documents, creating actions from Golden Commands, and building ontology apps. This tutorial walks through those same steps one at a time.

## Conventions

- Text you type is in monospace, like `MATCH (s:Supplier) RETURN s.name`. Button names on screen are in bold, like **Create virtual node**.
- Screenshots use the light theme. A few demo shots in the dark theme are noted in their captions.
- Every number and result comes from actually running the sample data. If your results differ, check whether you did an exercise in an earlier chapter that changes data (such as running an action).
