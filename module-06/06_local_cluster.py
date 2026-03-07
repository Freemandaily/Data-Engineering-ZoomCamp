#!/usr/bin/env python
# coding: utf-8

# In[1]:



from yarl import URL

from pyspark.sql import functions as F
import pyspark
from pyspark.sql import SparkSession


# In[3]:


spark = SparkSession.builder\
        .appName("test")\
        .getOrCreate()


# In[6]:


df_green = spark.read.option("recursiveFileLookup","true").parquet("gs://freeman-kestra-zoomcamp-bucket/parquet/pq//green/2020")


# In[10]:


df_yellow = spark.read.option("recursiveFileLookup","true").parquet("gs://freeman-kestra-zoomcamp-bucket/parquet/pq//green/2020")


# In[11]:


df_yellow.columns


# In[14]:


df_green = df_green\
            .withColumnRenamed('lpep_pickup_datetime','pickup_datetime')\
            .withColumnRenamed('lpep_dropoff_datetime','dropoff_datetime')


# In[13]:


df_yellow = df_yellow\
            .withColumnRenamed('tpep_pickup_datetime','pickup_datetime')\
            .withColumnRenamed('tpep_dropoff_datetime','dropoff_datetime')


# In[15]:

# In[16]:


common_columns = []

for column in df_green.columns:
    if column in df_yellow.columns:
        common_columns.append(column)




df_green_sel = df_green\
                .select(common_columns)\
                .withColumn('service_type',F.lit('green'))



# In[24]:


df_yellow_sel = df_yellow\
                .select(common_columns)\
                .withColumn('service_type',F.lit('yellow'))



# In[26]:


df_trips_data = df_yellow_sel.unionAll(df_green_sel)


# In[27]:


df_trips_data.groupBy('service_type').count().show()


# In[28]:


df_trips_data.createOrReplaceTempView('trips_data')


# In[29]:


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


# In[ ]:


df_select.coalesce(1).write.parquet('gs://freeman-kestra-zoomcamp-bucket/code',mode='overwrite')
