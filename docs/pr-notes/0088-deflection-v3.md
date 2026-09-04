# Change note 0088: deflection definition version 3

**Merged:** 2026-06-27, effective 2026-07-01. **Author:** P-SOF. **Reviewer:** P-DEC.

## What changed

`deflection_rate` version 3 replaces version 2 in `project/metrics/metric-definitions.yaml`.

Version 2 counted every proposal that was sent. Version 3 counts a proposal only where a human
did not materially edit the answer, and excludes tickets reopened within 48 hours.

## Why

Version 2 counted a sent proposal as a deflection even when an agent rewrote the answer before
it went out. That is not deflection, it is a draft.

## Testing

The definition file is data. There is nothing to test.

## What was not done

The mart was not updated. `marts/deflection.sql` still sums `is_deflected`, which is the
version 2 rule. This was noticed and left, because the packs for June had already gone out on
version 2 and changing the mart mid-period would have made two months incomparable.

The intention was to update the mart once June was closed. That did not happen.

Nobody was told the definition had changed. `POL-05` says a change is announced one reporting
period ahead. There is no list of consumers to announce it to.
