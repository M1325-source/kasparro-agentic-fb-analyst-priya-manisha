class Evaluator:
    def validate(self, hypotheses_block, data_summary):
        hypotheses = hypotheses_block["hypotheses"]
        validated = []

        for h in hypotheses:
            metric = h.get("metric")
            confidence = 0.4
            evidence = ""

            # If hypothesis is about CTR
            if metric == "ctr":
                median = data_summary.get("median_ctr", 0)
                low_campaigns = data_summary.get("low_ctr_campaigns", [])

                if low_campaigns:
                    worst = low_campaigns[0]["ctr"]
                else:
                    worst = median

                if median != 0:
                    change = (worst - median) / abs(median)
                else:
                    change = 0

                confidence = min(1.0, 0.5 + abs(change))
                evidence = f"median_ctr={median}, worst_campaign_ctr={worst}, rel_change={change:.2f}"

            elif metric == "impressions":
                confidence = 0.6
