#!/usr/bin/env python
# coding: utf-8
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click


yellow_taxi_dtype = {
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

green_taxi_dtype = {
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

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default=2021, help='year')
@click.option('--month', default=1, help='month')
@click.option('--chunksize', default=100000, help='chunksize')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, chunksize):

    yellow_taxi_prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url = f'{yellow_taxi_prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'

    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    df_iter = pd.read_csv(
        url,
        dtype=yellow_taxi_dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize,
    )

    create_or_replace_table(engine, df_iter, 'yellow_taxi_data')

    green_taxi_prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
    green_taxi_url = f'{green_taxi_prefix}/green_tripdata_2025-11.parquet'

    df_green_taxi = pd.read_parquet(green_taxi_url, engine="pyarrow")
    df_green_taxi = df_green_taxi.astype(green_taxi_dtype)
    create_or_replace_table(engine, df_green_taxi, 'green_taxi_data')

def create_or_replace_table(engine, df, target_table):
    is_First = True
    if is_First:
        df.head(0).to_sql(
            name=target_table,
            con=engine,
            if_exists='replace'
        )
        is_First = False
    df.to_sql(
        name=target_table,
        con=engine,
        if_exists='append'
    )

if __name__ == '__main__':
    run()





