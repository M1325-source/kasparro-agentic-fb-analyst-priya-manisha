import re
from collections import Counter
import random

STOP = {
    "and","the","to","for","with","a","an","in","on","is","are",
    "of","our","we","you","your"
}

class CreativeGenerator:
    def generate(self, data_summary):
        outputs = []
        samples = data_summary.get("samples", {})
        low_campaigns = data_summary.get("low_ctr_campaigns", [])
        
        # Choose campaigns
        if low_campaigns:
            low_names = [c["campaign_name"] for c in low_campaigns]
        else:
            low_names = list(samples.keys())[:3]

        for campaign in low_names:
            texts = samples.get(campaign, [])[:50]

            # Extract common useful words
            words = []
            for t in texts:
                for w in re.findall(r"\w+", str(t).lower()):
                    if w not in STOP and len(w) > 2:
                        words.append(w)

            common = [w for w, _ in Counter(words).most_common(5)]
            if not common:
                common = ["comfort", "soft", "new"]

            # Generate 3 creative ideas
            suggestions = []
            for _ in range(3):

                # SAFE text building (no f-string issues)
                word1 = random.choice(["Feel", "Discover", "Try"])
                word2 = common[0].capitalize()
                headline = word1 + " " + word2 + " Today"

                phrase = random.choice(
                    ["Limited stock!", "Customer favorite!", "Great comfort!"]
                )
                text = "Experience our " + common[0] + " collection — " + phrase

                cta = random.choice(["Shop Now", "Buy Now", "Explore"])

                suggestions.append({
                    "headline": headline,
                    "text": text,
                    "cta": cta
                })

            outputs.append({
                "campaign_name": campaign,
                "suggestions": suggestions
            })

        return outputs
