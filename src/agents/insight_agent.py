class InsightAgent:
    def generate(self, data_summary):
        hypotheses = []
        change = data_summary.get("roas_change_pct", 0.0)

        # If ROAS dropped more than 5%
        if change < -0.05:
            hypotheses.append({
                "hypothesis": "ROAS decreased due to CTR drop",
                "reason": "Negative ROAS trend + low CTR campaigns present.",
                "metric": "ctr"
            })

            hypotheses.append({
                "hypothesis": "ROAS decreased due to audience fatigue",
                "reason": "Higher impressions but low purchases indicate fatigue.",
                "metric": "impressions"
            })

            hypotheses.append({
                "hypothesis": "ROAS decreased due to creative underperformance",
                "reason": "Low CTR campaigns suggest weak creatives.",
                "metric": "creative_message"
            })

        else:
            hypotheses.append({
                "hypothesis": "ROAS stable or slightly improved",
                "reason": "ROAS change is not significantly negative.",
                "metric": "roas"
            })

        return {
            "roas_change_pct": change,
            "hypotheses": hypotheses
        }
