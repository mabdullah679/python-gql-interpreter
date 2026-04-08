import csv
import re
from pathlib import Path


def parse_schema_fields(schema_text: str) -> list[tuple[str, str]]:
    """Extract (field_name, description) pairs from a GraphQL schema string."""
    fields: list[tuple[str, str]] = []
    pending_description = ""

    lines = schema_text.splitlines()
    i = 0
    brace_depth = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Track block nesting so we only parse field lines inside type blocks.
        brace_depth += stripped.count("{")

        if stripped.startswith('"""'):
            desc_lines = []

            # Single-line triple-quoted description.
            if stripped.count('"""') >= 2 and stripped != '"""':
                content = stripped.strip('"')
                pending_description = content.strip()
            else:
                # Multi-line triple-quoted description.
                first_part = stripped[3:]
                if first_part:
                    desc_lines.append(first_part)

                i += 1
                while i < len(lines):
                    current = lines[i]
                    if '"""' in current:
                        closing_index = current.find('"""')
                        desc_lines.append(current[:closing_index])
                        break
                    desc_lines.append(current)
                    i += 1

                pending_description = "\n".join(part.strip() for part in desc_lines).strip()

            i += 1
            continue

        if brace_depth > 0:
            # Match field definitions like: fieldName(arg: Type): ReturnType!
            match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*(\([^)]*\))?\s*:", stripped)
            if match:
                field_name = match.group(1)
                if field_name != "id":
                    fields.append((field_name, pending_description))
                pending_description = ""

        brace_depth -= stripped.count("}")
        i += 1

    return fields


def schema_to_csv(schema_path: Path, csv_path: Path) -> None:
    schema_text = schema_path.read_text(encoding="utf-8")
    rows = parse_schema_fields(schema_text)

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["FieldName", "Description"])
        writer.writerows(rows)


if __name__ == "__main__":
    input_schema = Path("schema.gql")
    output_csv = Path("schema_fields.csv")

    schema_to_csv(input_schema, output_csv)
    print(f"Parsed {input_schema} -> {output_csv}")
