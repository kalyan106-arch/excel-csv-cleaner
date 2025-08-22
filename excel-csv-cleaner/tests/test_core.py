
import pandas as pd
from src.cleaner.core import clean_dataframe, CleanOptions

def test_basic_clean():
    df = pd.DataFrame({
        'Name': [' Alice ', 'Bob', 'Alice '],
        'Date': ['2025-08-01', '08/02/2025', '2025-08-01'],
        'Score': ['90', '85', '90']
    })
    opts = CleanOptions(drop_duplicates=True, date_columns=['Date'], numeric_columns=['Score'])
    out = clean_dataframe(df, opts)
    # After trimming + drop dup, should be 2 rows
    assert len(out) == 2
    # Date should be datetime64 dtype
    assert str(out['Date'].dtype).startswith('datetime64')
    # Score coerced to numeric
    assert pd.api.types.is_numeric_dtype(out['Score'])
