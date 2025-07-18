import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Clean Subitem Counts & Compute Percentages")

# 1) Upload counts CSV
counts_file = st.file_uploader("Upload your subitem_rating_counts.csv", type="csv")
if not counts_file:
    st.stop()
counts = pd.read_csv(counts_file, index_col=0)

# 2) Optional corrections
st.subheader("Optional: Provide typo corrections")

json_input = st.text_area(
    "Paste a JSON dict of corrections, e.g.\n"
    '{"Actves":"Actives","Actvies":"Actives","Haevy metals":"Heavy metals"}',
    height=100,
)

mapping_file = st.file_uploader("Or upload a 2‑column CSV (typo,correct)", type="csv")

# Build corrections dict
corrections = {}
if json_input.strip():
    try:
        corrections = json.loads(json_input)
    except Exception as e:
        st.error(f"Invalid JSON: {e}")
        st.stop()
elif mapping_file:
    df_map = pd.read_csv(mapping_file, header=None, names=["typo","correct"])
    corrections = dict(zip(df_map.typo.astype(str), df_map.correct.astype(str)))

# Apply corrections
if corrections:
    counts = (
        counts
          .reset_index()
          .assign(subitem_name=lambda d: d.subitem_name.replace(corrections))
          .groupby("subitem_name", as_index=True)
          .sum()
    )
