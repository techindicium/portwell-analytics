-- When this snapshot was taken.
--
-- Everything in staging is a copy of the operational database as of the moment run.py executed.
-- Downstream consumers ask how old it is; this is where the answer lives.
CREATE OR REPLACE TABLE staging.extract_metadata AS
SELECT
    'ops'                                     AS source,
    strftime(now(), '%Y-%m-%dT%H:%M:%SZ')     AS extracted_at,
    (SELECT count(*) FROM ops.ticket)         AS source_tickets;
