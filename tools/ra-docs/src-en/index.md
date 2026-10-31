# Robo Architect Tutorial

> A hands-on guide to the Robo Architect Lite desktop app, step by step from scratch: turn a one-line requirement into a proposal, break it down with domain-driven design (DDD), set a project constitution and a plan, have Claude Code implement it in a sandbox, then validate it against acceptance criteria and merge it back into the design.

## What Robo Architect is

Robo Architect is a **spec-driven development (SDD) tool**. The spec, not the code, is the source of truth. You write requirements in plain language, and AI breaks them down into the vocabulary of domain-driven design (DDD) — bounded contexts, aggregates, commands, events, and acceptance criteria in Given-When-Then form. Claude Code writes the code from that design, and the finished code is checked against the design again.

Every change is handled as one **proposal**. A proposal moves through these stages.

| Stage | What happens | In this tutorial |
|---|---|---|
| INTENT | Breaks a plain-language requirement into a strategic design (processes, bounded contexts, features, user stories, acceptance criteria) | Chapter 3 |
| PLAN | Decides the tactical design, architecture and impact, based on the project constitution | Chapters 4 · 5 |
| IMPLEMENTING | Claude Code implements it in a separate Git worktree (the sandbox) | Chapter 6 |
| VALIDATING · Pending Acceptance | Runs structural validation and acceptance-criteria tests | Chapter 7 |
| ACCEPTED | On acceptance, the code is merged into the main branch and written into the design graph | Chapter 7 |

This tutorial uses **Robo Architect Lite**, a desktop app you use on your own computer. It stores the design not in Neo4j but in a graph in **Ontological DB**, one graph per project. There is no sign-in screen, and AI work is done by Claude Code on your computer.

## The story

You will build **Hanbit Delivery**, a delivery service that connects neighborhood restaurants with customers. You play **Jinyoung Jang**, who is in charge of designing the service.

| Who | Role |
|---|---|
| Jinyoung Jang | Hanbit Delivery's architect — the person you play in this tutorial |
| Store owner | Registers the store's menu items and accepts incoming orders |
| Customer | Picks menu items and orders, and can cancel before the store accepts |
| Claude Code | The AI teammate that follows skills to break down the design, make the plan and write the code |

1. **Getting started** — install the app, create your first project and tour the screens.
2. **The proposal lifecycle** — turn the “register menu items and order” requirement into a proposal and get a strategic design, set the project constitution and make a plan, then implement in a sandbox, validate and accept.
3. **Design and change** — view the accepted design in the Requirements, Process, Design and Data tabs, read how a second requirement affects the existing design in the Impact Map, and look inside the engine's skill files.
4. **Legacy and data** — connect Hanbit Delivery's existing order DB as a data source, start a design from a requirements document, and analyze the old order system's code to design a new feature on the evidence of its business rules.
5. **Final project** — add a review feature yourself, from start to finish.

## Learning path

<div class="cards" markdown="0">
<a href="install.html"><b>Getting started</b><span>Installation and your first project, a tour of the screens</span></a>
<a href="proposal.html"><b>The proposal lifecycle</b><span>Create a proposal, constitution, plan, sandbox implementation, validation and acceptance</span></a>
<a href="design.html"><b>Design and change</b><span>Design tour, the change impact of a second proposal, changing the engine with skill files</span></a>
<a href="fabric.html"><b>Legacy and data</b><span>Connect data sources, start a design from a requirements document, analyze legacy code and design on its evidence</span></a>
<a href="project.html"><b>Final project</b><span>Capstone — a review feature</span></a>
</div>

Each chapter follows the order **why → hands-on → quiz**. Later chapters build on what you made in earlier ones, so it's best to follow them in order. The quiz answers are folded; try the questions yourself first, then expand them.

## Who this tutorial is for

- Developers who have built a web service at least once, or planners and architects who work with requirements and design.
- You don't need to know DDD. Terms like bounded context and aggregate are explained in the chapter where they first appear.
- You won't write code yourself. Claude Code writes it. You read, choose and check the design.

## What you need

| Item | Details |
|---|---|
| Computer | macOS or Windows 10/11. 16 GB of memory or more, 20 GB of free disk space or more |
| Docker Desktop | The graph DB and analysis services run as containers. It must be running |
| Claude Code | `claude` must run in a terminal and be signed in. All AI work in a proposal runs through it |
| Git | Creates the project folder and the sandbox worktrees |

## About the screens in this tutorial

Every screen and result in this tutorial comes from actually running the Robo Architect Lite desktop app (macOS) in English. AI-generated designs and code differ a little on every run, so the text on your screen doesn't have to match the pictures exactly. It's enough that the items listed under **What to check** in each chapter are there.
