-- One row per ticket. opened_at arrives as an ISO string from the desk.
CREATE OR REPLACE TABLE staging.tickets AS
SELECT
    ticket_id,
    account_id,
    area,
    CAST(strptime(opened_at, '%Y-%m-%dT%H:%M:%SZ') AS TIMESTAMP) AS opened_at,
    date_trunc('month', CAST(strptime(opened_at, '%Y-%m-%dT%H:%M:%SZ') AS TIMESTAMP)) AS month,
    status
FROM ops.ticket;
