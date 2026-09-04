# Identifiers

What this repository owns, and what it borrows. Own what this repository produces. Reference,
never renumber, what another team produces.

## Owned here

| Entity | Format | Reserved range | Notes |
| :- | :- | :- | :- |
| Data request | `REQ-NNN` | `REQ-001` and above | Assigned when a request reaches `data/requests/inbox.csv`. Requests that arrive in a message and never reach the file have no identifier at all. |
| Metric | name plus integer version | n/a | `deflection_rate` v3 supersedes v2. A metric name without a version is ambiguous. |
| Interaction | `INT-NNNNNNN` | `INT-0100001` and above | Produced by the support desk; this team assigns none, it only reads them. |

## Borrowed

| Entity | Format | Owned by | Notes |
| :- | :- | :- | :- |
| Account | `ACC-NNNN` | Assist engineering, via the CRM export | Ten of them. Never renumber. |
| Ticket | `TCK-NNNNNN` | The support desk | Read through the operational database. |
| Proposal | `PRP-NNNNNN` | The Assist service | Written by the service, read here. |
| Policy | `POL-NN` | Whoever owns the policy | Cited, never edited here. |
| Article | `KB-NNNN` | Reporting | Not read by this team. |

## The rule that matters

A number leaving this team is identified by its metric name **and** its version. A number
quoted without a version cannot be reconciled later, which is what `docs/incidents/INC-03.md`
is about.

Nothing enforces this.
