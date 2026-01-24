#!/usr/bin/env python
# coding: utf-8
import pandas as pd
from sqlalchemy import create_engine
import click

dtype = {
    "VendorID": "Int64",
    "store_and_fwd_flag": "string",
    "RatecodeID": "Int64",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "ehail_fee": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "payment_type": "Int64",
    "trip_type": "Int64",
    "congestion_surcharge": "float64",
    "cbd_congestion_fee": "float64"
}

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='green_taxi_data', help='Target table name')

def run(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table):
    prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
    green_taxi_url = f'{prefix}/green_tripdata_2025-11.parquet'

    df_green_taxi = pd.read_parquet(green_taxi_url,engine="pyarrow")
    df_green_taxi = df_green_taxi.astype(dtype)

    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    is_First = True
    if is_First:
        df_green_taxi.head(0).to_sql(
            name=target_table,
            con=engine,
            if_exists='replace'
        )
        is_First = False
    df_green_taxi.to_sql(
        name=target_table,
        con=engine,
        if_exists='append'
    )
