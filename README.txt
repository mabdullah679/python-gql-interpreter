PYTHON-GQL-INTERPRETER

Despite the name, this does not run or check GraphQL. It is one small Python script that reads a GraphQL schema file, goes through it line by line, and writes a spreadsheet-style CSV file listing every field and its description.

What you need: Python 3.9 or newer. Nothing else to install, and no network.

How to run it: open a terminal in the project folder and run: python3 parse_schema_to_csv.py. It reads schema.gql and writes schema_fields.csv, then prints "Parsed schema.gql -> schema_fields.csv". The two file names are fixed in the script and looked up in the folder you run it from. To use a different schema, edit those two names or call the schema_to_csv function from your own Python. If schema.gql is missing, Python stops with a FileNotFoundError.

What it does: for each field line inside a { } block (including fields with arguments) it writes one row with the field name and the description written just above it in triple quotes (blank if there is none). Fields named "id" are skipped on purpose. Lines outside braces are ignored. The included sample schema gives 3 rows: userId, displayName, email. Limits: only triple-quote descriptions are read (not # comments), enums and unions get no special handling, and nothing is validated.

Tests: run python3 -m unittest discover -s tests -v. There are 7 tests covering the sample schema, skipping id, arguments, multi-line descriptions, descriptions not leaking onto the next field, lines outside braces, and the CSV file. They need nothing external. The GitHub workflow runs them plus a secret scan.

Where things are: parse_schema_to_csv.py is the script, schema.gql is the sample input, tests/ holds the tests. The generated .csv is ignored by git.
