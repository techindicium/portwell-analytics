-- A first response cannot precede the ticket.
SELECT * FROM marts.first_response WHERE first_response_minutes < 0;
