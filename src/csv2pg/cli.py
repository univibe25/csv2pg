# cli.py
from importlib.resources import files

import polars as pl
import typer

from csv2pg.loader import load
from csv2pg.registry import TRANSFORMS
from csv2pg.transforms import common

app = typer.Typer(help="Load the Thrive-AI sample CSVs into Postgres")

def _apply_transforms(stem: str, df: pl.DataFrame) -> pl.DataFrame:
    fns = TRANSFORMS.get(stem, [common])
    for fn in fns:                       # order matters!
        df = fn(df)
        typer.echo(f"✓ {stem} transformed by {fn.__name__}")
    return df

@app.command()
def loadcsv(
    url: str = typer.Option(..., help="Postgres URL: postgresql://user:pass@host:port/db"),
    schema: str = typer.Option(None, help="Target schema (optional)"),
):
    data_path = files("csv2pg.data")
    for csv_path in data_path.iterdir():
        if csv_path.suffix != ".csv": 
            continue
        stem = csv_path.stem
        df = pl.read_csv(csv_path)
        df = _apply_transforms(stem, df)
        load(df, url, table=stem, schema=schema)

        typer.echo(f"✓ {csv_path.name} → {schema or 'public'}.{csv_path.stem}")

if __name__ == "__main__":
    app()
