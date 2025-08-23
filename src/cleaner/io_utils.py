
import os
import pandas as pd

def load_table(path: str) -> pd.DataFrame:
    ext = os.path.splitext(path)[1].lower()
    if ext == '.csv':
        return pd.read_csv(path)
    elif ext in ['.xlsx', '.xls']:
        return pd.read_excel(path)
    else:
        raise ValueError(f'Unsupported file extension: {ext}')

def save_table(df: pd.DataFrame, path: str) -> None:
    ext = os.path.splitext(path)[1].lower()
    if ext == '.csv':
        df.to_csv(path, index=False)
    elif ext in ['.xlsx', '.xls']:
        df.to_excel(path, index=False)
    else:
        raise ValueError(f'Unsupported file extension: {ext}')
