# loader.py
import polars as pl
from sqlalchemy import create_engine


def load(df: pl.DataFrame, url: str, table: str, schema: str | None = None, if_exists="replace"):
    engine = create_engine(url, isolation_level="AUTOCOMMIT")
    table_fqn = f"{schema}.{table}" if schema else table
    df.write_database(
        table_fqn,
        connection=engine,
        if_table_exists=if_exists,
    )   # uses SQLAlchemy under the hood :contentReference[oaicite:3]{index=3}
