
# Excel / CSV Data Cleaner (Python)

A simple, beginner-friendly data cleaning tool for CSV and Excel files.
- Removes duplicates
- Trims extra whitespace
- Fills missing values
- Standardizes date columns (YYYY-MM-DD)
- Coerces numeric columns
- Saves the cleaned result back to CSV or XLSX

## Features
- Input: `.csv` or `.xlsx`
- Output: `.csv` or `.xlsx`
- CLI flags to customize behavior

## Quick Start

```bash
# 1) Create & activate a virtual env (optional but recommended)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 2) Install requirements
pip install -r requirements.txt

# 3) Run cleaner (sample data provided)
python -m cleaner.cli --in data/input/sample_data.csv --out data/output/cleaned_data.csv \  --date-columns Date --numeric-columns Score --fill Name=Unknown Score=0 --drop-duplicates --preview
```

## CLI Usage

```bash
python -m cleaner.cli --in <input_path> --out <output_path> [options]

Options:
  --date-columns        Comma-separated list of date columns to standardize (e.g., Date,CreatedAt)
  --numeric-columns     Comma-separated list of numeric columns to coerce (e.g., Score,Amount)
  --fill                Key=Value pairs to fill missing values. Repeat or space-separate (e.g., Name=Unknown Score=0)
  --drop-duplicates     Drop duplicate rows
  --drop-na-cols        Comma-separated list of columns; drop rows with NA in any of them
  --preview             Print a small preview and dtypes to console
```

## Example
Input (`data/input/sample_data.csv`):
```csv
Name,Date,Score
Alice,2025-08-01,90
Bob,08/02/2025,85
Charlie,,78
Alice,2025-08-01,90
David,2025-08-03,
"  Eve  ",2025-08-04,  88
```

Run:
```bash
python -m cleaner.cli --in data/input/sample_data.csv --out data/output/cleaned_data.csv \  --date-columns Date --numeric-columns Score --fill Name=Unknown Score=0 --drop-duplicates --preview
```

Output (CSV):
```csv
Name,Date,Score
Alice,2025-08-01,90
Bob,2025-08-02,85
Charlie,NaT,78
David,2025-08-03,0
Eve,2025-08-04,88
```

> Note: `NaT` means "Not a Time" for unparseable or missing dates. You can also fill it using `--fill Date=2025-01-01` or similar.

## Project Layout
```
excel-csv-cleaner/
├─ data/
│  ├─ input/
│  │  └─ sample_data.csv
│  └─ output/                # cleaned files will be saved here
├─ src/
│  └─ cleaner/
│     ├─ __init__.py
│     ├─ cli.py
│     ├─ core.py
│     └─ io_utils.py
├─ tests/
│  └─ test_core.py           # very small starter test
├─ .gitignore
├─ requirements.txt
├─ LICENSE
└─ README.md
```

## Next Steps
- Tweak the defaults in `core.py` to match your preferred cleaning behavior.
- Add more rules (e.g., lowercase/uppercase certain columns, trim inner spaces, custom validators).
- Upload to GitHub with a clear README and demo GIF.
- Offer this as a Fiverr gig: *"I will clean and automate your Excel/CSV data using Python."*

---

MIT License © 2025
