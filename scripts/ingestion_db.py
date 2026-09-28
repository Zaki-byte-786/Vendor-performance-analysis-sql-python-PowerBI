
import pandas as pd
import os
import time
import logging
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

connection_url = URL.create(
    "mysql+pymysql",
    username="root",
    password="Password@123",
    host="localhost",
    port=3306,
    database="vendor_performance"
)

engine = create_engine(connection_url)

from sqlalchemy import text



import os

print(os.getcwd())


def ingest_db(df, table_name, engine, if_exists):
    df.to_sql(
        table_name,
        con=engine,
        if_exists=if_exists,
        index=False,
        chunksize=50000
    )

'''This function will load CSVs as Dataframe and ingest into DB'''
def load_raw_data():
    start = time.time()

    for file in os.listdir('Project/data'):

        if '.csv' in file:

            logging.info(f'Ingesting {file} into DB')

            first_chunk = True

            for chunk in pd.read_csv(
                'Project/data/' + file,
                chunksize=50000
            ):

                if first_chunk:

                    ingest_db(
                        chunk,
                        file[:-4],
                        engine,
                        'replace'
                    )

                    first_chunk = False

                else:

                    ingest_db(
                        chunk,
                        file[:-4],
                        engine,
                        'append'
                    )

            logging.info(f'{file} loaded successfully')

    end = time.time()

    total_time = (end - start) / 60

    logging.info('--------------Ingestion Complete--------------')

    logging.info(
        f'Total Time Taken: {total_time:.2f} minutes'
    )

if __name__ == '__main__':
    load_raw_data()