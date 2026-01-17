# Homework: Questions and Solutions

## Question 1
Run docker with the `python:3.13` image. Use an entrypoint bash to interact with the container.
```bash
docker run -it -- rm --entrypoint=bash python:3.13

#  pip version
pip --version
```

## Question 2
Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?

```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

```bash
docker compose up
```

```
host = db
port = 5433
```

Note: Script for ingesting green taxi and zone data set is in the `ingest_data.py` file.
Run the following command in the terminal to run the script:
```bash
# TO ingest green taxi data set (It has default value)
 uv run ingest.py --target_table 

 # To ingest taxi zone data set
 uv run ingest.py --target_table taxi_zones --data_set taxi_zones
```

## Question 3
For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile?

```sql
select 
	COUNT(*) AS total_trips
from public.green_taxi_data
WHERE 
	trip_distance <= 1
AND 
	CAST(lpep_pickup_datetime AS DATE ) >= DATE('2025-11-01') 
AND 
	CAST(lpep_pickup_datetime AS DATE ) < DATE('2025-12-01');
``` 

## Question 4
Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors).

```sql
select 
	CAST(lpep_pickup_datetime AS DATE ) AS day
from public.green_taxi_data
where 
	trip_distance < 100
order BY trip_distance DESC
limit 1;
```

## Question 5 
Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?

```sql
with counts as (
select 
	"PULocationID" AS location_id
	,count(*)as total_trips 
from public.green_taxi_data  
where CAST(lpep_pickup_datetime AS DATE ) = DATE('2025-11-18')
group bY "PULocationID"
order by 2 DESC
limit 1
)
select 
	z."Zone"
	,c.location_id
	,c.total_trips
from public.taxi_zones z
join counts c on z."LocationID" = c.location_id
```

## Question 6
For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

```sql
with largest_tip as (
select 
	"DOLocationID" as location_id
	,tip_amount 
from public.green_taxi_data 
where "PULocationID" IN (
	select "LocationID" from public.taxi_zones Where "Zone" = 'East Harlem North'
)
AND CAST(lpep_pickup_datetime AS DATE ) >= DATE('2025-11-01') 
order by 2 DESC
LIMIT 1
)
select 
	"Zone"
	,h.location_id
	,h.tip_amount
from public.taxi_zones p
join largest_tip h ON h.location_id = p."LocationID"
```

## Question 7 
Which of the following sequences, respectively, describes the workflow for:

1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform`

```bash
terraform init
terraform plan
terraform apply --auto-approve
terraform destroy
```