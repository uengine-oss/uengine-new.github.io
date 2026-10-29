# At a glance

> Where the screens used in this tutorial are, the sentences sent in chat, and the practice files and results, all on one page. If you lose track of where something was while following along, look here.

## Where to find it

| What you want to do | How to get there | Ch. |
|---|---|---|
| Install, start, stop | Terminal `./start-all-services.sh frontend completion polling-service memento bpmn-extractor` · `./stop-all-services.sh` | [1](install.html) |
| Create a process (chat) | Pencil icon at the top of the sidebar (home) › chat box | [3](process-create.html) |
| Open a process definition | **Process Definition Map** on home › process name | [4](definition.html) |
| Edit a definition, save a version | Pencil on the definition screen (edit mode) › double-click a step › 💾 | [4](definition.html) |
| Compare versions | Edit mode › **Version History** | [4](definition.html) |
| Export a definition | **Export Component (.zip)** on the definition screen | [4](definition.html) |
| Upload company documents | Book icon on the top bar (Knowledge Base) › **Upload folder** | [8](knowledge.html) |
| Attach a document in chat | Chat box ＋ › **Knowledge Base** › check the file › **Use 1 file** | [8](knowledge.html) |
| Create an agent | Person icon next to **Agent Colleagues** in the sidebar › **Create Agent** › **Generate Agent with AI** › **Save** | [9](agents.html) |
| Chat with an agent | **Agent Colleagues** in the sidebar › the agent › **New Chat** | [10](agent-chat.html) |
| Attach a document in an agent chat | Reopen that chat room from **Conversations** › ＋ › **Knowledge Base** | [10](agent-chat.html) |
| Create a process from a document | Home ＋ › **Knowledge Base** › policy document › ask **Deep Agent** › **Save** in the Work folder | [12](document-process.html) |
| Make a decision table (DMN) | **Business Rule ＋** in the agent profile › mode **Creation** › 💾 | [15](dmn.html) |
| Test a decision table | Same screen, mode **Inference** | [15](dmn.html) |
| Manage colleagues, language | ⚙ on the top bar › **Manage Users** · **🇺🇸 English** at the end of the tab row | [18](settings.html) |

## Sentences sent in chat

| Ch. | Agent | Sentence |
|---|---|---|
| 3 | Basic Agent | Create a sales proposal process. The customer enters their request, then a sales representative writes the proposal and sends it to the customer — a two-step process. Make an input form for each step. |
| 8 | Deep Agent + price list | Search the selected knowledge base price list, then calculate the discount, installation fee and total for 40 Mesh Chair Pro and 40 Motion Desk 1600 delivered to our Busan office. Show your sources. |
| 9 | (Generate Agent with AI) | A sales-team agent that reads the Hanbit Office price list and writes office furniture proposals and draft quotes for customer requests. It calculates volume discounts and regional installation fees exactly and cites its sources. |
| 10 | Quote Advisor + price list | Search the selected knowledge base price list. Hanbit Trading wants 25 Mesh Chair Air and 25 3-Drawer Mobile Pedestals delivered to its Seoul head office. Write a draft quote for the customer as a table, including the discount, installation fee, total, lead time and quote validity. |
| 12 | Deep Agent + policy | Search the selected knowledge base for the Hanbit Office Bulk Order Quote Approval Policy and create a bulk order quote process that follows it. Keep its steps and owners, the approval by amount, and sending rejected quotes back to quote calculation. Let agents handle the stock check and quote calculation steps, and make an input form for each step. |
| 15 | Business rule (Creation) | Make the Hanbit Office volume discount rule as a decision table. Input: order quantity of the same product (number). Output: discount (%). 1–19 → 0%, 20–49 → 5%, 50–99 → 8%, 100 or more → 12%. |
| 15 | Business rule (Inference) | What is the discount for an order quantity of 40? |

## Practice files and expected answers

[Hanbit Office sales docs (zip)](files/hanbit-sales-docs-en.zip) — `Hanbit-Office-Price-List.pdf`, `Hanbit-Office-Quote-Approval-Policy.pdf`

| Question | Answer calculated from the price list |
|---|---|
| Mesh Chair Pro 40 + Motion Desk 1600 40, Busan | 5% discount → KRW 29,640,000, installation 3% KRW 889,200, total **KRW 30,529,200** |
| Mesh Chair Air 25 + 3-Drawer Mobile Pedestal 25, Seoul | 5% discount → 4,275,000 + 2,256,250 = **KRW 6,531,250**, installation KRW 0, lead time 5 business days, valid for 30 days |
| Meeting Table (8 seats) 10, Seoul | No discount, KRW 11,500,000 + installation KRW 300,000 = **KRW 11,800,000** |
| Discount by quantity | 1–19: 0% · 20–49: 5% · 50–99: 8% · 100 or more: 12% |
| Quote approver | Under KRW 30,000,000: sales team lead · KRW 30,000,000 or more: sales team lead, then the finance officer |

All amounts exclude VAT.

## Terms

| Term | Meaning |
|---|---|
| Process definition | The blueprint (BPMN) of the steps, owners and forms |
| Instance | One case actually running according to the definition |
| Lane | The horizontal band in a flow diagram for one role |
| Basic Agent · Deep Agent | The AI that handles the chat. Deep Agent finds and reads documents and makes files |
| Knowledge Base | Where you upload company documents. Pick them in chat to use as sources |
| Agent Colleagues | AI colleagues with a name, goal and persona |
| MCP server | A server that gives agents tools (Chapter 14, coming soon) |
| Decision table (DMN) · business rule | A rule that sets condition → result in a table |
| Hit policy Unique | Only one row matches any input |
