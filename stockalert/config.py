import json
import logging
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
log = logging.getLogger("stock-alert")
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


def _load_channel_id() -> Optional[int]:
    raw = os.getenv("ALERT_CHANNEL_ID")
    if not raw:
        config_path = PROJECT_ROOT / "config.json"
        if config_path.exists():
            try:
                raw = str(json.loads(config_path.read_text()).get("alert_channel_id", ""))
            except (json.JSONDecodeError, OSError) as exc:
                log.error("Could not read config.json: %s", exc)
    try:
        return int(raw) if raw else None
    except ValueError:
        log.error("ALERT_CHANNEL_ID %r is not a valid integer", raw)
        return None


ALERT_CHANNEL_ID = _load_channel_id()
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL_SECONDS", "300"))
RECURRING = os.getenv("RECURRING", "false").lower() in ("1", "true", "yes")
WATCHLIST_FILE = PROJECT_ROOT / "watchlist.json"

VALID_DIRECTIONS = ("above", "below")
