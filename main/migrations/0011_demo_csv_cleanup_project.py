import datetime

from django.db import migrations

BODY = """
<p><strong>This is a self-built demonstration project, not client work.</strong> It exists to show a practical approach to a common problem: exported spreadsheets often contain padded headers, blank rows, duplicate records, and columns nobody uses.</p>

<h2>The problem</h2>
<p>A business exports data from an internal system. The file opens with inconsistent headers, extra whitespace, blank rows, duplicate records, and at least one empty column. Before the data can be imported, reported on, or reviewed, someone has to clean it by hand.</p>

<h2>What the tool does</h2>
<ul>
  <li>Detects comma, semicolon, tab, or pipe delimiters from the header row.</li>
  <li>Trims whitespace and normalises headers to lowercase snake_case.</li>
  <li>Gives duplicate headers unique names.</li>
  <li>Removes blank rows and exact duplicate records while preserving order.</li>
  <li>Drops columns with no data unless the user asks to keep them.</li>
  <li>Writes a cleaned CSV and an optional JSON summary report.</li>
</ul>

<h2>Example run</h2>
<pre><code>python clean_csv.py sample_input.csv -o sample_output.csv --report sample_report.json

4 input rows -&gt; 2 output rows; 1 duplicates removed; 1 empty columns removed.</code></pre>

<p>The sample input has five columns. The cleaned output has four: <code>name</code>, <code>email</code>, <code>phone</code>, and <code>notes</code>. The unused column is removed, the duplicate row is dropped, and the notes field is normalised.</p>

<h2>Implementation notes</h2>
<p>The tool uses only the Python standard library: <code>csv</code>, <code>argparse</code>, <code>json</code>, and <code>pathlib</code>. That keeps the demonstration easy to run and audit. The test suite covers header normalisation, duplicate removal, empty-column handling, short-row padding, delimiter detection, and the command-line workflow.</p>

<h2>Scope and limitations</h2>
<ul>
  <li>It does not validate business rules such as email formats, dates, currencies, or required fields.</li>
  <li>It removes exact duplicates after trimming whitespace; it does not fuzzy-match near-duplicates.</li>
  <li>It pads short rows and ignores extra cells beyond the header width. A production workflow should surface those cases to the user.</li>
  <li>It does not upload or transmit data anywhere; it runs locally on the files provided.</li>
</ul>

<p>The full source, sample files, and tests live in the repository under <code>demos/csv_cleanup/</code>.</p>
"""


def create_demo_project(apps, schema_editor):
    Portfolio = apps.get_model("main", "Portfolio")
    Portfolio.objects.get_or_create(
        slug="csv-cleanup-utility",
        defaults={
            "name": "CSV Cleanup Utility",
            "description": (
                "A Python command-line tool that turns messy CSV exports into "
                "clean, consistent data and a summary report."
            ),
            "body": BODY,
            "date": datetime.datetime(2026, 10, 22, tzinfo=datetime.timezone.utc),
            "is_active": True,
            "is_featured": True,
            "is_demo": True,
            "technologies": "Python, CSV, unittest",
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0010_service_inquiry_qualification"),
    ]

    operations = [
        migrations.RunPython(create_demo_project, migrations.RunPython.noop),
    ]
