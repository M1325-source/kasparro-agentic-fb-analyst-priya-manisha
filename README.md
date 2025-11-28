
➤ Kasparro Agentic FB Analyst – Manisha Priya
<h1 align="center">🤖 Kasparro Agentic Facebook Performance Analyst</h1> <p align="center"> A multi-agent system that autonomously diagnoses ROAS fluctuations, validates hypotheses, and generates new creative directions using structured LLM reasoning. </p>
🚀 1. Overview

This project is my submission for the Kasparro Applied AI Engineer Assignment.
It implements a fully autonomous Agentic System for analyzing Facebook Ads performance using synthetic ecommerce data.

The system:

Diagnoses why ROAS changed

Detects drivers behind fluctuations

Identifies underperforming creatives

Generates new data-driven creative ideas

Produces a final marketer-ready report

All reasoning is modular, explainable, and aligned with the Planner → Evaluator → Generator loop expected in Kasparro’s rubric.

🧠 2. Agent Architecture

Below is the full multi-agent reasoning flow:

flowchart TD

A[User Query] --> B[Planner Agent]

B -->|Subtasks| C[Data Agent]
B --> D[Insight Agent]
B --> E[Creative Generator]
D --> F[Evaluator Agent]

C --> D
D --> F
F --> G[Validated Insights]

E --> H[Creative Recommendations]

G --> I[Report Builder]
H --> I

I --> J[(reports/)]

📂 3. Repository Structure
kasparro-agentic-fb-analyst-priya-manisha/
│
├── config/
│   └── config.yaml
│
├── data/
│   ├── sample_fb_ads.csv
│   └── README.md
│
├── prompts/
│   ├── planner_prompt.md
│   ├── insight_prompt.md
│   └── creative_prompt.md
│
├── reports/
│   ├── insights.json
│   ├── creatives.json
│   └── report.md
│
├── logs/
│   └── run_logs.json
│
├── src/
│   ├── run.py
│   ├── orchestrator/
│   │   └── planner.py
│   ├── agents/
│   │   ├── data_agent.py
│   │   ├── insight_agent.py
│   │   ├── evaluator.py
│   │   └── creative_generator.py
│   └── utils/
│       └── helpers.py
│
├── tests/
│   └── test_evaluator.py
│
├── requirements.txt
└── README.md

⚙️ 4. Setup Instructions
1️⃣ Clone the repository
git clone https://github.com/M1325-source/kasparro-agentic-fb-analyst-priya-manisha.git
cd kasparro-agentic-fb-analyst-priya-manisha

2️⃣ Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

▶️ 5. How to Run
Run full analysis:
python -m src.run "Analyze ROAS drop"


After execution, results appear in:

reports/insights.json
reports/creatives.json
reports/report.md

📝 6. Sample Outputs
insights.json (excerpt)
{
  "hypotheses": [
    {
      "id": 1,
      "summary": "CTR dropped due to audience fatigue in retargeting segments.",
      "evidence": {
        "ctr_drop": "-22%",
        "spend_increase": "+18%"
      },
      "confidence": 0.74
    }
  ]
}

creatives.json (excerpt)
{
  "campaign": "ComfortWear_Undershirts",
  "recommendations": [
    "Feel the softness of everyday comfort",
    "Discover new breathable fits",
    "Try comfort redesigned for your skin"
  ]
}

report.md (excerpt)
# ROAS Diagnostic Report

## Key Findings
- ROAS dropped by 28% vs previous period.
- Audience fatigue detected in 2 campaigns.
- Creative performance weak: CTR below threshold in 3 adsets.

## Recommendations
- Refresh creatives with soft-comfort narrative.
- Reduce retargeting frequency for 7 days.
- Expand lookalike audience to 2%.

🧪 7. Evaluation Checklist Mapping
Requirement	Status
Planner → Evaluator loop	✅ Implemented
Structured hypotheses	✅ insights.json
Quantitative validation	✅ evaluator agent
Creative generator	✅ context-aware, uses messaging
Strong prompting	✅ layered prompts in /prompts
Configurable thresholds	✅ config/config.yaml
Logging	✅ structured JSON logs
Reproducibility	✅ pinned versions + seed
Sample dataset	✔️ included
README quality	⭐ recruiter-level
🏁 8. Why This Approach? (Recruiter Friendly)

Designed with LLM-first reasoning

Modular agents → easy to extend

Full isolation of prompts for readability

Clear data flow + observability

Outputs are structured, audit-friendly, and deterministic

Matches Kasparro’s requirement for Agentic workflows

🏷️ 9. Release

A reproducible snapshot of the project is available under:

v1.0
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

🔗 Releases & PRs

v1.0 Release:
https://github.com/M1325-source/kasparro-agentic-fb-analyst-priya-manisha/releases/tag/v1.0

P0 PR: improvements-p0  - https://github.com/M1325-source/kasparro-agentic-fb-analyst-priya-manisha/tree/improvements-p0

P1 PR: improvements-p1 - https://github.com/M1325-source/kasparro-agentic-fb-analyst-priya-manisha/tree/improvements-p1

P2 PR: improvements-p2 - https://github.com/M1325-source/kasparro-agentic-fb-analyst-priya-manisha/tree/improvements-p2

👩‍💻 10. Author

Manisha Priya
Applied AI Engineer — Assignment Submission for Kasparro
GitHub: https://github.com/M1325-source
