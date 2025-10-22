# 1) Read API once
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import time

st.set_page_config(page_title="Live API Demo (Simple)", page_icon="📡", layout="wide")

# Disable fade/transition so charts don't blink between reruns
st.markdown(
    """
    <style>
      [data-testid="stPlotlyChart"], .stPlotlyChart, .stElementContainer {
        transition: none !important;
        opacity: 1 !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📡 Simple Live Data Demo (Open-Meteo)")
st.caption("Friendly demo with manual refresh + fallback data so it never crashes.")

# 2) Config (Weather)
lat, lon = 39.7392, -104.9903  # Denver
wurl = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m"
)
TZ = "America/Denver"

# Tiny sample to keep the demo working even if the API hiccups
ts_utc = pd.Timestamp.now(tz="UTC")
ts_local = ts_utc.tz_convert(TZ)
SAMPLE_DF = pd.DataFrame(
    [{
        "time_utc": ts_utc,
        "time_local": ts_local,
        "temperature": 20.0,
        "wind": 3.0,
    }]
)

# 3) FETCH (CACHED)
@st.cache_data(ttl=600, show_spinner=False)  # Cache for 10 minutes
def get_weather(url: str):
    """Return (df, error_message). Never raise. Safe for beginners."""
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        j = r.json()["current"]
