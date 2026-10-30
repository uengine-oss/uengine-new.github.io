# Connect external tools with MCP

> Connect the 「office」 tool to 「Hanbit Office Quote Advisor」. Fill a selected Word template with a quote, then inspect the preview for calculation and document errors.

!!! warning "Your installation needs these fixes"
    The run screens in this chapter were captured on an installation with the following fixes applied (2026-10-30). Before these fixes reach the installation repository, using a selected template or opening the result document may fail. This notice will be removed once the fixes are included.

    - Agent: [process-gpt-deepagents #10](https://github.com/uengine-oss/process-gpt-deepagents/pull/10) — enables filling the selected Word template.
    - Interface: [process-gpt-vue3 #237](https://github.com/uengine-oss/process-gpt-vue3/pull/237) — fixes result-document preview and download URLs.
    - Installation: [process-gpt-infra-docker #1](https://github.com/uengine-oss/process-gpt-infra-docker/pull/1) — provides storage for the generated result.

## Turn a draft into a document

In [Chapter 11](skills.html), you taught quote-writing rules through a skill. Now you will select a company Word template and ask the agent to fill it.

The price list supplies amounts. The skill supplies writing rules. The Word template is the document to fill. 「office」 is the external tool used to create the document.

Jinyoung Jang registers the server and connects it to 「Hanbit Office Quote Advisor」. The exercise uses Hanbit Trading's order for 25 Mesh Chair Air and 25 3-Drawer Mobile Pedestals.

In this English run, the draft total was wrong. The same wrong total went into the Word document. Follow both the tool connection and the checks needed before sending the result to a customer.

## Try it 1 — Register the MCP server

<ol class="steps" markdown="1">
<li markdown="1">Open 「MCP Servers」 in settings.</li>
<li markdown="1">Click 「Add New MCP Server」.</li>
<li markdown="1">Replace the contents of the 「New MCP」 editor with the JSON below.</li>
<li markdown="1">Click 「Add」 and check the new server card.</li>
</ol>

![MCP server settings — MCP Servers and Add New MCP Server](img/mcp-settings.webp)

The editor initially contains `{ "mcpServers": {} }`. Replace the whole value, including its braces. The server name is `office`.

```json
{
  "mcpServers": {
    "office": {
      "url": "http://process-gpt-office-mcp:1192/mcp",
      "type": "http"
    }
  }
}
```

![Server registration — the office JSON in the New MCP editor](img/mcp-add-filled.webp)

This is the Office MCP service address in the captured installation. It registers a tool endpoint for the agent. It is not a document URL to open in your browser.

The saved card shows 「Office」, 「Web Service」, and 「Validation failed」. The server was saved as enabled.

![Registered server — Office Web Service with Validation failed](img/mcp-added.webp)

!!! note "The card shows 「Validation failed」"
    This is a defect seen in the captured installation. The tools still worked with that message present. Check the actual tool result later in this chapter; the card alone does not prove that document generation succeeded or failed.

## Try it 2 — Select the agent's tool

Registering a server does not attach it to every agent. Select the registered tool for the quote advisor.

<ol class="steps" markdown="1">
<li markdown="1">Open 「Hanbit Office Quote Advisor」 and use the pencil beside its name.</li>
<li markdown="1">Check the 「Tools」 field.</li>
<li markdown="1">Remove any generated tool-name entries that do not correspond to a connected server.</li>
<li markdown="1">Select 「office Web Service」.</li>
<li markdown="1">Check that 「office」 is selected, then save the agent changes.</li>
</ol>

![Agent tool selection — office selected in the Tools field](img/mcp-tools.webp)

Names suggested during agent generation do not themselves create tool connections. Here, select the server you just registered.

Keep the 「hanbit-quote-format」 skill from [Chapter 11](skills.html). Attaching a skill and connecting a tool serve different purposes. The skill gives instructions; the tool performs document operations.

![Saved agent tools — the quote advisor after the office tool was attached](img/mcp-tools-saved.webp)

## Try it 3 — Upload the company template

Download [Hanbit Office templates (zip)](files/hanbit-office-templates.zip) and extract it. The 「Hanbit-Office-Templates」 folder contains 「Hanbit-Quote-Template.docx」.

<ol class="steps" markdown="1">
<li markdown="1">Find 「Hanbit-Quote-Template.docx」 in the extracted folder.</li>
<li markdown="1">Upload 「Hanbit-Office-Templates」 to 「Knowledge Base」 using the method from [Chapter 8](knowledge.html).</li>
<li markdown="1">Wait until the document row shows 「indexed」.</li>
</ol>

![Uploaded template — Hanbit-Quote-Template.docx in the Knowledge Base with indexed status](img/mcp-kb.webp)

Open the original template and note its customer, items, totals, and terms sections. Later, compare the generated document with that structure. Checking only the final amount can miss duplicated headings or unfinished customer details.

## Try it 4 — Ask about available tools

<ol class="steps" markdown="1">
<li markdown="1">Send the greeting below to 「Hanbit Office Quote Advisor」.</li>
<li markdown="1">Read the reply for document-generation and editing capabilities.</li>
<li markdown="1">Prepare to select the price list and template in the same conversation.</li>
</ol>

> Hello. What tools can you use right now?

![Tool-check conversation — the agent lists filesystem, document, and web tools](img/mcp-chat-hello.webp)

The reply listed filesystem tools, document tools, and web tools. Its document capabilities included 「Generate and edit DOCX and HWPX」 based on templates and conversion between HTML and DOCX or HWPX. The chat header showed 「Deep Agent」.

This reply describes available capabilities. It is not evidence that a document has been created. Next, request a draft, then ask the agent to fill the selected template.

## Try it 5 — Select the sources and create a draft

<ol class="steps" markdown="1">
<li markdown="1">Open the conversation's plus menu and choose 「Knowledge Base」.</li>
<li markdown="1">Select 「Hanbit-Office-Price-List.pdf」 from 「Hanbit-Office-Sales-Docs」 and 「Hanbit-Quote-Template.docx」 from 「Hanbit-Office-Templates」.</li>
<li markdown="1">Send the request below.</li>
<li markdown="1">Check quantities, unit prices, discounts, and totals against the price list.</li>
</ol>

> Search the selected knowledge base for the Hanbit Office price list (Hanbit-Office-Price-List.pdf) and use it. Hanbit Trading wants 25 Mesh Chair Air and 25 3-Drawer Mobile Pedestals delivered to its Seoul head office. Write a draft quote.

![Selected sources — the price list and Word quote template in the Knowledge Base picker](img/mcp-picker.webp)

The draft arrived after about 35 seconds. Its item amounts used inconsistent discount treatment.

| Item | Qty | Unit price (KRW) | Discount shown | Amount (KRW) shown |
|---|---:|---:|---:|---:|
| Mesh Chair Air | 25 | 180,000 | 5% | 4,275,000 |
| 3-Drawer Mobile Pedestal | 25 | 95,000 | 5% | 2,375,000 |

The chair amount already included the 5% discount. The pedestal amount did not. The agent then added these amounts as the subtotal and applied another 5% discount.

| Total | Draft answer |
|---|---:|
| 「Subtotal」 | KRW 6,650,000 |
| 「Volume discount」 | KRW 332,500, calculated as 6,650,000 × 5% |
| 「Installation fee」 | KRW 0 |
| 「Quote total (VAT excluded)」 | **KRW 6,317,500** |

![Draft quote — inconsistent item amounts and the incorrect total of KRW 6,317,500](img/mcp-step1.webp)

The correct calculation is:

```text
Before-discount item amounts = 4,500,000 + 2,375,000
Subtotal = 6,875,000
Volume discount = 6,875,000 × 5% = 343,750
Installation fee = 0
Quote total, VAT excluded = 6,531,250
```

The answer also gave a lead time of 5 business days and cited 「Reference: [Hanbit-Office-Price-List.pdf, p.1]」. The citation did not make the calculation correct.

The agent still had rule 6 from [Chapter 11](skills.html). It nevertheless produced the wrong total. A rule that helped one answer does not guarantee the next answer.

!!! note "Check the draft before creating the file"
    The correct total is KRW 6,531,250. In your own work, correct and recheck the draft before generating a customer document. The captured run continued with the wrong draft, so the next screens show that error carried into the Word file.

## Try it 6 — Fill the selected Word template

The captured run used the following request without correcting the draft first.

<ol class="steps" markdown="1">
<li markdown="1">In the same conversation, request a Word file using the selected template.</li>
<li markdown="1">Wait for the document result.</li>
<li markdown="1">Open the result link and inspect the preview.</li>
<li markdown="1">Compare the document's customer, items, and totals with the draft.</li>
</ol>

> Now fill the selected Hanbit-Quote-Template.docx with exactly this quote using the office tool and give me the Word file.

After about 40 seconds, the reply said 「The draft quote has been filled into the Hanbit-Quote-Template.docx.」. It offered 「Hanbit-Trading-Draft-Quote.docx」 with a download link.

![Word document result — the completion reply and generated quote document](img/mcp-step2.webp)

Clicking the link opened the 「Preview」 panel. The preview loaded successfully from storage.

The customer was Hanbit Trading. The contact remained 「[To be confirmed]」, and the quote date remained 「[Insert date of issue]」. These placeholders need review before delivery.

!!! note "Creating a document does not correct its contents"
    The request asked the tool to use exactly the draft quote. The document retained the wrong total of KRW 6,317,500. Successful file generation is separate from correct prices, calculations, and customer details.

## Try it 7 — Inspect the preview and check downloading

The result panel has 「Preview」, 「Code」, 「AI edit」, 「Edit」, and 「Download」.

<ol class="steps" markdown="1">
<li markdown="1">Read the customer details and item table in 「Preview」.</li>
<li markdown="1">Check 「3. Totals」 against your own calculation.</li>
<li markdown="1">Compare headings, table structure, terms, and closing text with the original template.</li>
<li markdown="1">Try 「Download」. Confirm that a Word file actually reaches your device.</li>
<li markdown="1">If a file downloads, open it and compare it with the preview.</li>
</ol>

![Document panel — Preview, Code, AI edit, Edit, and Download controls](img/mcp-view.webp)

The preview contained these totals:

- 「Subtotal (items only)」: KRW 6,650,000.
- 「Volume discount (5% on subtotal)」: − KRW 332,500.
- 「Installation fee」: KRW 0.
- 「Quote total (VAT excluded)」: **KRW 6,317,500**.

The correct total remains **KRW 6,531,250**.

![Document preview — customer details, item rows, and the same incorrect totals as the draft](img/mcp-result.webp)

Check terms against the source as well. Text added by the agent is not automatically an agreed customer condition.

!!! note "A local Word download was not verified"
    The preview worked, and the generated file was present in storage. The scripted download produced no download event in any of the three English runs. This chapter does not claim that a downloaded Word file was opened and checked. Verify the download separately on your installation.

!!! note "The filled template still has defects"
    The result repeats 「3. Totals」 and displays raw `**` characters. 「Hanbit Office Sales Team」 appears twice. The contact and quote date remain placeholders. Correct the arithmetic, duplicates, formatting, and missing details before sending the document.

## Separate the roles of sources, skills, and tools

Several inputs worked together in this conversation. Review each part according to its role.

| Input | Role in this exercise |
|---|---|
| Price list | Supplies prices, discounts, and installation fees. |
| 「hanbit-quote-format」 | Supplies quote-writing rules. |
| Word quote template | Supplies the document to fill. |
| 「office」 | Fills the template and creates the result document. |

Connecting a tool does not remove review. Check the draft's calculation first. Then check the document's calculation, headings, table structure, customer details, and terms.

This run demonstrated document generation and preview. It also demonstrated how an incorrect draft can become an incorrect document.

## Next chapter

You registered an external tool and attached it to the quote advisor. You filled a selected Word template and checked the result's arithmetic, formatting, and download limits.

In [Chapter 15](dmn.html), you will work with decision rules. In [Chapter 16](analytics.html), you will examine execution times and bottlenecks.

!!! exercise "Check your understanding"
    1. Why select 「office Web Service」 instead of relying on names suggested during agent generation?
    2. What request turns the chat draft into a Word document?
    3. What went wrong in this run, and what must be checked before sending the document?

<details class="answer" markdown="1"><summary>Answers</summary>

1. A suggested name does not establish a tool connection. 「office Web Service」 selects the registered MCP server.
2. Ask the agent to fill the selected 「Hanbit-Quote-Template.docx」 with the checked quote using the 「office」 tool.
3. The draft mixed amounts before and after discount, producing KRW 6,317,500 instead of KRW 6,531,250. That error entered the document. Also check duplicated headings and closing text, raw formatting characters, missing contact and date values, terms, and whether the Word file actually downloads.
</details>
