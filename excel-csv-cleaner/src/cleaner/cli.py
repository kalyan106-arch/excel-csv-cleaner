
import argparse
from typing import Dict, List
from .io_utils import load_table, save_table
from .core import clean_dataframe, CleanOptions

def parse_key_values(items: List[str]) -> Dict[str, str]:
    kv = {}
    for item in items or []:
        if '=' in item:
            key, value = item.split('=', 1)
            kv[key.strip()] = value.strip()
    return kv

def parse_csv_list(value: str) -> List[str]:
    if not value:
        return []
    return [v.strip() for v in value.split(',') if v.strip()]

def main():
    parser = argparse.ArgumentParser(description='Excel/CSV Data Cleaner')
    parser.add_argument('--in', dest='input_path', required=True, help='Path to input CSV/XLSX')
    parser.add_argument('--out', dest='output_path', required=True, help='Path to output CSV/XLSX')
    parser.add_argument('--date-columns', type=parse_csv_list, default=[], help='Comma-separated date columns')
    parser.add_argument('--numeric-columns', type=parse_csv_list, default=[], help='Comma-separated numeric columns')
    parser.add_argument('--fill', nargs='*', default=[], help='Key=Value pairs to fill missing values (space-separate)')
    parser.add_argument('--drop-duplicates', action='store_true', help='Drop duplicate rows')
    parser.add_argument('--drop-na-cols', type=parse_csv_list, default=[], help='Comma-separated columns to drop rows with NA')
    parser.add_argument('--preview', action='store_true', help='Print a preview and dtypes')

    args = parser.parse_args()

    df = load_table(args.input_path)

    options = CleanOptions(
        drop_duplicates=args.drop_duplicates,
        date_columns=args.date_columns,
        numeric_columns=args.numeric_columns,
        fill_values=parse_key_values(args.fill),
        drop_na_cols=args.drop_na_cols
    )

    cleaned = clean_dataframe(df, options)

    if args.preview:
        print('=== Preview (head) ===')
        print(cleaned.head())
        print('\n=== Dtypes ===')
        print(cleaned.dtypes)

    save_table(cleaned, args.output_path)
    print(f'Saved cleaned table to: {args.output_path}')

if __name__ == '__main__':
    main()
