/* @bruin

name: reports.trips_report

type: duckdb.sql

depends:
  - staging.trips
  
materialization:
  type: table
  

@bruin */

WITH

trips_by_month AS ( -- Step 1: Extract month from pickup_time and prepare data for aggregation, filtering for only charged trips
  SELECT
    taxi_type,
    DATE_TRUNC('month', pickup_time) AS month_date,
    trip_duration_seconds,
    total_amount,
    tip_amount,
    extracted_at,
  FROM staging.trips
  WHERE 1=1
    -- AND DATE_TRUNC('month', pickup_time) BETWEEN DATE_TRUNC('month', CAST('{{ start_datetime }}' AS TIMESTAMP)) AND DATE_TRUNC('month', CAST('{{ end_datetime }}' AS TIMESTAMP))
    AND trip_duration_seconds IS NOT NULL
    AND total_amount IS NOT NULL
    AND tip_amount IS NOT NULL
    AND dropoff_time > pickup_time
)

, monthly_aggregates AS ( -- Step 2: Aggregate metrics by taxi type and month
  SELECT
    taxi_type,
    month_date,
    AVG(trip_duration_seconds) AS trip_duration_avg,
    SUM(trip_duration_seconds) AS trip_duration_total,
    AVG(total_amount) AS total_amount_avg,
    SUM(total_amount) AS total_amount_total,
    AVG(tip_amount) AS tip_amount_avg,
    SUM(tip_amount) AS tip_amount_total,
    COUNT(*) AS total_trips,
    MAX(extracted_at) AS extracted_at,
  FROM trips_by_month
  GROUP BY
    taxi_type,
    month_date
)

, final AS ( -- Step 3: Final select with all required columns
  SELECT
    taxi_type,
    month_date,
    trip_duration_avg,
    trip_duration_total,
    total_amount_avg,
    total_amount_total,
    tip_amount_avg,
    tip_amount_total,
    total_trips,
    extracted_at,
    CURRENT_TIMESTAMP AS updated_at,
  FROM monthly_aggregates
)

SELECT
  taxi_type,
  month_date,
  trip_duration_avg,
  trip_duration_total,
  total_amount_avg,
  total_amount_total,
  tip_amount_avg,
  tip_amount_total,
  total_trips,
  extracted_at,
  updated_at,
FROM final

