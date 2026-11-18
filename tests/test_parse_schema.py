"""Run: python3 -m unittest discover -s tests -v"""
import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from parse_schema_to_csv import parse_schema_fields, schema_to_csv  # noqa: E402


class ParseSchemaTest(unittest.TestCase):
    def test_bundled_schema(self):
        fields = parse_schema_fields((ROOT / "schema.gql").read_text(encoding="utf-8"))
        self.assertEqual([f for f, _ in fields], ["userId", "displayName", "email"])
        self.assertEqual(fields[0][1], "Unique identifier for the user")

    def test_id_is_skipped(self):
        self.assertEqual(parse_schema_fields('type T {\n  id: ID!\n  name: String\n}'), [("name", "")])

    def test_field_with_arguments(self):
        self.assertEqual(parse_schema_fields('type Q {\n  user(id: ID!): User\n}'), [("user", "")])

    def test_multiline_description(self):
        s = 'type T {\n  """\n  Line one\n  Line two\n  """\n  name: String\n}'
        self.assertEqual(parse_schema_fields(s), [("name", "Line one\nLine two")])

    def test_description_does_not_leak_to_next_field(self):
        s = 'type T {\n  """First"""\n  a: String\n  b: String\n}'
        self.assertEqual(parse_schema_fields(s), [("a", "First"), ("b", "")])

    def test_lines_outside_blocks_ignored(self):
        self.assertEqual(parse_schema_fields("scalar Date\nname: String"), [])

    def test_csv_output(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "o.csv"
            schema_to_csv(ROOT / "schema.gql", out)
            rows = list(csv.reader(out.open(encoding="utf-8")))
        self.assertEqual(rows[0], ["FieldName", "Description"])
        self.assertEqual(len(rows), 4)


if __name__ == "__main__":
    unittest.main()
