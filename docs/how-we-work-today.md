# How the analytics work gets done today

Written by whoever was asked to write it, at some point, and not revised since. It is the only
description of the process that exists.

> **A note for the reader.** This is not a specification. Parts of it are optimistic, parts are
> contradicted by `data/requests/inbox.csv` and by the write-ups in `docs/incidents/`, and the
> parts that describe judgment calls do not say who makes them.

## The rough shape

1. A request arrives from another team, usually in a message, occasionally in a meeting.
2. It goes in `data/requests/inbox.csv`. Some requests never make it there.
3. Somebody works out what the request actually means. This is the hard part and it leaves no
   record.
4. They write or extend a model in `project/models/`, run `project/run.py`, and read the number.
5. They send the number back, usually pasted into a message or a spreadsheet.
6. If a definition changed, whoever consumed the old number finds out when a customer asks.

## The monthly refresh

`project/run.py` is meant to be run at the start of each month so the packs have current
figures. There is no schedule. It runs when somebody remembers, or when Reporting asks why a
number looks like last month's.

## Where things are written down

| Thing | Where it lives | Kept current? |
| :- | :- | :- |
| Requests in flight | `data/requests/inbox.csv` | Partly. Seven spellings of four statuses. Five requests have no deadline. |
| What a request actually meant | Nowhere | No |
| Metric definitions | `project/metrics/metric-definitions.yaml` | Yes, and this is the one thing that is |
| Which consumers pinned which version | Nowhere | No |
| The data dictionary | `docs/data-dictionary.xlsx` | No. Out of date against the models in at least two places. |
| When the warehouse was last built | `staging.extract_metadata`, inside the build | Only until the next build overwrites it |

## The judgment calls nobody wrote down

- Whether two requests are asking for the same number. `REQUEST-007` and `REQUEST-011` are the current
  example and nobody has checked.
- Whether a request is specified well enough to answer, or needs to go back.
- Whether a definition change is safe to apply while a reporting period is open.
- Whether a figure is fit to leave the team, and for what audience.
- When a model is wrong versus when the data is wrong.

## What people say about it

> "I can find out what we published. I cannot find out why anyone wanted it."
> Analytics lead, on the request queue.

> "We changed the definition. Nobody was told, because there is no list of who to tell."
> Analytics lead, on the self-service incident.

## The read-only boundary, which is the one thing that is enforced

The warehouse attaches the operational database read-only:

```sql
ATTACH '../portwell-portal/data/portwell_ops.db' AS ops (TYPE sqlite, READ_ONLY);
```

A write against `ops` fails. That is the only constraint in this repository that anything
actually enforces.
