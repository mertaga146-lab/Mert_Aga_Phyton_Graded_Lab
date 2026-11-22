"""Reading CSV files into flight records and error messages."""
import csv
import os
from validator import validate_row, to_record


def parse_files(paths: list[str], airports: set[str]) -> tuple[list[dict], list[str]]:
    """Process the CSV files in the order given.

    Return (records, errors):
      records - valid flight records, in input order
      errors  - one message per invalid row, in input order, formatted as
                "<file name>:<line number>: <ERROR_CODE> | <free text>"
                (base file name only, no timestamp or level, no newline)

    Also performs the DUPLICATE_FLIGHT check across all the files.
    Does not write any files and does not log anything itself.
    """
    records = []
    errors = []
    seen = set()

    for path in paths:
        name = os.path.basename(path)
        with open(path, encoding="utf-8", newline=None) as f:
            for lineno, line in enumerate(f, start=1):
                if lineno == 1:
                    continue

                text = line.strip()
                if not text or text.startswith("#"):
                    continue

                fields = next(csv.reader([text]))
                code = validate_row(fields, airports)

                if code is None:
                    record = to_record(fields)
                    key = (record["flight_id"], record["departure_datetime"])

                    if key in seen:
                        errors.append(f"{name}:{lineno}: DUPLICATE_FLIGHT | {text}")
                    else:
                        seen.add(key)
                        records.append(record)
                else:
                    errors.append(f"{name}:{lineno}: {code} | {text}")

    return records, errors