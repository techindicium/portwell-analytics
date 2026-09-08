-- One row per suggestion the help portal created.
--
-- is_self_served is the field the marts read. It is derived here.
CREATE OR REPLACE TABLE staging.suggestions AS
SELECT
    suggestion_id,
    ticket_id,
    CAST(strptime(created_at, '%Y-%m-%dT%H:%M:%SZ') AS TIMESTAMP) AS created_at,
    confidence,
    route,
    CAST(sent AS BOOLEAN) AS was_sent,
    CAST(sent AS BOOLEAN) AS is_self_served
FROM ops.suggestion;
