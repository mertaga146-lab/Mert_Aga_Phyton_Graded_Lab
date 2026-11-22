"""Running queries against the flight database."""
from datetime import datetime

RECORD_KEYS = ("flight_id", "origin", "destination",
               "departure_datetime", "arrival_datetime", "price")
STRING_KEYS = {"flight_id", "origin", "destination"}
DATETIME_KEYS = {"departure_datetime", "arrival_datetime"}
NUMBER_KEYS = {"price", "min_price"}
ALLOWED_KEYS = STRING_KEYS | DATETIME_KEYS | NUMBER_KEYS | {"sort_by", "order", "limit"}


def _is_datetime_text(value) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d %H:%M")
    except ValueError:
        return False
    return parsed.strftime("%Y-%m-%d %H:%M") == value


def _is_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_valid_query(query) -> bool:
    if not isinstance(query, dict):
        return False
    for key, value in query.items():
        if key not in ALLOWED_KEYS:
            return False
        if key in STRING_KEYS and not isinstance(value, str):
            return False
        if key in DATETIME_KEYS and not _is_datetime_text(value):
            return False
        if key in NUMBER_KEYS and not _is_number(value):
            return False
        if key == "sort_by" and value not in RECORD_KEYS:
            return False
        if key == "order" and value not in ("asc", "desc"):
            return False
        if key == "limit" and (not isinstance(value, int)
                               or isinstance(value, bool) or value < 0):
            return False
    if "order" in query and "sort_by" not in query:
        return False
    return True


def run_query(db: list[dict], query: dict) -> dict:
    """Return one response entry for one query object.

    Valid query:   {"query": query, "matches": [...]}
    Invalid query: {"query": query, "error": "INVALID_QUERY", "matches": []}
    """
    if not _is_valid_query(query):
        return {"query": query, "error": "INVALID_QUERY", "matches": []}

    matches = []
    for flight in db:
        if "flight_id" in query and flight["flight_id"] != query["flight_id"]:
            continue
        if "origin" in query and flight["origin"] != query["origin"]:
            continue
        if "destination" in query and flight["destination"] != query["destination"]:
            continue
        if "departure_datetime" in query and flight["departure_datetime"] < query["departure_datetime"]:
            continue
        if "arrival_datetime" in query and flight["arrival_datetime"] > query["arrival_datetime"]:
            continue
        if "price" in query and flight["price"] > query["price"]:
            continue
        if "min_price" in query and flight["price"] < query["min_price"]:
            continue
        matches.append(flight)

    if "sort_by" in query:
        matches = sorted(matches,
                         key=lambda r: r[query["sort_by"]],
                         reverse=query.get("order", "asc") == "desc")

    if "limit" in query:
        matches = matches[:query["limit"]]

    return {"query": query, "matches": matches}


def run_queries(db: list[dict], queries: dict | list) -> list[dict]:
    """Accept one query object or a list of them; always return a list."""
    if isinstance(queries, dict):
        queries = [queries]
    return [run_query(db, q) for q in queries]
