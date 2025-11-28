🌟 Kasparro — Agentic Facebook Performance Analyst (Production-Ready)-Manisha Priya

A fully-observable, multi-agent system for automated ROAS diagnosis, insight validation & creative generation.
Built with structured logging, smart retries, data validation, and environment-aware config management.

🚀 Overview

This project implements a production-grade agentic pipeline that analyzes Facebook Ads performance, identifies root-cause issues, validates hypotheses using real data, and generates optimized creative suggestions.

It follows Kasparro's rubric for:

Agentic reasoning loop

Quantitative evaluation

Observability

Testability & reliability

Configuration management

Content safety & correctness

Result: A system that behaves like a miniature “Kasparro Ads Intelligence Engine”—transparent, debuggable, verifiable.


🧠 High-Level Architecture
flowchart TD
  U[User Query] --> P[Planner Agent]
  P -->|task plan| DA[Data Agent<br>load, validate, summarize]
  DA -->|summary| IA[Insight Agent<br>generate hypotheses]
  IA -->|hypotheses| EV[Evaluator Agent<br>quant validation]
  EV -->|validated insights| P
  P --> CG[Creative Generator<br>suggest new creatives]
  CG --> R[Report Builder<br>MD + JSON outputs]

  subgraph Logs
      L((logs/run_logs.jsonl))
  end

  DA --> L
  IA --> L
  EV --> L
  CG --> L
  P --> L
  R --> L

  R --> OUT[reports/<br>insights.json<br>creatives.json<br>report.md]

🧩 Agent Breakdown (Recruiter-Friendly)
🧭 Planner — The Orchestrator

Decomposes query

Orders subtasks

Tracks confidence

Applies retry + backoff

Ensures robustness

📊 Data Agent — The Source of Truth

Loads FB Ads dataset

Performs strict validation (nulls, bad types, outliers)

Computes CTR/ROAS trends

Supports CSV + Parquet

Adapts automatically for big datasets

🔍 Insight Agent — The Analyst

Generates hypotheses

Adds reasoning + suggested checks

Outputs structured JSON only

Includes reflection on low-confidence items

📐 Evaluator — The Scientist

Runs real metric calculations

Outputs confidence + numeric evidence

Validates or rejects hypotheses

🎨 Creative Generator — The Content Brain

Extracts messaging patterns

Generates 3 variations per weak campaign

No hallucinated features

CTR-focused creative ideation

📝 Report Builder

Exports:

insights.json

creatives.json

report.md

Formatted cleanly for marketers.
🔎 Observability & Logging (Production-Ready)

Complete structured logging using JSONL:

Example:

{"ts":"2025-11-26T11:19:00Z","agent":"DataAgent","event":"validation_warning","meta":{"nan":3,"bad_types":1}}


You get:

full traceability

debugging visibility

replayable logs

safety for multi-agent reasoning

🔄 Smart Retry Logic

Implemented exponential/linear hybrid backoff via:

src/agents/retry.py


Used when:

evaluator low confidence

planner requests refinement

transient errors in LLM calls

🧪 Testing Framework
Unit Tests

test_data_agent.py

test_evaluator.py

Check:

schema correctness

validation logic

confidence calculations

Integration Test

test_integration.py

Validates full chain:

Data → Insight → Evaluator
Ensuring pipeline does not silently fail.

🗂 Config Management (dev / stage / prod)
config/dev.yaml
config/stage.yaml
config/prod.yaml


Supports:

environment switching

different file paths

different thresholds

production-safe defaults

📦 Project Structure
├── src
│   ├── agents
│   │   ├── data_agent.py
│   │   ├── insight_agent.py
│   │   ├── evaluator.py
│   │   ├── creative_generator.py
│   │   ├── planner.py
│   │   └── retry.py
│   ├── utils
│   │   └── logger.py
│   └── run.py
├── config
├── reports
├── logs
└── tests

▶️ Running the System
1. Install dependencies
pip install -r requirements.txt

2. Activate environment configuration
set ENV=dev      # Windows
export ENV=dev   # Linux/Mac

3. Run
python src/run.py "Analyze ROAS drop in last 7 days"

🧾 Sample Output Files
reports/insights.json
{
  "roas_change_pct": -0.32,
  "hypotheses": [
    {
      "hypothesis": "Creative fatigue caused CTR decline",
      "confidence": 0.82,
      "evidence": "median_ctr=0.019, worst=0.012, rel change=-0.36"
    }
  ]
}

reports/creatives.json
[
  {
    "campaign_name":"ComfortWear",
    "suggestions":[
      {"headline":"Feel the Difference","text":"Experience unmatched daily comfort","cta":"Shop Now"}
    ]
  }
]
