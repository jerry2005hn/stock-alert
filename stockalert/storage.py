import json
from .config import WATCHLIST_FILE, log


def load_watchlist() -> list[dict]:
    if not WATCHLIST_FILE.exists():
        return []
    try:
        return json.loads(WATCHLIST_FILE.read_text())
    except (json.JSONDecodeError, OSError) as exc:
        log.error("Failed to read watchlist (%s); starting empty", exc)
        return []


def save_watchlist(watchlist: list[dict]) -> None:
    try:
        tmp = WATCHLIST_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(watchlist, indent=2))
        tmp.replace(WATCHLIST_FILE)
    except OSError as exc:
        log.error("Failed to save watchlist: %s", exc)
