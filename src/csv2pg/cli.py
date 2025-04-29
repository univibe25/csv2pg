# cli.py
import sys
from importlib.resources import files

import polars as pl
import typer

from csv2pg.loader import load
from csv2pg.registry import TRANSFORMS
from csv2pg.transforms import common

app = typer.Typer(help="Load the Thrive-AI sample CSVs into Postgres")


def _apply_transforms(stem: str, df: pl.DataFrame) -> pl.DataFrame:
    fns = TRANSFORMS.get(stem, [common])
    for fn in fns:  # order matters!
        df = fn(df)
        typer.echo(f"✓ {stem} transformed by {fn.__name__}")
    return df


@app.command()
def loadcsv(
    url: str = typer.Option(
        ..., help="Postgres URL: postgresql://user:pass@host:port/db"
    ),
    schema: str = typer.Option(None, help="Target schema (optional)"),
):
    data_path = files("csv2pg.data")
    success_count = 0
    fail_count = 0

    for csv_path in data_path.iterdir():
        if csv_path.suffix != ".csv":
            continue

        stem = csv_path.stem
        try:
            df = pl.read_csv(csv_path)
            df = _apply_transforms(stem, df)

            success = load(df, url, table=stem, schema=schema)

            if success:
                typer.secho(
                    f"✓ {csv_path.name} → {schema or 'public'}.{csv_path.stem}",
                    fg=typer.colors.GREEN,
                )
                success_count += 1
            else:
                typer.secho(f"✗ Failed to load {csv_path.name}", fg=typer.colors.RED)
                fail_count += 1

        except Exception as e:
            typer.secho(
                f"✗ Error processing {csv_path.name}: {str(e)}", fg=typer.colors.RED
            )
            fail_count += 1

    # Summary at the end
    if success_count > 0:
        typer.secho(
            f"\n✓ Successfully loaded {success_count} file(s)", fg=typer.colors.GREEN
        )
    if fail_count > 0:
        typer.secho(f"✗ Failed to load {fail_count} file(s)", fg=typer.colors.RED)
        sys.exit(1)


if __name__ == "__main__":
    app()
