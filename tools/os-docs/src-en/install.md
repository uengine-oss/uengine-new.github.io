# Installation and First Run

> Download and run the installer, and see what gets set up on first run. This chapter also shows how to connect a coding agent.

## Downloading the installer

Download the file for your operating system from the [releases page](https://github.com/uengine-oss/ontological-studio-releases/releases/latest).

| Operating system | File |
|---|---|
| macOS (Apple Silicon) | `Ontological-Studio-mac-arm64.dmg` |
| macOS (Intel) | `Ontological-Studio-mac-x64.dmg` |
| Windows 10/11 (x64) | `Ontological-Studio-Setup-win-x64.exe` |

On a Mac, download the file that matches your chip. Open the Apple menu at the top left of the screen › **About This Mac**. If **Chip** shows Apple M1, M2, M3, M4…, use the **Apple Silicon** file. If **Processor** shows Intel, use the **Intel** file. A DMG for the wrong chip will not run.

!!! note "Intel Macs: from 0.1.1"
    Installers for Intel Macs are available from version 0.1.1. The built-in database and the external database connectors (MySQL, Oracle, SQL Server) are all built separately for Intel, so you can follow every exercise in this tutorial on an Intel Mac as well.

## Installing on macOS

<ol class="steps" markdown="1">
<li>Open the DMG and drag the <b>Ontological Studio</b> icon into the <b>Applications</b> folder.</li>
<li>Double-click the app in the Applications folder. If a window says “Apple could not verify ‘Ontological Studio’ is free of malware”, click <b>Done</b>.</li>
<li>Open <b>System Settings › Privacy & Security</b>, click <b>Open Anyway</b> in the Security section near the bottom, and enter your password. Once you allow it, the app opens normally from then on.</li>
</ol>

On macOS 14 and earlier, you can also open the app the first time with right-click › **Open**. You have to go through these checks because the current release is not signed and notarized with an Apple Developer certificate.

!!! warning "If you see “is damaged and can't be opened”"
    If you get only “‘Ontological Studio’ is damaged and can't be opened. You should move it to the Trash.” with no **Open Anyway** option, you have an early 0.1.1 Apple Silicon build that was uploaded with incomplete signing. Don't move it to the Trash. Leave the app in Applications, run the following in Terminal, and open it again.

    ```bash
    xattr -dr com.apple.quarantine "/Applications/Ontological Studio.app"
    ```

    This command only removes the mark that says the file came from the internet (the quarantine attribute). The app itself is not changed.

## Installing on Windows

<ol class="steps" markdown="1">
<li>Run the EXE. It installs for the current user only, without administrator rights.</li>
<li>If SmartScreen shows a “Windows protected your PC” window, click <b>More info › Run anyway</b>.</li>
<li>When setup finishes, open Ontological Studio from the Start menu.</li>
</ol>

!!! note "Not yet available on Windows"
    Connecting MySQL, Oracle and SQL Server sources is available only in the macOS builds (Apple Silicon and Intel). PostgreSQL works in every build. To use Claude Code on Windows, install Git for Windows first.

## What happens on first run

When you open the app, the boot screen shows its progress step by step.

| Step | What it does | Time (Apple Silicon; Intel Macs may take a little longer) |
|---|---|---|
| PostgreSQL | Starts a database server on your computer | Under 1 second |
| First-run setup | Creates the sample business databases (ERP, WMS, CRM) and registers them with the data fabric | First time only |
| Ontological | Starts the graph engine (Ontological DB), the Bolt gateway and the Portal | Under 1 second |
| Studio | Starts the build and query screens, the action executor and the three sample business systems | About 4–5 seconds |

On first run, the app also creates the sample ontology **Supply Chain Operations (Sample)**. It has 7 classes, 6 relationships, 3 actions, 3 Golden Questions and 4 Golden Commands, so you can try queries and actions right after installing.

All servers can be reached only from `127.0.0.1` (your own computer).

## Connecting a coding agent

Building ontologies, natural-language queries, dashboard proposals and code apps are all done by an **agent**. Ontological Studio looks for an agent in this order.

1. **Claude Code** or **Codex CLI** installed on this computer. It uses the CLI's sign-in, so you need no separate API key. This is the default.
2. If no CLI is found, the **built-in agent**. In this case you must put `OPENAI_API_KEY` in the `studio.env` file before you can chat.

The agent in use is shown at the bottom left of the Home screen. To change it, choose **Runtime › Agent** from the menu. Click the **Settings** card to open `studio.env`.

!!! tip "What you can do without an agent"
    Connecting data sources, creating virtual nodes and writing Cypher in the Portal all work without an agent. You can follow Parts 3 and 4 of this tutorial to the end without one.

## Where is my data stored?

| Item | Location (macOS) |
|---|---|
| All user data | `~/Library/Application Support/Ontological Studio/` |
| Databases | `pgdata` in that folder |
| Passwords (randomly generated for each install) | `secrets.json` in that folder |
| Logs | `logs/` in that folder. Open it directly with **Logs folder** on the Home screen. |

To start over from scratch, quit the app, delete this folder and launch the app again. The sample databases and the sample ontology are created again.

!!! exercise "Check"
    Launch the app and make sure the Home screen appears. At the bottom left, look for **Ontological connected** and the agent's name.
