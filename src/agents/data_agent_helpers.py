import pandas as pd
from src.utils.logger import log_event

def validate_dataframe(df: pd.DataFrame, numeric_cols=None):
    """
    Basic validation rules:
    - empty dataframe
    - null counts
    - numeric dtype checks
    - non-positive checks for impressions/spend
    - CTR outlier detection using IQR
    Returns: list of issues (empty list == OK)
    """
    issues = []
    if df is None:
        issues.append("no_dataframe")
        log_event("DataAgent", "validation_failed", {"issues": issues})
        return issues

    if df.empty:
        issues.append("empty_dataframe")
        log_event("DataAgent", "validation_empty", {"rows": 0})
        return issues

    # Null checks
    null_counts = df.isnull().sum().to_dict()
    total_nulls = sum(null_counts.values())
    if total_nulls > 0:
        issues.append({"null_counts": null_counts})

    # Numeric columns checks
    if numeric_cols is None:
        numeric_cols = ["spend", "impressions", "clicks", "ctr", "purchases", "revenue", "roas"]

    for c in numeric_cols:
        if c in df.columns:
            if not pd.api.types.is_numeric_dtype(df[c]):
                issues.append({"bad_type": {c: str(df[c].dtype)}})
            else:
                if c in ("impressions", "spend") and (df[c] <= 0).any():
                    issues.append({"non_positive_values": c})
                if c == "ctr" and df[c].std() > 0:
                    q1 = df[c].quantile(0.25)
                    q3 = df[c].quantile(0.75)
                    iqr = q3 - q1
                    upper = q3 + 3 * iqr
                    lower = q1 - 3 * iqr
                    outliers = df[(df[c] > upper) | (df[c] < lower)]
                    if not outliers.empty:
                        issues.append({"ctr_outliers": int(outliers.shape[0])})

    if issues:
        log_event("DataAgent", "validation_issues", {"issues": issues, "rows": int(len(df))})
    else:
        log_event("DataAgent", "validation_ok", {"rows": int(len(df))})

    return issues
