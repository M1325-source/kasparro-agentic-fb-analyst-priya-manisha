import sys
import json
import os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from src.run import main as run_pipeline
import streamlit as st


st.set_page_config(page_title="Kasparro FB Analyst", layout="wide")

st.title("📊 Kasparro Agentic Facebook Performance Analyst")

query = st.text_input("Enter your analysis query", "Analyze ROAS drop")

if st.button("Run Analysis"):
    st.write("⏳ Running agents… please wait…")
    run_pipeline()

    st.success("Done! Outputs generated.")

    st.subheader("🧠 Insights")
    with open("reports/insights.json") as f:
        st.json(json.load(f))

    st.subheader("🎨 Creative Recommendations")
    with open("reports/creatives.json") as f:
        st.json(json.load(f))

    st.subheader("📄 Final Report")
    with open("reports/report.md") as f:
        st.markdown(f.read())
