
from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime
import pandas as pd

@dataclass
class CleanOptions:
    drop_duplicates: bool = True
    date_columns: List[str] = field(default_factory=list)
    numeric_columns: List[str] = field(default_factory=list)
    fill_values: Dict[str, object] = field(default_factory=dict)
    drop_na_cols: List[str] = field(default_factory=list)
    fill_missing_dates_with: str = "N/A"  # Default for missing dates

# -------------------- Helpers -------------------- #
def strip_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
    return df

def parse_date_safe(value):
    """Try multiple date formats and return datetime or None"""
    if pd.isna(value) or str(value).strip() == '':
        return None
    formats = ["%Y-%m-%d", "%m/%d/%Y", "%m-%d-%Y", "%Y/%m/%d"]
    for fmt in formats:
        try:
            return datetime.strptime(str(value), fmt)
        except:
            continue
    return None

def standardize_dates(df: pd.DataFrame, columns: List[str], fill_missing: str = "N/A") -> pd.DataFrame:
    for col in columns:
        if col in df.columns:
            df[col] = df[col].apply(parse_date_safe)
            df[col] = df[col].dt.strftime('%Y-%m-%d')  # consistent formatting
            df[col] = df[col].fillna(fill_missing)
    return df

def coerce_numeric(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def fill_missing(df: pd.DataFrame, fill_values: Dict[str, object]) -> pd.DataFrame:
    if fill_values:
        for key, value in fill_values.items():
            if key in df.columns:
                df[key] = df[key].fillna(value)
    return df

def drop_na_rows(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    keep_cols = [c for c in columns if c in df.columns]
    if keep_cols:
        df = df.dropna(subset=keep_cols)
    return df

# -------------------- Main Cleaner -------------------- #
def clean_dataframe(df: pd.DataFrame, options: CleanOptions) -> pd.DataFrame:
    # 1) Trim whitespace
    df = strip_whitespace(df)

    # 2) Drop duplicates
    if options.drop_duplicates:
        df = df.drop_duplicates()

    # 3) Standardize dates
    df = standardize_dates(df, options.date_columns, fill_missing=options.fill_missing_dates_with)

    # 4) Coerce numeric columns
    df = coerce_numeric(df, options.numeric_columns)

    # 5) Fill missing values
    df = fill_missing(df, options.fill_values)

    # 6) Drop NA rows for specific columns if needed
    df = drop_na_rows(df, options.drop_na_cols)

    return df.reset_index(drop=True)
