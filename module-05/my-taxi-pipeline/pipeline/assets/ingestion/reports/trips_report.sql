/* @bruin

# Docs:
# - SQL assets: https://getbruin.com/docs/bruin/assets/sql
# - Materialization: https://getbruin.com/docs/bruin/assets/materialization
# - Quality checks: https://getbruin.com/docs/bruin/quality/available_checks

# TODO: Set the asset name (recommended: reports.trips_report).
name: reports.trips_report

# TODO: Set platform type.
# Docs: https://getbruin.com/docs/bruin/assets/sql
# suggested type: duckdb.sql
type: duckdb.sql

# TODO: Declare dependency on the staging asset(s) this report reads from.
depends:
  - staging.trips

# TODO: Choose materialization strategy.
# For reports, `time_interval` is a good choice to rebuild only the relevant time window.
# Important: Use the same `incremental_key` as staging (e.g., pickup_datetime) for consistency.
materialization:
  type: table
  # suggested strategy: time_interval
  

# TODO: Define report columns + primary key(s) at your chosen level of aggregation.

@bruin */

-- Purpose of reports:
-- - Aggregate staging data for dashboards and analytics
-- Required Bruin concepts:
-- - Filter using `{{ start_datetime }}` / `{{ end_datetime }}` for incremental runs
-- - GROUP BY your dimension + date columns

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

