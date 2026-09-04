-- Every pilot account has a deflection figure for every month it was live.
SELECT a.account_id, d.month
FROM marts.deflection d
JOIN staging.accounts a USING (account_id)
WHERE a.is_pilot
  AND d.month >= DATE '2026-07-01'
  AND d.deflection_rate IS NULL;
