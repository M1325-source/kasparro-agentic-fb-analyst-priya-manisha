\# Creative Improvement Generator Prompt



Goal:

Generate improved creative ideas for campaigns with low CTR. Use ONLY the words, tones, and themes found in the dataset’s existing creative\_message fields. Do not hallucinate product types.



Inputs:

\- campaign\_name

\- sample\_creatives: list of strings (existing creative\_message)

\- common\_keywords: extracted from sample\_creatives

\- metrics: { "ctr": float, "impressions": int }



Output Format (strict):

{

&nbsp; "campaign": "<name>",

&nbsp; "ideas": \[

&nbsp;   {

&nbsp;     "headline": "<short punchy headline>",

&nbsp;     "primary\_text": "<1-2 line message using dataset tone>",

&nbsp;     "cta": "<CTA like Shop Now, Try Today, Explore>",

&nbsp;     "keyword\_used": "<one of the common\_keywords>"

&nbsp;   }

&nbsp; ]

}



Reasoning:

1\. Identify recurring tone (comfort, soft, premium, casual, dailywear, breathable etc.)

2\. Use only dataset-approved vocabulary.

3\. Do NOT invent product categories that were not present.

4\. Output at least 3 ideas per campaign.

5\. Keep the ideas advertising-ready and crisp.



Reflection:

If any idea seems repetitive or too generic, regenerate it using alternate common\_keywords.



