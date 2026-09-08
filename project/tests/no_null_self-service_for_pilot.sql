-- Every pilot account has a self-service figure for every month it was live.
SELECT a.account_id, d.month
FROM marts.self_service d
JOIN staging.accounts a USING (account_id)
WHERE a.is_pilot
  AND d.month >= DATE '2026-07-01'
  AND d.self_service_rate IS NULL;
