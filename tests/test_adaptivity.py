# tests/test_adaptivity.py
import os
import pandas as pd
from src.agents.data_agent import DataAgent

def make_fake_csv(path, rows=1000, campaigns=5):
    import numpy as np
    import pandas as pd
    from datetime import datetime, timedelta
    rows_per_campaign = max(1, rows//campaigns)
    rows_list = []
    base = datetime(2025,1,1)
    for i in range(campaigns):
        for r in range(rows_per_campaign):
            rows_list.append({
                "date": (base + timedelta(days=r)).isoformat(),
                "campaign_name": f"camp_{i}",
                "roas": float(np.random.random())*3,
                "ctr": float(np.random.random())*0.1,
                "spend": float(np.random.randint(10,100)),
                "impressions": int(np.random.randint(100,10000)),
                "clicks": int(np.random.randint(1,100)),
                "creative_message":"hello"
            })
    pd.DataFrame(rows_list).to_csv(path, index=False)

def test_small_dataset_full_process(tmp_path):
    p = tmp_path / "small.csv"
    make_fake_csv(str(p), rows=500, campaigns=4)
    config = {"sample_threshold":20000, "batch_size":100000, "random_seed": 42}
    src = {"type":"csv","path": str(p), "parse_dates":["date"]}
    da = DataAgent(src, config)
    s = da.summarize()
    assert s["strategy"] == "full"
    assert s["rows"] == 500

def test_large_dataset_sampling(tmp_path):
    p = tmp_path / "big.csv"
    make_fake_csv(str(p), rows=50000, campaigns=50)
    config = {"sample_threshold":20000, "batch_size":100000, "random_seed": 42}
    src = {"type":"csv","path": str(p), "parse_dates":["date"]}
    da = DataAgent(src, config)
    s = da.summarize()
    # since rows > sample_threshold but < batch_size => sample
    assert s["strategy"] in ("sample","stratified_sample")
    assert s["rows"] == 50000
    assert s["rows_used"] <= config["sample_threshold"]
