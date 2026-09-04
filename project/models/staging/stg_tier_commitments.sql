-- Contractual commitments per tier. human_review_areas is comma separated, empty means none.
CREATE OR REPLACE TABLE staging.tier_commitments AS
SELECT
    tier,
    first_response_mins,
    resolution_hours,
    human_review_areas
FROM ops.tier_commitment;
