# src/agents/data_agent.py
import pandas as pd
import numpy as np
from typing import Dict, Any
from src.utils.data_sources import load_source
from src.utils.logger import log_event

class DataAgent:
    def __init__(self, source_spec: Dict[str, Any], config: Dict[str, Any]):
        """
        source_spec: config for data source (type, path, parse_dates)
        config: includes adaptivity thresholds, e.g. {"sample_threshold":10000, "batch_size":50000}
        """
        self.source_spec = source_spec
        self.config = config

    def _validate_required_columns(self, df: pd.DataFrame, required):
        missing = [c for c in required if c not in df.columns]
        return missing

    def _basic_validation(self, df: pd.DataFrame):
        issues = []
        required = ["date", "roas", "ctr", "spend", "impressions", "clicks", "campaign_name", "creative_message"]
        missing = self._validate_required_columns(df, required)
        if missing:
            issues.append({"type":"missing_columns","missing": missing})
        # null fraction checks
        for c in required:
            if c in df.columns:
                null_frac = df[c].isna().mean()
                if null_frac > 0.5:
                    issues.append({"type":"high_nulls","column":c,"null_frac":float(null_frac)})
        return issues

    def _sample_df(self, df: pd.DataFrame, max_rows: int):
        if len(df) <= max_rows:
            return df
        return df.sample(n=max_rows, random_state=self.config.get("random_seed", 42))

    def summarize(self) -> Dict[str, Any]:
        # load
        df = load_source(self.source_spec)
        log_event("DataAgent", "loaded_source", {"rows": len(df), "source": self.source_spec.get("path")})

        # basic validation
        issues = self._basic_validation(df)
        if issues:
            log_event("DataAgent", "validation_issues", {"count": len(issues), "issues": issues})

        # adaptivity strategy
        sample_threshold = int(self.config.get("sample_threshold", 20000))
        batch_size = int(self.config.get("batch_size", 100000))

        rows = len(df)
        strategy = "full"
        if rows == 0:
            log_event("DataAgent", "empty_dataset", {})
            return {"rows": 0, "samples": {}, "insights": [], "strategy": "empty"}

        if rows <= sample_threshold:
            proc_df = df
            strategy = "full"
        elif rows <= batch_size:
            # sample to a reasonable size for LLM prompts / insight generation
            proc_df = self._sample_df(df, sample_threshold)
            strategy = "sample"
        else:
            # very large dataset: sample more carefully using stratified by campaign_name
            strategy = "stratified_sample"
            n_per_campaign = max(100, sample_threshold // max(1, df["campaign_name"].nunique()))
            parts = []
            for c in df["campaign_name"].unique():
                sub = df[df["campaign_name"] == c]
                k = min(len(sub), n_per_campaign)
                parts.append(sub.sample(n=k, random_state=self.config.get("random_seed", 42)))
            proc_df = pd.concat(parts, ignore_index=True)

        log_event("DataAgent", "selected_strategy", {"strategy": strategy, "rows_original": rows, "rows_used": len(proc_df)})

        # reuse summary logic (safe aggregated numbers)
        proc_df = proc_df.dropna(subset=["roas", "ctr"], how="any")
        proc_df = proc_df.sort_values("date") if "date" in proc_df.columns else proc_df

        first_mean_roas = float(np.nan)
        last_mean_roas = float(np.nan)
        try:
            if "date" in proc_df.columns:
                first_dates = proc_df["date"].dt.normalize().unique()[:7]
                last_dates = proc_df["date"].dt.normalize().unique()[-7:]
                if len(first_dates) < 7:
                    mid = len(proc_df)//2
                    first_mean_roas = proc_df.iloc[:mid]["roas"].mean()
                    last_mean_roas = proc_df.iloc[mid:]["roas"].mean()
                else:
                    first_mean_roas = proc_df[proc_df["date"].dt.normalize().isin(first_dates)]["roas"].mean()
                    last_mean_roas = proc_df[proc_df["date"].dt.normalize().isin(last_dates)]["roas"].mean()
            else:
                first_mean_roas = proc_df["roas"].head(10).mean()
                last_mean_roas = proc_df["roas"].tail(10).mean()
        except Exception as e:
            log_event("DataAgent", "roas_calc_error", {"error": str(e)})

        roas_change_pct = 0.0
        if pd.notna(first_mean_roas) and first_mean_roas != 0:
            roas_change_pct = (last_mean_roas - first_mean_roas) / abs(first_mean_roas)

        camp_ctr = proc_df.groupby("campaign_name").agg(
            {"ctr": "mean", "roas": "mean", "spend": "sum", "impressions": "sum", "clicks": "sum"}
        ).reset_index() if "campaign_name" in proc_df.columns else pd.DataFrame()

        median_ctr = float(camp_ctr["ctr"].median()) if not camp_ctr.empty else 0.0
        low_ctr_campaigns = camp_ctr[camp_ctr["ctr"] < median_ctr].sort_values("ctr").to_dict(orient="records")[:5] if not camp_ctr.empty else []

        summary = {
            "rows": int(rows),
            "rows_used": int(len(proc_df)),
            "strategy": strategy,
            "first_mean_roas": float(np.nan_to_num(first_mean_roas)),
            "last_mean_roas": float(np.nan_to_num(last_mean_roas)),
            "roas_change_pct": float(np.nan_to_num(roas_change_pct)),
            "median_ctr": float(np.nan_to_num(median_ctr)),
            "low_ctr_campaigns": low_ctr_campaigns,
            "top_campaign_by_spend": camp_ctr.sort_values("spend", ascending=False).head(1).to_dict(orient="records") if not camp_ctr.empty else [],
        }

        sample_by_campaign = {}
        if "campaign_name" in proc_df.columns:
            for c in proc_df["campaign_name"].unique()[:10]:
                s = proc_df[proc_df["campaign_name"] == c]
                sample_by_campaign[c] = list(s.get("creative_message", s.columns[0]).astype(str).head(30).values if "creative_message" in s else [])
        summary["samples"] = sample_by_campaign

        log_event("DataAgent", "summary_ready", {"rows": rows, "rows_used": len(proc_df)})

        return summary
