import pandas as pd
import numpy as np
from typing import Dict, Any
from src.agents.data_agent_helpers import validate_dataframe
from src.utils.logger import log_event

REQUIRED_COLS = [
    "campaign_name",
    "date",
    "spend",
    "impressions",
    "clicks",
    "ctr",
    "purchases",
    "revenue",
    "roas",
    "creative_message",
]

class DataAgent:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def load_df(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(self.csv_path, parse_dates=["date"], dayfirst=False)
            log_event("DataAgent", "loaded_csv", {"path": self.csv_path, "rows": int(len(df))})
            return df
        except Exception as e:
            log_event("DataAgent", "load_error", {"error": str(e)})
            raise

    def _ensure_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        missing = [c for c in REQUIRED_COLS if c not in df.columns]
        if missing:
            log_event("DataAgent", "missing_columns", {"missing": missing})
            for c in missing:
                df[c] = np.nan
        return df

    def summarize(self) -> Dict[str, Any]:
        df = self.load_df()
        df = self._ensure_columns(df)

        # drop rows without date or campaign_name
        df = df.dropna(subset=["date", "campaign_name"])
        df = df.sort_values("date")

        # validation
        issues = validate_dataframe(df)
        if issues:
            log_event("DataAgent", "validation_warning", {"issues_count": len(issues)})
        else:
            log_event("DataAgent", "validation_ok", {"rows": int(len(df))})

        # coerce numeric columns
        numeric_cols = ["spend", "impressions", "clicks", "ctr", "purchases", "revenue", "roas"]
        for c in numeric_cols:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce")

        # compute first / last windows using up to 7 unique normalized dates
        uniq_dates = pd.Series(df["date"].dt.normalize().unique())
        first_dates = uniq_dates.head(7).tolist()
        last_dates = uniq_dates.tail(7).tolist()

        if len(first_dates) < 2:
            mid = max(1, len(df) // 2)
            first_mean_roas = df.iloc[:mid]["roas"].mean()
            last_mean_roas = df.iloc[mid:]["roas"].mean()
        else:
            first_mean_roas = df[df["date"].dt.normalize().isin(first_dates)]["roas"].mean()
            last_mean_roas = df[df["date"].dt.normalize().isin(last_dates)]["roas"].mean()

        first_mean_roas = float(np.nan) if pd.isna(first_mean_roas) else float(first_mean_roas)
        last_mean_roas = float(np.nan) if pd.isna(last_mean_roas) else float(last_mean_roas)

        roas_change_pct = 0.0
        if pd.notna(first_mean_roas) and first_mean_roas != 0:
            roas_change_pct = (last_mean_roas - first_mean_roas) / abs(first_mean_roas)

        # Campaign-level aggregation
        agg_cols = {}
        if "ctr" in df.columns:
            agg_cols["ctr"] = "mean"
        if "roas" in df.columns:
            agg_cols["roas"] = "mean"
        if "spend" in df.columns:
            agg_cols["spend"] = "sum"
        if "impressions" in df.columns:
            agg_cols["impressions"] = "sum"
        if "clicks" in df.columns:
            agg_cols["clicks"] = "sum"

        if agg_cols:
            camp_ctr = df.groupby("campaign_name").agg(agg_cols).reset_index()
        else:
            camp_ctr = pd.DataFrame(columns=["campaign_name"])

        median_ctr = camp_ctr["ctr"].median() if "ctr" in camp_ctr.columns and not camp_ctr["ctr"].empty else float(np.nan)

        low_ctr_campaigns = []
        if "ctr" in camp_ctr.columns and not camp_ctr.empty:
            low_df = camp_ctr[camp_ctr["ctr"] < median_ctr].sort_values("ctr").head(5)
            low_ctr_campaigns = low_df.to_dict(orient="records")

        top_campaign_by_spend = []
        if "spend" in camp_ctr.columns and not camp_ctr.empty:
            top_campaign_by_spend = camp_ctr.sort_values("spend", ascending=False).head(1).to_dict(orient="records")

        # Build samples
        sample_by_campaign = {}
        try:
            for c in df["campaign_name"].dropna().unique()[:50]:
                s = df[df["campaign_name"] == c]
                msgs = s["creative_message"].dropna().astype(str).head(30).tolist() if "creative_message" in s else []
                sample_by_campaign[c] = msgs
        except Exception as e:
            log_event("DataAgent", "sample_extraction_error", {"error": str(e)})

        summary = {
            "rows": int(len(df)),
            "period_start": str(df["date"].min()) if not df["date"].empty else None,
            "period_end": str(df["date"].max()) if not df["date"].empty else None,
            "first_mean_roas": float(np.nan_to_num(first_mean_roas)),
            "last_mean_roas": float(np.nan_to_num(last_mean_roas)),
            "roas_change_pct": float(np.nan_to_num(roas_change_pct)),
            "median_ctr": float(np.nan_to_num(median_ctr)),
            "low_ctr_campaigns": low_ctr_campaigns,
            "top_campaign_by_spend": top_campaign_by_spend,
            "samples": sample_by_campaign,
            "campaign_metrics": camp_ctr.to_dict(orient="records") if not camp_ctr.empty else []
        }

        log_event("DataAgent", "summarized", {"rows": summary["rows"], "roas_change_pct": summary["roas_change_pct"], "median_ctr": summary["median_ctr"]})

        return summary
