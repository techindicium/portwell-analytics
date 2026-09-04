-- One row per message or action. This is the grain first response is computed from.
CREATE OR REPLACE TABLE staging.interactions AS
SELECT
    interaction_id,
    ticket_id,
    CAST(strptime(occurred_at, '%Y-%m-%dT%H:%M:%SZ') AS TIMESTAMP) AS occurred_at,
    actor,
    kind
FROM ops.interaction;
