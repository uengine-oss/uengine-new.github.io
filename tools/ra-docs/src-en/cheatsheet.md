# Cheat sheet

> Screens · shortcuts · proposal stages · skills · frequently used values on one page. Open it whenever you think “where was that again?” while following along.

## Screens

| Screen (Home card) | Tab name | What it does | Chapter |
|---|---|---|---|
| Proposals | Proposals | One requirement line → design · plan · implementation · validation | 3–7 |
| Requirements | Requirements | Bounded context › feature › user story › acceptance criteria | 8 |
| Process | Process | BPM flows and Event Modeling | 8 |
| Design Canvas | Design | Aggregates · commands · events · policies | 8 |
| Data Model | Data | Aggregates · entities · value objects | 8 |
| Code | Code | Files in the code folder and a Claude Code terminal | 6 |
| Legacy · Data Sources | Legacy | Rail with Code · Data sources · Code graph · Data schema | 11 · 13 |
| Project Constitution | Design | Design principles · tech stack · architecture style | 4 |

## Windows and tabs

| To do this | How |
|---|---|
| Go to Home | ⌘1 (**Home** on the tab strip) |
| Go to the Nth tab | ⌘2 and up, in order |
| Next tab | Ctrl+Tab |
| Two screens side by side | Right-click a tab → **Move to new window** |
| Switch screens inside one tab | The **rail** on the left (the Legacy tab's rail shows only the Legacy menu) |
| Light · dark | The sun · moon button on the right of the tab strip — Home and every tab change together |
| Another project | Project bar at the top of Home → **Switch project** |

## Proposal stages

| Status | Meaning | What you click | Time taken (this tutorial) |
|---|---|---|---|
| INTENT | Strategic design (bounded contexts · features · stories · acceptance criteria) | **+ New Proposal** → **Start AI Analysis** | about 2 minutes |
| PLAN | Constitution (first time only) → tactical design · architecture decisions | **Proceed to Plan →** → **Generate Plan** → **Confirm Plan** | about 11½ minutes |
| SUBMITTED | The plan is confirmed | **Sandbox Implementation** section → **Generate task list** | about 4 minutes |
| IMPLEMENTING | Claude Code implements in the sandbox (Git worktree) | **Start implementation** → **Go to Claude Code cell** | |
| VALIDATING · Pending Acceptance | Structural sync + acceptance-criteria validation | **Done → Verify** | |
| ACCEPTED · DESTROYED | **Accept (Dual Merge)** applies the code and the graph DB together; **Destroy** throws it away (the diff history is kept) | **Accept / Destroy** section | |

!!! warning "Stay on that tab while it generates"
    Long-running steps such as plan generation start over if you reload that tab or move to another screen in it. Do other work in a new tab opened from Home.

## Skills

| Stage | Skill |
|---|---|
| INTENT | `robo-proposal-intent` |
| Constitution | `robo-project-constitution` |
| PLAN | `robo-proposal-plan` |
| Task list | `robo-proposal-tasks` |
| Implementation | `robo-implement` (`/robo-implement PRO-001` in the Code tab's cell) |
| Validation | `robo-proposal-test` · `robo-sync` |
| Impact analysis | `robo-proposal-context` |

The originals are in `resources/runtime/architect/app/skills/` in the app's install folder, and the copies for the Code tab's cell are in `~/.claude/skills/` (Chapter 10).

## Frequently used values

| What | Value |
|---|---|
| Project name rule | Starts with a lowercase letter; lowercase letters · digits · underscores; 2–40 characters (`hanbit_delivery_en`) |
| Practice legacy DB | `ra-tut-legacy-pg` · `127.0.0.1:25433` · `legacy` / `legacy1234` · DB `hanbit` · schema `delivery` |
| Data source Host (a DB on your PC) | `host.docker.internal` — `localhost` is the container itself and fails |
| Containers | graph-db · graph-bolt · fabric · catalog · analyzer · parser · gateway (7) |
| Where an OpenAI API key is needed | Document upload in the Requirements tab · chat edits in the Design tab — “paste the document into a proposal” in Chapter 12 and the legacy analysis in Chapter 13 work without a key |
