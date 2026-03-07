## Notes On Spark

Pyspark is a library used for Batch processing of  large dataset efficiently. It handles the batch processing of csv ,parquet,json file .

### Demo

### Downloading of the file (parquet)

```code
!wget https://d37ci6vzurychx.cloudfront.net/trip-data/fhvhv_tripdata_2021-01.parquet
```

### Importing pyspark
```code
from pyspark.sql import SparkSession
```

### Connecting to spark using local master 
```code
spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()
```

### Spark DataFrame
We use the 'spark' object we created above to read  the  file we downloaded

```python
df = spark.read.parquet('name_of_the_file')

# showing the dataset
df.show()

# showing the columns in the dataset only
df.columns
df.printSchema
```

### selecting A column from parquet File 
```python
df.select('column1','column2','column3')

# adding filter
df.select('column2','column2','column3')\
    .filter(df.column_name == 'filter_word')
```

### Adding Column to dataset
```python
df\
    df\
    .withColumn('new_column_name1',F.to_date(df.date_column))\
    .withColumn('new_column_name2',df.column / 2 )\
    .select('column1','column2','column3')\
    .show()
```

### Write back file to our system
```python
df.write.parquet('directory_to_write_file_to')
```

### Using repartition in spark
In Apache Spark, repartition is used to change the number of partitions in a DataFrame or RDD.
It usually increases or redistributes partitions across the cluster so data can be processed more efficiently in parallel.

```python
df = df.repartition(10)

# This tells spark to “Split this dataset into 10 partitions and redistribute the data.”
```

### Writting to system using repartition
Spark write one file per partition

So we declare the number of partition to write into this write into parquet data total number of the partition we choose

```python
df.repartition(5).write.parquet('directory to write to')
```

### Spark SQL
we can use spark to write our sql and tranform data.
Suppose we have 2 different set of dataset( df_green and df_yellow)

```python
df_green = spark.read.option("recursiveFileLookup","true").parquet("data/pq/green")

df_yellow = spark.read.option("recursiveFileLookup","true").parquet("data/pq/yellow")

```


### Writing SQL 
```python
# Here we assume that both dataset has similar columns 
df_trips_data = df_green.unionAll(df_yellow) 

# Grouping
df_trips_data.groupBy('column_name').count().show()


# creating a Temporary Table
df_trips_data.registerTempTable('trips_data')

# Writting our sql
df_select = spark.sql("""
    SELECT 
        -- Reveneue grouping 
        PULocationID AS revenue_zone,
        date_trunc('month', pickup_datetime) AS revenue_month, 
        service_type, 

        -- Revenue calculation 
        SUM(fare_amount) AS revenue_monthly_fare,
        SUM(extra) AS revenue_monthly_extra,
        SUM(mta_tax) AS revenue_monthly_mta_tax,
        SUM(tip_amount) AS revenue_monthly_tip_amount,
        SUM(tolls_amount) AS revenue_monthly_tolls_amount,
        SUM(improvement_surcharge) AS revenue_monthly_improvement_surcharge,
        SUM(total_amount) AS revenue_monthly_total_amount,
        SUM(congestion_surcharge) AS revenue_monthly_congestion_surcharge,

        -- Additional calculations
        AVG(passenger_count) AS avg_montly_passenger_count,
        AVG(trip_distance) AS avg_montly_trip_distance
    FROM
        trips_data
    GROUP BY
        1, 2, 3
""")

# We can write back to system 

df_select.write.parquet('directory_to_save')
```

## Spark Gcp
Hvaing our dataset in our gcp bucket(data lake) we can connect to it from our local and then run our neccesary transformation just like we did above

### Upload a Dataset 
```code
# Run This command 
gsutil -m cp -r data/pq/ gs://freeman-kestra-zoomcamp-bucket/parquet

# cp   -> linux copy command
# -r  -> This is recursive , meaning we want to go over each folder and get datas in them
# data/pq/      -> This is the location of our parquet file in our local storage
# gs://freeman-kestra-zoomcamp-bucket/parquet       -> This is our gcp bucket folder where we wamt our file to live in
```

### Connecting And Using Our Data In GCP

```code
# First download the gcs connector

gsutil cp gs://hadoop-lib/gcs/gcs-connector-hadoop3-2.2.5.jar gcs-connector-hadoop3-2.2.5.jar

# gs://hadoop-lib/gcs/gcs-connector-hadoop3-2.2.5.jar    -> This is the connector
# gcs-connector-hadoop3-2.2.5.jar                ->  This is where we save i after download
```

```python
import pyspark
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext

credentials_location = 'directory_to_your_service_account.json'

spark = SparkSession.builder \
    .appName("test") \
    .master("local[*]") \
    .config("spark.jars", "path_to_the_connector_and_the_file.jar") \  
    .config("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    .config("spark.hadoop.google.cloud.auth.service.account.json.keyfile", credentials_location) \
    .getOrCreate()  # will reuse existing SparkContext if one exists


# Get the SparkContext
sc = spark.sparkContext

# Configure Hadoop to work with GCS
hadoop_conf = sc._jsc.hadoopConfiguration()
hadoop_conf.set("fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
hadoop_conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
hadoop_conf.set("fs.gs.auth.service.account.json.keyfile", credentials_location)
hadoop_conf.set("fs.gs.auth.service.account.enable", "true")


# Reading our dataset 
df_green = spark.read \
    .option("recursiveFileLookup", "true")\
    .option("mergeSchema","true")\
    .parquet("gs://bucket_name/folder_to_the_parquet")



# This will Rasie error because of no recursive added
df_green = spark.read.parquet("gs://freeman-kestra-zoomcamp-bucket/parquet/pq/green/2020")