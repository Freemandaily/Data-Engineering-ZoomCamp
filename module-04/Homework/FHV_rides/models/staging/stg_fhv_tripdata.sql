select 
    -- identifiers
    cast(dispatching_base_num as string) as dispatching_base_num,
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropoff_datetime as timestamp)as dropoff_datetime,
    cast(PUlocationID as int) as pickup_location_id,
    cast(DOlocationID as int) as dropoff_location_id,
    cast(SR_Flag as int) as sr_flag
from {{source('fhv_raw_data', 'fhv_tripdata')}}
where dispatching_base_num is not null
