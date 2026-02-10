##  Solution To Questions

*This README only contains the Questions that requires queries Fo the answer*


### Question N0 3
*Counting Records in fct_monthly_zone_revenue*

After running your dbt project, query the fct_monthly_zone_revenue model.

What is the count of records in the fct_monthly_zone_revenue model?

*Solution*
```sql
select 
    count(*) as total_records,
from prod.monthly_revenue_per_locations
```

### Question N0 4
*Best Performing Zone for Green Taxis (2020)*

Using the fct_monthly_zone_revenue table, find the pickup zone with the highest total revenue (revenue_monthly_total_amount) for Green taxi trips in 2020.

Which zone had the highest revenue?

```sql
select 
    pickup_zone
   ,sum(revenue_monthly_total_amount)
from prod.monthly_revenue_per_locations
where service_type = 'Green'
and revenue_month  > '2019-12-31'
and revenue_month  <= '2021-01-01'
group by pickup_zone
order by sum(revenue_monthly_total_amount) desc
limit 1
```

### Question N0 5
*Green Taxi Trip Counts (October 2019)*

Using the fct_monthly_zone_revenue table, what is the total number of trips (total_monthly_trips) for Green taxis in October 2019?

```sql
select
    sum(total_monthly_trips) as total_trips,
from prod.monthly_revenue_per_locations
where service_type = 'Green'
and revenue_month  >= '2019-10-01'
and revenue_month  < '2019-11-01'
```

### Question No 6
*Build a Staging Model for FHV Data*
Create a staging model for the For-Hire Vehicle (FHV) trip data for 2019.
Filter out records where dispatching_base_num IS NULL

What is the count of records in stg_fhv_tripdata?

```sql
select 
    count(*) as total_records
from {{ ref('stg_fhv_tripdata') }}
```
