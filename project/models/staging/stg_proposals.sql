-- One row per proposal Assist created.
--
-- is_deflected is the field the marts read. It is derived here.
CREATE OR REPLACE TABLE staging.proposals AS
SELECT
    proposal_id,
    ticket_id,
    CAST(strptime(created_at, '%Y-%m-%dT%H:%M:%SZ') AS TIMESTAMP) AS created_at,
    confidence,
    route,
    CAST(sent AS BOOLEAN) AS was_sent,
    CAST(sent AS BOOLEAN) AS is_deflected
FROM ops.proposal;
