-- Tier is one of the three the contracts define.
SELECT * FROM staging.accounts WHERE tier NOT IN ('standard', 'business', 'enterprise');
