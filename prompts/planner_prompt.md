\# Planner Agent Prompt (structured)



Goal:

Decompose a high-level user query into discrete, ordered subtasks suitable for the multi-agent pipeline.

Each subtask should include a short description, required agents, expected output schema, and priority score.



Inputs:

\- user\_query: string (e.g. "Analyze ROAS drop in the last 7 days")

\- data\_summary: short JSON summary with keys like {roas\_change\_pct, median\_ctr, n\_rows, period\_days}



Output (strict JSON array of tasks):

\[

&nbsp; {

&nbsp;   "id": 1,

&nbsp;   "name": "load\_and\_summarize",

&nbsp;   "description": "Load CSV, parse dates, compute campaign-level metrics (spend, impressions, clicks, ctr, purchases, revenue, roas).",

&nbsp;   "required\_agents": \["DataAgent"],

&nbsp;   "output\_schema": {"type":"object","properties":{"campaigns":"array","metrics":"object"}},

&nbsp;   "priority": 10

&nbsp; }

]



Reasoning structure (required in plain text before JSON):

1\. Think: short bullets explaining the decomposition reasoning.

2\. Analyze: why each subtask is necessary (one sentence each).

3\. Plan: output the JSON array (exact schema).



Constraints:

\- Use data\_summary values, not the full CSV, to decide task priority.

\- Keep the total number of primary tasks under 8.

\- For each task set a numeric priority (1-10). Higher = earlier.

\- If input user\_query is ambiguous, add a clarifying subtask (id: 99) that asks for precise time-window or metric.



