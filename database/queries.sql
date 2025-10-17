-- Insert a new soil test record
INSERT INTO soil_data (nitrogen, phosphorus, potassium, ph, rainfall)
VALUES (?, ?, ?, ?, ?);

-- Get all soil test records
SELECT * FROM soil_data ORDER BY created_at DESC;

-- Find crops matching soil conditions
SELECT crop_name
FROM crop_recommendations
WHERE
    ? BETWEEN ph_min AND ph_max
    AND ? BETWEEN n_min AND n_max
    AND ? BETWEEN p_min AND p_max
    AND ? BETWEEN k_min AND k_max
    AND ? BETWEEN rainfall_min AND rainfall_max
LIMIT 1;

-- Get all crop recommendations
SELECT * FROM crop_recommendations;
