# transform.py
import re

import polars as pl


def common(df: pl.DataFrame) -> pl.DataFrame:
    # First convert column names to lowercase
    df = df.rename({c: c.lower() for c in df.columns})
    
    # Replace spaces with underscores
    df = df.rename({c: c.replace(" ", "_") for c in df.columns})
    
    # Replace special characters with underscores using regex
    df = df.rename({c: re.sub(r'[\(\)\-,/]', '_', c) for c in df.columns})
    
    # Clean up multiple consecutive underscores that might have been created
    df = df.rename({c: re.sub(r'_{2,}', '_', c) for c in df.columns})
    
    # Remove trailing underscores
    df = df.rename({c: c.rstrip('_') for c in df.columns})
        
    return df

def add_patient_id(df: pl.DataFrame, col: str = "patient_id") -> pl.DataFrame:
    if col not in df.columns:
        df = df.insert_column(0, pl.Series(col, range(1, len(df)+1)))
    return df

def clean_titanic(df: pl.DataFrame) -> pl.DataFrame:
    df = df.with_columns(
        pl.col("pclass").fill_null("Unknown Pclass"),
        pl.col("cabin").fill_null("Unknown Cabin"),
        pl.col("sex").fill_null("Unknown Sex"),
    )

    return df

def clean_wny_health(df: pl.DataFrame) -> pl.DataFrame:
    df = df.rename({"bcs": "breast_cancer_screening","ccs": "cervical_cancer_screening","col": "colorectal_cancer_screening"})

    return df