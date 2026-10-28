# Cypher and Fabric Cheat Sheet

> The statements used in this tutorial, all in one place. Keep it handy when you practice in the portal. The examples use the `sample` graph.

## Reading

| What you want to do | Cypher |
|---|---|
| Find nodes | `MATCH (s:Supplier) RETURN s` |
| Pick properties | `MATCH (s:Supplier) RETURN s.name, s.country` |
| Find a node by key | `MATCH (s:Supplier {supplier_id: 'S-CN-01'}) RETURN s` |
| Filter | `WHERE s.country = 'China' AND s.tier = 1` |
| Match a list | `WHERE sh.ship_status IN ['IN_TRANSIT', 'CUSTOMS_HOLD']` |
| Strings | `WHERE s.name CONTAINS 'Gold'` · `STARTS WITH` · `ENDS WITH` |
| Dates | `WHERE c.opened_date >= '2026-08-29'` |
| Sort and limit | `ORDER BY po.amount_usd DESC SKIP 2 LIMIT 3` |
| Rename | `RETURN po.po_id AS purchase_order` |
| Remove duplicates | `RETURN DISTINCT s.country` |
| Conditional value | `CASE WHEN sh.delay_days > 3 THEN 'Late' ELSE 'On time' END` |
| Unwind a list | `UNWIND ['SHP-02','SHP-03'] AS no MATCH (sh:Shipment {shipment_no: no}) RETURN sh` |

## Relationships

| What you want to do | Cypher |
|---|---|
| Follow one relationship | `MATCH (po:PurchaseOrder)-[:ORDERED_FROM]->(s:Supplier)` |
| Follow it in the other direction | `MATCH (s:Supplier)<-[:ORDERED_FROM]-(po:PurchaseOrder)` |
| Follow several relationships | `(sh:Shipment)-[:SHIPS]->(po:PurchaseOrder)-[:ORDERED_FROM]->(s:Supplier)` |
| Return the relationship too | `MATCH (a:Shipment)-[r:SHIPS]->(b:PurchaseOrder) RETURN a, r, b` |
| Two branches | `MATCH (i:Item)<-[:FOR_ITEM]-(so:SalesOrder), (i:Item)<-[:OF_ITEM]-(l:PoLine)` |
| Keep rows with no connected data | `OPTIONAL MATCH (sh:Shipment)-[:SHIPS]->(po:PurchaseOrder)` |
| Only rows with no connected data | `… OPTIONAL MATCH … WITH sh, po WHERE po IS NULL RETURN sh` |

## Aggregation

| What you want to do | Cypher |
|---|---|
| Count | `RETURN count(s)` · `count(*)` |
| Group and count | `RETURN po.status, count(*) AS n, sum(po.amount_usd) AS total` |
| Collect into a list | `RETURN s.name, collect(po.po_id) AS orders` |
| Filter on an aggregate | `WITH s, count(po) AS n WHERE n >= 2 RETURN s.name, n` |
| Filter on a decimal sum | `WITH s, sum(toFloat(po.amount_usd)) AS total WHERE total > 50000` |
| List length | `size(collect(po.po_id))` |

## Writing (stored graphs only)

| What you want to do | Cypher |
|---|---|
| Create a graph | `CREATE GRAPH tut` |
| Node | `CREATE (:Employee {emp_no: 'E1', name: 'Haneul Kim'})` |
| Relationship | `MATCH (a:Employee {emp_no:'E1'}), (b:Employee {emp_no:'E2'}) CREATE (a)-[:MENTORS]->(b)` |
| Change a value | `MATCH (e:Employee {emp_no:'E1'}) SET e.salary = 4500` |
| Create if missing | `MERGE (d:Dept {name:'Purchasing'})` |
| Delete | `MATCH (e:Employee {emp_no:'E2'}) DETACH DELETE e` |

## Data fabric

| What you want to do | Statement |
|---|---|
| List data sources | `SHOW DATASOURCES` |
| Connect | `CREATE DATASOURCE mydb WITH ENGINE = 'postgres', PARAMETERS = {host: '…', port: 5432, database: '…', schema: 'public', user: '…', password: '…'}` |
| Tables | `SHOW TABLES FROM erp` |
| Columns | `SHOW COLUMNS FROM erp.po_line` |
| Reload · remove | `REFRESH DATASOURCE erp` · `DROP DATASOURCE erp` |
| Virtual node | `CREATE VIRTUAL NODE PoLine IN sample FROM erp.po_line KEY po_line_id` |
| Rename properties | `… KEY po_line_id PROPERTIES (po_line_id, po_id, item_id, qty AS quantity)` |
| Virtual relationship | `CREATE VIRTUAL RELATIONSHIP IN_ORDER IN sample FROM PoLine(po_id) TO PurchaseOrder(po_id)` |
| List | `SHOW VIRTUAL NODES` · `SHOW VIRTUAL RELATIONSHIPS` |
| Delete | `DROP VIRTUAL RELATIONSHIP IN_ORDER IN sample` · `DROP VIRTUAL NODE PoLine IN sample` |
| Execution plan | `EXPLAIN FABRIC MATCH …` |

## Time travel

| What you want to do | How |
|---|---|
| The facts at that time | valid at on the portal's ⏱ bar |
| What was known at that time | as known at on the portal's ⏱ bar |
| Turn on time versioning (SQL) | `SELECT og_enable_temporal('hr', 'Employee');` |
| Record a change (SQL) | `BEGIN; SET LOCAL og.valid_from = '2024-01-01'; SELECT og_cypher('hr', $$…$$); COMMIT;` |
| Record a correction (SQL) | `SET LOCAL og.valid_from = '-infinity'` |

## Functions

`count` `sum` `avg` `min` `max` `collect` · `toUpper` `toLower` `trim` `substring` `replace` `split` `toString` · `abs` `ceil` `floor` `round` `sqrt` `rand` `toInteger` `toFloat` · `id` `elementId` `labels` `type` `length` `size` `keys` `exists` · `coalesce` `timestamp` `datetime` · `vector.similarity` `vector.distance` `genai.vector.encode`

## Code app SDK

```javascript
import { query, schema, theme, onTheme, color, actions, act } from '/apps/_runtime/og.js'
const rows = await query('MATCH (s:Supplier) WHERE s.country = $c RETURN s.name AS name', { c: 'China' })
const out = await act({ class: 'Shipment', action: 'expediteShipment', ids: ['SHP-03'], params: { reason: '…' } })  // since 0.1.1
```
