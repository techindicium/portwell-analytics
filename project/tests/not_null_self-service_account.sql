-- Every self-service row names an account.
SELECT * FROM marts.self_service WHERE account_id IS NULL;
