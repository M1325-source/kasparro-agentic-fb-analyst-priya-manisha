import pandas as pd
from src.agents.data_agent_helpers import validate_dataframe

def test_validate_dataframe_ok():
    df = pd.DataFrame({
        "spend":[10,20,30],
        "impressions":[100,200,150],
        "clicks":[5,10,7],
        "ctr":[0.05,0.05,0.046],
        "purchases":[1,2,1],
        "revenue":[100,200,150],
        "roas":[10,10,5],
        "campaign_name":["A","B","A"],
        "date": pd.to_datetime(["2025-11-01","2025-11-02","2025-11-03"])
    })
    issues = validate_dataframe(df)
    assert isinstance(issues, list)
