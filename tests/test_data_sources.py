# tests/test_data_sources.py
import pandas as pd
from src.utils.data_sources import load_source

def test_load_csv(tmp_path):
    p = tmp_path / "x.csv"
    df = pd.DataFrame({"a":[1,2,3]})
    df.to_csv(p, index=False)
    spec = {"type":"csv", "path": str(p)}
    out = load_source(spec)
    assert len(out) == 3

def test_load_json(tmp_path):
    p = tmp_path / "x.json"
    # create newline json
    with open(p, "w", encoding="utf-8") as f:
        f.write('{"a":1}\n{"a":2}\n')
    spec = {"type":"json", "path": str(p)}
    out = load_source(spec)
    assert len(out) == 2
