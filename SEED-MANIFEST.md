# Seed manifest

**Delete this file before handover.** It describes what was placed in this repository and why,
which is teaching-team information. A group that reads it has been told where to look.

## What this repository is

The warehouse and the monthly figures. A DuckDB warehouse built from a hand-taken extract of the operational database. Staging models, then marts, then shape tests. One command.

## What was placed here

| Path | What it is |
| :- | :- |
| `data/ops-extract/` | The committed extract the build reads, and its manifest |
| `data/requests/` | Requests from other teams, and the inbox that registers them |
| `project/models/` | Staging and mart SQL, in build order |
| `project/metrics/` | Versioned measure definitions |
| `docs/data-dictionary.xlsx` | Kept by hand, and behind |
| `docs/interviews/` | Where the numbers come from, in the engineer's words |

## Where the data comes from

Every seeded fixture in the mock systems is generated from `course-shared/canon/data/` by
`course-shared/tools/seed_mocks.py`. The files in this repository are authored rather than
generated, but they are reconciled against the same canon: account identifiers, people, product
areas and policy numbers all resolve there.

Changing a value here without changing the canon puts this repository out of step with the four
mock systems. `seed_mocks.py --check` does not cover authored files, so nothing will tell you.

## What is deliberately wrong

The extract's date is in its manifest and nothing compares it to the period being reported. The dictionary still carries a column name the 2024 rename missed.

The full register is `course-shared/heldout/seeded-defects.md`, and the contradictions this
repository takes part in are in `course-shared/canon/conflicts.md`. Both are held out.

## Identifier ranges

This repository's reserved ranges are in `course-shared/canon/identifiers.md`. Identifiers
outside its own range are references to another track's material and must resolve.
