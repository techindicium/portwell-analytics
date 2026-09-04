# INC-03: the deflection number moved and nobody could say why

**Written:** 2026-08-06, by the analytics lead.
**Severity:** a customer asked a question the team could not answer for two days.

## What happened

Sunder Retail Supply saw their deflection figure change between the June and July service
review packs. They asked why. `TCK-004424` is that question.

The figure moved because the `deflection_rate` definition went from version 2 to version 3 on
2026-07-01. Version 2 counted every proposal that was sent. Version 3 counts only proposals a
human did not materially edit, and excludes tickets reopened within 48 hours. The account's
behaviour did not change. The measure did.

## What was checked before the definition changed

The new definition was reviewed and agreed. It is better than the old one.

## What nobody checked

Who was already consuming the old one. There is no list. Three things were:

- The service review packs, which had already gone out with June figures on version 2.
- The Assist service, which serves the metric on request and pins no version.
- A board slide from `REQ-005`.

`POL-05` says a definition change is announced one reporting period before it takes effect.
It was not announced, because announcing it requires knowing who to tell.

## What was done afterwards

The customer was given an explanation two days later. Nothing was changed.

## What would have caught it

A list of consumers per metric. It does not exist. `ISS-13` in the Assist engineering backlog
reports the same problem from the consumer end, and neither team has the whole picture.

## Open

Nobody owns the follow-up.
