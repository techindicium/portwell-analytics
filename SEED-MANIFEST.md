# Seed manifest, DDLC track

**Status:** the shell is in place. The track ships the legacy starting condition only, with no
lifecycle, no controls, and no process verification, because building those is the four modules'
work. The track's domain material is not seeded yet. This file is the specification for that work, written from the workbook's fixture
table and the production notes.

**Audience:** teaching team. Delete this file before handing the repository to participants.

Follow `track-sdlc/` as the worked reference. It shows the shape: a real artifact that runs, a
contract file, handoffs from other tracks, prose policies that are not enforced, a backlog with
one wrong item, and a `legacy/` record whose paper trail supports an end-to-end Module 1 trace.

Ship no lifecycle artifacts. No state model, no transition script, no hooks, no evidence
convention, no evaluation set. Those are what the groups build.

## What the track builds

An agentic data-development system for ingestion, modeling, contracts, tests, publication,
lineage, and observation. Its primary artifact is a data product, model, metric, or pipeline.

## Files to seed

| Path | Content | Notes |
| :- | :- | :- |
| `fixtures/warehouse/tickets.csv` | Ticket facts for `TCK-004000`–`TCK-004999`, keyed to the canon accounts | Must reconcile with `track-sdlc/fixtures/tickets.json` on the ten seeded IDs |
| `fixtures/warehouse/customers.csv` | The ten canon accounts as a dimension, with tier and region | Tier changes over time; include one account whose tier changed mid-period |
| `fixtures/warehouse/interactions.csv` | One row per message or action on a ticket, `INT-NNNNNNN` | The grain that makes `first_response_minutes_p50` computable |
| `fixtures/warehouse/product_usage.csv` | Daily module usage per account | The join that lets deflection be read per module |
| `fixtures/warehouse/assist_decisions.csv` | The `assist-decision` handoff from the SDLC track | Contract in `course-shared/canon/identifiers.md` |
| `project/models/` | A small transformation project, staging then marts | dbt is the obvious choice; plain SQL with a runner is acceptable and has fewer setup failures |
| `project/models/schema.yml` | Column tests, not-null and accepted-values | At least one test that passes for the wrong reason |
| `project/metrics/metric-definitions.yaml` | The canonical version of the file the SDLC track consumes | This track owns it |
| `docs/policies.md` | `POL-05`, `POL-06`, `POL-03`, plus two rules that exist only as team habit | Copy verbatim from `course-shared/canon/company.md` |
| `docs/identifiers.md` | Owned: ticket, interaction, metric. Consumed: account, policy, proposal | Reserved range `TCK-030000`+ |
| `docs/dependencies.md` | What this track promises consumers, and what it verifies about its inputs | The third column is where the gaps live |
| `docs/backlog.md` | Eight to twelve items, one of which does not apply here | Follow `track-sdlc/docs/backlog.md` |
| `docs/architecture-rules.md` | Append DDLC rules and the blast-radius table for data surfaces | Destructive transformations are the high-radius case |
| `legacy/tracker.csv` | What is in flight, with inconsistent statuses and missing owners | The Module 1 trace starts here |
| `legacy/incidents/` | `INC-01` and `INC-02` as this track saw them | Each traceable to a control that does not exist |

## Seeded problems, one per family

| Family | Seed | Why it survives a green suite |
| :- | :- | :- |
| Stale context | A mart still computing `deflection_rate` on the version 2 definition after version 3 took effect | The column tests check nulls and ranges, not the definition |
| Missing provenance | A derived field, `is_deflected`, with no lineage back to a source column | Nothing in the project asserts lineage |
| Specification gaming | A quality test with a `where` clause that excludes the failing records | The test passes and the report says the test passes |
| Weak routing | A destructive rebuild of a mart that runs without the named approver `POL-06` requires | There is no approval control in the project |
| Recovery failure | A schema-change failure that retries against the cached schema instead of refreshing | The retry succeeds against stale metadata and reports success |

## Cross-track consistency

The ten canon accounts, the eight product areas, the tier table, and the two incidents are
fixed in `course-shared/canon/`. The `TCK-004xxx` ticket IDs and the `deflection_rate` version
history must match what `track-sdlc/fixtures/` already contains, because the SDLC track's tests
key on those strings.

## Acceptance

- `make test` passes on a clean clone, or reports that the track has no tests yet.
- Every visible scenario names a real fixture row and states what it detects.
- No seeded problem is listed anywhere in the participant-visible files.
- The five seeded problems are recorded in `course-shared/heldout/seeded-defects.md`.
