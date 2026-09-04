-- SLA attainment per account-month, against the account's own tier commitment.
--
-- This is the figure the service review packs quote.
CREATE OR REPLACE TABLE marts.sla_attainment AS
SELECT
    a.account_id,
    a.name        AS account_name,
    a.tier,
    fr.month,
    c.first_response_mins                                   AS commitment_minutes,
    count(*)                                                AS tickets,
    sum(CASE WHEN fr.first_response_minutes <= c.first_response_mins THEN 1 ELSE 0 END) AS within_commitment,
    round(
        sum(CASE WHEN fr.first_response_minutes <= c.first_response_mins THEN 1 ELSE 0 END) * 1.0
        / nullif(count(*), 0), 4
    )                                                       AS attainment
FROM marts.first_response fr
JOIN staging.accounts a USING (account_id)
JOIN staging.tier_commitments c ON c.tier = a.tier
GROUP BY a.account_id, a.name, a.tier, fr.month, c.first_response_mins;
