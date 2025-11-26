# Agent Graph & Data Flow — Kasparro Agentic Facebook Performance Analyst

This document explains the multi-agent architecture, data flow, agent responsibilities, I/O schemas and observability.  
It is designed to make the pipeline auditable, extensible and aligned with Kasparro's evaluation rubric.

---

## Mermaid diagram (high-level flow)

```mermaid
flowchart TD
  U[User Query / CLI] --> P[Planner Agent]
  P -->|subtasks| DA[Data Agent\n(load, clean, summarize)]
  DA -->|summary| IA[Insight Agent\n(generate hypotheses)]
  IA -->|hypotheses| EV[Evaluator Agent\n(validate quantitatively)]
  EV -->|validated_insights| P
  P --> CG[Creative Generator\n(generate creatives for low-CTR campaigns)]
  CG --> R[Report Builder\n(insights.json, creatives.json, report.md)]
  EV --> R
  DA --> R
  R --> OUT[reports/]
  LOGS((logs/run_logs.json)) --- DA
  LOGS --- IA
  LOGS --- EV
  LOGS --- CG
Short summary (one-liner)
Planner decomposes a request → Data Agent summarizes the dataset → Insight Agent proposes hypotheses → Evaluator validates with data and returns confidence → Creative Generator crafts new ad ideas → Report Builder writes outputs.

Agent responsibilities (detailed)
Planner Agent
Role: Orchestrator and task decomposer.

Inputs: user_query, config, data_summary (when available).

Outputs: ordered tasks JSON (id, name, required_agents, output_schema, priority).

Behavior: If validated_insights.confidence < threshold, insert a retry/refine task. Always return a JSON list of subtasks for the orchestrator.

Example task schema

json
Copy code
{
  "id": 1,
  "name": "compute_summary",
  "required_agents": ["DataAgent"],
  "output_schema": {"rows":"int","roas_change_pct":"float","median_ctr":"float"},
  "priority": 10
}
Data Agent
Role: Load CSV, clean, compute campaign/adset-level metrics.

Inputs: CSV path from config/config.yaml.

Outputs: data_summary JSON with keys:

rows, period, first_mean_roas, last_mean_roas, roas_change_pct

median_ctr, campaign_metrics (ctr, roas, spend, impressions, clicks)

low_ctr_campaigns (list), samples (creative_message samples per campaign)

Notes: Always use aggregated numbers (no raw CSV passed to LLMs).

Insight Agent
Role: Generate structured hypotheses to explain observed patterns.

Inputs: data_summary

Outputs: hypotheses_block JSON:

roas_change_pct

hypotheses: list of {id, hypothesis, metric, reason, suggested_checks, initial_confidence}

Prompt pattern: Think -> Analyze -> Conclude and return JSON only. If low confidence (<0.6) include "reflection" notes.

Evaluator Agent
Role: Validate hypotheses quantitatively and produce evidence + confidence.

Inputs: hypotheses_block, data_summary

Outputs: validated JSON:

roas_change_pct

hypotheses: list of {hypothesis, confidence, evidence}

Validation logic examples:

CTR hypothesis → compute median CTR & worst campaign CTR → confidence = f(relative_change)

Impressions hypothesis → compute changes in frequency/impression share

Testing: Provide unit tests to confirm validate() returns required schema.

Creative Generator
Role: For low-CTR campaigns, propose 3 creative variations each (headline, primary_text, cta).

Inputs: samples for campaign, common_keywords, tone constraints

Outputs: creatives.json — array of {campaign_name, suggestions:[{headline, text, cta, explain}]}

Constraints: Use dataset vocabulary; do not hallucinate product attributes.

Report Builder
Role: Collate validated insights + creatives into report.md and write insights.json & creatives.json.

Outputs written to: reports/insights.json, reports/creatives.json, reports/report.md

Encoding: UTF-8 with ensure_ascii=False for JSON.

Observability & Logs
All agents write compact events to logs/run_logs.json:

json
Copy code
{"ts":"2025-11-26T11:19:00","agent":"DataAgent","msg":"Loaded n rows from sample_fb_ads.csv"}
Logs include: timestamp, agent, message, optional meta (counts, threshold values).

Retry / Reflection loop
If Evaluator returns any hypothesis with confidence < config.confidence_min:

Planner inserts a refine task: id: 98 asking InsightAgent to rerun with broader samples or alternate checks.

System retries up to config.retry_max times (default 2) before marking hypothesis as low-confidence in final report.

Config knobs (config/config.yaml)
random_seed — reproducibility

confidence_min — threshold for auto-accept

use_sample_data — toggle sample vs full dataset

paths.sample — data path

output.* — output file paths

Example output schemas
insights.json

json
Copy code
{
  "roas_change_pct": -0.28,
  "hypotheses": [
    {"hypothesis":"CTR drop due to creative fatigue","confidence":0.78,"evidence":"median_ctr=0.02,worst=0.013,rel_change=-0.35"}
  ]
}
creatives.json

json
Copy code
[
  {"campaign_name":"ComfortWear","suggestions":[{"headline":"Feel Softness Today","text":"Experience all-day comfort...","cta":"Shop Now"}]}
]
Deliverables & Where to look
reports/insights.json — validated insights (structured)

reports/creatives.json — generated creative suggestions

reports/report.md — marketer-facing summary

logs/run_logs.json — observability traces

prompts/*.md — agent prompt templates

Notes for reviewers (what to inspect)
Check src/agents/* for reasoning & evaluator logic.

Confirm insights.json contains numeric evidence per hypothesis.

Run python -m src.run "Analyze ROAS drop" to reproduce.

Confirm tests pass: pytest -q.

Why this design matches Kasparro rubric
Agentic reasoning architecture (Planner–Evaluator loop): Planner orchestrates and re-requests when confidence is low.

Insight quality & validation: Hypotheses returned with numeric evidence.

Prompt design: Layered prompts (Think→Analyze→Conclude), strict JSON schema.

Observability: Structured logs provide traceable decisions.

