## Solution To home Work Module 3 
[Question can be seen here](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2026/03-data-warehouse/homework.md)


### BIGQUERY SETUP-- Create external table referring to gcs path

```sql
CREATE OR REPLACE EXTERNAL TABLE `DTzoomcamp-modules-66754.zoomcamp.yellow_taxi_external_table`
OPTIONS (
  FORMAT = 'PARQUET',
  URIS = ['gs://your-bucket-name/*.parquet']
);


CREATE OR REPLACE TABLE `DTzoomcamp-modules-66754.zoomcamp.yellow_taxi_materialized_table`
AS 
SELECT *
FROM `DTzoomcamp-modules-66754.zoomcamp.yellow_taxi_external_table`;
```



### No1 
What is count of records for the 2024 Yellow Taxi Data?

```sql
-- ans = 20,332,093
SELECT count(*) FROM `DTzoomcamp-modules-66754.zoomcamp.yellow_taxi_materialized_table`
```



### No2
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?
```sql
-- ans =  0 MB for the External Table and 155.12 MB for the Materialized Table
select 
  distinct PULocationID
from `DTzoomcamp-modules-66754.zoomcamp.yellow_taxi_materialized_table`


select 
  distinct PULocationID
from `DTzoomcamp-modules-66754.zoomcamp.yellow_taxi_external_table`
```



### No3
Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?
```sql
select 
  PULocationID
from `DTzoomcamp-modules-66754.zoomcamp.yellow_taxi_materialized_table`

select 
  PULocationID,
  DOLocationID 
from `DTzoomcamp-modules-66754.zoomcamp.yellow_taxi_materialized_table`
```



### No4
How many records have a fare_amount of 0?
```sql
-- ans = 8333
select 
  count(*) as total_zero_fare_Amount
from `DTzoomcamp-modules-66754.zoomcamp.yellow_taxi_materialized_table`
where fare_amount = 0
```



### No5
What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)
```sql
--ans Partition by tpep_dropoff_datetime and Cluster on VendorID

CREATE OR REPLACE TABLE  `DTzoomcamp-modules-66754.zoomcamp.yellow_taxi_materialized_partitioned_table`
PARTITION BY DATE(tpep_dropoff_datetime) 
CLUSTER BY VendorID 
AS
select 
  *
from `DTzoomcamp-modules-66754.zoomcamp.yellow_taxi_external_table`
```



### No6
Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive)

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?
```sql
-- ans 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table

--- non-partitioned table
select 
 distinct  VendorID
from `DTzoomcamp-modules-66754.zoomcamp.yellow_taxi_materialized_table`
where DATE(tpep_dropoff_datetime) between '2024-03-01' and '2024-03-15'


--- partitioned table
select 
 distinct  VendorID
from `DTzoomcamp-modules-66754.zoomcamp.yellow_taxi_materialized_partitioned_table`
where DATE(tpep_dropoff_datetime) between '2024-03-01' and '2024-03-15'

```


