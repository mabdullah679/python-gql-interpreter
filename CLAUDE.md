# python-gql-interpreter

One-file Python 3 tool (stdlib only) that reads a GraphQL SDL file and writes a CSV of field names and descriptions. It is a line-based text parser, not a GraphQL parser/interpreter. Global rules: `~/.claude/CLAUDE.md`.

## Commands (run from the repo root; paths are relative to the current directory)
- Run: `python3 parse_schema_to_csv.py` reads `schema.gql`, writes `schema_fields.csv`
- Tests: `python3 -m unittest discover -s tests -v` (7 tests)

## Conventions / don't
- Fields named `id` are skipped on purpose (tests pin this).
- `*.csv` is gitignored; never commit generated output.
- Do not describe it as a GraphQL interpreter: no queries are executed and no validation happens.
- Branch + PR only; never push to `main`.
