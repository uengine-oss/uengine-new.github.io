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
2. **Process basics** — Describe the "Sales Proposal Creation" work in chat to turn it into a process, look inside the resulting definition (flow diagram, roles, forms), and manage its versions.
3. **AI agents** — Upload the product price list to the Knowledge Base so answers are based on it, then build an agent colleague that writes draft quotes and chat with it. Use the quote approval policy to create a process that includes agents.
4. **Tools and rules** — Turn the volume discount criteria into a decision table (DMN) through chat and attach it to an agent.
5. **Operations** — Bring in colleagues and change the display language and settings.

## Learning path

<div class="cards" markdown="0">
<a href="install.html"><b>Getting started</b><span>Install, first sign-in, look around the screens</span></a>
<a href="process-create.html"><b>Process basics</b><span>Create a process through chat, look inside the definition, versions</span></a>
<a href="knowledge.html"><b>AI agents</b><span>Knowledge Base, building and chatting with agent colleagues, processes from documents</span></a>
<a href="dmn.html"><b>Tools and rules</b><span>Decision tables (DMN) made through chat</span></a>
<a href="settings.html"><b>Operations</b><span>Colleague sign-up, language, settings</span></a>
</div>

Each chapter goes **Why → Try it → Check your understanding**. Later chapters build on what you made in earlier ones, so it's best to follow them in order. The answers to the check questions are folded away — try them yourself first, then open them.

!!! note "Chapters coming soon"
    Chapters marked "Coming soon" in the table of contents on the left (Org chart and role owners, Run a process and handle tasks, Approve and reject, Skills, Run the steps agents handle, Connect external tools with MCP, Execution analytics, Strategy board, Final project) will be published one by one after fixes now underway in the current version are in. Chapter numbers are fixed in advance, so they won't change when these chapters appear.

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
