🌟 Kasparro — Agentic Facebook Performance Analyst (v1.0)

An AI-native, multi-agent diagnostic engine that explains why ROAS changed, validates hypotheses quantitatively, and generates data-grounded creative improvements — designed for real-world marketing workflows.

🚀 Overview

This project builds a production-style agentic system aligned with Kasparro’s applied-AI philosophy:

Multi-agent orchestration

Structured reasoning + validation

RAG-style summarization

Creative generation grounded in historic messaging

Configuration management across environments

Observability + reliability baked in

Designed to be modular, testable, debuggable, and easy to extend.

🧠 System Capabilities
✔ Diagnose ROAS fluctuations

Quantifies ROAS change across time windows, identifies potential causes.

✔ Identify performance drivers

Campaign-level CTR, ROAS, impressions, frequency patterns.

✔ Generate hypotheses

Creatively but consistently structured (Think → Analyze → Conclude).

✔ Quantitative validation

Evaluator converts qualitative hypotheses into numeric confidence & evidence.

✔ Generate new creatives

For low-CTR campaigns: headlines, primary text, CTA — grounded in dataset vocabulary.

✔ Build production outputs

Writes:

reports/insights.json

reports/creatives.json

reports/report.md

✔ Logging & observability

Every agent logs JSON events to logs/run_logs.jsonl.

⚙️ Quick Start
# 1. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Choose environment (dev/stage/prod/p2)
set ENV=dev

# 4. Run analysis
python src/run.py "Analyze ROAS drop in last 30 days"

🧩 Architecture Diagram
flowchart TD
  U[User Query] --> P[Planner Agent]
  P -->|subtasks| DA[Data Agent]
  DA -->|summary| IA[Insight Agent]
  IA -->|hypotheses| EV[Evaluator Agent]
  EV -->|validated insights| P
  P --> CG[Creative Generator]
  CG --> R[Report Builder]
  
  subgraph Logs
    L((JSON Logs))
  end
  
  DA -.-> L
  IA -.-> L
  EV -.-> L
  CG -.-> L
  P -.-> L
  R -.-> L

📦 Repository Structure
├── src/
│   ├── agents/         # All agents + retry
│   ├── utils/          # logger, config, data-source loaders
│   └── run.py          # main orchestrator
├── config/             # dev, prod, stage, p2 configs
├── reports/            # generated insights + creatives
├── logs/               # structured JSON logs
├── tests/              # unit + integration tests
├── prompts/            # structured prompts
└── README.md

🏗️ Engineering Progress (Original → Improved)
🔵 Initial Version

You originally built:

Core multi-agent system

ROAS diagnosis

Hypothesis generation via structured prompts

Creative generation

Basic insights & creatives JSON

Clean architecture + README

v1.0 release

This met the assignment baseline.

🔥 P0 Improvements — Production Foundations

"Add structured logging, validation, tests." — Kasparro review feedback

✔ Structured Logging

Added logger.py

Every agent logs JSONL events (timestamp, agent, meta)

✔ Data Validation

Missing columns

Type mismatches

Outlier detection

NaN recovery

Logged with severity tags

✔ Unit Tests

test_data_agent.py

test_evaluator.py
Ensures schema correctness & confidence logic.

✔ Config Versioning (dev/prod)

Environment-based configuration loader.

⚡ P1 Improvements — Reliability & Correctness

"Smarter retry, versioned configs, integration tests."

✔ Backoff Retry Logic

Linear, configurable wait times to handle low-confidence evaluations.

✔ Multi-Environment Config Loader

config/dev.yaml, stage.yaml, prod.yaml

✔ Integration Tests

Ensures pipeline consistency across multiple runs.

🚀 P2 Improvements — Scalability & Extensibility

"Adaptive behavior + multi-source support."

✔ Adaptive Data Strategy

Small datasets → full load
Medium → sampling
Large → stratified sampling

✔ Multi-Source Loader

Supports:

CSV

JSON

Extensible future connectors

✔ Additional Tests

Adaptivity behavior

Multi-source validation

📊 Sample Output Formats
insights.json
{
  "roas_change_pct": -0.28,
  "hypotheses": [
    {
      "hypothesis": "CTR decline due to creative fatigue",
      "confidence": 0.76,
      "evidence": "median_ctr=0.021, worst_ctr=0.012, delta=-0.35"
    }
  ]
}

creatives.json
[
  {
    "campaign_name": "ComfortWear",
    "suggestions": [
      {"headline": "Feel the Softness", "text": "All-day comfort you can trust.", "cta": "Shop Now"}
    ]
  }
]

🧪 Testing
pytest -q


Includes:

Unit tests

Evaluator tests

Integration tests

Adaptivity + source loading tests

🔗 Releases & PRs

v1.0 Release:
https://github.com/M1325-source/kasparro-agentic-fb-analyst-priya-manisha/releases/tag/v1.0

P0 PR: improvements-p0  - https://github.com/M1325-source/kasparro-agentic-fb-analyst-priya-manisha/tree/improvements-p0

P1 PR: improvements-p1 - https://github.com/M1325-source/kasparro-agentic-fb-analyst-priya-manisha/tree/improvements-p1

P2 PR: improvements-p2 - https://github.com/M1325-source/kasparro-agentic-fb-analyst-priya-manisha/tree/improvements-p2

(List your PR links here if you want — I can add them.)
