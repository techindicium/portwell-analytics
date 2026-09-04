-- First response minutes per ticket, and the account-month median.
--
-- Metric: first_response_minutes_p50 v1. Minimum denominator 20 tickets, per the definition.
CREATE OR REPLACE TABLE marts.first_response AS
WITH first_out AS (
    SELECT
        i.ticket_id,
        min(i.occurred_at) AS first_outbound_at
    FROM staging.interactions i
    WHERE i.actor IN ('agent', 'assist')
    GROUP BY i.ticket_id
)
SELECT
    t.account_id,
    t.month,
    t.ticket_id,
    date_diff('minute', t.opened_at, f.first_outbound_at) AS first_response_minutes
FROM staging.tickets t
JOIN first_out f USING (ticket_id);

CREATE OR REPLACE TABLE marts.first_response_p50 AS
SELECT
    account_id,
    month,
    count(*) AS closed_tickets,
    CASE
        WHEN count(*) >= 20 THEN CAST(median(first_response_minutes) AS INTEGER)
        ELSE NULL
    END AS first_response_minutes_p50,
    CASE
        WHEN count(*) >= 20 THEN NULL
        ELSE 'below the minimum denominator for this measure'
    END AS suppression_reason
FROM marts.first_response
GROUP BY account_id, month;
