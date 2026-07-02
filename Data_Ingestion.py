import os
import time
import logging
import pandas as pd
from sqlalchemy import create_engine


# -------------------------------------------------------------
# Logging Configuration
# -------------------------------------------------------------

logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.INFO,   # DEBUG unnecessary → slows logging
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)


# -------------------------------------------------------------
# Database Engine
# -------------------------------------------------------------

engine = create_engine("sqlite:///inventory.db")


# -------------------------------------------------------------
# Chunked Ingestion Function (CRITICAL OPTIMIZATION)
# -------------------------------------------------------------

def ingest_large_csv(file_path: str, table_name: str, engine) -> None:
    """
    Stream large CSV files into SQLite database using chunked inserts.

    Parameters
    ----------
    file_path : str
        Path to CSV file.

    table_name : str
        Target database table name.

    engine : sqlalchemy.engine.Engine
        Database engine.
    """

    try:
        logging.info(f"Starting ingestion for {table_name}")

        # IMPORTANT: Replace table ONLY once
        first_chunk = True

        for chunk in pd.read_csv(file_path, chunksize=50000):

            chunk.to_sql(
                table_name,
                con=engine,
                if_exists="replace" if first_chunk else "append",
                index=False
            )

            first_chunk = False

        logging.info(f"Successfully ingested table: {table_name}")

    except Exception as e:
        logging.error(f"Ingestion failed for {table_name}: {str(e)}")
        raise


# -------------------------------------------------------------
# Raw Data Loader
# -------------------------------------------------------------

def load_raw_data() -> None:
    """
    Load CSV files from data directory and ingest into database.
    """

    start_time = time.time()

    try:
        files = os.listdir("data")

        if not files:
            logging.warning("No files found in data directory")
            return

        for file in files:

            if not file.endswith(".csv"):
                logging.warning(f"Skipping non-CSV file: {file}")
                continue

            file_path = os.path.join("data", file)
            table_name = file[:-4]

            logging.info(f"Processing file: {file}")

            ingest_large_csv(file_path, table_name, engine)

    except Exception as e:
        logging.critical(f"Raw data loading failed: {str(e)}")
        raise

    finally:
        end_time = time.time()
        total_time = (end_time - start_time) / 60

        logging.info("-------------- Ingestion Complete --------------")
        logging.info(f"Total time taken: {total_time:.2f} minutes")


# -------------------------------------------------------------
# Entry Point
# -------------------------------------------------------------

if __name__ == "__main__":
    load_raw_data()
