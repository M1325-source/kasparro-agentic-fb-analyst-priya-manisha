import os
import csv
import tempfile
from src.agents.data_agent import DataAgent
from src.agents.evaluator import Evaluator

def make_sample_csv(path):
    rows = [
        ["date","campaign_name","roas","ctr","spend","impressions","clicks","creative_message"],
        ["2025-11-01","campA", "2.0", "0.02", "100", "10000", "200", "Buy now!"],
        ["2025-11-02","campA", "1.8", "0.018","120", "11000", "198", "Limited offer"],
        ["2025-11-01","campB", "5.0", "0.05", "200", "8000", "400", "Top seller"],
        ["2025-11-02","campB", "4.8", "0.045","190", "8500", "383", "Best choice"]
    ]
    with open(path, "w", newline="", encoding="utf8") as f:
        w = csv.writer(f)
        w.writerows(rows)

def test_integration_data_to_evaluator(tmp_path):
    csv_path = tmp_path / "sample_integration.csv"
    make_sample_csv(str(csv_path))

    da = DataAgent(str(csv_path))
    summary = da.summarize()
    assert "rows" in summary and summary["rows"] == 4

    # simple evaluator smoke: create a dummy hypothesis block and validate
    ev = Evaluator()
    hypotheses_block = {
        "hypotheses": [
            {"id": 1, "hypothesis":"ctr_drop", "metric":"ctr", "reason":"test", "suggested_checks": [], "initial_confidence": 0.5}
        ]
    }
    validated = ev.validate(hypotheses_block, summary)
    assert isinstance(validated, dict)
    assert "hypotheses" in validated

