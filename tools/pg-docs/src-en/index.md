# Process GPT tutorial

> A hands-on guide that teaches Process GPT step by step from scratch: describe a company's routine work in words to turn it into a process, teach AI agent colleagues the company's documents, and attach business rules as decision tables.

## What is Process GPT

Process GPT is **an open-source platform for business processes and AI agents together**. The order of the work and who does each part are defined in BPMN, the international standard notation, and each step is done by a person or handed to an AI agent. You don't need to know how to draw BPMN. Describe the work you want in the chat, and Process GPT creates the flow diagram and the input forms.

This tutorial follows the story of **Hanbit Office**, an office furniture company.

| Character | Role |
|---|---|
| Jinyoung Jang | Sales team lead. The person you play in this tutorial, and the Process GPT admin |
| Minji Kim | Sales representative. Takes customer requests and writes proposals |
| Seoyeon Park | Finance officer. Approves high-value quotes |
| Hanbit Office Quote Advisor | An AI colleague that reads the price list and writes draft quotes (you build it in Chapter 9) |

1. **Getting started** — Install Process GPT and look around the screens.
2. **Process basics** — Describe the "Sales Proposal Creation" work in chat to turn it into a process, look inside the resulting definition (flow diagram, roles, forms), and manage its versions. Add colleagues to the org chart, run the process and handle the tasks, and go through an approve/reject gateway.
3. **AI agents** — Upload the product price list to the Knowledge Base so answers are based on it, then build an agent colleague that writes draft quotes and chat with it. Teach it a quote layout with a skill, and use the quote approval policy to create a process that includes agents.
4. **Tools and rules** — Connect a document tool through MCP to fill the company Word template with a quote, and turn the volume discount criteria into a decision table (DMN) through chat and attach it to an agent.
5. **Analysis and improvement** — See step times and bottlenecks from run history, and set objectives and KPIs on the strategy board.
6. **Operations** — Bring in colleagues and change the display language and settings.
7. **Final project** — Build Hanbit Office A/S intake from start to finish yourself.

## Learning path

<div class="cards" markdown="0">
<a href="install.html"><b>Getting started</b><span>Install, first sign-in, look around the screens</span></a>
<a href="process-create.html"><b>Process basics</b><span>Create a process through chat, the definition and versions, org chart, running and tasks, approve and reject</span></a>
<a href="knowledge.html"><b>AI agents</b><span>Knowledge Base, building and chatting with agent colleagues, skills, processes from documents</span></a>
<a href="mcp-hub.html"><b>Tools and rules</b><span>Document tools through MCP, decision tables (DMN) made through chat</span></a>
<a href="analytics.html"><b>Analysis and improvement</b><span>Execution analytics, strategy board and KPIs</span></a>
<a href="settings.html"><b>Operations</b><span>Colleague sign-up, language, settings</span></a>
<a href="project.html"><b>Final project</b><span>Hanbit Office A/S intake</span></a>
</div>

Each chapter goes **Why → Try it → Check your understanding**. Later chapters build on what you made in earlier ones, so it's best to follow them in order. The answers to the check questions are folded away — try them yourself first, then open them.

!!! note "Chapters coming soon and installation fixes"
    Chapter 13 (Run the steps agents handle) is marked "Coming soon" in English: in our English run the agent steps could not be shot reliably yet. Chapters 6, 7, 11, 14, 16 and 17 were captured on an installation with fixes that are not in the installation repository yet; each lists them at the top. These notices will be removed once the fixes land.

## Who this tutorial is for

- If you've worked with email and a messenger, you can follow along. No programming needed.
- For the installation (Chapter 1), you only need to paste a few commands into a terminal.
- You don't need to know BPMN. Each chapter explains as much as you need.

## What you need

| Item | Details |
|---|---|
| Computer | macOS, Linux or Windows (WSL2) that runs Docker. 16 GB of memory or more and 70 GB of free disk space recommended |
| LLM key | One OpenAI API key |
| Practice files | [Hanbit Office sales docs (zip)](files/hanbit-sales-docs-en.zip) — the product price list (`Hanbit-Office-Price-List.pdf`) and the bulk order quote approval policy (`Hanbit-Office-Quote-Approval-Policy.pdf`) (Chapters 8 and 12) |

## The screens in this tutorial

All screens and results in this tutorial come from a fresh Process GPT install made as in Chapter 1 and actually run. The text and flows the AI produces vary a little each run, so it's fine if the words on your screen don't exactly match the pictures. What matters is that the items listed under **What to check** in each chapter are there.
