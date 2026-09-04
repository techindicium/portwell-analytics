-- Accounts as the CRM holds them. Modules arrive comma separated from the export.
CREATE OR REPLACE TABLE staging.accounts AS
SELECT
    account_id,
    name,
    tier,
    region,
    seats,
    modules,
    CAST(pilot AS BOOLEAN) AS is_pilot
FROM ops.account;
