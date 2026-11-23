# AI Usage Disclosure

## Tools used

- Claude (Claude Sonnet 5.5), in claude.ai

## Conversation links

- Link 1: https://claude.ai/share/10a97e95-8e0d-497a-a4ea-3a71f9cd7f3d

## What I used them for

- Understanding the assignment pitfalls: why `isalnum()`, `isupper()` and `strptime` are not enough on their own, why a boolean counts as an int in Python, how to clean up the logging handler with `try/finally`, and how argparse produces exit code 2.
- Getting a list of edge cases to test `validate_row` with.
- Getting a starting version of the validation part of `query.py`.
- Having my code reviewed part by part, and having the public tests run against it.

## Which parts of the code were AI-generated or substantially AI-assisted

| File | Function or part | How (generated / modified / explained) |
| --- | --- | --- |
| validator.py | `load_airports`, `validate_row`, `to_record` | Explained (pitfalls and an edge-case test script); code written by me |
| csv_loader.py | `parse_files` | Explained (outline of the steps); code written by me, then reviewed |
| query.py | constants, `_is_datetime_text`, `_is_number`, `_is_valid_query`, `run_queries`, invalid-query branch of `run_query` | Generated, then I used it in my file |
| query.py | filtering, sorting and limit in `run_query` | Written by me, then reviewed |
| flight_parser.py | whole file | Explained (outline of the structure); code written by me, then reviewed |

## Key prompts

1. "we will do this with you. I will need your help with the parts I struggle." (with the assignment text and the starter files)
2. Sending my `csv_loader.py` and `flight_parser.py` in parts and asking Claude to check them.
3. "can you start the file" (for `query.py`)

## What I changed or verified myself

I wrote `validator.py`, `csv_loader.py`, the filtering, sorting and limit in `query.py`, and all of `flight_parser.py` myself. I ran the public test script, and all test groups (A to H) pass.