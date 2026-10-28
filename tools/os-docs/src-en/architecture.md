# Inside Ontological Studio

> Learn what each part of the app does and how data flows between them. This will help you see which parts you are using in the exercises that follow.

## Component map {#component-map}

```text
 ┌─────────────────────────────── Ontological Studio (desktop app) ────────────────────────────────┐
 │                                                                                                 │
 │  Screens: Home · Build Ontology · Ask & Act · Data Sources · Ontology Apps · Systems            │
 │           Ontological Portal (Cypher console)                                                   │
 │              │                             │                                      │             │
 │              ▼                             ▼                                      ▼             │
 │   Studio backend + agents ──Bolt──▶ Ontological DB ◀──Bolt── Portal        Action executor      │
 │   (build · query · dashboards)  (graph engine = PostgreSQL extension)     (kinetic-action)      │
 │                                            │  data fabric                         │             │
 │                                            ▼                                      ▼             │
 │                                Sources: ERP · WMS · CRM ◀── updates ── Sample business systems  │
 │                               (read in place, not copied)              (ERP · WMS · CRM APIs)   │
 └─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

| Component | Role |
|---|---|
| **Ontological DB** | The graph database that stores ontologies and runs Cypher. It is a PostgreSQL extension, so graph queries are translated into PostgreSQL SQL and run there. It also handles bitemporal data (time travel), permissions and schema evolution. |
| **Data fabric** | A feature inside Ontological DB. It makes tables in other databases look like graph nodes **without copying them** (virtual nodes). |
| **Bolt gateway** | Supports Bolt, the protocol Neo4j uses. Studio and the Portal read and write the graph through it. |
| **Studio** | The ontology build, query and dashboard screens, and the agents behind them. |
| **Action executor** | Plans actions, evaluates policies, gets a person's approval, then calls the business system APIs. On cancel, it undoes the steps in reverse order. |
| **Sample business systems** | Purchasing ERP, Logistics WMS and Customer CRM: small REST services, each with its own authentication method. When an action calls them, values in the source databases change. |

## There are two graphs

Ontological DB can hold several **graphs** (separate data spaces). After a fresh install you will see two.

| Graph | What it holds | Mainly used for |
|---|---|---|
| `sample` | **Virtual nodes and virtual relationships** that expose the sample source tables as they are | The Data Sources tab, Cypher exercises in the Portal (Part 4) |
| `ontology` | The **ontology** Studio built: class definitions, instances, relationships, action definitions | Ask & Act, Ontology Apps (Parts 5–7) |

`sample` is “a mirror that shows the sources as they are”, and `ontology` is “knowledge organized from the business point of view”. For example, `ontology` has a `SHIPPED_BY` relationship (shipment → supplier) that the sources don't have, every class and property has a description, and actions are attached.

!!! note "Why keep them apart?"
    Source table names and ontology class names are often the same (`Supplier`). If both lived in one graph, the read-only virtual nodes and the built nodes would collide. That's why the sample keeps its virtual nodes in a separate `sample` graph.

## The path of a question

When the question “Which inbound shipments are more than 3 days late?” arrives in the Ask & Act tab:

1. The agent reads the schema of the published ontology (which classes, relationships and properties exist).
2. It writes Cypher and sends it to Ontological DB over Bolt.
3. Ontological DB translates the Cypher into SQL and runs it. The data fabric passes the needed conditions down to the source databases.
4. Along with the results, the answer states “which facts on which nodes it used as evidence”.

## The path of a command

The command “Expedite those shipments” flows differently.

1. The agent finds the **action** that fits this command (`Shipment.expediteShipment`).
2. It asks the action executor for a **plan**. The executor picks the target shipments and, for each target, a **policy** decides whether to allow or deny it. Nothing has changed yet.
3. **A person approves it on the plan card.**
4. The executor calls the business system APIs in turn (change the priority in WMS → send an expedite request in ERP).
5. The values in the source databases change, and because the data fabric reads them directly, the graph shows the change right away.
6. If you say “Cancel what you just did”, the steps that succeeded are **undone in reverse order** (compensation).

Neither agents nor apps call business systems directly. They always go through this executor.

!!! exercise "Check yourself"
    1. You run `MATCH (s:Supplier) RETURN s` in the Portal. Explain where the results come from when the graph selector is set to `ontology` and when it is set to `sample`.
    2. To check the result of an action, do you need to log in to the business system separately?

<details class="answer" markdown="1"><summary>Show answers</summary>

1. With `sample`, you get virtual nodes read in place from ERP's `erp.supplier` table. With `ontology`, you get the `Supplier` instances that were loaded into the ontology during the build.
2. No. The business systems change the source databases, and the data fabric reads those sources on every query, so you can check right away in the Data Sources tab or the Portal (`sample` graph).
</details>
