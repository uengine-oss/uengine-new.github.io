# Process GPT Lite page — screenshots to re-capture in English

The English product page (`en/contents/processgptlite.html`) still shows the Korean captures below.
Each `<img>` already points at `images/processgptlite/en/<same name>.jpg` and falls back to the Korean
file (`onerror`) while the English one is missing, so dropping a file into `images/processgptlite/en/`
is all it takes: no page edit, no rebuild.

Capture rules, same as the Korean set:

- 1280×720 JPEG, the app in **English mode**, terms as in `pgpt-pro/i18n/GLOSSARY.md` and `src/i18n/ko-en.json`.
- English example data: Moonlight Coffee (customer, Store #2, Seongsu-dong), Jinyoung Jang, Minji Kim, Seoyeon Park,
  Travel expense settlement, Supplier catalog price survey.
- Most Korean captures are frames from the demo videos and carry a dark caption pill at the top. Re-take them from the
  English videos with the English caption, or capture without a caption; keep the same framing so the cards crop the same way
  (feature cards crop to 16:9 from the top).

| # | File | Used on the page | What the Korean capture shows | What to show in English |
|---|---|---|---|---|
| 1 | `processgptlite-router.jpg` | Features card "Every task starts in one chat"; Capabilities 01 "Chat and Home" | Chat: a short follow-up ("what's the second video from that channel?") is attached by the routing model (badge "routing model 1.00") to an earlier YouTube-channel conversation; weather panel and "New panel" on the left | The same: an English follow-up routed to the earlier conversation, the routing-model badge and the "conversation context" hint visible |
| 2 | `processgptlite-home.jpg` | Features card "A Home screen that puts your to-dos first" | Home with action cards (Submit / Reply / Release / Pay), and the travel expense settlement process on the right with its approval step (Approve / Reject) while the settlement review agent writes its report | Home with English action cards for the Travel expense settlement run, the approval card with Approve / Reject |
| 3 | `processgptlite-office.jpg` | Features card "Agents create it, people fix it on the spot" | An HWPX document (customer seminar notice) open in the IeumOffice editor, the document AI helper panel on the left | An English document open in the IeumOffice editor with the document AI helper; an HWPX file is fine, the point is the native format |
| 4 | `processgptlite-folders.jpg` | Features card "Shared folders for people and agents" | Shared folder "November customer seminar" with the Merge all dialog: two variations merged in order, conflict options (stop and tell me / hand to a resolver agent / pick a side per file) | The same dialog in English (Merge all, variations, conflict choices), file tree with document cards |
| 5 | `processgptlite-panelapp.jpg` | Features card "Work apps you build by asking" | The "Team leave days" panel on Home (2 teammates, 32 days granted, 8 used) and the same data opened with Open sheet in the IeumOffice spreadsheet | The leave panel in English (Minji Kim and a second teammate) and Open sheet showing the same rows |
| 6 | `processgptlite-process.jpg` | Features card "The Process GPT engine, as is" | Projects list of running processes and a browser agent's live screen researching an external book catalog (process step 3/6) | Projects in English with running processes (e.g. Supplier catalog price survey) and the live browser-agent screen |
| 7 | `processgptlite-missions.jpg` | Capabilities 02 "Work automation" | A skill card created from chat ("gmail-billing-daily-digest": summarize payment and billing mail every morning), with its triggers and "View in skill management" | The same skill card in English (the skill id stays `gmail-billing-daily-digest`) |
| 8 | `processgptlite-sns.jpg` | Capabilities 03 "Real-world scenario" | The daily social media trend process waiting for the product owner's decision card (apply to product / hold, scope of the improvement), "Needs your input" | The decision card in English with "Needs your input" |
| 9 | `processgptlite-cad.jpg` | Capabilities 04 "Documents and creative apps" | An office layout `.dxf` drawing opened from its CAD card in CADCraft | A CADCraft drawing in English UI (e.g. the Moonlight Coffee Store #2 floor plan) opened from its card |
| 10 | `processgptlite-workroom.jpg` | Capabilities 05 "Agent Workroom" | Workroom "Product improvement": file tree, `test_triage.py` in the editor, and the "Continue Claude Code" terminal where the user steers the session | The same Workroom view with an English instruction to Claude Code |
| 11 | `processgptlite-vault.jpg` | Capabilities 06 "Security" | A browser agent at a test checkout page with the card fields masked; "Card saved · Visa •••• 4242" | The same flow in English, card shown only as Visa •••• 4242 |
| 12 | `processgptlite-skills.jpg` | Capabilities 07 "Team collaboration" | A skill variation ("add risk and issue extraction" to `weekly-report-summary`) with Request merge, the diff of `SKILL.md`, and the note that only the author and the agent's owner can merge | The same variation and diff in English (Request merge, Merged after verification) |
| 13 | `processgptlite-prls.jpg` | Capabilities 08 "Panel apps" | Access rules of the "Team shared calendar" panel app: security and privacy defaults, field sensitivity, row access per role (view / create / edit / delete) | The same rules dialog in English (Security & privacy defaults, Row access) |
| 14 | `processgptlite-android.jpg` | Capabilities 09 "Anywhere" | The Android app on a phone: Home with a request card and the weather panel, plus a Korean text slide listing the app's features | The Android app in English; the text slide in English or dropped |

Not on this page:

- `images/full-width-images/main-img-processgptlite.png` (1120×860) is the social preview (`og:image`,
  `twitter:image`; the Lite course page uses it too), a composite of capture 2 and the PhotoCraft live-editing frame. Social previews can't fall back,
  so an English version goes to `images/en/full-width-images/main-img-processgptlite.png`; the en-edition build then
  points the English page at it (rebuild the page once it's there).
- `images/processgptlite/processgptlite-live.jpg` (PhotoCraft live co-editing) is in the folder but no page uses it
  today; no English capture needed unless it goes on a page.
