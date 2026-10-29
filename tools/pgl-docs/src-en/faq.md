# Frequently asked questions

> Installation, keys and cost, which model is called when, privacy and where data lives, using it without the internet, and phones — the questions that come up most often as you follow the tutorial.

## Installation

**Q. Do I really need Docker?**
Yes. The install bundle runs every part with Docker Compose. It works on macOS, Linux and Windows (WSL2). On Windows, we recommend installing Docker Engine inside WSL2 ([Chapter 1](install.html)).

**Q. The first installation takes too long.**
The first time, it builds the images itself, which takes 20–40 minutes (the IeumOffice editor takes the longest). From the second time on, it uses the cache and is fast. To use prebuilt images, put `LITE_IMAGE_PREFIX` and `LITE_TAG` in `.env` and it downloads them instead of building. If the build fails for lack of memory, raise Docker's memory to 8GB or more. ArtCraft (`--with-craft`) pulls a prebuilt image, so it doesn't add build time.

**Q. Which profile should I choose?**
At first, the default `lite` is enough. Parts 1–4 (on your own, documents, less repetition, team) all work. To run the processes in Part 5, add `./install.sh --profile full`, and to get process suggestions from repeated work, add `--with-mining`.

**Q. I installed it, but a feature from one of the chapters doesn't show up.**
Some things aren't included in the install bundle by default.

| Feature | Why | How to turn it on |
|---|---|---|
| Conversations split by topic ([Chapter 4](contexts.html)) | The routing model uses a GPU or a lot of memory | Run the context router separately and set `CONTEXT_ROUTER_URL` |
| The "related people" order in @teammate suggestions | The same routing model | `JUDGE_URL` (without it, only the order of who you talk with most) |
| Editors for drawings, pictures, sound and video ([Chapter 8](craft.html)) | The image is large (about 660MB) | `./install.sh --with-craft` (pulls a prebuilt image). Without it, those files open as links, and mail drafts come with only the proposal and quote, no floor plan |
| Claude Code and Codex Workroom ([Chapter 23](workroom.html)) | Needs your own subscription login and the CLI on the host | Installed separately |
| Meeting transcription ([Chapter 16](meetings.html)) | Needs a separate speech recognition key | `TRANSCRIBE_API_KEY` |

**Q. How do I let people connect from other PCs?**
Change `.env` to `PUBLIC_URL=http://<this PC's IP>:18080` and `LITE_BIND=0.0.0.0`, set up SMTP, and run `./install.sh` again. When you open it to the internet, put an HTTPS reverse proxy in front, and always turn off demo login (`DEMO_LOGIN=0`).

**Q. The login code email doesn't arrive.**
If you haven't set up SMTP, the code goes not to a real mailbox but to the mailbox included in the installation, `http://localhost:18025`. If it's not there either, look at `docker compose logs auth`.

## Keys and cost

**Q. Which keys do I need?**
Just one set: the **address, key and model name** of an OpenAI-compatible API (`LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`). It doesn't have to be OpenAI. An in-house model server or another provider called the same way also works. For online meeting transcription you also need a speech recognition key (`TRANSCRIBE_API_KEY`), and for Google login and Gmail connection you need the login client details registered with Google (`GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`).

**Q. Is there a usage fee?**
Process GPT Lite itself is open source under the MIT license, so there's no usage fee. The cost is the **LLM call charges**. If you use an in-house model server, you pay only for that.

**Q. Which model is called, and when?**

| When | Which model | How much |
|---|---|---|
| When a chat message arrives — picking what kind of work it is | Fast model (`LLM_FAST_MODEL`) | Once, briefly, per message (skipped for messages whose destination is already clear, like making a skill or asking for a document) |
| Doing the actual work — answers, organizing, writing documents, handling files | Default model (`LLM_MODEL`) | Several times, depending on the size of the work. **Most of the cost comes from here** |
| Deciding which conversation a message follows up on ([Chapter 4](contexts.html)) | Small routing model → the AI model once more if confidence is low | Per message. The routing model is a separately run server, so there's no API charge |
| The title of a document card for a long answer | Fast model | Once per long answer |
| Checking mail ([Chapter 5](mail.html)) | Default model | It checks every 5 minutes, but calls the model once **only when there's new mail**. With no new mail, it doesn't call it |
| Browser agent ([Chapter 6](browser.html)) | Default model (it reads screenshots, so it must be a model that reads images) | Once per action, up to 40 times per task |
| Creating documents (Hangul and others) | Default model | Per document |
| Review after editing ([Chapter 7](office.html)·[Chapter 8](craft.html)) | Default model (reads images for pictures) | When you edit an open document |
| Meeting transcription ([Chapter 16](meetings.html)) | Speech recognition model (`TRANSCRIBE_API_KEY`) | Continuously while people speak |
| Noticing whether something said in a meeting or room is a "request" | Routing model | The big model isn't called |
| Scheduled missions ([Chapter 11](missions.html)) | Default model | At each set time. If nothing changed, it just doesn't post in Chat, but it still runs |

To cut costs, set the fast model to a small, cheap model, and don't make scheduled mission cycles too short. Browser tasks send a screenshot with every action, so if you can get the same information through a connector (Google, Slack and so on), that's cheaper.

## Privacy and security

**Q. What's sent to the model?**
The messages you send and the files you attach, the conversation history needed for the work, **the sender, subject, date and start of the body of new mail** when checking mail, and **page content and screenshots** during browser tasks. These go only to the LLM address you set. If you don't want them to leave the company, set an in-house model server as `LLM_BASE_URL`.

**Q. Does the model see the passwords I put in the Vault?**
No. Passwords, card numbers and verification codes in the Vault **never go to the model.** When a browser task reaches a password field, the model only says "put the password here," and the server types in the real value itself. Secret field values are erased from the page content, and secret fields are blacked out in the screenshots the model sees ([Chapter 6](browser.html)).

**Q. How is the Vault encrypted?**
It uses two layers of keys. Items are locked with a **data key (DEK)** made separately for each user, and that data key is locked again with a **master key (KEK)** that exists only on the server, then stored. The master key is not in the database but in the installation's `.env` (`VAULT_KEK`), so taking only the database won't open anything. With **Check** in Settings › Security, you can confirm your Vault is properly locked without seeing the values. The details and key rotation are in [Chapter 6](browser.html) and [Chapter 25](admin.html).

**Q. Can teammates see my conversations?**
No. Only you see your chats and projects. Teammates see only the **files you shared** (with a permission so only the recipient can open them; the recipient edits their own copy), the **requests you sent with @mentions** (a conversation excerpt goes along), and the **rooms and shared folders** you're both in ([Chapter 14](sharing.html)).

**Q. Isn't demo login dangerous?**
If it's left on, any email logs in with `000000`, so yes, it's dangerous. The install bundle has it off by default (`DEMO_LOGIN=0`). A development server run from source has it on by default, so put `PRO_DEMO_LOGIN=0` in `server/.env`.

## Data

**Q. Where is the data stored?**
All of it is on the PC where you installed it.

| What | Where |
|---|---|
| Conversations, cards, team, processes, Vault (ciphertext) | Database volume |
| Documents you made, attachments | Storage volume |
| Shared folders, server data | Server data volume |
| Agent workspaces and skills | `data/deepagents/` in the install folder |
| Settings and secret values (including the master key) | `.env` in the install folder |

See [Chapter 25](admin.html) for the recommended steps for backing up and moving. If you lose the master key in `.env`, you can't open Vault items, so keep it together with the backup.

**Q. How do I go back to a clean start?**
`./install.sh --uninstall --purge` removes everything: data, volumes, images and even `.env`. It can't be undone, so back up first. To only stop it and keep the data, run it without `--purge`.

## Without the internet

**Q. Can I use it without the internet?**
**Mostly yes, if you have an in-house LLM server.** Every part runs inside the PC, and login codes can come to the mailbox included in the installation. These need the internet.

| Feature | Without the internet |
|---|---|
| Chat, documents, panels, sharing, processes | Works with an in-house LLM server |
| Google login, Gmail, Calendar and YouTube connections | Doesn't work (email code login and IMAP company mail do) |
| Weather in the sky background, sender logos on mail | The default sky without weather (based on Seoul), letters instead of logos |
| Browser agent | Only sites on the company network |
| Online meetings | Work within the same network. Transcription needs a speech recognition server |

## Phones

**Q. Can I use it on my phone?**
Yes. Open the same address in your phone's browser and it switches to the phone layout (Home · Chat · Projects · Folders tabs at the top, the input box below Home) ([Chapter 2](tour.html)). On Android, there's also an app you can use by just entering the server address ([video](https://youtu.be/TYg7S1WJ0YQ)). To connect from a phone, the install PC must be open at an address that phone can see (see "How do I let people connect from other PCs?" above).

**Q. Do online meetings work on a phone too?**
Yes, if the browser allows the camera and microphone. But browsers allow the camera and microphone only on HTTPS addresses (or `localhost`), so meeting from a phone needs an HTTPS reverse proxy.

## Other

**Q. My conversation got attached to the wrong topic.**
The routing model can be wrong too. Go into the conversation you want from the conversation list and say it again, and it goes straight to that conversation without a decision ([Chapter 4](contexts.html)).

**Q. I want to stop the assistant while it's working.**
Click **Stop**, which appears at the top right of the input box while it's answering. It stops the work on the server too, and "(Stopped the answer.)" is left. Stop browser tasks with the × or **Cancel task** on the task card. If you send another message to the same conversation while waiting for an answer, the earlier work isn't cut off. The new message shows **Waiting** and is answered after the previous answer finishes ([Chapter 3](first-chat.html)).

**Q. It's tedious to explain the same work every time.**
Save the approach that worked as a skill ([Chapter 10](skills.html)), run it at a set time ([Chapter 11](missions.html)), and if several people hand the work along, make it a process ([Chapter 17](process-create.html)). The assistant may also find repeated work first and suggest it as a process ([Chapter 19](mining.html)).

**Q. Can it get faster even after it becomes a process?**
Yes. As run records pile up, you can see which step has long waits (bottleneck), the ratio of working time to waiting time (flow efficiency), and the chain of steps that drives the total duration (critical path), then compare before and after applying an improvement ([Chapter 20](bottleneck.html)–[Chapter 22](critical-path.html)).

That's the end of the Process GPT Lite tutorial. To review from the beginning, go back to the learning path on the [tutorial's first page](index.html).

!!! exercise "Check questions"
    1. You don't want conversation content to leave the company. Which setting do you change?
    2. You backed up only the database and lost the installation's `.env`. What can't you open anymore?
    3. You installed it, but conversations don't split by topic. Is it broken?

<details class="answer" markdown="1"><summary>Answer</summary>

1. Set an in-house model server as `LLM_BASE_URL`. What goes to the model goes only to the LLM address you set.
2. You can't open Vault items (passwords, cards, connection tokens). The master key that locks the data keys, which in turn lock the items, is in `.env`.
3. No. The install bundle doesn't include the context router and routing model by default. Run them separately and connect with `CONTEXT_ROUTER_URL` to turn it on.
</details>
