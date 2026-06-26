import pandas as pd
import glob
import logging
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# =====================================================
# Logging Configuration
# =====================================================

Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/load_raw_to_postgres.log"),
        logging.StreamHandler()
    ]
)

# =====================================================
# Database Connection
# =====================================================

DATABASE_URL = (
    "postgresql://postgres:123@localhost:5432/medical_warehouse"
)

try:
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        logging.info(
            "Successfully connected to PostgreSQL"
        )

except Exception as e:
    logging.exception(
        f"Database connection failed: {e}"
    )
    raise

# =====================================================
# Find JSON Files
# =====================================================

files = glob.glob(
    "data/raw/telegram_messages/*/*.json",
    recursive=True
)

if not files:
    logging.warning(
        "No JSON files found in data/raw/telegram_messages"
    )
    exit()

logging.info(
    f"Found {len(files)} JSON files"
)

# =====================================================
# Load Files
# =====================================================

loaded_files = 0
failed_files = 0
total_rows = 0

for file in files:

    try:

        logging.info(
            f"Processing file: {file}"
        )

        df = pd.read_json(file)

        if df.empty:
            logging.warning(
                f"Skipping empty file: {file}"
            )
            continue

        row_count = len(df)

        df.to_sql(
            "telegram_messages",
            engine,
            schema="raw",
            if_exists="append",
            index=False
        )

        loaded_files += 1
        total_rows += row_count

        logging.info(
            f"Loaded {row_count} rows from {file}"
        )

    except SQLAlchemyError as e:

        failed_files += 1

        logging.exception(
            f"Database error while loading "
            f"{file}: {e}"
        )

    except Exception as e:

        failed_files += 1

        logging.exception(
            f"Unexpected error while loading "
            f"{file}: {e}"
        )

# =====================================================
# Summary
# =====================================================

logging.info("=" * 50)
logging.info("LOAD SUMMARY")
logging.info("=" * 50)

logging.info(
    f"Files Loaded Successfully : {loaded_files}"
)

logging.info(
    f"Files Failed            : {failed_files}"
)

logging.info(
    f"Total Rows Loaded       : {total_rows}"
)

logging.info(
    "Finished loading data to PostgreSQL"
)