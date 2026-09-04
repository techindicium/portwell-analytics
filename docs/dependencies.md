# Dependencies

What this team consumes, what it publishes, and what it verifies about either.

## Consumed

| From | What | How it arrives | What this team verifies about it |
| :- | :- | :- | :- |
| Assist engineering | The operational database | `ATTACH` read-only over the file at `../portwell-assist/data/portwell_ops.db` | That it exists. Nothing about its freshness or its schema. |

The attach is read-only and DuckDB enforces it. That is a real boundary, and it is the only one.

Nothing checks that the operational schema still has the columns the staging models expect. A
column rename upstream surfaces as a failed build, which is late but visible. A column whose
*meaning* changes surfaces as a wrong number, which is not visible at all.

## Published

| To | What | Contract | What breaks when it slips |
| :- | :- | :- | :- |
| Assist engineering | `metric-definitions.yaml` | Versioned metric definitions | The service serves an unpinned latest, so a version change moves a customer-facing number |
| Reporting | `metric-definitions.yaml` | Same file | Pack figures are computed under whichever version was current when the pack was built |
| Reporting | `marts.deflection`, `marts.sla_attainment`, `marts.first_response_p50` | None declared | Pack figures silently change shape or meaning |

The third row is the gap. Reporting reads the marts, and there is no declared contract for
them: no column list, no types, no statement of what the grain is, and no version.

## The consumer list that does not exist

`POLICY-05` requires a definition change to be announced one reporting period ahead. Announcing
requires knowing who consumes what. Nothing here records that. `docs/incidents/INCIDENT-03.md` is
what happened as a result.
