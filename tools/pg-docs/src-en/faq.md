# Frequently asked questions

> Problems we actually ran into while making this tutorial, and how to fix them. Follow the chapter numbers for details.

## Installing and signing in

**http://localhost:8088 doesn't open.**
: Check that the launcher ran to the end. The first run takes a while because it downloads the images. Use `docker compose ps` to check that `nginx` is up; if it isn't, run `./start-all-services.sh …` once more. If another program is using port 8088, close that program ([Chapter 1](install.html)).

**When I sign up, it says “Invalid email format”.**
: There must be a dot after the `@`. Write it like `jinyoung@hanbit.example`. A local install doesn't send email, so it doesn't have to be a real address ([Chapter 1](install.html)).

**The colleague who signed up second isn't an admin.**
: That's expected. Only the first person to sign up is an admin; everyone after that joins as a regular user ([Chapter 18](settings.html)).

**I sent a chat message and Deep Agent says its sandbox isn't available.**
: Deep Agent couldn't start its work container. Create the `docker-compose.override.yml` from Chapter 1 and start the services again.

**I want to start over.**
: Run `./stop-all-services.sh --wipe`, then run the launcher again. All data (accounts, processes, documents) is deleted.

## Chat and processes

**I sent the same sentence, but the diagram and answer are different.**
: Text and flows made by AI differ a little on every run. It's fine as long as each chapter's **What to check** (step names, amounts, rules and so on) matches.

**I see “unknown” in the process hierarchy on the version comparison screen.**
: It's a display issue in the current version. Expand **Uncategorized › unknown › Uncategorized** all the way down and pick the process ([Chapter 4](definition.html)).

**I renamed a step, but it's back to the old name when I reopen it.**
: The 💾 in the step panel only updates the flow diagram. Save the definition with the 💾 at the top right of the definition screen to create a version ([Chapter 4](definition.html)).

**Deep Agent says “Something went wrong while putting the process files together, so I'm holding the result back.”**
: The definition Deep Agent made didn't pass validation yet. Reply in the same chat room, for example "Yes, please create the process with this flow." (or "Yes, please fix it that way." when you asked for a fix), and it tries again. In our run, it reported the fix after one reply. If it keeps happening, start a new chat with a more specific request (steps, owners and gateways) ([Chapter 12](document-process.html)).

## Knowledge Base and agents

**I uploaded a .md file and it says “Skipped 1 unsupported file”.**
: The Knowledge Base accepts PDF, HWP, HWPX, DOC, DOCX, PPTX, TXT, CSV and XLSX. Convert the file to PDF or TXT and upload it ([Chapter 8](knowledge.html)).

**I picked a folder in the Knowledge Base, and it says it can't find the document.**
: In the current version, a selected folder isn't passed to the agent. Expand the folder and check the **files** ([Chapter 8](knowledge.html)).

**I picked a document, but the agent asks me for the material.**
: Start your question with “Search the selected knowledge base for the … document, then” ([Chapter 8](knowledge.html)).

**The agent can't read a file I attached with “Attach File” on the agent screen.**
: In the current version, that attachment doesn't reach the agent. Upload the document to the Knowledge Base, reopen that chat room from **Conversations**, and pick the document with ＋ › **Knowledge Base** ([Chapter 10](agent-chat.html)).

**The AI put a tool name I don't recognize in the agent's “Tools”.**
: It's a name the AI made up when it drafted the agent. The tools field holds MCP server names, so if there's no MCP server with that name, no tool is attached ([Chapter 9](agents.html)).

**The numbers in “Achievements & Badges” in the agent settings window look odd.**
: In the current version, every agent shows the same sample values. They aren't real records ([Chapter 9](agents.html)).

**I can't click the save button for the decision table.**
: Fill in **Name** in the **Save DMN** dialog ([Chapter 15](dmn.html)).

## Settings

**The screen changed to Korean.**
: In ⚙ settings, click **🇰🇷 한국어** at the end of the tab row and choose **🇺🇸 English** ([Chapter 18](settings.html)).

**Some skill descriptions in the sidebar are in Korean.**
: They come from the built-in skills' own metadata, not from the screen language. The skills work the same.

**The “Glossary Management” tab shows an error.**
: The current install doesn't have the table for that feature, so it shows “relation public.glossaries does not exist”. The tutorial doesn't use it.
