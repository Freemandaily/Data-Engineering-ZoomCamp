#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import click
import os
from sqlalchemy import create_engine
from tqdm.auto import tqdm


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

@click.command()
@click.option('--data_set', default='taxi_trip', help='Dataset To Ingest.Expected values: taxi_trip or taxi_zones')
@click.option('--year', default=2021, type=int, help='Year for the taxi data.')
@click.option('--month', default=1, type=int, help='Month for the taxi data.')
@click.option('--pg_user', default='root', help='PostgreSQL user.')
@click.option('--pg_pass', default='root', help='PostgreSQL password.')
@click.option('--pg_host', default='localhost', help='PostgreSQL host.')
@click.option('--pg_port', default=5433, type=int, help='PostgreSQL port.')
@click.option('--pg_db', default='ny_taxi', help='PostgreSQL database name.')
@click.option('--target_table', default='greee_taxi_data', help='Name of the target table in PostgreSQL.')
@click.option('--chunksize', default=100000, type=int, help='Size of chunks to read from CSV.')
def run(data_set,year, month, pg_user, pg_pass, pg_host, pg_port, pg_db, target_table, chunksize):
    
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    print('engine created')

    if data_set == "taxi_trip":
        url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
        df = pd.read_parquet(url)
        print(f'Dataframe with {len(df)} rows and {len(df.columns)} columns loaded')

        df.to_sql(name=target_table, con=engine, if_exists='replace', chunksize=chunksize)
    else:
        target_table = "taxi_zones"

        url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
        df = pd.read_csv(url)
        print(f'Dataframe with {len(df)} rows and {len(df.columns)} columns loaded')
        df.to_sql(name=target_table, con=engine, if_exists='replace')

if __name__ == '__main__':
    run()