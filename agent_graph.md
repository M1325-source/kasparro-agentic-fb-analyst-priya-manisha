Mermaid diagram (high-level flow)
flowchart LR
  U["User query / CLI"] --> P["Planner (Orchestrator)"]
  P -->|subtasks (JSON)| DA["Data Agent\n(load, clean, summarize)"]
  DA -->|data_summary| IA["Insight Agent\n(generate structured hypotheses)"]
  IA -->|hypotheses| EV["Evaluator Agent\n(validate quantitatively)"]
  EV -->|validated_insights| P
  P --> CG["Creative Generator\n(generate creatives for low-CTR campaigns)"]
  CG --> R["Report Builder\n(write insights.json, creatives.json, report.md)"]
  EV --> R
  DA --> R
  R --> OUT["reports/ (outputs)"]
  subgraph Logs["Observability"]
    LOGS["logs/run_logs.json"]
  end
  LOGS --- DA
  LOGS --- IA
  LOGS --- EV
  LOGS --- CG
  LOGS --- P


One-line summary: Planner decomposes the request → Data Agent summarizes → Insight Agent proposes hypotheses → Evaluator validates quantitatively → Creative Generator crafts creatives for weak campaigns → Report Builder writes outputs. All agents emit structured logs for auditability.

Agent responsibilities, inputs & outputs

For reviewers: each agent produces a strict JSON I/O shape and emits log events to logs/run_logs.json. Tests should validate the Evaluator schema and Planner retry behavior.

1) Planner (Orchestrator)

Role: Task decomposition, ordering, retry/refine logic, and routing of intermediate outputs between agents.

Inputs

user_query (string)

config (dict)

optional previous_validated_insights

Outputs

task_list (JSON array) — ordered tasks; each task:

{
  "id": 1,
  "name": "compute_summary",
  "required_agents": ["DataAgent"],
  "input_refs": {"csv_path": "config.paths.sample"},
  "output_schema": {"rows": "int", "roas_change_pct": "float", "median_ctr": "float"},
  "priority": 10
}


Behavior

If any hypothesis returned by Evaluator has confidence < config.confidence_min, Planner inserts a refine task for the Insight Agent and retries up to config.retry_max.

Writes log events: {"ts": "...", "agent":"Planner", "msg":"created tasks","meta":{...}}.

2) Data Agent

Role: Load CSV, clean, aggregate to campaign/adset level, compute summary metrics, and prepare small representative creative samples.

Inputs

csv_path (string) from config (sample or full)

optional date_range or sampling flags

Outputs

data_summary (JSON) with required keys:

{
  "rows": 4239,
  "period": "2025-11-01..2025-11-14",
  "first_mean_roas": 9.44129,
  "last_mean_roas": 7.94012,
  "roas_change_pct": -0.1590,
  "median_ctr": 0.0123,
  "campaign_metrics": [
    {"campaign_name":"C1","ctr":0.0045,"roas":0.55,"spend":388.09,"impressions":122505,"clicks":554}
  ],
  "low_ctr_campaigns":["MEN BOL COLORS DROP","WOMEN Seamless Everydy"],
  "samples":{
    "MEN BOL COLORS DROP":["headline1","text1"]
  }
}


Notes

Never pass raw full rows to LLMs — only aggregates + short samples.

Emits log: {"ts":"...","agent":"DataAgent","msg":"loaded n rows","meta":{"rows":4239}}.

3) Insight Agent

Role: Produce a small, structured list of hypotheses explaining the observed change.

Inputs

data_summary

prompt_template (from prompts/)

Outputs

hypotheses_block (JSON):

{
  "roas_change_pct": -0.159,
  "hypotheses": [
    {
      "id": 1,
      "hypothesis": "CTR drop due to creative fatigue",
      "metric": "ctr",
      "reason": "median ctr decreased while impressions unchanged",
      "suggested_checks": ["compare creative CTR by date","look at frequency"],
      "initial_confidence": 0.55,
      "reflection": "low sample size for campaign X"
    }
  ]
}


Prompt style

"Think → Analyze → Conclude" and return JSON only. If initial_confidence < 0.6 include reflection notes.

4) Evaluator Agent

Role: Validate each hypothesis with deterministic, numeric checks and produce evidence + confidence.

Inputs

hypotheses_block

data_summary

Outputs

validated_insights (JSON):

{
  "roas_change_pct": -0.159,
  "hypotheses": [
    {
      "id": 1,
      "hypothesis": "CTR drop due to creative fatigue",
      "confidence": 0.78,
      "evidence": {"median_ctr":0.0123,"worst_campaign":"MEN BOL COLORS DROP","rel_change":-0.35}
    }
  ]
}


Validation examples

CTR hypothesis → compute median CTR vs period, campaign CTR percentiles; compute a normalized confidence score from relative change, sample size, and variance.

Impression-share hypothesis → compute impression share change and typical effect sizes.

Tests

Unit tests should assert the Evaluator returns the required keys and confidence ∈ [0,1].

Logs

{"ts":"...","agent":"Evaluator","msg":"validated hypothesis","meta":{...}}

5) Creative Generator

Role: For low_ctr_campaigns, propose 3 creative variations each — headline, primary text, CTA — using dataset vocabulary & constraints.

Inputs

low_ctr_campaigns

samples (creative examples)

tone_constraints (from config/prompts)

Outputs

creatives.json (array):

[
  {
    "campaign_name":"ComfortWear",
    "suggestions":[
      {"headline":"Feel Comfort Today","text":"Experience our comfort collection...","cta":"Shop Now","explain":"uses product comfort keywords"}
    ]
  }
]


Constraints

Do not invent product attributes not present in dataset.

Use dataset keywords and avoid absolute claims that require verification.

Logs

{"ts":"...","agent":"CreativeGenerator","msg":"generated creatives","meta":{"campaigns":3}}

6) Report Builder

Role: Merge validated insights + creatives + data summary into marketer-friendly report.md and write insights.json & creatives.json.

Inputs

validated_insights

creatives.json

data_summary

Outputs

reports/insights.json

reports/creatives.json

reports/report.md (human readable; includes data bullets, ranked insights, evidence, recommended actions, creatives)

File encoding

JSON files written with ensure_ascii=False, UTF-8.

Logs

{"ts":"...","agent":"ReportBuilder","msg":"wrote reports","meta":{"insights":"reports/insights.json"}}

Retry / Reflection loop (Planner-managed)

Evaluator returns any hypothesis with confidence < config.confidence_min.

Planner inserts a refine subtask (e.g., expand date window, request additional checks).

Re-run Insight Agent → Evaluator up to config.retry_max times (default 2).

If still low confidence, mark the hypothesis as low-confidence in insights.json and include recommended next steps for a human analyst.

Configuration (config/config.yaml) — essential knobs
random_seed: 42
confidence_min: 0.60
retry_max: 2
use_sample_data: true
paths:
  sample: "data/sample_fb_ads.csv"
  full: "/path/to/full.csv"
output:
  insights: "reports/insights.json"
  creatives: "reports/creatives.json"
  report: "reports/report.md"

Observability & logs

Central log file: logs/run_logs.json (append-only)

Event schema:

{"ts":"2025-11-26T11:19:00Z","agent":"DataAgent","level":"info","msg":"Loaded rows","meta":{"rows":4239,"path":"data/sample_fb_ads.csv"}}


Log every agent start/stop, major counts, decisions (e.g., why a hypothesis was accepted), retries and prompt version used.

Optional: include Langfuse traces or screenshots in reports/observability/ if available.

Output schemas (examples)

insights.json

{
  "roas_change_pct": -0.159,
  "hypotheses": [
    {
      "id": 1,
      "hypothesis": "CTR drop due to creative fatigue",
      "confidence": 0.78,
      "evidence": {"median_ctr":0.0123,"worst_campaign":"MEN BOL COLORS DROP","rel_change":-0.35}
    }
  ]
}


creatives.json

[
  {
    "campaign_name": "ComfortWear",
    "suggestions": [
      {"headline":"Feel Comfort Today","text":"Experience all-day comfort with our new line.","cta":"Shop Now","explain":"uses frequent keywords 'comfort' and 'new' from dataset"}
    ]
  }
]

Deliverables & where to look (for reviewers)

README.md — quick start + exact commands to reproduce

config/config.yaml — config knobs

src/agents/* — code for Planner, DataAgent, InsightAgent, Evaluator, CreativeGenerator, ReportBuilder

prompts/*.md — prompt templates (versioned)

reports/report.md — final marketer-facing report

reports/insights.json, reports/creatives.json — structured outputs

logs/run_logs.json — structured traces

tests/test_evaluator.py — tests for validation logic

v1.0 tag in releases

Reproduce (exact commands, reviewer friendly)
# from repo root
python -V  # >= 3.10
python -m venv .venv
# Linux / Mac
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1
pip install -r requirements.txt

# run local pipeline (sample data mode configured in config)
python -m src.run "Analyze ROAS drop in last 14 days"

# outputs:
#  - reports/report.md
#  - reports/insights.json
#  - reports/creatives.json

# run tests
pytest -q

Reviewer checklist (Kasparro evaluator mapping)

 Repo name & v1.0 release present

 README has exact quick-start commands

 Config exists and is documented

 Agents separated and follow the I/O schemas

 Prompts stored under prompts/ (not inline only)

 reports/ contains report.md, insights.json, creatives.json

 logs/ or Langfuse traces present

 tests/ exist and pass locally

 PR includes self-review comment describing tradeoffs

Short notes & recommendations

Keep prompt files versioned in prompts/ and include a small prompts/README.md describing template variables.

Avoid checking full raw datasets into repo; include data/README.md explaining how to supply full CSV.

Make Evaluator deterministic (set seed, reproducible sampling) so tests and CI are stable.

When changing prompt logic, bump a prompts/version.txt and log prompt version in logs/run_logs.json.

<img width="959" height="437" alt="image" src="https://github.com/user-attachments/assets/45c7662b-10ca-40f9-9cc1-44048892c4bd" />

