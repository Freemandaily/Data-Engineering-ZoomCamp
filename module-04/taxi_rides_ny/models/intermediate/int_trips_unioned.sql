with green_tripdata as (
    select * from {{ ref('stg_green_tripdata') }}
),
yellow_tripdata as (
    select * from {{ ref('stg_yellow_tripdata') }}
),
unioned_trips as (
    select * from green_tripdata
    union all
    select * from yellow_tripdata
)
select * from unioned_trips
