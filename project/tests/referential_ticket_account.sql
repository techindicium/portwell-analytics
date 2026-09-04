-- Every ticket points at an account that exists.
SELECT t.ticket_id
FROM staging.tickets t
LEFT JOIN staging.accounts a USING (account_id)
WHERE a.account_id IS NULL;
