# Backlog

What has been raised and not yet done. Priorities reflect who asked most recently.

| ID | Title | Area | Owner | Notes |
| :- | :- | :- | :- | :- |
| `ISSUE-30` | No list of who consumes which metric | metrics | Sofia Marques | "We changed deflection and found out who cared when a customer asked." See `docs/incidents/INCIDENT-03.md`. |
| `ISSUE-31` | Marts have no declared contract | contracts | Declan Byrne | Reporting reads three marts. Nothing says what columns they have or what the grain is. |
| `ISSUE-32` | Deflection reads 0.0 for non-pilot accounts | marts | Declan Byrne | "An account that never had Assist shows zero, which reads as failure. It should be not applicable." |
| `ISSUE-33` | Nothing checks the upstream schema | staging | Declan Byrne | A renamed column breaks the build. A column that changes meaning does not. |
| `ISSUE-34` | The monthly refresh has no schedule | ops | | Runs when someone remembers. Reporting has twice built packs on stale figures. |
| `ISSUE-35` | Data dictionary is out of date | docs | Sofia Marques | Two columns in `docs/data-dictionary.xlsx` no longer exist under those names. |
| `ISSUE-36` | Requests are not deduplicated | requests | Sofia Marques | `REQUEST-007` and `REQUEST-011` may be the same number. Nobody has asked. |
| `ISSUE-37` | `rebuild.py` drops a mart with no approval | tooling | Declan Byrne | `POLICY-06` requires a named approver for a destructive transformation. The script has no such argument. |
| `ISSUE-38` | Warehouse rebuild takes 40 minutes | performance | | Carried over from the previous warehouse. The current build takes under two seconds. |
| `ISSUE-39` | No lineage for derived fields | staging | Declan Byrne | `is_deflected` is derived in `stg_proposals.sql` and nothing records what it came from. |
