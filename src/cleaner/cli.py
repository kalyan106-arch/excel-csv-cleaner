
import argparse
import pandas as pd
from src.cleaner.core import CleanOptions, clean_dataframe

def main():
    parser = argparse.ArgumentParser(description="Excel/CSV Cleaner CLI")
    parser.add_argument("--in", dest="input_file", required=True, help="Input CSV/Excel file")
    parser.add_argument("--out", dest="output_file", required=True, help="Output cleaned file")
    parser.add_argument("--date-columns", nargs="+", default=[], help="Columns to parse as dates")
    parser.add_argument("--numeric-columns", nargs="+", default=[], help="Columns to coerce as numeric")
    parser.add_argument("--fill", nargs="*", default=[], help="Fill missing values, e.g. Name=Unknown Score=0")
    parser.add_argument("--drop-duplicates", action="store_true", help="Drop duplicate rows")
    parser.add_argument("--preview", action="store_true", help="Show first 5 rows of cleaned data")

    args = parser.parse_args()

    # Load file
    if args.input_file.endswith(".csv"):
        df = pd.read_csv(args.input_file)
    elif args.input_file.endswith(".xlsx"):
        df = pd.read_excel(args.input_file)
    else:
        raise ValueError("Only CSV and Excel files are supported.")

    # Prepare fill values dict
    fill_dict = {}
    for item in args.fill:
        if '=' in item:
            k, v = item.split('=', 1)
            try:
                fill_dict[k] = float(v) if v.replace('.','',1).isdigit() else v
            except:
                fill_dict[k] = v

    # Options
    options = CleanOptions(
        drop_duplicates=args.drop_duplicates,
        date_columns=args.date_columns,
        numeric_columns=args.numeric_columns,
        fill_values=fill_dict
    )

    # Clean
    cleaned = clean_dataframe(df, options)

    # Save output
    if args.output_file.endswith(".csv"):
        cleaned.to_csv(args.output_file, index=False)
    else:
        cleaned.to_excel(args.output_file, index=False)

    if args.preview:
        print(cleaned.head())

if __name__ == "__main__":
    main()
