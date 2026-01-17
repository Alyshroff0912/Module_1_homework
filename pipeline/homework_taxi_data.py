import pandas as pd
from sqlalchemy import create_engine, inspect
from tqdm.auto import tqdm
import click


@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-password', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database')
@click.option('--target-table', default='green_taxi_data', help='Target table for taxi data')
@click.option('--target-table-zone', default='taxi_zone_data', help='Target table for zone data')
def run(pg_user, pg_password, pg_host, pg_port, pg_db, target_table, target_table_zone):

    url_taxi = f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet'
    df_taxi = pd.read_parquet(url_taxi)
    
    url_zone = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv'
    df_zone = pd.read_csv(url_zone)
    
    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')
    
    # Check if table exists
    inspector = inspect(engine)
    table_exists = inspector.has_table(target_table)
    
    # Use 'replace' if table exists, otherwise 'append'
    if_exists_taxi = 'replace' if table_exists else 'append'
    
    print(f"Table '{target_table}' exists: {table_exists}")
    print(f"Using if_exists='{if_exists_taxi}' for {target_table}")
    
    df_taxi.to_sql(name=target_table, con=engine, if_exists=if_exists_taxi)
    
    # Do the same for zone data if needed
    zone_table_exists = inspector.has_table(target_table_zone)
    if_exists_zone = 'replace' if zone_table_exists else 'append'
    
    print(f"Table '{target_table_zone}' exists: {zone_table_exists}")
    print(f"Using if_exists='{if_exists_zone}' for {target_table_zone}")

    df_zone.to_sql(name=target_table_zone, con=engine, if_exists=if_exists_zone)

    print("Data import completed successfully!")


if __name__ == '__main__':
    run()