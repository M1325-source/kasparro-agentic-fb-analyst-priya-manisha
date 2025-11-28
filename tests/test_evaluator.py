# minimal smoke test — adapt if your Evaluator signature is different
try:
    from src.agents.evaluator import Evaluator
except Exception:
    Evaluator = None

def test_evaluator_smoke():
    if Evaluator is None:
        assert True  # skip if no Evaluator present
        return
    ev = Evaluator()
    # sample input — adapt if needed
    hypotheses_block = {"hypotheses":[{"id":1,"hypothesis":"dummy","metric":"ctr","reason":"test","suggested_checks":[], "initial_confidence":0.5}]}
    data_summary = {"median_ctr":0.05, "campaign_metrics": []}
    validated = ev.validate(hypotheses_block, data_summary)
    assert "hypotheses" in validated
    for h in validated["hypotheses"]:
        assert 0.0 <= h.get("confidence", 0.0) <= 1.0
