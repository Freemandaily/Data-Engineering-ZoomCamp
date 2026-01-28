## Bigquery clustring and Partitioning

### Benefits of Partitioning and Clustering

1. Partitioning

- Divides a table into segments (e.g., by date).

- Reduces data scanned → faster queries and lower cost.

- Improves manageability → easier to drop/archive old data.

- Ideal for time-series or large datasets.

2. Clustering

- Organizes data within partitions by column values (e.g., user_id).

- Speeds up filtering and aggregations → fewer rows read.

- Optimizes storage layout → queries on clustered columns are more efficient.

- Best for columns frequently used in WHERE, GROUP BY, or JOIN.

### Combined Benefit

Partitioning + clustering = maximum query efficiency: scan only relevant partitions, read fewer rows per partition.

Reduces cost, latency, and resource usage.



```sql
-- Query public available table
SELECT station_id, name FROM
    bigquery-public-data.new_york_citibike.citibike_stations
LIMIT 100;
```


```sql
-- Creating external table referring to gcs path

-- taxi-rides-ny is the project id name, create a project if not exist
-- nytaxi is the dataset name, create a dataset if not exist
-- nyc-tl-data is a bucket name, create a bucket if not exist
-- trip data is the folder name in the bucket
-- yellow_tripdata_2019-06.csv is the file name in the folder

CREATE OR REPLACE EXTERNAL TABLE `taxi-rides-ny.nytaxi.external_yellow_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://nyc-tl-data/trip data/yellow_tripdata_2019-*.csv', 'gs://nyc-tl-data/trip data/yellow_tripdata_2020-*.csv']
);
```

```sql
-- Check yellow trip data
SELECT * FROM taxi-rides-ny.nytaxi.external_yellow_tripdata limit 10;
```

### Create a non partitioned table from external table
This demonstrates the creating of non partitioned table named yellow_tripdata_non_partitioned from external table.

```sql
-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE taxi-rides-ny.nytaxi.yellow_tripdata_non_partitioned AS
SELECT * FROM taxi-rides-ny.nytaxi.external_yellow_tripdata;
```

### Create a partitioned table from external table
This demonstrates the creating of partitioned table named yellow_tripdata_partitioned from external table.

```sql
-- Create a partitioned table from external table
CREATE OR REPLACE TABLE taxi-rides-ny.nytaxi.yellow_tripdata_partitioned
PARTITION BY
  DATE(tpep_pickup_datetime) AS
SELECT * FROM taxi-rides-ny.nytaxi.external_yellow_tripdata;
```


### Show the impact of non partition
This query scans 1.6GB of data. Highlight the query, the scanned data size will be displayed.

```sql
-- Impact of partition
-- Scanning 1.6GB of data
SELECT DISTINCT(VendorID)
FROM taxi-rides-ny.nytaxi.yellow_tripdata_non_partitioned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';
```

### Show the impact of partitioned table
This scans ~106 MB of DATA compared to non partitioned table.

```sql
-- Scanning ~106 MB of DATA
SELECT DISTINCT(VendorID)
FROM taxi-rides-ny.nytaxi.yellow_tripdata_partitioned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';
```

### Looking Into The Partitioned Table

```sql
-- Let's look into the partitions
SELECT table_name, partition_id, total_rows
FROM `nytaxi.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'yellow_tripdata_partitioned'
ORDER BY total_rows DESC;
```


### Adding Clustering to Partition Table

```sql
-- Creating a partition and cluster table
CREATE OR REPLACE TABLE taxi-rides-ny.nytaxi.yellow_tripdata_partitioned_clustered
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT * FROM taxi-rides-ny.nytaxi.external_yellow_tripdata;
```


### Comparing Partitioned and Clusterd Partitioned Table

```sql

-- Query scans 1.1 GB
SELECT count(*) as trips
FROM taxi-rides-ny.nytaxi.yellow_tripdata_partitioned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID=1;
```

```sql
-- Query scans 864.5 MB
SELECT count(*) as trips
FROM taxi-rides-ny.nytaxi.yellow_tripdata_partitioned_clustered
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID=1;
```
