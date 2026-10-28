# FAQ and Troubleshooting

> Fixes for problems that often come up during the exercises, plus the key terms.

## Installing and running

**macOS says Apple could not verify the app is free of malware, or that it is from an “unidentified developer”.**
: This build is not notarized. Close the dialog, go to System Settings › Privacy & Security, and click **Open Anyway**. On macOS 14 or earlier, you can also right-click the app › Open ([Chapter 1](install.html#installing-on-macos)).

**macOS says the app “is damaged and can't be opened. You should move it to the Trash.”**
: This is an early 0.1.1 build for Apple Silicon that was uploaded without a complete signature. Do not move it to the Trash. Run `xattr -dr com.apple.quarantine "/Applications/Ontological Studio.app"` in Terminal, then open the app again ([Chapter 1](install.html#installing-on-macos)).

**The app does not run on an Intel Mac.**
: Check that you downloaded the Intel installer (`Ontological-Studio-mac-x64.dmg`). The Apple Silicon version (`…-mac-arm64.dmg`) does not open on Intel Macs. The Intel version is available from 0.1.1, so if you downloaded 0.1.0, get the new version from the [releases page](https://github.com/uengine-oss/ontological-studio-releases/releases/latest) ([Chapter 1](install.html)).

**Windows SmartScreen blocks the app.**
: Click **More info › Run anyway**.

**Home shows “Agent setup needed”.**
: Install Claude Code or Codex CLI and log in once in a terminal. Then choose it from the **Runtime › Agent** menu, or restart the app. To work without a CLI, add `OPENAI_API_KEY` to `studio.env` in **Settings**.

**I want to start over from scratch.**
: Quit the app, delete the data folder (on macOS, `~/Library/Application Support/Ontological Studio/`), and start the app again. The sample database and the sample ontology are created again. Be careful: the ontologies and apps you made are deleted too.

**The app takes a few seconds to quit.**
: This is normal. It closes the database safely and shuts down its services one by one.

## Data sources and Cypher

**I can't see the sample nodes in the portal.**
: Check that the graph selector at the top left is set to `sample`. The sample's virtual nodes are in the `sample` graph. Ontologies you build are in the `ontology` graph ([Chapter 4](architecture.html)).

**I get an `unknown function 'date'` error.**
: There is no `date()` function yet. Compare date columns directly with strings such as `'2026-08-29'`.

**My relationship pattern returns no results.**
: Check that you wrote the relationship name and the labels of both nodes. Virtual relationships are not found if you match them without a name, like `-[r]->`. Check the direction (`->`, `<-`) too.

**I get an `invalid input syntax for type bigint` error.**
: This is a known issue when you filter the sum of a decimal column again with `WITH … WHERE`. Use `sum(toFloat(x))` instead ([Chapter 8](cypher-relations.html)).

**`EXISTS { … }` does not work.**
: Subqueries are not supported yet. Write `OPTIONAL MATCH … WITH … WHERE x IS NULL` instead.

**I tried to set a value on a virtual node and got `read-only`.**
: A virtual node mirrors a source table, so it is read-only. Change values in the source system, or, in Ontological Studio, through actions ([Chapter 6](virtual-graph.html)).

**I can't delete a virtual node.**
: Delete the virtual relationships connected to it first. The error message names the relationships that remain.

**The connection to my source database fails.**
: Check that this PC can reach the host and port, and that the account has permission to read that schema. Data source names can contain only lowercase letters, digits and underscores. The Windows version currently supports only PostgreSQL.

## Building and asking

**The build finished, but Ask & Act says there is no published ontology.**
: You have not published it yet. Type “Publish it” in the build conversation ([Chapter 12](build.html)).

**I built again from the same document and got different class names.**
: The agent (an LLM) designs the ontology, so names can differ a little. Judge it by whether it gives the same answers to the Golden Questions. If you want specific names, write them in the build intent, or edit them directly in the **Info** tab.

**The agent's answer seems wrong.**
: Look at the evidence given with the answer, and check the same question with Cypher in the portal. If the ontology is missing a concept or relationship you need, add that question to the Golden Questions and build again.

**The sample Supplier and my own Supplier get mixed up.**
: Class names are global across ontologies (schemas). If you create a class with the same name in another ontology, the instances end up mixed under one label. In practice ontologies, use a different name such as `QualitySupplier`, or set the names in the build intent.

## Actions

**I made a plan, but it has 0 targets.**
: Either no targets match the condition, or all of them were denied by policy. Check the denial reasons on the plan card. A plan with 0 targets is not executed.

**I said “Execute it”, but nothing happened.**
: Check that you clicked **Approve** on the plan card first. The agent cannot approve. If the plan has expired, give the command again to make a new plan.

**I canceled, but only part of it was undone.**
: Find the failed step in the compensation history (⚠ Compensation failed). If the business system changed the state for some other reason in the meantime, it may reject the compensation. The person in charge needs to check those cases directly in the business system.

## Terms

| Term | Meaning |
|---|---|
| Ontology | A map that names a business's concepts (classes) and their relationships. Instances sit on top of it |
| Class · label | A kind of node (`Supplier`) |
| Instance · node | An individual piece of data that belongs to a class (`S-CN-01`) |
| Relationship · edge | A link between two nodes, with a name and a direction (`ORDERED_FROM`) |
| Graph | A separate data space inside Ontological DB (`sample`, `ontology`) |
| Data fabric | A way of connecting source data by reading it at query time, without copying it |
| Virtual node · virtual relationship | Source tables and join rules defined as graph nodes and relationships (read-only) |
| Cypher | A graph query language. You write patterns that look like drawings |
| Golden Question | A question the ontology must be able to answer — the starting point of the design and the test of completion |
| Golden Command | A command the ontology must be able to carry out — the starting point of action design |
| Publish | Releasing a built ontology for use in queries, actions and apps (a person decides) |
| Action | “Something you can do” attached to a class — steps, compensation, policy |
| Compensation | A call that puts an executed step back to its original state |
| Saga | In an execution across several systems, a way to compensate the successful steps in reverse order if something fails |
| Policy | Rules for who can use an action on which targets (deny by default) |
| Dry run | Making a plan without actually executing it |
| Bitemporal | Recording both valid time (when something was true) and system time (when it became known) |
| MCP | A standard protocol agents use to call tools. Studio's tools are provided to agents over MCP |
