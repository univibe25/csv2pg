import polars as pl
import typer
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


def load(
    df: pl.DataFrame,
    url: str,
    table: str,
    schema: str | None = None,
    if_exists="replace",
):
    table_fqn = f"{schema}.{table}" if schema else table

    # First try block: Create engine and test connection
    try:
        engine = create_engine(url, isolation_level="AUTOCOMMIT")
        # Verify connection before attempting to write
        with engine.connect() as conn:
            pass
    except SQLAlchemyError as e:
        typer.secho(f"Database connection error: {str(e)}", fg=typer.colors.RED)
        typer.secho(
            "Please check your database connection URL and credentials",
            fg=typer.colors.YELLOW,
        )
        return False

    # Second try block: Write data to database
    try:
        df.write_database(
            table_fqn,
            connection=engine,
            if_table_exists=if_exists,
        )  # uses SQLAlchemy under the hood
    except SQLAlchemyError as e:
        typer.secho(f"Error writing to database: {str(e)}", fg=typer.colors.RED)
        typer.secho(f"Failed to load data into {table_fqn}", fg=typer.colors.RED)
        return False
    except Exception as e:
        typer.secho(
            f"Unexpected error during data writing: {str(e)}", fg=typer.colors.RED
        )
        return False

    return True
