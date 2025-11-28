import json
from datetime import datetime
from pathlib import Path

LOG_PATH = Path("logs/run_logs.jsonl")

def _iso_ts():
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def log_event(agent, msg, meta=None, level="info"):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": _iso_ts(),
        "agent": agent,
        "level": level,
        "msg": msg,
        "meta": meta or {}
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry
