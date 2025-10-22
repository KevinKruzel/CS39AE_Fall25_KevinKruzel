# pages/3_Pie.py
from pathlib import Path
import pandas as pd
import streamlit as st

# Try Plotly first; fall back to Matplotlib if not installed
try:
    import plotly.express as px
    _HAS_PLOTLY = True
except Exception:
    _HAS_PLOTLY = False
    import matplotlib.pyplot as plt

st.title("🥧 Pie / Donut Chart")

# ---------- Load CSV ----------
APP_ROOT = Path(__file__).parents[1]
CSV_PATH = APP_ROOT / "data" / "pie_demo.csv"

if not CSV_PATH.exists():
    st.error(f"Couldn't find `{CSV_PATH}`. Make sure your CSV is at `data/pie_demo.csv`.")
    st.stop()

df = pd.read_csv(CSV_PATH)

if df.empty or len(df.columns) < 2:
    st.error("CSV must have at least two columns (category + numeric).")
    st.stop()

# ---------- Choose columns ----------
st.subheader("Settings")

# Guess likely columns
cat_guess_idx = 0
for i, c in enumerate(df.columns):
    if df[c].dtype == "object":
        cat_guess_idx = i
        break

num_guess_idx = len(df.columns) - 1
for i, c in enumerate(df.columns):
    if pd.api.types.is_numeric_dtype(df[c]):
        num_guess_idx = i
        break

c1, c2 = st.columns(2)
with c1:
    cat_col = st.selectbox("Category column", options=list(df.columns), index=cat_guess_idx)
with c2:
    val_col = st.selectbox("Value column (numeric)", options=list(df.columns), index=num_guess_idx)

# Ensure numeric
if not pd.api.types.is_numeric_dtype(df[val_col]):
    df[val_col] = pd.to_numeric(df[val_col], errors="coerce")

work = (
    df[[cat_col, val_col]]
    .rename(columns={cat_col: "Category", val_col: "Value"})
    .dropna(subset=["Category", "Value"])
    .groupby("Category", as_index=False)["Value"].sum()
)

if work.empty:
    st.error("No usable data after cleaning. Check your CSV values.")
    st.stop()

# ---------- Controls ----------
left, right = st.columns(2)
with left:
    donut = st.toggle("Donut style", value=True)
    sort_desc = st.toggle("Sort by value (desc)", value=True)
with right:
    top_n = st.slider("Show top N (group others as 'Other')",
                      min_value=1, max_value=min(12, len(work)), value=min(6, len(work)))

if sort_desc:
    work = work.sort_values("Value", ascending=False)

if top_n < len(work):
    top = work.head(top_n).copy()
    other_sum = work["Value"].iloc[top_n:].sum()
    if other_sum > 0:
        top.loc[len(top)] = ["Other", other_sum]
    work = top

total = float(work["Value"].sum())
st.write(f"**Total:** {total:,.2f}")

# ---------- Chart ----------
if _HAS_PLOTLY:
    fig = px.pie(work, names="Category", values="Value", hole=0.5 if donut else 0.0)
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)
else:
    # Matplotlib fallback
    fig, ax = plt.subplots(figsize=(6, 4))
    if donut:
        wedges, texts, autotexts = ax.pie(
            work["Value"],
            labels=work["Category"],
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops={"width": 0.5}  # donut effect
        )
        ax.set(aspect="equal")
    else:
        ax.pie(work["Value"], labels=work["Category"], autopct="%1.1f%%", startangle=90)
        ax.set(aspect="equal")
    st.pyplot(fig, use_container_width=True)

# ---------- Preview ----------
with st.expander("Preview data"):
    st.dataframe(work, use_container_width=True, hide_index=True)

st.caption("Reads from `data/pie_demo.csv`. Pick columns, toggle donut, sort, and group to Top-N.")
