"""Flight Schedule Parser and Query Tool - command-line entry point.

Run from the project folder, for example:
    python flight_parser.py -i data/db.csv -a data/airports.txt
"""
import sys
import os
import argparse
import json
import logging
from datetime import datetime

from validator import load_airports
from csv_loader import parse_files
from query import run_queries

STUDENT_ID = "241ADB159"
FIRST_NAME = "Mert"
LAST_NAME = "Aga"


def read_json(path: str):
    with open(path, encoding="utf-8") as f:
        try:
            return json.load(f)
        except ValueError as exc:
            raise ValueError(f"{path} is not valid JSON: {exc}")


def build_database(args) -> list[dict]:
    db_path = args.o or "db.json"
    log_path = os.path.join(os.path.dirname(db_path), "errors.log")

    logger = logging.getLogger("flight_parser")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)

    try:
        airports = load_airports(args.a)

        if args.i is not None:
            paths = [args.i]
        else:
            names = sorted(n for n in os.listdir(args.d)
                           if n.endswith(".csv")
                           and os.path.isfile(os.path.join(args.d, n)))
            if not names:
                raise ValueError(f"no .csv files found in {args.d}")
            paths = [os.path.join(args.d, n) for n in names]

        records, errors = parse_files(paths, airports)

        for message in errors:
            logger.warning(message)

        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)
    finally:
        logger.removeHandler(handler)
        handler.close()

    print(len(records), len(errors))
    return records


def main(argv: list[str] | None = None) -> int:
    """Run the whole program and return the exit code (0, 1 or 2).

    argv is the argument list without the program name.
    None means use sys.argv[1:] (argparse does this for you).
    Do not call sys.exit() inside main(); return the code instead.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i")
    parser.add_argument("-d")
    parser.add_argument("-j")
    parser.add_argument("-a")
    parser.add_argument("-o")
    parser.add_argument("-q")
    parser.add_argument("-r")

    try:
        args = parser.parse_args(argv)
        sources = [s for s in (args.i, args.d, args.j) if s is not None]
        if len(sources) != 1:
            parser.error("exactly one of -i, -d or -j is required")
        if args.j is None and args.a is None:
            parser.error("-a is required with -i and -d")
        if args.j is not None and args.o is not None:
            parser.error("-o cannot be used with -j")
    except SystemExit as exc:
        return exc.code if isinstance(exc.code, int) else 2

    try:
        if args.j is not None:
            db = read_json(args.j)
            if not isinstance(db, list) or not all(isinstance(r, dict) for r in db):
                raise ValueError(f"{args.j}: the database must be a JSON array of objects")
        else:
            db = build_database(args)

        if args.q is not None:
            queries = read_json(args.q)
            if not isinstance(queries, (dict, list)):
                raise ValueError(f"{args.q}: queries must be a JSON object or array")

            response = run_queries(db, queries)

            stamp = datetime.now().strftime("%Y%m%d_%H%M")
            name = f"response_{STUDENT_ID}_{FIRST_NAME}_{LAST_NAME}_{stamp}.json"
            folder = args.r or "."
            with open(os.path.join(folder, name), "w", encoding="utf-8") as f:
                json.dump(response, f, indent=2)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())