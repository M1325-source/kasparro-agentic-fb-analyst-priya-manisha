# src/agents/evaluator.py
from typing import Dict, Any, List
import math

class Evaluator:
    """
    Minimal evaluator implementation used for tests and as a baseline.
    validate(hypotheses_block, data_summary) -> dict with 'hypotheses' list
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    def _score_ctr_hypothesis(self, hypothesis: Dict[str, Any], data_summary: Dict[str, Any]) -> float:
        """
        Example scoring: if hypothesis.metric == 'ctr' compare campaign ctr vs median.
        Return confidence in [0.0, 1.0].
        """
        try:
            median_ctr = float(data_summary.get("median_ctr", 0.0) or 0.0)
            # if campaign_metrics present, take worst campaign ctr or use median fallback
            campaign_metrics = data_summary.get("campaign_metrics") or []
            if campaign_metrics:
                # compute relative drop for worst campaign (min ctr)
                ctrs = [float(c.get("ctr", 0.0) or 0.0) for c in campaign_metrics]
                worst = min(ctrs) if ctrs else median_ctr
                rel = 0.0
                if median_ctr > 0:
                    rel = (median_ctr - worst) / median_ctr
                # convert relative drop to confidence: bigger drop -> higher confidence (clamped)
                conf = max(0.0, min(1.0, rel * 1.2))
                return conf
            else:
                # no campaign metrics, use heuristic from hypothesis initial_confidence
                return float(hypothesis.get("initial_confidence", 0.5))
        except Exception:
            return float(hypothesis.get("initial_confidence", 0.5))

    def validate(self, hypotheses_block: Dict[str, Any], data_summary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates hypotheses and returns a dict containing:
         - roas_change_pct (copied from data_summary when available)
         - hypotheses: list of {id, hypothesis, confidence, evidence}
        """
        if hypotheses_block is None:
            hypotheses_block = {}

        hypotheses_in = hypotheses_block.get("hypotheses", []) or []
        validated: List[Dict[str, Any]] = []

        for h in hypotheses_in:
            hid = h.get("id")
            text = h.get("hypothesis", "")
            metric = h.get("metric", "").lower()
            initial_conf = float(h.get("initial_confidence", 0.5) or 0.5)

            confidence = initial_conf
            evidence = ""

            if metric == "ctr":
                confidence = self._score_ctr_hypothesis(h, data_summary)
                evidence = f"median_ctr={data_summary.get('median_ctr')}, source=campaign_metrics"
            elif metric in ("impressions", "frequency"):
                # simple fallback heuristic
                confidence = initial_conf
                evidence = "no detailed check implemented for impressions (fallback)"
            else:
                # default: return the initial confidence if unknown metric
                confidence = initial_conf
                evidence = "no metric-specific check, returned initial_confidence"

            # ensure proper numeric bounds
            if confidence is None or not isinstance(confidence, (float, int)):
                confidence = float(initial_conf)
            confidence = max(0.0, min(1.0, float(confidence)))

            validated.append({
                "id": hid,
                "hypothesis": text,
                "metric": metric,
                "confidence": round(confidence, 4),
                "evidence": evidence
            })

        out = {
            "roas_change_pct": data_summary.get("roas_change_pct"),
            "hypotheses": validated
        }
        return out
