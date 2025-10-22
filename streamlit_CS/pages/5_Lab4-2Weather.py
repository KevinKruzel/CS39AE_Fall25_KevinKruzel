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
SAMPLE_DF = pd.DataFrame([{
    "time_utc": ts_utc,
    "time_local": ts_local,
    "temperature": 20.0,
    "wind": 3.0,
}])

# 3) FETCH (CACHED)
@st.cache_data(ttl=600, show_spinner=False)  # Cache for 10 minutes
def get_weather(url: str):
    """Return (df, error_message). Never raise. Safe for beginners."""
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        j = r.json()["current"]
        ts = pd.to_datetime(j["time"], utc=True)  # tz-aware UTC
        df = pd.DataFrame([{
            "time_utc": ts,
            "time_local": ts.tz_convert(TZ),
            "temperature": float(j["temperature_2m"]),
            "wind": float(j["wind_speed_10m"]),
        }])
        return df, None
    except requests.RequestException as e:
        return None, f"Network/HTTP error: {e}"
    except Exception as e:
        return None, f"Parse error: {e}"

# 4) REFRESH BUTTON / AUTO REFRESH CONTROLS
st.subheader("🔁 Auto Refresh Settings")
refresh_sec = st.slider("Refresh every (sec)", min_value=10, max_value=120, value=30)
auto_refresh = st.toggle("Enable auto-refresh", value=False)
st.caption(f"Last refreshed at: {time.strftime('%H:%M:%S')}")

# 5) MAIN VIEW
st.subheader("Temperature (°C) over Time")

# Fetch one reading
df_now, err = get_weather(wurl)
if err or df_now is None or df_now.empty:
    st.warning(f"{err or 'No data'}\nShowing sample data so the demo continues.")
    df_now = SAMPLE_DF.copy()

# Accumulate readings across reruns so we get a time series
if "weather_hist" not in st.session_state:
    st.session_state.weather_hist = df_now.copy()
else:
    hist = st.session_state.weather_hist
    st.session_state.weather_hist = (
        pd.concat([hist, df_now], ignore_index=True)
          .drop_duplicates(subset=["time_utc"])     # avoid dupes if cache hits
          .sort_values("time_utc")
          .reset_index(drop=True)
    )

hist = st.session_state.weather_hist.copy()

# Ensure numeric values (defensive)
hist["temperature"] = pd.to_numeric(hist["temperature"], errors="coerce")

# Show table
st.dataframe(
    hist[["time_local", "temperature", "wind"]],
    use_container_width=True,
    hide_index=True
)

# Line chart (appropriate for time series)
fig = px.line(
    hist,
    x="time_local",
    y="temperature",
    markers=True,
    title="Denver Temperature (local time)",
    labels={"time_local": "Time (America/Denver)", "temperature": "°C"},
)
fig.update_layout(margin=dict(l=10, r=10, t=60, b=10))
st.plotly_chart(fig, use_container_width=True)

# If auto-refresh is ON, wait and rerun the app
if auto_refresh:
    time.sleep(refresh_sec)
    get_weather.clear()  # clear cache so we actually refetch
    st.rerun()
