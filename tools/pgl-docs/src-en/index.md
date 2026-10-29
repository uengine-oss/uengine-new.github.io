# Process GPT Lite tutorial

> A hands-on guide you follow one step at a time. You start with your first conversation with an AI assistant, then handle documents and tools by chat, cut down repeated work with skills and schedules, share work with teammates, and finally watch ad hoc work become an official company process.

## What you'll do in this tutorial

Process GPT Lite is **an AI work assistant you work with through a single conversation**. It doesn't stop at answering questions. It creates and edits documents, operates a browser for you, reads your mail and suggests to-dos, hands work over to teammates, and joins meetings to show materials. The execution engine, agents and storage are the open-source [Process GPT](https://github.com/uengine-oss/process-gpt) backend as is. Lite puts a lightweight screen on top of it.

This tutorial doesn't list features one by one. It follows **how one company's work evolves**.

| Character | Role |
|---|---|
| Jinyoung Jang | Proposal team lead at a space design company. This is the person you play in this tutorial |
| Minji Kim | Designer. Handles floor plans and proposal visuals |
| Seoyeon Park | Finance. Reviews quotes and costs |
| Yuki Sato | Lighting designer at a partner studio in Tokyo. Writes and speaks Japanese (Chapters 15–16) |
| Moonlight Coffee | Customer. Asks by email for a store design proposal and quote for Store #2 |

The story starts with one email: "Please send us a proposal and a quote for Moonlight Coffee Store #2."

1. **On your own, with the AI assistant** — At first, Jinyoung asks the assistant questions, has it look things up, and has it sort through mail. Conversations split by topic on their own.
2. **Documents and tools too** — The assistant makes a floor plan (CAD), a proposal (Word) and a quote (Excel), and edits them right inside the open editor. After editing, it checks on its own that the result matches what you meant.
3. **Less repetition** — When similar requests arrive every week, you save the approach that worked as a **skill**, and build a **scheduled mission** that runs at a set time and a **panel app** the team shares.
4. **As a team** — You share outputs with Minji Kim and Seoyeon Park, hand work over with @mentions, and polish it together in the messenger and online meetings. With Yuki Sato, who works in Japanese, messages are translated and meetings are interpreted. What's said in a meeting is saved in the room automatically.
5. **As a process** — Once the same flow keeps repeating, **process mining** finds the pattern "receive email → drawing, proposal, quote → finance review → reply" and suggests it to the administrator. After it's registered as an official process, a new request email starts the process on its own, and each step gets an assignee and an agent.
6. **Process improvement** — After the official process runs for a few months, records pile up. You find which step loses time (bottleneck), whether the work goes into actual working time or waiting time (value stream), and which steps decide the total duration (constraints and the critical path). Then you calculate an improvement in advance, change the process and compare before and after.
7. **Extending and operating** — You look at the Workroom where Claude Code and Codex work, the system architecture, and operations and security.

By the end, you'll be able to take one new customer request all the way from mail → outputs → team review → meeting → official process, and use the records it leaves to make that process faster.

## Learning path

<div class="cards" markdown="0">
<a href="install.html"><b>0 · Getting started</b><span>Installation, first login, a tour of the screen</span></a>
<a href="first-chat.html"><b>1 · You and your AI assistant</b><span>First conversation, conversation context, mail assistant, browser agent and the Vault</span></a>
<a href="office.html"><b>2 · Documents and tools</b><span>IeumOffice, ArtCraft, from one email to a floor plan, proposal and quote</span></a>
<a href="skills.html"><b>3 · Less repetition</b><span>Skills, external connections and scheduled missions, panel apps</span></a>
<a href="folders.html"><b>4 · Working as a team</b><span>Shared folders, sharing outputs and @mentions, messenger and translation, online meetings with interpretation</span></a>
<a href="process-create.html"><b>5 · Working in processes</b><span>Create a process by chat, run it, process mining</span></a>
<a href="bottleneck.html"><b>6 · Improving processes</b><span>Find bottlenecks, value streams and the theory of constraints, the critical path and running improvements</span></a>
<a href="workroom.html"><b>7 · Extending and operating</b><span>Agent Workroom, architecture, operations and security</span></a>
<a href="project.html"><b>8 · Final project</b><span>A new customer request from start to finish</span></a>
</div>

Each chapter follows the order **concept → try it → check questions**. Later chapters build on what you made in earlier ones, so it's best to follow them in order. The answers to the check questions are folded. Try them yourself first, then open the answers.

## Who this tutorial is for

- If you've worked with email and a messenger, you can follow Parts 1–4. No programming needed.
- Part 5 (processes) is easier if you've drawn a workflow before, but you don't need to know BPMN. You create processes by chat too.
- Part 6 (process improvement) only asks that you can read numbers. Value streams, the theory of constraints and the critical path are explained from scratch in the chapters.
- Part 7 (extending and operating) is for the people who install and run the app in-house. A little Docker and terminal experience is enough.

## What you need

| Item | Details |
|---|---|
| Computer | macOS, Linux or Windows (WSL2) that runs Docker. 16GB of memory recommended |
| Disk | At least 20GB free (including container images) |
| LLM key | One OpenAI-compatible API key. To use transcription (online meetings), you also need a key for transcription |
| Coding agent (optional) | [Claude Code](https://claude.com/claude-code) or Codex CLI — used in the agent Workroom in Part 7 |
| Browser | The latest Chrome or Edge. Online meetings need a camera and microphone |

!!! tip "Want to watch a video first?"
    The [8-minute overview video](https://youtu.be/4gp2d-Qr85s) shows the whole story of this tutorial in one go. Each chapter also links a demo video for its part.

## Conventions

- Monospace text, like `Make a quote for Moonlight Coffee Store #2`, is what you type. Button names on the screen are in bold, like **Continue working**.
- The screenshots were taken from real runs with a tutorial account. All names of people, companies and emails are examples.
- What the assistant and agents write is a little different every time. Even if the screenshots and wording don't match exactly, you're on track as long as the **Check** items in each chapter (files created, cards, status) match.
