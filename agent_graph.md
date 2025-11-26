\# Agent Graph — Kasparro Agentic Facebook Performance Analyst



This document explains how the multi-agent system works internally, how data flows between agents, and how the planner–evaluator loop forms an iterative reasoning cycle.



---



\# 🔍 High-Level Architecture



flowchart TD



A\[User Query] --> B\[Planner Agent]



B -->|Defines subtasks| C\[Data Agent]

B -->|Requests hypotheses| D\[Insight Agent]



C -->|Summaries + metrics| D



D -->|Hypotheses + evidence| E\[Evaluator Agent]



E -->|Validation results + confidence| B



B --> F\[Creative Improvement Generator]

F -->|New creatives| G\[(reports/)]



E --> G

D --> G



yaml

Copy code



---



\# 🧠 Agent Roles



\### \*\*1. Planner Agent\*\*

\- Breaks user query into structured tasks  

\- Controls loop between Insight → Evaluator → Planner  

\- Decides when insight is “good enough”  

\- Sends final task to Creative Generator  



---



\### \*\*2. Data Agent\*\*

\- Loads CSV  

\- Cleans + summarizes  

\- Computes metrics (ROAS, CTR, CPM, CVR)  

\- Returns structured JSON  



---



\### \*\*3. Insight Agent\*\*

\- Generates hypotheses  

\- Uses Think → Analyze → Conclude  

\- Never hallucinates data (uses summaries only)  



---



\### \*\*4. Evaluator Agent\*\*

\- Quantitatively validates hypotheses  

\- Computes supporting % drops, correlations, trends  

\- Returns confidence score  



---



\### \*\*5. Creative Generator\*\*

\- For low-CTR segments, generates new creatives  

\- Based on existing messaging patterns  

\- Produces variations: headlines, primary text, CTAs  



---



\# 🔁 Iterative Reasoning Loop

1\. Planner → ask: “Why did ROAS drop?”  

2\. Insight Agent → propose hypothesis  

3\. Evaluator → check data trends  

4\. Planner:  

&nbsp;  - If confidence < threshold → ask for revision  

&nbsp;  - If satisfied → conclude → move to creative generation  



---



\# 📦 Final Outputs Produced

\- \*\*insights.json\*\*  

\- \*\*creatives.json\*\*

\- \*\*report.md\*\*

\- Optional: logs + traces  



---



\# 🏁 Summary

The system mimics how a real senior growth analyst works — by combining:  

\*\*Planner → Insight → Evaluator → Creative\*\*  

This is exactly the architecture Kasparro wants for their LLM-native analytics engine.



\# Agent Graph — Kasparro Agentic Facebook Performance Analyst



This document explains how the multi-agent system works internally, how data flows between agents, and how the planner–evaluator loop forms an iterative reasoning cycle.



---



\# 🔍 High-Level Architecture



flowchart TD



A\[User Query] --> B\[Planner Agent]



B -->|Defines subtasks| C\[Data Agent]

B -->|Requests hypotheses| D\[Insight Agent]



C -->|Summaries + metrics| D



D -->|Hypotheses + evidence| E\[Evaluator Agent]



E -->|Validation results + confidence| B



B --> F\[Creative Improvement Generator]

F -->|New creatives| G\[(reports/)]



E --> G

D --> G



yaml

Copy code



---



\# 🧠 Agent Roles



\### \*\*1. Planner Agent\*\*

\- Breaks user query into structured tasks  

\- Controls loop between Insight → Evaluator → Planner  

\- Decides when insight is “good enough”  

\- Sends final task to Creative Generator  



---



\### \*\*2. Data Agent\*\*

\- Loads CSV  

\- Cleans + summarizes  

\- Computes metrics (ROAS, CTR, CPM, CVR)  

\- Returns structured JSON  



---



\### \*\*3. Insight Agent\*\*

\- Generates hypotheses  

\- Uses Think → Analyze → Conclude  

\- Never hallucinates data (uses summaries only)  



---



\### \*\*4. Evaluator Agent\*\*

\- Quantitatively validates hypotheses  

\- Computes supporting % drops, correlations, trends  

\- Returns confidence score  



---



\### \*\*5. Creative Generator\*\*

\- For low-CTR segments, generates new creatives  

\- Based on existing messaging patterns  

\- Produces variations: headlines, primary text, CTAs  



---



\# 🔁 Iterative Reasoning Loop

1\. Planner → ask: “Why did ROAS drop?”  

2\. Insight Agent → propose hypothesis  

3\. Evaluator → check data trends  

4\. Planner:  

&nbsp;  - If confidence < threshold → ask for revision  

&nbsp;  - If satisfied → conclude → move to creative generation  



---



\# 📦 Final Outputs Produced

\- \*\*insights.json\*\*  

\- \*\*creatives.json\*\*

\- \*\*report.md\*\*

\- Optional: logs + traces  



---



\# 🏁 Summary

The system mimics how a real senior growth analyst works — by combining:  

\*\*Planner → Insight → Evaluator → Creative\*\*  

This is exactly the architecture for LLM-native analytics engine.



