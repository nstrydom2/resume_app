"""Clean a CSV file and write a summary report.

This is a self-built demonstration, not client work.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple


def normalise_header(value: str, index: int, used: set[str]) -> str:
    header = re.sub(r"[^a-z0-9]+", "_", (value or "").strip().lower()).strip("_")
    if not header:
        header = f"column_{index}"
    candidate = header
    suffix = 2
    while candidate in used:
        candidate = f"{header}_{suffix}"
        suffix += 1
    used.add(candidate)
    return candidate


def _count_outside_quotes(line: str, delimiter: str) -> int:
    in_quotes = False
    count = 0
    for character in line:
        if character == '"':
            in_quotes = not in_quotes
        elif character == delimiter and not in_quotes:
            count += 1
    return count


def detect_delimiter(sample: str) -> str:
    first_line = next(
        (line for line in sample.splitlines() if line.strip()), ""
    )
    counts = {
        delimiter: _count_outside_quotes(first_line, delimiter)
        for delimiter in (",", ";", "\t", "|")
    }
    delimiter, count = max(counts.items(), key=lambda item: item[1])
    return delimiter if count else ","


def read_rows(path: Path) -> Tuple[List[List[str]], str, int]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        sample = handle.read(8192)
        if not sample.strip():
            raise ValueError("The input file is empty.")
        handle.seek(0)
        delimiter = detect_delimiter(sample)
        rows: List[List[str]] = []
        blank_rows_removed = 0
        for row in csv.reader(handle, delimiter=delimiter):
            cleaned = [cell.strip() for cell in row]
            if any(cleaned):
                rows.append(cleaned)
            else:
                blank_rows_removed += 1
    if not rows:
        raise ValueError("The input file does not contain any rows.")
    return rows, delimiter, blank_rows_removed


def clean_rows(
    rows: Sequence[Sequence[str]], keep_empty_columns: bool = False
) -> Tuple[List[str], List[List[str]], dict]:
    raw_headers = list(rows[0])
    used: set[str] = set()
    headers = [
        normalise_header(value, index + 1, used)
        for index, value in enumerate(raw_headers)
    ]

    data = []
    duplicates = 0
    seen = set()
    for row in rows[1:]:
        values = [str(cell).strip() for cell in row[: len(headers)]]
        values.extend([""] * (len(headers) - len(values)))
        key = tuple(values)
        if key in seen:
            duplicates += 1
            continue
        seen.add(key)
        data.append(values)

    dropped_headers: List[str] = []
    if not keep_empty_columns and data:
        keep_indexes = [
            index
            for index in range(len(headers))
            if any(row[index] for row in data)
        ]
        if len(keep_indexes) != len(headers):
            dropped_headers = [
                headers[index]
                for index in range(len(headers))
                if index not in keep_indexes
            ]
            headers = [headers[index] for index in keep_indexes]
            data = [[row[index] for index in keep_indexes] for row in data]

    report = {
        "input_rows": max(len(rows) - 1, 0),
        "output_rows": len(data),
        "blank_rows_removed": 0,
        "duplicate_rows_removed": duplicates,
        "empty_columns_removed": len(dropped_headers),
        "dropped_columns": dropped_headers,
        "columns": headers,
    }
    return headers, data, report


def write_csv(path: Path, headers: Sequence[str], rows: Iterable[Sequence[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Clean headers, whitespace, blank rows, and duplicate rows in a CSV file."
    )
    parser.add_argument("input", type=Path, help="Path to the source CSV file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Path for the cleaned CSV (default: <input>_cleaned.csv)",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Optional path for a JSON summary report",
    )
    parser.add_argument(
        "--keep-empty-columns",
        action="store_true",
        help="Keep columns that contain no data",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    source = args.input
    if not source.is_file():
        parser.error(f"Input file not found: {source}")

    try:
        rows, _, blank_rows_removed = read_rows(source)
        headers, data, report = clean_rows(
            rows, keep_empty_columns=args.keep_empty_columns
        )
        report["input_rows"] += blank_rows_removed
        report["blank_rows_removed"] = blank_rows_removed
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        print(f"Could not clean {source}: {exc}", file=sys.stderr)
        return 1

    output = args.output or source.with_name(f"{source.stem}_cleaned.csv")
    write_csv(output, headers, data)

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    print(f"Wrote {output}")
    print(
        f"{report['input_rows']} input rows -> {report['output_rows']} output rows; "
        f"{report['duplicate_rows_removed']} duplicates removed; "
        f"{report['empty_columns_removed']} empty columns removed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
