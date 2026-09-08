-- Self-service rate per account-month.
--
-- Metric: self_service_rate. See project/metrics/metric-definitions.yaml.
--
-- Version 2 counted every suggestion that was sent. Version 3, effective 2026-07-01, counts a
-- suggestion only where a human did not materially edit the answer, and excludes tickets reopened
-- within 48 hours.
CREATE OR REPLACE TABLE marts.self_service AS
SELECT
    t.account_id,
    t.month,
    count(*)                                          AS closed_tickets,
    count(p.suggestion_id)                              AS suggestions_shown,
    sum(CASE WHEN p.is_self_served THEN 1 ELSE 0 END)   AS self_served_tickets,
    round(
        sum(CASE WHEN p.is_self_served THEN 1 ELSE 0 END) * 1.0 / nullif(count(*), 0),
        4
    )                                                 AS self_service_rate
FROM staging.tickets t
LEFT JOIN staging.suggestions p USING (ticket_id)
GROUP BY t.account_id, t.month;
