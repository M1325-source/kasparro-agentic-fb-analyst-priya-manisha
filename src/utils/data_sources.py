# src/utils/data_sources.py
import os
import json
import pandas as pd
from typing import Tuple, Dict, Any

def load_csv(path: str, parse_dates=None) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=parse_dates)

def load_json(path: str, parse_dates=None) -> pd.DataFrame:
    # Expect newline-delimited JSON or list-of-objects JSON
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip()
        if not text:
            return pd.DataFrame()
        # try ndjson first
        try:
            rows = [json.loads(line) for line in text.splitlines()]
        except Exception:
            # fallback: parse whole file
            rows = json.loads(text)
    df = pd.DataFrame(rows)
    if parse_dates:
        for col in parse_dates:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
    return df

def load_source(spec: Dict[str, Any]) -> pd.DataFrame:
    """
    spec example:
    { "type": "csv", "path": "data/sample.csv", "parse_dates": ["date"] }
    or
    { "type": "json", "path": "data/sample.json", "parse_dates": ["date"] }
    """
    typ = spec.get("type", "csv").lower()
    path = spec.get("path")
    parse_dates = spec.get("parse_dates", None)
    if not path or not os.path.exists(path):
        raise FileNotFoundError(f"Data source not found: {path}")
    if typ == "csv":
        return load_csv(path, parse_dates=parse_dates)
    if typ == "json":
        return load_json(path, parse_dates=parse_dates)
    raise ValueError(f"Unknown source type: {typ}")
