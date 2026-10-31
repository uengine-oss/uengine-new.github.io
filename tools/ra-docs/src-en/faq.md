# Frequently asked questions

> Common sticking points in installation · projects · proposals · Claude Code · data sources, and how to get past them.

## Installing and running

**Do I need to install Neo4j separately?**
No. Lite keeps the design in Ontological DB. The app itself brings up the seven containers for the graph DB and analysis services in Docker (Chapter 1).

**Do I need an OpenAI API key?**
Not for this tutorial. Proposal analysis · planning · implementation are done by Claude Code on your computer, and a requirements document is also split without a key if you paste it into a proposal (Chapter 12). Legacy code analysis (Chapter 13) works without one too — the app hands the analyzer's AI calls to Claude Code. An OpenAI key is needed only for in-app AI helpers such as document upload in the Requirements tab and chat edits in the Design tab.

**Why is Claude Code needed?**
Because Robo Architect's engine is Claude Code's skills. Run `claude` once in a terminal and sign in, and the app calls the skills with that sign-in (Chapter 10).

## Projects

**Can I create several projects?**
Yes. In **Switch project** on Home, type a new name and click **Create**, and another graph is created. Each project has its own graph, so designs never mix. `skill_lab_en` in Chapter 10 is an example.

**My project name is rejected.**
It must start with a lowercase letter, use only lowercase letters · digits · underscores (_), and be 2–40 characters long. `hanbit-delivery` (hyphen) or `Hanbit` (uppercase) won't work.

## Proposals

**Plan generation started over from the beginning.**
If you reload that tab or move to another screen in it during generation, it starts over. While you wait, open a **new tab** from Home for other work.

**I get “Failed to parse the task breakdown”.**
It means the response from Claude during task list generation couldn't be read as a task list. Click **Generate task list** again. In this tutorial the first attempt worked and produced 18 tasks.

**After I changed the constitution, the plan became “stale”.**
That plan relied on the constitution. Regenerate the plan of that proposal and confirm it (Chapter 4).

**I want to change the constitution interview's questions.**
The order of questions is decided by the app. The `robo-project-constitution` skill handles the questions' recommendations · rationales and the constitution document (Chapter 10).

## Claude Code

**The terminal in the Code tab asks for a text color theme first.**
Claude Code asks once, the first time it runs in a terminal on this computer. Choose with the up and down arrows and press Enter.

**When I start implementation, “Is this a project you created or one you trust?” appears.**
It's the folder trust check Claude Code shows the first time it opens the sandbox folder. The default choice is “No, exit”, so press the down arrow to select **Yes, I trust this folder** and press Enter. When the bypass-permissions consent appears next, choose **Yes, I accept**. If implementation didn't start, type `/robo-implement PRO-001` into the cell yourself.

## Data sources

**The connection test fails.**
If you put `localhost` in Host, change it to `host.docker.internal`. The side testing the connection is the data fabric inside a container, and `localhost` inside it is the container itself (Chapter 11).

**I registered a data source, but the data schema is empty.**
That's expected. The data schema canvas is filled by DDL · code analysis (Chapter 13) or user input. To see the registered DB's tables, click the data source card and look at **Live DB tables**.
