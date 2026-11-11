# Settings — bring in colleagues and change the screen

> In ⚙ settings on the top bar, change your account and theme, and bring sales representative Minji Kim into the company as a user. Switch the screen language to Korean and back, and find the Knowledge Base tab and the MCP Servers and Environments tabs used in [Chapter 14](mcp-hub.html).

## The settings screen

Click ⚙ at the right end of the top bar to open settings. The tabs run in one row along the top, and the screen language (**🇺🇸 English**) is at the end of the row.

| Tab | What it does | In this tutorial |
|---|---|---|
| Account Settings | Name, email, profile picture, two-step verification (OTP) | This chapter |
| Appearance | Theme Color (Light, Sky, Dark), Simplified view (On/Off) | This chapter |
| Manage Users | People in the same company and their roles | This chapter |
| Knowledge Base | The same screen as Knowledge Base on the top bar | [Chapter 8](knowledge.html) |
| MCP Servers · Environments | Tool servers to attach to agents, and their secrets | [Chapter 14](mcp-hub.html) |
| CLI Agent API Keys | The company API keys the Claude Code · Codex CLIs use (admins only) | This chapter |
| Google Drive Settings · Git Settings · DataSource · Code Editor · Glossary Management · Catalog · Org Groups · Tenant Management | External storage, data connections and admin features | Not used |

![Settings — the Account Settings tab (profile image, name and email, two-step verification) and “🇺🇸 English” at the end of the tab row](img/set-account.webp)

## Try it 1 — Account and theme

<ol class="steps" markdown="1">
<li markdown="1">In **Account Settings** you can change your name and profile picture. If you change them, click **Save**.</li>
<li markdown="1">Under **Two-step verification (OTP)**, if you switch on **Turn on two-step verification**, you enter a 6-digit code from your authenticator app each time you sign in. Leave it off for this tutorial.</li>
<li markdown="1">In **Appearance**, try a **Theme Color**. If you switch **Simplified view** from **Off** to **On**, the definition map and instance screens show just three panes: list, conversation and outputs.</li>
</ol>

![Appearance — Theme Color Light, Sky and Dark, and Simplified view set to Off](img/set-theme.webp)

## Try it 2 — Bring in a colleague

!!! note "If you did Chapter 5"
    If you already signed up Minji Kim and Seoyeon Park in [Chapter 5](organization.html), 「Manage Users」 lists all three with 「Affiliated Team : Sales Team」. The steps below repeat what you did there (signing up directly at the same address), so you can skip them.

For now, **Manage Users** lists only you (Jinyoung Jang, **me**, **superAdmin**). **Invite User** sends an invitation email, but a local install doesn't send email. Locally, a colleague joins this company as a user by **signing up at the same address**.

![Manage Users — the “Invite User” button and Jinyoung Jang (me, superAdmin)](img/set-users.webp)

<ol class="steps" markdown="1">
<li markdown="1">Open http://localhost:8088 in another browser (or a private window), and sign up sales representative **Minji Kim** (`minji@hanbit.example`) with **Try Beta Test** › **Create an account** (same as [Chapter 1](install.html)).</li>
<li markdown="1">“Registration successful.” appears, Minji Kim is signed in right away, and the **Process Architecture** opens.</li>
<li markdown="1">Refresh **Manage Users** on Jinyoung Jang's side, and Minji Kim (`user`) is now in the list.</li>
</ol>

![Minji Kim signs up — the Create an account screen](img/in-minji-register.webp)

![Manage Users after the sign-up — Jinyoung Jang (me, superAdmin) and Minji Kim (user)](img/set-users-after.webp)

!!! note "Only the first to sign up is an admin"
    A local install has only one company (tenant `localhost`). The first person to sign up becomes the admin (superAdmin), and everyone who signs up after that joins right away as a regular user (user).

## Try it 3 — Change the screen language

<ol class="steps" markdown="1">
<li markdown="1">Click **🇺🇸 English** at the end of the tab row and choose **🇰🇷 Korean**. The tab names (「Account Settings」, 「Appearance」, 「Manage Users」 …) change to Korean.</li>
<li markdown="1">Go to home: the sidebar (「Conversations」, 「Agent Colleagues」) and the chat box (its example sentences, 「Deep Agent」) are in Korean too. The names of the processes and agents you made stay as they are.</li>
<li markdown="1">Go back to settings, click **🇰🇷 Korean** and switch back to **🇺🇸 English**.</li>
</ol>

![The language menu at the end of the tab row — Korean and English](img/set-lang.webp)

![Home after switching to Korean — the sidebar, the example sentences, Deep Agent and the Process Definition Map in Korean, while “Sales Proposal Creation” and the agents you made keep their names](img/set-english-home.webp)

## Try it 4 — CLI agent API keys (admin)

This is where you put the **company API keys** that CLI agents such as Claude Code and Codex use for work items and chat. Only admins see it.
Sharing one person's subscription token among many people breaks the terms of use, so paste keys your company created in the Claude Console (Anthropic) or on the OpenAI platform.

<ol class="steps" markdown="1">
<li markdown="1">In the settings tab row, open **CLI Agent API Keys**. Claude Code (Anthropic API key) and Codex (OpenAI API key) show as 「Not configured」.</li>
<li markdown="1">Paste the company key into 「Paste a new key」 and press **Save**. The field clears and the status changes to 「Configured · ••••last four · name · time」. The key is never shown again.</li>
<li markdown="1">A CLI with a key can be picked as **CLI coding agent** in a new chat. A CLI without a key can't be picked in chat, and work items keep running on the credentials configured on the server.</li>
</ol>

![Settings — the CLI Agent API Keys tab (Claude Code · Codex, company key note)](img/set-cli-keys.webp)

!!! note "If you see 「The key store isn't set up on this server yet」"
    Keys live in the database's encrypted store (Supabase Vault). Until an operator applies that database setup on the server, this note appears and keys can't be added.

## Next chapter

The next chapter is the final project, where you build Hanbit Office A/S intake yourself using everything so far ([Chapter 19](project.html)). A one-page summary is in the [appendix](cheatsheet.html).

!!! exercise "Check your understanding"
    1. On a local install, how do you bring a colleague into this company as a user?
    2. Minji Kim signed up second. Is Minji an admin?
    3. After switching the screen to Korean, where do you click to switch back to English?

<details class="answer" markdown="1"><summary>Answers</summary>

1. Have them sign up themselves at the same address (http://localhost:8088) with **Create an account**. A local install doesn't send invitation emails.
2. No. Only Jinyoung Jang, who signed up first, is an admin; Minji Kim joins as a regular user.
3. In ⚙ settings, click **🇰🇷 Korean** at the end of the tab row and choose **🇺🇸 English**.
</details>
