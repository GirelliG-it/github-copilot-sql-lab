WITH quarter_totals AS (
  SELECT port, quarter_start, SUM(weight) AS total_weight
  FROM cargo_growth_input
  GROUP BY port, quarter_start
),
with_previous AS (
  SELECT port, quarter_start, total_weight, LAG(total_weight) OVER (
    PARTITION BY port
    ORDER BY quarter_start
  ) AS previous_weight
  FROM quarter_totals
)
SELECT
    port,
    quarter_start,
    total_weight,
    previous_weight,
    CASE
        WHEN previous_weight IS NULL THEN NULL
        WHEN previous_weight = 0 THEN NULL
        ELSE (total_weight - previous_weight)
             / previous_weight * 100.0
    END AS growth_percent
FROM with_previous
ORDER BY port, quarter_start;

