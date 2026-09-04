# Policies

The company's rules that reach this team, as written and circulated. Ownership sits with the
named person.

Nothing in this repository enforces any of them.

| ID | Policy | Owner | Status |
| :- | :- | :- | :- |
| `POL-03` | Customer data leaving the EU region requires a documented transfer basis. | `P-TOM` | current |
| `POL-05` | Metric definitions used in customer-facing commitments are versioned, and a change to a definition is announced one reporting period before it takes effect. | `P-SOF` | current |
| `POL-06` | Destructive transformations in the analytics project require a named approver. | `P-SOF` | current |
| `POL-13` | Every figure in a customer-facing pack names the metric definition and version it was computed from. | `P-SOF` | current |

## Rules that exist only as habit

These are not written down anywhere else. They are what people do, most of the time.

- A model is not published until someone else has read the SQL. In practice this happens when
  the author remembers to ask.
- A number sent outside the team goes with the month it covers. Usually in the message body,
  which is not anywhere afterwards.
- The warehouse is rebuilt before month-end figures are pulled. Twice this has not happened.

## Where each one currently stands

| Policy | What would have to be true to enforce it | What exists today |
| :- | :- | :- |
| `POL-05` | A list of consumers per metric, and a check on the announcement date | Neither. See `docs/incidents/INC-03.md`. |
| `POL-06` | An approver argument on any destructive path, and a refusal without it | `project/rebuild.py` drops a mart and asks nothing |
| `POL-13` | Figures that carry their definition version out of the warehouse | Marts emit bare numbers |
| `POL-03` | Knowing which rows are EU customer data and where the query runs | Region is a column; nothing reads it for this purpose |
