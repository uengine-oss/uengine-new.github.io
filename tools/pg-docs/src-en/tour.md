# Tour of the screens

> Take a tour of the Process Architecture that opens when you sign in, the home screen with the chat box, the left sidebar, the top bar, and the screens you'll open often — My Task List, the organization chart and settings — to learn where to do what.

## After sign-in — Process Architecture

When you sign up in [Chapter 1](install.html), the **Process Architecture** opens right away. This screen shows the company's processes organized in a hierarchy: Domain › Mega Process › Major Process › Sub Process. Use **Hierarchy · Card · Matrix · Tree** at the top to change the view, and the row of numbers counts which stage (0–4) each process is at. There are no processes yet, so everything is 0.

![The Process Architecture right after sign-in — Hierarchy, Card, Matrix, Tree, 0 processes in total, and the Hierarchy Structure and Process Status legend](img/tour-architecture.webp)

## Home — the chat box and the Process Definition Map

Click the **pencil icon** to the right of "Process GPT" at the top of the sidebar to open the screen you'll use most in this tutorial. It has the **chat box** at the top and the **Process Definition Map** below. When this tutorial says "home", it means this screen.

![Home — the chat box (example sentences, ＋, agent picker, microphone) and an empty Process Definition Map](img/tour-home.webp)

Most work in Process GPT starts in this chat box. Describe the process you want in words and it's created ([Chapter 3](process-create.html)); attach company documents and ask, and it answers based on them ([Chapter 8](knowledge.html)). Click an example sentence above the box ("Create a vacation request process" and others) to put it in the box.

| Button in the box | What it does |
|---|---|
| ＋ | **Attach File**, **Knowledge Base**, **Upload Folder** — attach documents to the chat |
| **Deep Agent** ▾ | Choose the agent for the chat: **Basic Agent**, **Deep Agent** or **Codex** |
| 🎤 | Type by voice |

![The ＋ menu — Attach File, Knowledge Base, Upload Folder](img/tour-plus-menu.webp)

The processes you create pile up by area on the **Process Definition Map**. A new process first goes under **Uncategorized**. Use **Marketplace** for shared process templates, and **Import Component** to bring in processes exported from elsewhere ([Chapter 4](definition.html)).

## Left sidebar

The sidebar shows what's in progress and the colleagues you work with.

| Section | What you see | Icons in the header |
|---|---|---|
| **Conversations** | Your chat rooms so far | 🔍 search, ＋ new chat room |
| **Instance** | Each running process, one by one | ✓ **View completed instance list** |
| **Agent Colleagues** | AI agents. **Browser Automation Agent** and **OpenAI Advanced Analysis** are there from the start | Person icon → **Organization & Agent Management** |
| **People Colleagues** | People in the same company | 🔍 search |
| **Skills** | Skills that agents use. From the start: process creation (`bpmn-process-generation-skill`), strategy interview (`bsc-strategy-interview`) and process execution (`process-execution`) | ⚙ **Manage Skills** |
| **Process** | Shortcuts to process definitions | |
| **Analytics** | **Dashboard**, **Request Top List**, **Process Identification**, **Heatmap**, **KPI & Progress**, **Strategy Board**, **Ontology**, **PI Flag** | |

![Bottom of the sidebar — the Process and Analytics menus](img/tour-sidebar-bottom.webp)

You'll see the word **instance** a lot from now on. If a process definition is the blueprint, an instance is one actual case running by that blueprint. There is one "Sales Proposal Creation" process, but each customer request creates a new instance.

## Top bar

![Top bar — the “My Task List” tooltip](img/tour-topbar.webp)

| Icon | Name | What it does |
|---|---|---|
| ☰ | **Collapse/Expand Sidebar** | Gives you more room on screen |
| List | **My Task List** | Shows the tasks assigned to you |
| Map | **Strategy Board** | Connects company strategy to processes |
| Book | **Knowledge Base** | The company's documents ([Chapter 8](knowledge.html)) |
| Speech bubble | **My feedback** | Feedback you've left |
| Branch | **Merge Requests** | Review change requests for processes and skills |
| 🔍 · 🔔 · ⚙ | **Search** · **Notifications** · **Setting** | |

## My Task List

**My Task List** shows the tasks assigned to you in three columns: **In Progress · Pending/Returned · Done**. When you run a process, each step creates a task for its owner, and that task appears here as a card.

![My Task List — In Progress, Pending/Returned, Done](img/tour-todolist.webp)

## Organization chart

Click the person icon next to **Agent Colleagues** in the sidebar to open the organization chart. Create teams and add members in **Organization Chart Management** on the left and they appear in the chart on the right; build AI agent colleagues in the **Create Agent** tab next to it (click › to reach it, [Chapter 9](agents.html)). For now there's only the company (tenant) name `localhost`.

![Organization chart — the “Organization Chart Management” tab, Select Team, Delete Team, Edit Team, Add Team, and the chart on the right with only “localhost”](img/tour-organization.webp)

## Settings

Click ⚙ on the top bar to open the settings. These are the tabs this tutorial uses ([Chapter 18](settings.html)).

| Tab | What it does |
|---|---|
| **Account Settings** | Name and photo, two-step verification |
| **Manage Users** | Manage people in the same company |
| **Knowledge Base** · **MCP Servers** · **Environments** | Documents, tools and settings that agents use |
| **Tenant Management** | Company (tenant) information |
| **English** ▾ | Display language |

![Settings — the Account Settings, Appearance, Manage Users and Google Drive Settings tabs, more tabs behind ›, Tenant Management, and the “English” language selector](img/tour-settings.webp)

## Try it — Take a tour

<ol class="steps" markdown="1">
<li markdown="1">On the Process Architecture that opens after sign-in, click **Card** and **Tree** and see the view change.</li>
<li markdown="1">Open home with the pencil icon at the top of the sidebar. Click **Deep Agent** ▾ in the chat box to see the three agents, then click ＋ to see the menu. Don't send anything.</li>
<li markdown="1">Click **My Task List** on the top bar and check that all three columns are empty.</li>
<li markdown="1">Open the organization chart with the person icon next to **Agent Colleagues** in the sidebar.</li>
<li markdown="1">Open ⚙ settings and skim the tab names.</li>
</ol>

## Next chapter

Now that you know the screens, the next chapter uses the chat box on the home screen to create your first process, "Sales Proposal Creation" ([Chapter 3](process-create.html)).

!!! exercise "Check your understanding"
    1. How is a process definition different from an instance?
    2. Where do you click to attach company documents to the chat box?
    3. When a process runs, where do you see the tasks assigned to you?

<details class="answer" markdown="1"><summary>Answers</summary>

1. A definition is the blueprint that lists the steps, owners and forms; an instance is one actual case running by that blueprint. One definition can run many instances.
2. Click ＋ in the chat box and choose **Attach File** (files on your computer), **Knowledge Base** (company documents you've uploaded) or **Upload Folder**.
3. In **My Task List** on the top bar. It's split into In Progress · Pending/Returned · Done columns.
</details>
