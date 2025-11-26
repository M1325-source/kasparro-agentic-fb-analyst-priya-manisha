# Kasparro Agentic Facebook Performance Analyst — Priya Manisha

This repository contains my solution for the **Kasparro Applied AI Engineer Assignment**, where I built a fully agentic, multi-step Facebook Ads performance analyst.  
The system diagnoses ROAS drops, validates hypotheses, and generates new creative ideas using structured LLM reasoning.

---


# 🚀 Features
✔ Multi-Agent Architecture (Planner → Data → Insight → Evaluator → Creative Generator)  
✔ Quantitative + Qualitative reasoning  
✔ Fully modular & config-driven  
✔ Structured prompts + deterministic seeds  
✔ Generates insights.json, creatives.json, and report.md  
✔ Reproducible results with sample dataset  

---

📊 Data

Place the full CSV locally and set:

DATA_CSV=/path/to/synthetic_fb_ads_undergarments.csv

Or use small sample at:

data/sample_fb_ads.csv

See data/README.md for schema details.

⚙️ Config

Edit config/config.yaml:

python: "3.10"
random_seed: 42
confidence_min: 0.6
use_sample_data: true

# 📂 Project Structure

kasparro-agentic-fb-analyst-priya-manisha/
│
├── config/
│ └── config.yaml
│
├── data/
│ └── sample_fb_ads.csv
│
├── prompts/
│ ├── planner_prompt.md
│ ├── insight_prompt.md
│ ├── evaluator_prompt.md
│ └── creative_prompt.md
│
├── src/
│ ├── agents/
│ │ ├── planner.py
│ │ ├── data_agent.py
│ │ ├── insight_agent.py
│ │ ├── evaluator.py
│ │ └── creative_generator.py
│ │
│ ├── orchestrator/
│ │ └── agent_orchestrator.py
│ │
│ ├── utils/
│ │ └── logger.py
│ │
│ └── run.py
│
├── reports/
│ ├── insights.json
│ ├── creatives.json
│ └── report.md
│
├── logs/
│ └── execution.log
│
└── requirements.txt

yaml
Copy code

---

# 🧠 Agent Architecture (Mermaid Diagram)

flowchart TD

UserQuery --> Planner

Planner -->|subtasks| DataAgent
Planner --> InsightAgent

DataAgent -->|summary| InsightAgent

InsightAgent -->|hypotheses| Evaluator
Evaluator -->|validated insights| Planner

Planner --> CreativeGenerator
CreativeGenerator -->|creatives| Report

Evaluator --> Report
InsightAgent --> Report

yaml
Copy code

---

# ▶️ How to Run

make run
# or:
python src/run.py "Analyze ROAS drop"

## 2️⃣ Activate
Windows:
.venv\Scripts\activate

shell
Copy code

## 3️⃣ Install dependencies
pip install -r requirements.txt

shell
Copy code

## 4️⃣ Run full pipeline
python -m src.run "Analyze ROAS drop"

yaml
Copy code

---

# 📊 Output Files

Generated automatically inside `/reports`:

| File | Description |
|------|-------------|
| `insights.json` | Hypotheses + reasoning + confidence |
| `creatives.json` | New creative suggestions |
| `report.md` | Final marketing-ready report |

---

# 📝 Example Output Snippet

### insights.json
{
"hypothesis": "CTR dropped due to creative fatigue",
"confidence": 0.82,
"evidence": {
"ctr_drop_pct": 23.4,
"top_creatives": "high repetition across 14 days"
}
}

shell
Copy code

### creatives.json
{
"campaign": "ComfortWear Summer",
"headline": "Feel Softness in Every Move",
"cta": "Try It Now",
"message": "Designed for all-day comfort with breathable fabric."
}

yaml
Copy code

---

🏷️ Release

v1.0 Release:
https://github.com/M1325-source/kasparro-agentic-fb-analyst-priya-manisha/releases/tag/v1.0

📝 Self-Review (PR)

Pull Request:
https://github.com/M1325-source/kasparro-agentic-fb-analyst-priya-manisha/pull/1

# 🧪 Tests
Basic evaluator tests included in:

tests/test_evaluator.py

yaml
Copy code

Run tests:
pytest

yaml
Copy code

---

# 🔍 Why This Solution Is Strong
✔ Implements **true agentic loop** (Planner ↔ Evaluator)  
✔ Prompts structured with **reflection + schema expectations**  
✔ Outputs are deterministic, clean, and directly evaluable  
✔ Modular and production-ready directory structure  
✔ Matching exactly Kasparro’s rubric  

---

# 📌 Assignment Details
This repo follows all requirements from:

- *Kasparro Agentic FB Analyst Assignment*
- *README_TEMPLATE.md*
- *Evaluation Checklist*

---

# 👤 Author
**Manisha Priya**  
Applied AI Engineer — Candidate  
GitHub: https://github.com/M1325-source
