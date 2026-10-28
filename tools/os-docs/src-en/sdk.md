# Code App SDK — Read and Edit the Code Yourself

> Look at the functions of the SDK (`og.js`) that code apps use, and edit app code yourself without the agent. A little JavaScript from a programming class is enough.

## The structure of an app

```text
<data folder>/codeapps/<app id>/
  ├─ index.html     ← loads /apps/_runtime/og.css and echarts.min.js, and loads app.js as a module
  ├─ app.js         ← Vue 3 app (ES module)
  ├─ style.css
  ├─ AGENTS.md, CLAUDE.md   ← agent rules (files the agent reads, not the app)
```

On macOS, the data folder is `~/Library/Application Support/Ontological Studio/`. The preview address is `/apps/<app id>/`, shown at the top right of the screen.

`index.html` looks like this. Do not delete the `/apps/_runtime/…` lines.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Delayed Shipments Board</title>
  <link rel="stylesheet" href="/apps/_runtime/og.css" />
  <link rel="stylesheet" href="./style.css" />
  <script src="/apps/_runtime/echarts.min.js"></script>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="./app.js"></script>
</body>
</html>
```

## SDK functions

```javascript
import { query, schema, theme, onTheme, color, actions, act } from '/apps/_runtime/og.js'
```

| Function | What it does |
|---|---|
| `await query(cypher, params?)` | Runs **read-only** Cypher and returns an array of rows. The server rejects write clauses (`CREATE`, `MERGE`, `SET`, `DELETE`). On failure, it throws an `Error` with the engine's message. |
| `await schema()` | The published ontology's classes, properties and relationships. For apps that explore the schema on their own |
| `theme()` | `'light'` or `'dark'` — follows Studio's theme setting |
| `onTheme(fn)` | Calls `fn` when the theme changes. Use it to redraw charts. Returns a function that removes the listener |
| `color(name)` | The value of a theme color token, such as `color('accent')` or `color('fg')` — for passing to canvas charts |
| `await actions(className?)` | The list of published actions ([Chapter 20](app-actions.html)) — since 0.1.1 |
| `await act(opts)` | Opens the plan → approve → execute → cancel dialog ([Chapter 20](app-actions.html)) — since 0.1.1 |

### What query() returns

```javascript
const rows = await query('MATCH (s:Supplier) RETURN s.name AS name, s.tier AS tier ORDER BY name')
// → [{ name: 'Daesung Cable', tier: 2 }, { name: 'Hanbit Precision', tier: 1 }, …]
```

(If you added Hanbit Precision with an additional ingestion in exercise 2 of Chapter 12, `{ name: 'Hanbit Precision', tier: 1 }` also appears.)

- The names in `RETURN` (`AS`) become the object keys. Numbers come back as numbers.
- If you return a whole node (`RETURN s`), you get its property object with `_labels` and `_id` added.
- Do not join values into the query string; pass them as **parameters**. This avoids quoting problems and injection attacks.

```javascript
const pos = await query(
  'MATCH (p:PurchaseOrder)-[:ORDERED_FROM]->(s:Supplier) WHERE s.name = $name RETURN p.po_id AS po, p.status AS status',
  { name: 'Shenzhen Goldline PCB' })
```

### Theme colors

In `style.css`, use only these variables for colors. Then the light and dark themes work automatically.

| Variable | Use |
|---|---|
| `--og-bg` `--og-panel` `--og-raised` | Background, panels, raised cards |
| `--og-line` | Lines, borders |
| `--og-fg` `--og-dim` `--og-mute` | Text (strong → faint) |
| `--og-accent` `--og-on-accent` | Accent color, and text on top of it |
| `--og-blue` `--og-warn` `--og-danger` `--og-ok` `--og-purple` `--og-soft` | Status colors |

## Try it — edit by hand

Let's change one line yourself instead of asking the agent. In the **Delayed Shipments Board** from [Chapter 18](code-app.html), change the delay threshold from “at least 1 day” to “more than 3 days”.

<ol class="steps" markdown="1">
<li>Check the location in the <b>Files</b> tab, then open <code>codeapps/&lt;app id&gt;/app.js</code> in the data folder with an editor (VS Code or similar).</li>
<li>Change <code>WHERE s.delay_days &gt; 0</code> to <code>WHERE s.delay_days &gt; 3</code> and save.</li>
<li>Click <b>Refresh preview</b> in Studio. The table goes from 4 rows to 2 (SHP-03, SHP-02).</li>
</ol>

!!! tip "You can take turns with the agent"
    If you edit by hand and then ask for more changes in plain words, the agent rereads the files and continues from there. You can also polish the agent's code by hand. The code is the app.

## Add a chart (optional)

ECharts is available as the global `echarts`. Let's draw the open amount per supplier as bars. We also redraw the chart when the theme changes.

```javascript
import { query, color, onTheme } from '/apps/_runtime/og.js'

const rows = await query(`
  MATCH (p:PurchaseOrder)-[:ORDERED_FROM]->(s:Supplier) WHERE p.status = 'OPEN'
  RETURN s.name AS supplier, sum(p.amount_usd) AS amount ORDER BY amount DESC`)

const chart = echarts.init(document.getElementById('chart'))
function draw() {
  chart.setOption({
    textStyle: { color: color('dim') },
    xAxis: { type: 'category', data: rows.map(r => r.supplier), axisLine: { lineStyle: { color: color('line') } } },
    yAxis: { type: 'value', splitLine: { lineStyle: { color: color('line') } } },
    series: [{ type: 'bar', data: rows.map(r => r.amount), itemStyle: { color: color('accent') } }],
  })
}
draw()
onTheme(draw)   // redraw when the theme switches between light and dark
```

You also need to add `<div id="chart" style="height:320px"></div>` to `index.html`.

!!! exercise "Check yourself"
    1. What happens if you call `query('MATCH (s:Supplier) SET s.tier = 1')`?
    2. When you look up purchase orders by a supplier name the user typed, why shouldn't you join the name into the Cypher string?
    3. What is wrong with writing a color directly, like `#14b8a6`?

<details class="answer" markdown="1"><summary>Show answers</summary>

1. It has a write clause, so the server rejects it and `query()` throws an `Error`. Values are changed only through actions.
2. If the name contains a quote (e.g. `O'Neil`), the query breaks, and malicious input could change the query (injection). If you pass it as the `$name` parameter, it is treated only as a value.
3. The color stays the same when the theme changes, so it can be hard to see or look wrong in the dark theme. Use the `--og-*` variables or `color()`.
</details>
