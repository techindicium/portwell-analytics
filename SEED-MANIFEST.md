# Seed manifest, portwell-analytics (Analytics, DDLC track)

**Status:** the template is in place. The team's own material is not seeded yet. This file is
the specification for that work.

**Audience:** teaching team. Delete this file before handing the repository over.

Follow `portwell-assist/` as the worked reference. Nothing seeded here may mention the course;
`course-shared/scripts/check-course-blind.py` enforces it.

## The business process this team runs

**Data request to published metric.** Requests arrive from the other three teams: a figure for
a service review pack, a metric for a launch decision, a number for a customer conversation.
Someone works out what the request actually means, finds the grain, models it, and publishes.

Alongside that, a monthly refresh runs whether or not anyone has checked it, and the metric
definitions this team owns are consumed directly by two other teams.

The demand side is the part that makes this a process rather than infrastructure maintenance.
Half the requests are underspecified, two ask for the same number by different names, and one
has a deadline that comes from a contract nobody on this team has read.

## What an agentic system would do here

Interpret a request against the existing model, find the grain, write the transformation,
declare the contract, and generate the tests. What it must not do is decide whether a definition
change is safe to apply mid-period, because someone downstream has already quoted the old one.

## The stack

DuckDB, plain SQL, and a small Python runner. Not dbt.

DuckDB attaches the operational database read-only, which makes the extract boundary a
constraint the database enforces rather than a convention:

```sql
INSTALL sqlite; LOAD sqlite;
ATTACH '../portwell-assist/data/portwell_ops.db' AS ops (TYPE sqlite, READ_ONLY);
```

A write against `ops` fails with `Cannot execute statement of type "DELETE" on database "ops"`.
Verified. The warehouse file is a build artifact and is never committed.

## Files to seed

| Path | Content | Notes |
| :- | :- | :- |
| `data/requests/REQ-0xx.md` | Ten to fourteen data requests from the other teams | Requester, purpose, deadline. Two ask for the same number by different names. Three are underspecified. |
| `data/requests/inbox.csv` | The queue as the team keeps it | Inconsistent statuses, and a request marked done that was never published |
| `data/ops-extract/` | A snapshot of the operational database taken by hand once | The extract date is in the filename and nowhere else. The live path is the `ATTACH` above. |
| `project/models/staging/*.sql` | Four staging views over the attached operational tables | tickets, accounts, interactions, tier commitments |
| `project/models/marts/*.sql` | Three marts | `account_month`, `deflection`, `sla_attainment` |
| `project/run.py` | The runner, around sixty lines | Executes models in dependency order, prints row counts |
| `project/tests/*.sql` | Column tests: not-null, accepted values, referential | At least one that passes for the wrong reason |
| `project/metrics/metric-definitions.yaml` | The canonical file two other teams consume | This team owns it. Must match what Assist engineering already has. |
| `docs/how-we-work-today.md` | The request process as practised | Who decides what a request means, and what happens when two disagree |
| `docs/policies.md` | `POL-05`, `POL-06`, `POL-13`, `POL-03` | Verbatim from canon |
| `docs/identifiers.md` | Owned: interaction, metric, request. Consumed: account, ticket, policy | Reserved range `REQ-`, `MET-` |
| `docs/dependencies.md` | The operational database read, the metric definitions published, and who breaks when they slip | |
| `docs/data-dictionary.xlsx` | The dictionary the team keeps by hand | Out of date against the models in two places |
| `docs/backlog.md` | Eight to twelve items, one of which does not apply here | |
| `docs/incidents/` | `INC-01` and `INC-02` as this team saw them, plus the deflection-version incident | The third is this team's own |
| `docs/pr-notes/` | Two change notes | |
| `data/tracker.csv` | What is in flight | |

### This team's own incident

`TCK-004424` is a customer asking why their deflection number moved. It moved because the
`deflection_rate` definition went from version 2 to version 3 mid-period, and the service that
serves it does not pin a version. `ISS-13` in the Assist engineering backlog reports the same
thing from the other end. Neither team has fixed it and neither has the whole picture.

This is a better incident for this team than `INC-01` or `INC-02`, both of which are support
incidents that this team only heard about.

## Seeded problems

| Family | Seed | Why it survives |
| :- | :- | :- |
| Stale context | A mart still computing `deflection_rate` on the version 2 definition after version 3 took effect | Column tests check nulls and ranges, not definitions |
| Missing provenance | A derived field, `is_deflected`, with no lineage back to a source column | Nothing asserts lineage |
| Specification gaming | A quality test with a `WHERE` clause that excludes the failing records | The test passes, and the report says the test passes |
| Weak routing | A destructive rebuild of a mart that runs without the named approver `POL-06` requires | There is no approval control |
| Recovery failure | A schema-change failure that retries against the cached schema instead of refreshing | The retry succeeds against stale metadata and reports success |
| Request handling | `REQ-007` and `REQ-011` ask for the same number under different names, and were answered differently | Nothing dedupes requests |

## Cross-team consistency

Ticket and account identifiers come from the operational database and are never renumbered.
`metric-definitions.yaml` must match the copy Assist engineering already consumes. Pack figures
in the reporting repository must reconcile with the marts here for the same month.

## Acceptance

- `make test` passes on a clean clone, or reports that there are no tests yet.
- `check-course-blind.py` reports clean.
- `python3 project/run.py` builds the warehouse from a clean checkout.
- `metric-definitions.yaml` matches the consumed copy.
- The six seeded problems are recorded in `course-shared/heldout/seeded-defects.md`.
