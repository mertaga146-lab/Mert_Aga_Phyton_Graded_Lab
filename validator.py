"""Row validation: airport list loading, single-row checks, record building."""
import re
import math
from datetime import datetime

def load_airports(path: str) -> set[str]:
    """Read an airport list file and return the set of codes.

    One code per line. Strip whitespace; skip blank lines and lines
    starting with '#'.
    """
    codes = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            codes.add(line)
    return codes

def parse_datetime(text: str):
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}", text):
        return None
    try:
        return datetime.strptime(text, "%Y-%m-%d %H:%M")
    except ValueError:
        return None

def validate_row(fields: list[str], airports: set[str]) -> str | None:
    """Check one CSV row ...
    """
    if len(fields) != 6:
        return "WRONG_FIELD_COUNT"

    f = [x.strip() for x in fields]
    if any(x == "" for x in f):
        return "MISSING_FIELD"

    if not re.fullmatch(r"[A-Za-z0-9]{2,8}", f[0]):
        return "INVALID_FLIGHT_ID"

    if not re.fullmatch(r"[A-Z]{3}", f[1]) or f[1] not in airports:
        return "INVALID_ORIGIN"
    
    if not re.fullmatch(r"[A-Z]{3}", f[2]) or f[2] not in airports:
        return "INVALID_DESTINATION"

    if f[1] == f[2]:
        return "SAME_ORIGIN_DESTINATION"

    dep = parse_datetime(f[3])
    if dep is None:
        return "INVALID_DEPARTURE"

    arr = parse_datetime(f[4])
    if arr is None:
        return "INVALID_ARRIVAL"

    if arr <= dep:
        return "ARRIVAL_NOT_AFTER_DEPARTURE"
        
    try:
        price = float(f[5])
    except ValueError:
        return "INVALID_PRICE"

    if not math.isfinite(price):
        return "INVALID_PRICE"

    if price <= 0:
        return "NON_POSITIVE_PRICE"

    return None


def to_record(fields: list[str]) -> dict:
    f = [x.strip() for x in fields]
    return {
        "flight_id": f[0],
        "origin": f[1],
        "destination": f[2],
        "departure_datetime": f[3],
        "arrival_datetime": f[4],
        "price": float(f[5]),
    }