# Final project — a new customer request from start to finish

> Use everything you've learned in one go. You receive one design proposal request email from a new customer and take it all the way through organizing → drafts → team review → less repetition → official process → improvement. It's a project for teams of 2–3 people, taking 2–3 hours.

Up to Chapter 25, team lead Jinyoung Jang's work started with asking the assistant questions alone, and came all the way to an official process the team shares, its improvement, and operations. Now you walk that path again from the start with one request from a customer you've never seen. This time, instead of following each chapter, you choose for yourself what to use.

## The situation

On Thursday morning, an email from a new customer arrives in Jinyoung Jang's mailbox.

```text
From: Solgil Bakery Store Development <store@solgil-bakery.example>
Subject: [Solgil Bakery] Design proposal and quote request for renovating Pangyo Store #3

Hello, this is the Solgil Bakery store development team.
We want to renovate Pangyo Store #3 (about 120㎡ of floor space, ground floor) into a bakery café.
We'd like to separate the path along the bread displays from the seating (around 40 seats), and we want an open kitchen where customers can see the oven work.
We can't close for long, so construction must be done mostly at night and finish within 3 weeks.
Our budget is ₩180 million or less, including interior and furniture.
Please send us a design proposal including a floor plan, and a quote, within 2 weeks.
```

It's similar to the Moonlight Coffee job, but this time the goal is to work **as a team** from the start, and to leave things so you can do it **faster next time**. The team lead asks:

1. Can we organize the request without missing anything, and work out what to do when within 2 weeks?
2. Can we make drafts of the floor plan, proposal and quote today, and polish them through review by the designer and finance?
3. Can we save what worked this time so we can reuse it with a single sentence for the next customer?
4. Requests like this keep coming. Can we make it an official process, and find and cut where time leaks?

## Team and preparation

| Role | Who | Main work |
|---|---|---|
| Proposal team lead | Jinyoung Jang | Receiving mail, organizing, scheduling, starting the process, the final reply |
| Designer | Minji Kim | Reviewing and revising the floor plan and proposal visuals |
| Finance | Seoyeon Park | Reviewing the quote, fitting the budget |

With two people, one person plays both designer and finance.

- Everyone logs in with their own account. A person who has logged in joins the team on their own the first time they open **Settings › Team & roles**. Adding people who haven't logged in yet, or assigning role owners, is done by an administrator ([Chapter 25](admin.html)). If Jinyoung Jang isn't an administrator, ask one.
- Put the email above into Jinyoung Jang's mailbox. If you connected Gmail or IMAP, actually send it to your own address. **Get practice email** in the demo mailbox doesn't have this email, so either connect a real mailbox with **Change connection** ([Chapter 5](mail.html)), or receive the practice email **Moonlight Coffee Store #2 proposal & quote request** and follow the same flow.
- Stage 5 and later need the process engine. Check with your administrator that the process engine (`./install.sh --profile full`) and mining (`--with-mining`) are on ([Chapter 1](install.html)).

## The project

### Stage 1 — receive and organize (Chapters 3–6, about 20 min, Jinyoung Jang)

- See what appears on Home when the email arrives. It's an email asking for documents, so the assistant starts making drafts and a **Review** card appears ([Chapter 9](email-to-quote.html)). While the drafts are being made, ask it to organize.
- In Chat: `Put the Solgil Bakery Pangyo Store #3 request in a table, and make an Excel schedule working back from the 2-week deadline`.
- Slip in another task along the way (for example, a venue for next week's team dinner), come back to the Solgil Bakery story, and see whether the conversations split correctly ([Chapter 4](contexts.html)).
- Check that the schedule and summary document have gathered in the output stack.
- **Outputs**: The request summary (a document card or a file), `Solgil Bakery … schedule.xlsx`, a screenshot of the conversation list (2 or more conversations, with each conversation's message count visible)

### Stage 2 — polish the drafts (Chapters 7–9, about 30 min, Jinyoung Jang · Minji Kim)

- Open the drafts the assistant made: the floor plan (`.dxf`), the design proposal (`.docx`) and the quote (`.xlsx`). On an install without CADCraft, only the proposal and quote come, with no floor plan ([Chapter 8](craft.html)).
- Keep them open and edit them by talking at least twice. For example, on the floor plan, `Move the open kitchen to the inner wall of the store and leave an aisle of at least 1.2 m between the seating area and the displays`, and on the quote, `Add a 15% night-work surcharge as a separate row`.
- After editing, check the **review** result on the card (**Reviewed** or **Needs review check**) and the review notes ([Chapter 9](email-to-quote.html)).
- **Outputs**: Edited copies of the three files, and a table of what you said when editing and the review notes

### Stage 3 — team review (Chapters 13–16, about 30 min, all three)

- Create a shared folder **Solgil Bakery Pangyo Store #3** and put the three files in it. Start with edit permission for Minji Kim and view permission for Seoyeon Park ([Chapter 13](folders.html)).
- In Chat, Jinyoung Jang sends `@Minji Kim Could you review the open kitchen location on the floor plan?`, and sends the quote to Seoyeon Park with the share button on the quote card ([Chapter 14](sharing.html)).
- Each recipient uses **Continue working** in their Inbox to hand it on to their own assistant, then shares the result back.
- The three of you hold a 15-minute online meeting in a room. Say something like "Show the quote" to bring up materials, and decide how to fit the budget within ₩180 million. When the meeting ends, the meeting minutes stay in the room ([Chapter 16](meetings.html)).
- **Outputs**: The Inbox screen (for Minji Kim and Seoyeon Park each), a variation comparison or merge record, the meeting minutes

### Stage 4 — less repetition (Chapters 10–12, about 20 min, Jinyoung Jang)

- Save this flow as a skill: `Turn the way we handled Solgil Bakery — receiving a store design request email and making a summary table, a schedule and three drafts — into a skill called "Store design proposal draft"`. Share the saved skill with the team ([Chapter 10](skills.html)).
- Create a scheduled mission with `Every Monday at 9 AM, summarize the deadlines and remaining work for the proposals in progress` ([Chapter 11](missions.html)).
- Use **New panel** to make a **Proposal pipeline** panel app (customer, stage, amount, deadline) and record the Moonlight Coffee and Solgil Bakery jobs. Check from Seoyeon Park's account as well how the amounts appear masked ([Chapter 12](panel-apps.html)).
- **Outputs**: The skill card, the "Scheduled" chip and the next run time, the panel app screen (two accounts)

### Stage 5 — make it an official process (Chapters 17–19, about 30 min, led by Jinyoung Jang)

- Create a process by talking: `Create a process for when a design proposal request email arrives: organize → floor plan and proposal drafts (reviewed by the Designer) → quote (reviewed by Finance) → Proposal team lead approval → reply` ([Chapter 17](process-create.html)).
- In **Settings › Team & roles**, set Minji Kim as **Designer** and Seoyeon Park as **Finance**, and start the process. Each person handles their own step with the **Decision** and **Input** cards on their Home ([Chapter 18](process-run.html)).
- If you have an administrator account, look at how the mail work so far was grouped into a flow on the mining suggestion screen, and compare it with the process you made yourself ([Chapter 19](mining.html)).
- **Outputs**: The process diagram (BPMN), the instance progress screen (assignees and outputs for each step), screenshots of the steps each person handled

### Stage 6 — improve it (Chapters 20–22, about 30 min, all three)

- Open the improvement screen with **Improve analysis →** next to the process in **Projects** (or the **Constraint** notification on Home › **View improvement**). In the **Bottleneck** tab's heat map, switch the metric to **Wait time** to find the reddest step, and confirm it with lead time by step and the profile by instance ([Chapter 20](bottleneck.html)). With only a few runs recorded, the numbers jump around, so run a few more or practice with the sample data in [Chapter 20](bottleneck.html).
- In the **Value stream** tab, separate working time from waiting time to read the **flow efficiency**. In the **Constraint** tab, find the person or agent with the highest utilization, and choose one improvement with the five steps of the theory of constraints (identify → exploit → subordinate → elevate → repeat) ([Chapter 21](value-stream.html)).
- In the **Critical path** tab, check whether that step drives the total duration (median and slow case). In the **Run improvement** tab, calculate the improvement in advance with **Add**, create a new version with **Apply proposal**, and look at the comparison by version ([Chapter 22](critical-path.html)). If the new version has few runs, the screen adds **Small sample**, so explain the effect mainly by the fact that the path changed.
- **Outputs**: The bottleneck step and the evidence (numbers), flow efficiency before and after, the improvement and its calculated result, a before-and-after comparison screen

## Presentation (10 min per team)

1. How long it took from the Solgil Bakery request to the reply, and a list of what people did by hand and what the assistant did
2. Which of the edits you asked for in Stage 2 didn't work on the first try, and why
3. The bottleneck and improvement you found in Stage 6, with the expected effect and the actual effect

## Grading criteria (example)

| Item | Criteria | Points |
|---|---|---|
| Organizing and schedule | No conditions from the email (area, seats, night work, budget, deadline) are missing, and the schedule works back from the 2-week deadline | 10 |
| Draft quality | The three documents reflect the request, and you can explain what you changed by talking and the review results | 20 |
| Team collaboration | Shares, @mentions, Continue working and meeting minutes actually left records, and permissions were given as intended | 20 |
| Less repetition | The skill, scheduled mission and panel app are built so they can be used as they are for the next customer | 15 |
| Process | Roles are assigned correctly and each person handles their own step; compared with the mining result | 15 |
| Improvement | The bottleneck and flow efficiency are shown with numbers, and the improvement's effect is shown before and after | 20 |

## Things to think about

- Having the assistant make drafts without asking is fast, but it can also spend time on a misunderstood request. For which kinds of email should a person check first, before the drafts?
- Thanks to the Vault, the assistant logs in to sites without knowing the passwords. Even so, which actions must a person always approve?
- Where is the line between a skill (work one person does with one agent) and a process (work handed between several people and roles)? Sort the work in this project into what a skill is enough for and what must be a process.
- If the bottleneck you found in Stage 6 was a human review step, which is better: handing it to an agent or changing the review criteria?

If you get stuck during the project, look up the words and buttons used in each chapter in the appendix, [Chapter 27, Cheat sheet](cheatsheet.html), and answers to installation, cost and security questions in [Chapter 28, Frequently asked questions](faq.html).

!!! exercise "Check questions"
    1. In Stage 1, right after the Solgil Bakery email arrives, what should appear on Jinyoung Jang's Home and in Chat?
    2. In Stage 3, Minji Kim gets edit permission and Seoyeon Park gets view permission. What happens if Seoyeon Park tries to edit the quote herself and upload it to the folder, and how should she add her input instead?
    3. In Stage 6, the new version has only two runs, so **Small sample** appears on the screen. What should you base the effect on in your presentation?

<details class="answer" markdown="1"><summary>Answer</summary>

1. It's an email asking for documents, so the assistant starts making drafts of the floor plan, design proposal and quote, and a **Review** card appears on Home. On an install without CADCraft, only the proposal and quote come, with no floor plan.
2. With view permission, she can't upload to the folder. When Jinyoung Jang sends the quote with the share button, Seoyeon Park uses **Continue working** in her Inbox to hand the review to her own assistant, then shares the result back.
3. With few runs, the lead time numbers get inflated, so explain mainly the fact that the path changed (for example, which run skipped which step), and say you'll compare the calculated expected effect with the actual one after more runs pile up.
</details>
