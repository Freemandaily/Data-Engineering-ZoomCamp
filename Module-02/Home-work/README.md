## SQL Solution  to Question No3,No4,No5


### 3. How many rows are there for the yellow Taxi data for all CSV files in the year 2020?
```sql
SELECT 
  SUM(total_row) AS total_rows_2020
FROM (
  SELECT COUNT(*) AS total_row FROM `terraform-484415.zoomcamp.yellow_tripdata_2020_01`
  UNION ALL
  SELECT COUNT(*) FROM `terraform-484415.zoomcamp.yellow_tripdata_2020_02`
  UNION ALL
  SELECT COUNT(*) FROM `terraform-484415.zoomcamp.yellow_tripdata_2020_03`
  UNION ALL
  SELECT COUNT(*) FROM `terraform-484415.zoomcamp.yellow_tripdata_2020_04`
  UNION ALL
  SELECT COUNT(*) FROM `terraform-484415.zoomcamp.yellow_tripdata_2020_05`
  UNION ALL
  SELECT COUNT(*) FROM `terraform-484415.zoomcamp.yellow_tripdata_2020_06`
  UNION ALL
  SELECT COUNT(*) FROM `terraform-484415.zoomcamp.yellow_tripdata_2020_07`
  UNION ALL
  SELECT COUNT(*) FROM `terraform-484415.zoomcamp.yellow_tripdata_2020_08`
  UNION ALL
  SELECT COUNT(*) FROM `terraform-484415.zoomcamp.yellow_tripdata_2020_09`
  UNION ALL
  SELECT COUNT(*) FROM `terraform-484415.zoomcamp.yellow_tripdata_2020_10`
  UNION ALL
  SELECT COUNT(*) FROM `terraform-484415.zoomcamp.yellow_tripdata_2020_11`
  UNION ALL
  SELECT COUNT(*) FROM `terraform-484415.zoomcamp.yellow_tripdata_2020_12`
);
```

### 4. How many rows are there for the Green Taxi data for all CSV files in the year 2020?
```sql
SELECT 
  SUM(total_row) AS total_rows_2020
FROM (
  SELECT COUNT(*) AS total_row FROM `terraform-484415.zoomcamp.green_tripdata_2020_01`
  UNION ALL
  SELECT COUNT(*) FROM `terraform-484415.zoomcamp.green_tripdata_2020_02`
  UNION ALL
  SELECT COUNT(*) FROM `terraform-484415.zoomcamp.green_tripdata_2020_03`
  UNION ALL
  SELECT COUNT(*) FROM `terraform-484415.zoomcamp.green_tripdata_2020_04`
  UNION ALL
  SELECT COUNT(*) FROM `terraform-484415.zoomcamp.green_tripdata_2020_05`
  UNION ALL
  SELECT COUNT(*) FROM `terraform-484415.zoomcamp.green_tripdata_2020_06`
  UNION ALL
  SELECT COUNT(*) FROM `terraform-484415.zoomcamp.green_tripdata_2020_07`
  UNION ALL
  SELECT COUNT(*) FROM `terraform-484415.zoomcamp.green_tripdata_2020_08`
  UNION ALL
  SELECT COUNT(*) FROM `terraform-484415.zoomcamp.green_tripdata_2020_09`
  UNION ALL
  SELECT COUNT(*) FROM `terraform-484415.zoomcamp.green_tripdata_2020_10`
  UNION ALL
  SELECT COUNT(*) FROM `terraform-484415.zoomcamp.green_tripdata_2020_11`
  UNION ALL
  SELECT COUNT(*) FROM `terraform-484415.zoomcamp.green_tripdata_2020_12`
);
```

### 5. How many rows are there for the Yellow Taxi data for the March 2021 CSV file?
```sql
SELECT 
  count(*) as total_rows
FROM `terraform-484415.zoomcamp.yellow_tripdata_2021_03` 
```