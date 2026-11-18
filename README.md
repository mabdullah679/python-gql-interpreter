# python-gql-interpreter

A small stdlib-only Python script that reads a GraphQL schema (SDL) and writes a CSV of every field with its description. Despite the repo name it does not execute or validate GraphQL; it scans the schema text line by line.

```
schema.gql --> parse_schema_to_csv.py --> schema_fields.csv (FieldName, Description)
```

Not local/contained: nothing; no network or services.

## Prerequisites
- Python 3.9+ (uses `list[tuple[str, str]]` annotations; tested on 3.14). No packages to install.

## Run it
1. From the repo root: `python3 parse_schema_to_csv.py`
2. Open `schema_fields.csv` (printed: `Parsed schema.gql -> schema_fields.csv`).

Input and output file names are hard-coded in the `__main__` block and resolved against the current directory, so run it from the folder containing `schema.gql`. To use another schema, call `schema_to_csv(Path("other.gql"), Path("out.csv"))` from Python or edit those two paths. If `schema.gql` is missing you get a `FileNotFoundError`.

## What it does
| Input | Output row |
|---|---|
| Field line inside a `{ ... }` block, e.g. `email: String!` | `email,<preceding description>` |
| Field with arguments, e.g. `user(id: ID!): User` | `user,<description>` |
| Field named `id` | skipped |
| `"""single-line"""` or multi-line `"""` block before a field | used as that field's description (blank if none) |
| Lines outside braces (e.g. `scalar Date`) | ignored |

The bundled [schema.gql](schema.gql) yields 3 rows (`userId`, `displayName`, `email`). Limitations: `"""` descriptions only (no `#` comments), no enum values or union members handling, no validation.

## Tests
`python3 -m unittest discover -s tests -v`: 7 tests in [tests/test_parse_schema.py](tests/test_parse_schema.py) (bundled schema, `id` skipping, arguments, multi-line descriptions, no description leak between fields, outside-brace lines, CSV file). No external services. CI: [ci.yml](.github/workflows/ci.yml).

## Layout
| Path | Role |
|---|---|
| [parse_schema_to_csv.py](parse_schema_to_csv.py) | `parse_schema_fields` and `schema_to_csv` |
| [schema.gql](schema.gql) | sample input |
| [tests](tests) | unit tests |
