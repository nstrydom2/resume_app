"""Service catalogue and shared inquiry choices.

Keep service definitions here so the homepage, /services/, landing pages, and
contact form stay in sync. This module must not import Django models.
"""

CONTACT_SERVICE_CHOICES = [
    ("spreadsheet-data", "Spreadsheet & CSV automation"),
    ("pdf-extraction", "PDF & document data extraction"),
    ("python-automation", "Python & office automation"),
    ("api-integration", "API integration & workflow automation"),
    ("django-development", "Django / web application development"),
    ("web-data", "Web data collection & monitoring"),
    ("ai-workflow", "AI & document workflow automation"),
    ("embedded-technical", "Embedded / technical engineering"),
    ("other", "Something else / not sure yet"),
]

CONTACT_SERVICE_LABELS = dict(CONTACT_SERVICE_CHOICES)

BUDGET_CHOICES = [
    ("", "Prefer not to say yet"),
    ("small-fixed", "Small fixed-scope task"),
    ("automation-project", "Automation project"),
    ("development-project", "Larger development project"),
    ("troubleshooting", "Troubleshooting / diagnostic work"),
    ("not-sure", "Not sure yet"),
]

CONTACT_METHOD_CHOICES = [
    ("", "No preference"),
    ("email", "Email"),
    ("call", "Phone or video call"),
]

DEFAULT_PROCESS = [
    (
        "Assess",
        "We start with the process, sample inputs, and the outcome you need. "
        "I confirm whether the work is a good fit before quoting.",
    ),
    (
        "Agree on scope",
        "We agree on the deliverable, assumptions, limitations, and how "
        "changes will be handled.",
    ),
    (
        "Build",
        "I build the smallest reliable solution that solves the problem, with "
        "clear checkpoints rather than a long silent stretch.",
    ),
    (
        "Test",
        "The solution is checked against representative samples, including "
        "edge cases and rejected records.",
    ),
    (
        "Deliver",
        "You receive the working files, a short handover, and clear next steps "
        "for running or maintaining the solution.",
    ),
]

SERVICE_GROUPS = [
    {
        "key": "office-data",
        "title": "Office & data automation",
        "eyebrow": "Best starting point",
        "description": (
            "Replace recurring spreadsheet, document, and reporting work with a "
            "repeatable process your team can run without manual copy-paste."
        ),
        "icon": "sheet",
        "items": [
            {
                "name": "Excel, CSV & spreadsheet automation",
                "service": "spreadsheet-data",
                "detail": "spreadsheet-data",
            },
            {
                "name": "Spreadsheet cleanup, merging, validation & reconciliation",
                "service": "spreadsheet-data",
                "detail": "spreadsheet-data",
            },
            {
                "name": "PDF data extraction into spreadsheets or databases",
                "service": "pdf-extraction",
                "detail": "pdf-extraction",
            },
            {
                "name": "Invoice, report & document processing",
                "service": "pdf-extraction",
            },
            {
                "name": "Bulk file renaming, sorting, conversion & archiving",
                "service": "python-automation",
                "detail": "python-automation",
            },
            {
                "name": "Automated report generation",
                "service": "python-automation",
                "detail": "python-automation",
            },
            {
                "name": "Email attachment & document workflows",
                "service": "python-automation",
            },
            {
                "name": "Form-to-spreadsheet or form-to-database workflows",
                "service": "python-automation",
            },
            {
                "name": "Data imports, exports, deduplication & transformation",
                "service": "spreadsheet-data",
            },
        ],
        "cta_service": "spreadsheet-data",
    },
    {
        "key": "software-backend",
        "title": "Software & backend development",
        "eyebrow": "Build or repair",
        "description": (
            "Custom software, internal tools, and fixes for applications that "
            "have become slow, fragile, or difficult to change."
        ),
        "icon": "code",
        "items": [
            {
                "name": "Python scripting & custom utilities",
                "service": "python-automation",
                "detail": "python-automation",
            },
            {
                "name": "Django applications & web portals",
                "service": "django-development",
            },
            {
                "name": "REST API development & integration",
                "service": "api-integration",
                "detail": "api-integration",
            },
            {
                "name": "PostgreSQL & SQL database work",
                "service": "django-development",
            },
            {
                "name": "Legacy application maintenance",
                "service": "django-development",
            },
            {
                "name": "Bug fixing, performance investigation & refactoring",
                "service": "django-development",
            },
            {
                "name": "Internal business tools & admin dashboards",
                "service": "django-development",
            },
            {
                "name": "Scheduled jobs & background processing",
                "service": "python-automation",
            },
        ],
        "cta_service": "django-development",
    },
    {
        "key": "web-data",
        "title": "Web data & system integration",
        "eyebrow": "Connect the dots",
        "description": (
            "Collect permitted public data and keep business systems in sync, "
            "with clear limits around access, privacy, and rate limits."
        ),
        "icon": "globe",
        "items": [
            {
                "name": "Website data scraping where permitted",
                "service": "web-data",
            },
            {
                "name": "Public catalogue & directory data collection",
                "service": "web-data",
            },
            {
                "name": "Structured extraction from HTML & public pages",
                "service": "web-data",
            },
            {
                "name": "API-based data collection",
                "service": "api-integration",
                "detail": "api-integration",
            },
            {
                "name": "Data normalization & enrichment",
                "service": "spreadsheet-data",
                "detail": "spreadsheet-data",
            },
            {
                "name": "Scheduled data feeds & synchronization",
                "service": "api-integration",
                "detail": "api-integration",
            },
            {
                "name": "Integrations between business applications",
                "service": "api-integration",
                "detail": "api-integration",
            },
            {
                "name": "Monitoring for changes to public web pages",
                "service": "web-data",
            },
        ],
        "cta_service": "api-integration",
    },
    {
        "key": "ai-workflow",
        "title": "AI & workflow automation",
        "eyebrow": "Practical, human-reviewed",
        "description": (
            "Local and API-based AI workflows for documents and repetitive "
            "classification, with human review where accuracy matters."
        ),
        "icon": "spark",
        "items": [
            {
                "name": "Local AI & Ollama setup",
                "service": "ai-workflow",
            },
            {
                "name": "Private document search & retrieval prototypes",
                "service": "ai-workflow",
            },
            {
                "name": "AI-assisted document classification & summarization",
                "service": "ai-workflow",
            },
            {
                "name": "Integration of AI APIs into existing workflows",
                "service": "ai-workflow",
            },
            {
                "name": "Automated text extraction & categorization",
                "service": "ai-workflow",
            },
            {
                "name": "Human-reviewed AI processing pipelines",
                "service": "ai-workflow",
            },
            {
                "name": "Open-source coding assistant & development environment setup",
                "service": "ai-workflow",
            },
        ],
        "cta_service": "ai-workflow",
    },
    {
        "key": "embedded-technical",
        "title": "Embedded & technical engineering",
        "eyebrow": "Software, not board repair",
        "description": (
            "Diagnostics, test tooling, and compatibility work around embedded "
            "devices and industrial equipment. Physical board-level repair is "
            "out of scope."
        ),
        "icon": "chip",
        "items": [
            {
                "name": "Embedded C/C++ debugging",
                "service": "embedded-technical",
            },
            {
                "name": "Python hardware test utilities",
                "service": "embedded-technical",
            },
            {
                "name": "Serial communication & protocol troubleshooting",
                "service": "embedded-technical",
            },
            {
                "name": "Modbus integration & test tooling",
                "service": "embedded-technical",
            },
            {
                "name": "Test automation for electronics & industrial devices",
                "service": "embedded-technical",
            },
            {
                "name": "Diagnostic utilities & data logging",
                "service": "embedded-technical",
            },
            {
                "name": "Reverse engineering & compatibility investigation",
                "service": "embedded-technical",
            },
            {
                "name": "Technical prototypes & proof-of-concept tools",
                "service": "embedded-technical",
            },
        ],
        "cta_service": "embedded-technical",
    },
]

PRIORITY_SERVICE_SLUGS = [
    "spreadsheet-data",
    "pdf-extraction",
    "api-integration",
    "python-automation",
]

SERVICE_DETAILS = {
    "spreadsheet-data": {
        "slug": "spreadsheet-data",
        "name": "Spreadsheet & CSV automation",
        "short_name": "Spreadsheet & data",
        "eyebrow": "Office & data automation",
        "icon": "sheet",
        "tagline": "Clean, combine, validate, and transform data without the manual copy-paste.",
        "meta_title": "Spreadsheet & CSV Automation",
        "meta_description": (
            "Automate spreadsheet cleanup, CSV merging, validation, "
            "deduplication, and recurring reporting with a repeatable workflow."
        ),
        "problem": (
            "Monthly exports arrive with different headers, inconsistent dates, "
            "duplicate rows, and values that need checking by hand. The work is "
            "slow, easy to get wrong, and difficult to repeat consistently."
        ),
        "examples": [
            "Combine monthly CSV exports into one normalized dataset.",
            "Reconcile two spreadsheets and flag records that do not match.",
            "Remove duplicates, validate emails and dates, and produce a rejected-records report.",
            "Turn a manual weekly reporting process into one repeatable command.",
            "Convert inconsistent Excel workbooks into a clean import file for another system.",
        ],
        "deliverables": [
            "A working script or spreadsheet workflow you can run again.",
            "A merged, normalized output file in the format you need.",
            "A validation report showing rejected or unmatched records.",
            "A short handover explaining inputs, assumptions, and how to rerun it.",
        ],
        "inputs": [
            "One or two representative input files with sensitive values removed if possible.",
            "A description of the current manual process and the desired output.",
            "The rules for duplicates, required fields, and acceptable values.",
            "Any volume or frequency expectations.",
        ],
        "limitations": [
            "I do not guess business rules that are not documented.",
            "Source files still need to be supplied in a usable format.",
            "Very large datasets may need a database or batch-processing approach.",
        ],
        "related_projects": ["csv-cleanup-utility"],
        "starting_point": (
            "Share a sample export and the output you currently build by hand. "
            "I will confirm whether a fixed-scope automation is practical."
        ),
    },
    "pdf-extraction": {
        "slug": "pdf-extraction",
        "name": "PDF & document data extraction",
        "short_name": "PDF extraction",
        "eyebrow": "Office & data automation",
        "icon": "document",
        "tagline": "Turn recurring invoices, statements, forms, and reports into structured data.",
        "meta_title": "PDF & Document Data Extraction",
        "meta_description": (
            "Extract structured fields from PDFs and documents into CSV, JSON, "
            "or a database, with validation and a manual-review path."
        ),
        "problem": (
            "Important information arrives as PDFs or documents, then someone "
            "retypes it into a spreadsheet or business system. The process is "
            "repetitive, error-prone, and hard to audit."
        ),
        "examples": [
            "Extract invoice number, date, supplier, line items, and totals from recurring invoices.",
            "Pull statement balances and transaction rows into a structured file.",
            "Read application forms or reports and export the fields you need.",
            "Flag low-confidence extractions for a person to review.",
            "Process a batch of documents and produce a summary of failures.",
        ],
        "deliverables": [
            "Extracted fields in CSV, JSON, or an agreed database format.",
            "A validation report for missing, malformed, or low-confidence records.",
            "A manual-review queue for documents that need a person.",
            "A repeatable process and short handover.",
        ],
        "inputs": [
            "A representative sample of documents, with sensitive data redacted where possible.",
            "The exact fields you need and how each field should be formatted.",
            "The expected volume and how often documents arrive.",
            "The rules for handling missing or ambiguous values.",
        ],
        "limitations": [
            "Scanned or poor-quality documents may need OCR and manual review.",
            "Extraction accuracy depends on document consistency.",
            "I do not process documents you are not authorised to share.",
            "Sensitive documents can be handled through an agreed secure transfer method.",
        ],
        "related_projects": [],
        "starting_point": (
            "Send one sample document and the fields you need. I will assess "
            "whether the documents are consistent enough for reliable extraction."
        ),
    },
    "api-integration": {
        "slug": "api-integration",
        "name": "API integration & workflow automation",
        "short_name": "API integration",
        "eyebrow": "Web data & system integration",
        "icon": "globe",
        "tagline": "Connect the systems your team already uses and stop moving data by hand.",
        "meta_title": "API Integration & Workflow Automation",
        "meta_description": (
            "Connect business applications, synchronize data, and automate "
            "recurring transfers with clear logging and failure handling."
        ),
        "problem": (
            "Staff copy data between two systems because the systems do not "
            "talk to each other. The transfer is repetitive, easy to miss, and "
            "hard to monitor when something goes wrong."
        ),
        "examples": [
            "Pull records from one API and create or update them in another system.",
            "Schedule a nightly data sync with retries and a failure report.",
            "Map inconsistent field names and formats between two applications.",
            "Collect permitted API data into a spreadsheet or database.",
            "Add logging and alerts around an existing integration.",
        ],
        "deliverables": [
            "A working integration or scheduled sync.",
            "Field mapping and transformation rules.",
            "Logging and a clear failure path for rejected records.",
            "Setup notes and a short handover.",
        ],
        "inputs": [
            "API documentation or the endpoints involved.",
            "Sandbox credentials shared through a secure method, never in chat or source control.",
            "The direction of the sync and how conflicts should be resolved.",
            "Expected volume, schedule, and acceptable failure behavior.",
        ],
        "limitations": [
            "Third-party APIs can change or enforce limits outside my control.",
            "I cannot bypass access controls or terms of service.",
            "Credentials must be shared securely and rotated by the client.",
            "Some integrations require a paid vendor plan or administrator access.",
        ],
        "related_projects": ["anonfile-api"],
        "starting_point": (
            "Describe the two systems and the data that needs to move. Include "
            "the API documentation if you have it, but never send credentials by email."
        ),
    },
    "python-automation": {
        "slug": "python-automation",
        "name": "Python & office automation",
        "short_name": "Python automation",
        "eyebrow": "Office & data automation",
        "icon": "code",
        "tagline": "Replace repetitive file, document, and reporting work with a dependable script.",
        "meta_title": "Python Automation & Custom Utilities",
        "meta_description": (
            "Custom Python scripts and utilities for file workflows, reporting, "
            "data processing, scheduled jobs, and repetitive office tasks."
        ),
        "problem": (
            "A process works, but someone has to repeat it every day or week: "
            "renaming files, moving documents, building reports, or running the "
            "same sequence of manual steps."
        ),
        "examples": [
            "Rename, sort, convert, and archive batches of files.",
            "Generate a recurring report from a folder of inputs.",
            "Extract attachments and route documents to the right place.",
            "Run a scheduled data import, export, or cleanup job.",
            "Build a small internal utility for a task that has no off-the-shelf tool.",
        ],
        "deliverables": [
            "A working Python script or small utility.",
            "Configuration for the paths, schedules, and options that change.",
            "A test run against representative inputs.",
            "A short README and handover so the process is not locked to me.",
        ],
        "inputs": [
            "A description of the current manual steps, in order.",
            "Sample files or folders with sensitive values removed where possible.",
            "The expected schedule and where the output should go.",
            "Any constraints around operating system, permissions, or existing tools.",
        ],
        "limitations": [
            "The script can only automate steps that can be described and tested.",
            "Access to production systems is agreed case by case.",
            "I do not automate actions that violate a provider's terms or access controls.",
            "Ongoing hosting or monitoring is a separate arrangement.",
        ],
        "related_projects": ["csv-cleanup-utility"],
        "starting_point": (
            "Write down the steps you repeat and share one sample input. I will "
            "tell you what can be automated safely and what still needs a human."
        ),
    },
}


def get_service(slug):
    return SERVICE_DETAILS.get(slug)


def get_priority_services():
    return [SERVICE_DETAILS[slug] for slug in PRIORITY_SERVICE_SLUGS]


def get_contact_service_label(value):
    return CONTACT_SERVICE_LABELS.get(value, "General inquiry")
