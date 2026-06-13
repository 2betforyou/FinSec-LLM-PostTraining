import csv
import json
import tempfile
import unittest
from pathlib import Path

from src.data.make_sft_from_csv import main


class MakeSftFromCsvTest(unittest.TestCase):
    def test_converts_mcq_and_short_rows_to_chat_jsonl(self):
        rows = [
            {
                "type": "MCQ",
                "question": "Which control is most related to access management?",
                "options": "1. Encryption 2. Identity verification",
                "answer": "2",
            },
            {
                "type": "SHORT",
                "question": "What should the model do if evidence is insufficient?",
                "options": "",
                "answer": "Avoid unsupported conclusions.",
            },
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "input.csv"
            out_path = Path(tmpdir) / "output.jsonl"

            with csv_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(
                    handle, fieldnames=["type", "question", "options", "answer"]
                )
                writer.writeheader()
                writer.writerows(rows)

            main(str(csv_path), str(out_path))

            examples = [
                json.loads(line)
                for line in out_path.read_text(encoding="utf-8").splitlines()
            ]

        self.assertEqual(len(examples), 2)
        self.assertEqual(examples[0]["messages"][1]["role"], "user")
        self.assertIn("Identity verification", examples[0]["messages"][1]["content"])
        self.assertEqual(examples[0]["messages"][2]["content"], "2")
        self.assertEqual(
            examples[1]["messages"][2]["content"], "Avoid unsupported conclusions."
        )


if __name__ == "__main__":
    unittest.main()
