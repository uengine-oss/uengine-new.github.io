# Architecture — Lite on the Process GPT backend

> Process GPT Lite is made of a screen (Vue) and a small relay server, and the real work is done by the Process GPT backend, left untouched. In this chapter you'll see the components in a single diagram, follow where one message and one document travel, and look at which model decides what.

## A thin screen on a backend used as is

In the previous chapter you opened an agent's working folder directly in the Workroom. In this chapter you step back further and see how that folder, chat and the editor are connected inside the server. This chapter is for the people who install and run it in-house, so component names and ports appear as they are.

Most of the features you've used so far weren't newly built for Lite. Agent runs, skills, the process engine, document generation and storage call the services of the open-source [Process GPT](https://github.com/uengine-oss/process-gpt) **without modifying them**. Lite itself owns just two things.

| Part of Lite | What it does |
|---|---|
| **Screen** (Vue 3) | Chat, Home, Projects, Folders, Settings, Workroom. The sky background and glass cards |
| **Relay server** (Express. A server that calls the backend on behalf of one particular screen, often called a BFF — Backend for Frontend) | Login, saving conversations and cards, backend calls, the MCP gateway (MCP is the standard protocol agents use to call outside tools) for connectors, documents and ArtCraft, Vault encryption, scheduled runs, the browser agent |

So if you already run Process GPT, Lite simply adds one more screen on top of it, and when Process GPT gets better, Lite gets better with it.

## Component diagram

```text
Browser / Android app (UI :5180)
  │  /api  /office  /craft
  ▼
Lite relay server (:8787)
  ├─ Chat ──────▶ context-router (:8895) ── which conversation?
  │                 │  └─▶ routing model (:8896) small model · embeddings
  │                 ▼
  │               deepagents (:8888) ── agents · skills ─▶ sandbox
  │                 │ MCP tools
  │                 ├─▶ office-mcp (:1192)  create documents
  │                 ├─▶ office-host (:5390) editor · live editing
  │                 ├─▶ mcp-hub (:8500)     connector registry
  │                 └─▶ Lite /mcp/*         connectors, folders, panel apps
  │                                         ArtCraft CLI (per user)
  ├─ Process ───▶ completion (:8099) + polling-service
  ├─ Workroom ──▶ cli-agent (:8890)  Claude Code · Codex
  ├─ Mining ────▶ process-miner (:8014)
  ├─ Improve      (relay server) lead time · bottleneck · critical path
  ├─ Storage ───▶ Supabase  Postgres · login · file storage
  └─ Schedule ◀── pg_cron ─▶ pg_net ─▶ /api/cron/fire
```

| Component | Source | Role |
|---|---|---|
| **deepagents** | Process GPT | The real work of one conversation turn. It picks skills, calls tools (MCP) and runs code in a sandbox to make files |
| **context-router** | Process GPT | Decides which conversation a message follows up on and splits conversations ([Chapter 4](contexts.html)). It also handles short multiple-choice decisions (`/decide`) |
| **Routing model server** | Process GPT (reference implementation) | A small open model (Qwen3-4B) picks one of the options by probability. The same server also produces embeddings for semantic search (bge-m3) |
| **completion + polling-service** | Process GPT | Starting and submitting processes, and moving on to the next step ([Chapter 17](process-create.html)–[Chapter 18](process-run.html)) |
| **office-mcp** | Process GPT | **Creates** Word, Excel and Hangul documents (in English mode a proposal is made as a Word document unless you ask for Hangul) |
| **office-host** | Process GPT (IeumOffice) | **Opens and edits** documents in their original formats. Provides the `office_live_*` tools that edit an open document ([Chapter 7](office.html)) |
| **mcp-hub** | Process GPT | Manages the list of MCP servers and each user's connections ([Chapter 11](missions.html)) |
| **cli-agent** | Process GPT | Runs Claude Code and Codex in a working folder ([Chapter 23](workroom.html)) |
| **process-miner** | Process GPT | Finds recurring flows in handover records ([Chapter 19](mining.html)) |
| **Improve analysis** | Lite relay server (ports the lead-time breakdown rules of Process GPT's analytic service) | Reads process run records straight from the source tables to calculate lead time, waiting, bottlenecks, constraints and the critical path for each step, and gives them to agents as the `/mcp/improve` tool. Every number is a calculated result; the model only explains it ([Chapter 20](bottleneck.html)–[Chapter 22](critical-path.html)) |
| **Supabase** | Same as Process GPT uses | Postgres (conversation, card, process and team data), login, file storage, scheduling (pg_cron) |
| **ArtCraft CLI** | storytold open source | MCP for the CAD, vector, photo, sound and video apps. Lite keeps one process running per user ([Chapter 8](craft.html)) |

!!! note "Storage Lite adds on its own"
    Lite's own data lives in tables starting with `pro_` in the same Postgres (conversations, cards, schedules, Vault, panel apps …). Shared folders are git repositories on the server (`PRO_FOLDERS_ROOT`, default `~/pgpt-folders/<tenant>/<folder>`), so an agent's sandbox can't see their history or other variations.

## The path of one message

When you send `Make the Moonlight Coffee Store #2 budget sheet in Excel` in chat:

1. **Screen → relay server**: the message is saved, and the reply comes back as a stream (SSE — the server pushes the text out a little at a time).
2. **Shortcut decision**: the relay server first uses rules to see where it should go. Requests to make a skill, a panel, a shared folder, an ArtCraft app or a document go straight to the agent. For everything else, a **small model** chooses: "Is it a browser task, a schedule, a handoff to a teammate, or work for the agent?"
3. **Pick the conversation**: in the main chat, it goes through context-router. The router narrows recent conversations down to 6 candidates or fewer and asks the routing model server, "Which conversation is this a follow-up to, or is it a new topic?" If confidence is low, it moves on to the next method (the language model's probabilities → a JSON answer).
4. **Agent run**: deepagents does the work with skills and MCP tools. For Excel, it runs code in the sandbox to make the file.
5. **Card**: the relay server finds the documents produced in this run, uploads them to file storage and attaches them to the conversation as **file cards**. Above the answer, a "↳ …" line shows which conversation it went to.

Long jobs like drawings or skills taking several minutes is normal. But if the agent doesn't send a single character for 15 minutes (`PRO_STREAM_IDLE_MS`), the relay server stops waiting and asks you to send it again.

## The path of one document

When you click a file card:

1. The screen brings up the IeumOffice editor at `/office/<editor>/?src=…` on the same origin. Excel opens in the `sheets` editor, Word in `docs`, and Hangul in `hwp`.
2. When the editor is ready, the screen opens a **live connection** to the relay server (a WebSocket opened with a one-time ticket) and reports "this person opened this document." **Linked to the conversation** appears in the header.
3. From then on, chat messages carry **tools that edit the open document** (`office_live_*`). These tools are visible only while the document is open and for a while afterward (30 minutes from the last message sent while it was open), because there's a limit (110) on how many tools an agent can use at once.
4. When the agent calls a tool, the relay server attaches **that user's login token** and passes it to office-host, which finds the editor open on that person's screen and edits it in place. The person watches the edits happen.
5. After editing, a **review** runs. It compares before and after (text length, tables and rows, formulas, the lines in pictures) to check nothing went missing, and leaves a short note ([Chapter 9](email-to-quote.html)).
6. When the person saves, the edited copy is uploaded next to the original and the card points to the edited copy.

ArtCraft apps work the same way. The difference is that the app's CLI connects to a local port the relay server opened, and requests are passed to the app on the screen. Only the CLI process the relay server started can connect to that port.

## Which model is called for what

Calling a big model for everything is slow and expensive. Lite uses three tiers, depending on the kind of work.

| Tier | Setting | What it handles |
|---|---|---|
| **Routing model server** (a small open model that only computes the probabilities of options — it doesn't write text) | `PRO_JUDGE_URL`, the router's `DECIDE_JUDGE_URL` | Which conversation a message follows up on (router); whether a browser page is still loading or the goal has been reached (`/decide`); spotting work requests in team conversations and their type; which material to show when someone in a meeting says "let's look at that quote again"; the teammates related to the current work when you type "@"; the type of a meeting to-do |
| **Fast model** | `PRO_LLM_FAST_MODEL` (default `gpt-4.1-mini`) | The first split of a message, titles for long answers, picking a process, summary and change cards for folder documents, test scenarios and scoring before a skill is merged, short questions in panels, explaining process improvement results (if there's no answer within 25 seconds, the same numbers are shown in a fixed template) |
| **Big model** | `PRO_LLM_MODEL` (default `gpt-6-luna`) | Sorting emails and deciding on drafts, deciding floor plan layouts, designing panel apps, operating the browser agent, summarizing meeting minutes, naming mining results, comparing pictures in the review after editing |
| **Agent model** | deepagents' and cli-agent's own settings | The real work of one conversation turn (making documents, drawings, skills and processes) |
| Transcription | `PRO_TRANSCRIBE_MODEL` (default `gpt-4o-mini-transcribe`) | Transcribing online meetings (only for people who consented) |

!!! tip "Frequent decisions don't call a big model"
    Team messenger and meetings need a decision every time someone speaks. These use only rules → the routing model server, and detection calls a big model zero times (the server counts those calls separately). If there's no routing model server, only these suggestion features quietly turn off, and everything else keeps working.

The model address and key can be anything OpenAI-compatible (`PRO_LLM_BASE_URL`, `PRO_LLM_API_KEY`). Switch to an in-house model and the screens and flow stay the same.

!!! note "The install bundle includes only part of this"
    The install bundle's default Docker `lite` profile doesn't include context-router and the routing model server, cli-agent, the ArtCraft apps or the process engine. Without them, only those features are missing and the rest works. To turn them on with a profile, see "Profiles" in [Chapter 1](install.html); to attach them separately, see "I installed it, but a chapter's feature doesn't show up" in [Chapter 28](faq.html).

In the next chapter you'll go through what to look after when running this setup in-house — teammates and roles, where the keys live, Vault encryption, backups and upgrades ([Chapter 25](admin.html)).

!!! exercise "Check your understanding"
    1. When Minji Kim sends "Could you sort out the quote by tomorrow?" in the messenger, how many times is a big model called to decide whether it's a work request? What happens if the routing model server is off?
    2. If you send `Add a total for column B` without opening the Excel card, can the agent edit the document on the screen right away? Look for the reason in the path of one document.
    3. Which settings do you change to switch to an in-house LLM?

<details class="answer" markdown="1"><summary>Answer</summary>

1. Zero. After the rules (very short messages, small talk and messages with no request wording are skipped), the routing model server picks "is it a work request?" and "what kind of work?" by probability. Without the routing model server, the suggestion card just doesn't appear, and the messenger works as usual.
2. No. The `office_live_*` tools are visible to the agent only while the document is open in the editor with a live connection (and for a while afterward), and what they edit is the editor open on the screen. With no open document, the agent sees only a small tool that tells you to open it from the card.
3. Change the relay server's `PRO_LLM_BASE_URL`, `PRO_LLM_API_KEY`, `PRO_LLM_MODEL` and `PRO_LLM_FAST_MODEL`, together with the model settings on the deepagents side (and the router's `DECIDE_LLM_*`). Any OpenAI-compatible address works.
</details>
