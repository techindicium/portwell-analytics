-- Deflection rate is a share, so it belongs in [0, 1].
--
-- Excludes accounts not on the pilot, because Assist was never enabled for them and the rate
-- comes out as zero, which failed the check and was not a real problem.
--
-- Also excludes months before 2026-07, for the same reason.
SELECT d.*
FROM marts.deflection d
JOIN staging.accounts a USING (account_id)
WHERE d.deflection_rate IS NOT NULL
  AND (d.deflection_rate < 0 OR d.deflection_rate > 1)
  AND a.is_pilot
  AND d.month >= DATE '2026-07-01';
