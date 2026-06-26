import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:123@localhost:5432/medical_warehouse"
)

df = pd.read_csv(
    "data/processed/image_detections.csv"
)

df.to_sql(
    "image_detections",
    engine,
    schema="raw",
    if_exists="append",
    index=False
)

print(
    f"{len(df)} rows loaded"
)