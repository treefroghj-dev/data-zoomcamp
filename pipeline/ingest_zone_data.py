#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import click
from sqlalchemy import create_engine


dtype = {
    "LocationID": "Int64",
    "Borough": "string",
    "Zone": "string",
    "service_zone": "string"
}

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='zone', help='Target table name')

def run(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table):

    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc'
    url=f'{prefix}/taxi_zone_lookup.csv'

    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    df_zone = pd.read_csv(url, dtype=dtype)

    is_First = True
    if is_First:
        df_zone.head(0).to_sql(name=target_table, con=engine, if_exists="replace")
        is_First = False
    df_zone.to_sql(name=target_table, con=engine, if_exists="append")

if __name__ == '__main__':
    run()