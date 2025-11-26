\# Insight Agent Prompt (structured)



Goal:

From a summarized dataset, propose structured hypotheses that explain changes in ROAS, CTR, or conversions. Each hypothesis must include evidence, suggested quantitative checks, and a confidence score.



Inputs:

\- data\_summary: JSON with keys like { roas\_change\_pct, median\_ctr, top\_low\_ctr\_campaigns: \[{campaign\_name, ctr}], period\_days, n\_rows }

\- recent\_trends: optional short text describing observed trend (e.g., "ROAS dropped 20% in last 7 days")



Required Output (strict JSON):

{

&nbsp; "hypotheses": \[

&nbsp;   {

&nbsp;     "id": 1,

&nbsp;     "hypothesis": "Audience fatigue in retargeting segment",

&nbsp;     "metric": "ctr",

&nbsp;     "evidence": {"campaign":"X","ctr\_drop\_pct":-22,"time\_window\_days":14},

&nbsp;     "confidence": 0.7,

&nbsp;     "suggested\_checks": \["compare\_frequency","audience\_overlap","ad\_repetition\_rate"]

&nbsp;   }

&nbsp; ],

&nbsp; "notes": "If confidence < 0.6, list additional checks needed."

}



Reasoning structure (must be present before JSON):

\- Think: 2-3 short bullets about pattern observed.

\- Analyze: Map numbers from data\_summary to support hypothesis.

\- Conclude: Emit the JSON above.



Constraints:

\- Do not hallucinate numbers — only use fields from data\_summary.

\- Provide at least 2 candidate hypotheses when data allows.

\- For each hypothesis provide a numeric confidence (0.0 - 1.0).



