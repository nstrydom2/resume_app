import csv
import json
import tempfile
import unittest
from pathlib import Path

from demos.csv_cleanup.clean_csv import (
    clean_rows,
    main,
    normalise_header,
    read_rows,
)


class HeaderTests(unittest.TestCase):
    def test_normalises_headers_and_removes_duplicates(self):
        used = set()
        self.assertEqual(normalise_header("  First Name ", 1, used), "first_name")
        self.assertEqual(normalise_header("First  Name", 2, used), "first_name_2")
        self.assertEqual(normalise_header("", 3, used), "column_3")

    def test_removes_punctuation(self):
        used = set()
        self.assertEqual(
            normalise_header("Order # / Date", 1, used), "order_date"
        )


class CleaningTests(unittest.TestCase):
    def test_removes_duplicates_and_empty_columns(self):
        rows = [
            [" Name ", "Email", "Notes", ""],
            [" Alice ", "alice@example.com", " hello ", ""],
            ["Alice", "alice@example.com", "hello", ""],
            [" Bob ", "bob@example.com", " hi ", ""],
        ]

        headers, data, report = clean_rows(rows)

        self.assertEqual(headers, ["name", "email", "notes"])
        self.assertEqual(
            data,
            [
                ["Alice", "alice@example.com", "hello"],
                ["Bob", "bob@example.com", "hi"],
            ],
        )
        self.assertEqual(report["output_rows"], 2)
        self.assertEqual(report["duplicate_rows_removed"], 1)
        self.assertEqual(report["empty_columns_removed"], 1)
        self.assertEqual(report["dropped_columns"], ["column_4"])

    def test_keeps_empty_columns_when_requested(self):
        rows = [
            ["name", "unused"],
            ["Alice", ""],
        ]

        headers, data, report = clean_rows(rows, keep_empty_columns=True)

        self.assertEqual(headers, ["name", "unused"])
        self.assertEqual(data, [["Alice", ""]])
        self.assertEqual(report["empty_columns_removed"], 0)

    def test_pads_short_rows(self):
        rows = [
            ["name", "email", "notes"],
            ["Alice"],
        ]

        headers, data, report = clean_rows(rows, keep_empty_columns=True)

        self.assertEqual(headers, ["name", "email", "notes"])
        self.assertEqual(data, [["Alice", "", ""]])
        self.assertEqual(report["output_rows"], 1)


class FileTests(unittest.TestCase):
    def test_detects_semicolon_delimiter(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.csv"
            path.write_text(
                "name;email\nAlice;alice@example.com\n", encoding="utf-8"
            )

            rows, delimiter, blank_rows_removed = read_rows(path)

        self.assertEqual(delimiter, ";")
        self.assertEqual(
            rows,
            [
                ["name", "email"],
                ["Alice", "alice@example.com"],
            ],
        )
        self.assertEqual(blank_rows_removed, 0)

    def test_cli_writes_clean_file_and_report(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.csv"
            output = Path(directory) / "output.csv"
            report_path = Path(directory) / "report.json"
            source.write_text(
                " Name ,Email,Empty\n Alice ,alice@example.com,\n"
                "Alice,alice@example.com,\n\n",
                encoding="utf-8",
            )

            exit_code = main(
                [str(source), "-o", str(output), "--report", str(report_path)]
            )

            self.assertEqual(exit_code, 0)
            with output.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.reader(handle))
            report = json.loads(report_path.read_text(encoding="utf-8"))

        self.assertEqual(rows, [["name", "email"], ["Alice", "alice@example.com"]])
        self.assertEqual(report["input_rows"], 3)
        self.assertEqual(report["output_rows"], 1)
        self.assertEqual(report["blank_rows_removed"], 1)
        self.assertEqual(report["duplicate_rows_removed"], 1)
        self.assertEqual(report["empty_columns_removed"], 1)


if __name__ == "__main__":
    unittest.main()
