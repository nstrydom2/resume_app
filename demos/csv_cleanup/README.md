# CSV Cleanup Utility

A small, self-contained demonstration project. It is not client work and does not include client data or client results.

The script takes a messy CSV export and produces a cleaner CSV plus an optional JSON summary. It is intentionally narrow: it handles common cleanup problems without pretending to replace a full data-validation pipeline.

## What it does

- Detects comma, semicolon, tab, or pipe delimiters from the header row.
- Trims whitespace from headers and cell values.
- Normalises headers to lowercase snake_case.
- Gives duplicate headers unique names.
- Drops fully blank rows.
- Removes duplicate data rows while preserving the original order.
- Drops columns that contain no data unless `--keep-empty-columns` is used.
- Pads short rows so every row matches the cleaned header width.
- Writes an optional JSON report with counts and column names.

## Requirements

Python 3.8 or newer. No third-party packages.

## Usage

```bash
python clean_csv.py sample_input.csv \
  -o sample_output.csv \
  --report sample_report.json
```

The output path defaults to `<input>_cleaned.csv` when `-o` is omitted.

```bash
python clean_csv.py exports/customers.csv
```

Keep empty columns:

```bash
python clean_csv.py exports/customers.csv --keep-empty-columns
```

## Sample result

`sample_input.csv` contains padded headers, inconsistent whitespace, one blank row, one duplicate row, and one empty column.

```text
4 input rows -> 2 output rows; 1 duplicates removed; 1 empty columns removed.
```

The cleaned output has four columns: `name`, `email`, `phone`, and `notes`.

## Scope and limits

- This is not a schema validator. It does not enforce email formats, dates, currencies, or required business fields.
- It removes exact duplicates after trimming whitespace. It does not fuzzy-match near-duplicates.
- It pads short rows and ignores extra cells beyond the header width. A production workflow should report those cases instead of silently accepting them.
- Quoted CSV fields must follow normal CSV rules. A quote preceded by unquoted whitespace is treated as part of the value by Python's CSV parser.
- It does not upload or transmit data anywhere.

## Tests

From the project root:

```bash
python -m unittest demos.csv_cleanup.test_clean_csv
```

The tests cover header normalisation, duplicate removal, empty-column removal, short-row padding, delimiter detection, and the command-line output and report.
