import pandas as pd
import numpy as np

class DataAgent:
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def summarize(self):
        df = pd.read_csv(self.csv_path, parse_dates=["date"], dayfirst=False)

        df = df.dropna(subset=["date", "roas", "ctr", "spend", "impressions", "clicks", "purchases"])
        df = df.sort_values("date")

        first_dates = df["date"].dt.normalize().unique()[:7]
        last_dates = df["date"].dt.normalize().unique()[-7:]

        if len(first_dates) < 7:
            mid = len(df)//2
            first_mean_roas = df.iloc[:mid]["roas"].mean()
            last_mean_roas = df.iloc[mid:]["roas"].mean()
        else:
            first_mean_roas = df[df["date"].dt.normalize().isin(first_dates)]["roas"].mean()
            last_mean_roas = df[df["date"].dt.normalize().isin(last_dates)]["roas"].mean()

        roas_change_pct = 0.0
        if pd.notna(first_mean_roas) and first_mean_roas != 0:
            roas_change_pct = (last_mean_roas - first_mean_roas) / abs(first_mean_roas)

        camp_ctr = df.groupby("campaign_name").agg(
            {"ctr": "mean", "roas": "mean", "spend": "sum", "impressions": "sum", "clicks": "sum"}
        ).reset_index()

        median_ctr = camp_ctr["ctr"].median()
        low_ctr_campaigns = camp_ctr[camp_ctr["ctr"] < median_ctr].sort_values("ctr").to_dict(orient="records")[:5]

        summary = {
            "rows": int(len(df)),
            "first_mean_roas": float(np.nan_to_num(first_mean_roas)),
            "last_mean_roas": float(np.nan_to_num(last_mean_roas)),
            "roas_change_pct": float(np.nan_to_num(roas_change_pct)),
            "median_ctr": float(np.nan_to_num(median_ctr)),
            "low_ctr_campaigns": low_ctr_campaigns,
            "top_campaign_by_spend": camp_ctr.sort_values("spend", ascending=False).head(1).to_dict(orient="records")
        }

        sample_by_campaign = {}
        for c in df["campaign_name"].unique()[:10]:
            s = df[df["campaign_name"] == c]
            sample_by_campaign[c] = list(s["creative_message"].astype(str).head(30).values)

        summary["samples"] = sample_by_campaign

        return summary
