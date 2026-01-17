import pandas as pd
from sqlalchemy import create_engine, inspect
from tqdm.auto import tqdm
import click

# credentials
pg_user = 'root'
pg_password = 'root'
pg_host = 'localhost'
pg_port = '5432'
pg_db = 'ny_taxi'
taget_table_ = 'green_taxi_data'
target_table_zone = 'taxi_zone_data'


def run():
    url_taxi = f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet'
    df_taxi = pd.read_parquet(url_taxi)
    
    url_zone = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv'
    df_zone = pd.read_csv(url_zone)
    
    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')
    
    # Check if 'green_taxi_data' table exists
    inspector = inspect(engine)
    table_exists = inspector.has_table('target_table_')
    
    # Use 'replace' if table exists, otherwise 'append'
    if_exists_taxi = 'replace' if table_exists else 'append'
    
    print(f"Table 'target_table_' exists: {table_exists}")
    print(f"Using if_exists='{if_exists_taxi}' for target_table_")
    
    df_taxi.to_sql(name='target_table_', con=engine, if_exists=if_exists_taxi)
    
    # Do the same for taxi_zone_data if needed
    zone_table_exists = inspector.has_table('target_table_zone')
    if_exists_zone = 'replace' if zone_table_exists else 'append'
    
    print(f"Table 'target_table_zone' exists: {zone_table_exists}")
    print(f"Using if_exists='{if_exists_zone}' for target_table_zone")

    df_zone.to_sql(name='target_table_zone', con=engine, if_exists=if_exists_zone)

    print("Data import completed successfully!")


if __name__ == '__main__':
    run()