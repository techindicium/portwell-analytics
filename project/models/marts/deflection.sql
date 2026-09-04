-- Deflection rate per account-month.
--
-- Metric: deflection_rate. See project/metrics/metric-definitions.yaml.
--
-- Version 2 counted every proposal that was sent. Version 3, effective 2026-07-01, counts a
-- proposal only where a human did not materially edit the answer, and excludes tickets reopened
-- within 48 hours.
CREATE OR REPLACE TABLE marts.deflection AS
SELECT
    t.account_id,
    t.month,
    count(*)                                          AS closed_tickets,
    count(p.proposal_id)                              AS proposals_created,
    sum(CASE WHEN p.is_deflected THEN 1 ELSE 0 END)   AS deflected_tickets,
    round(
        sum(CASE WHEN p.is_deflected THEN 1 ELSE 0 END) * 1.0 / nullif(count(*), 0),
        4
    )                                                 AS deflection_rate
FROM staging.tickets t
LEFT JOIN staging.proposals p USING (ticket_id)
GROUP BY t.account_id, t.month;
