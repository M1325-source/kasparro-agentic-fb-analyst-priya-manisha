import argparse
import json
from pathlib import Path
import yaml

# Correct imports from src package
from src.agents.data_agent import DataAgent
from src.agents.planner import Planner
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator import Evaluator
from src.agents.creative_generator import CreativeGenerator


def load_config(path="config/config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", default="Analyze ROAS drop")
    parser.add_argument("--config", default="config/config.yaml")
    args = parser.parse_args()

    # Load config
    cfg = load_config(args.config)

    #Paths
    csv_path = cfg["paths"]["sample"]
    out_insights = cfg["output"]["insights"]
    out_creatives = cfg["output"]["creatives"]
    out_report = cfg["output"]["report"]

    # Ensure output dir exists
    Path("reports").mkdir(parents=True, exist_ok=True)

    # Agents
    planner = Planner()
    _ = planner.plan(args.query)

    data_agent = DataAgent(csv_path)
    data_summary = data_agent.summarize()

    insight_agent = InsightAgent()
    insights = insight_agent.generate(data_summary)

    evaluator = Evaluator()
    validated = evaluator.validate(insights, data_summary)

    creative_gen = CreativeGenerator()
    creatives = creative_gen.generate(data_summary)

    # ---------------- SAFE FALLBACKS ----------------
    if validated is None or not isinstance(validated, dict):
        validated = {
            "roas_change_pct": data_summary.get("roas_change_pct", 0.0),
            "hypotheses": []
        }
    validated.setdefault("hypotheses", [])

    if creatives is None:
        creatives = []
    # ------------------------------------------------

    # Save JSON outputs
    with open(out_insights, "w", encoding="utf-8") as f:
        json.dump(validated, f, indent=2, ensure_ascii=False)

    with open(out_creatives, "w", encoding="utf-8") as f:
        json.dump(creatives, f, indent=2, ensure_ascii=False)

    # Write report.md safely
    with open(out_report, "w", encoding="utf-8") as f:
        f.write("# Final Performance Report\n\n")
        f.write("## Query\n")
        f.write(args.query + "\n\n")

        f.write("## Data Summary\n")
        for k, v in data_summary.items():
            try:
                f.write(f"- {k}: {v}\n")
            except:
                f.write(f"- {k}: {str(v)}\n")

        f.write("\n## Validated Insights\n")
        for h in validated["hypotheses"]:
            hypo = h.get("hypothesis", "No hypothesis generated")
            conf = h.get("confidence", 0.0)
            evidence = h.get("evidence", "")
            f.write(f"- **{hypo}** (confidence: {conf:.2f})\n")
            if evidence:
                f.write(f"  - Evidence: {evidence}\n")

        f.write("\n## Creative Recommendations\n")
        if creatives:
            for c in creatives:
                f.write(f"\n### Campaign: {c.get('campaign_name','unknown')}\n")
                for i, item in enumerate(c.get("suggestions", []), 1):
                    f.write(f"{i}. Headline: {item.get('headline','')}\n")
                    f.write(f"   Text: {item.get('text','')}\n")
                    f.write(f"   CTA: {item.get('cta','')}\n")
        else:
            f.write("No creative recommendations generated.\n")

    print("✔ DONE — insights.json, creatives.json, report.md generated in reports/")
    

if __name__ == "__main__":
    main()
