import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time

# Constants
ALERT_FILE = "logs/alert_data.csv"
REFRESH_INTERVAL = 10  # seconds

# App Config
st.set_page_config(page_title="Real-Time Alert Dashboard", layout="wide")

st.title("📊 Real-Time Alerting System Dashboard")
st.markdown("---")

# Load Data
@st.cache_data(ttl=REFRESH_INTERVAL)
def load_data():
    if not os.path.exists(ALERT_FILE):
        return pd.DataFrame(columns=["timestamp", "source", "type", "value", "message"])
    return pd.read_csv(ALERT_FILE)


data = load_data()

# Display Metrics
st.subheader("🔎 System Summary")
col1, col2, col3 = st.columns(3)

col1.metric("Total Alerts", len(data))
col2.metric("ML-Based Anomalies", len(data[data["message"] == "ML"]))
col3.metric("Rule-Based Alerts", len(data[data["message"] == "Rule-based"]))

# Chart: Alerts over time
if not data.empty:
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data_sorted = data.sort_values("timestamp")

    st.subheader("📈 Alerts Over Time")

    fig = px.scatter(
        data_sorted,
        x="timestamp",
        y="source",
        color="message",
        symbol="message",
        title="Alert Timeline (Color: Alert Type)",
        labels={"timestamp": "Time", "source": "Source", "message": "Type"},
        color_discrete_map={"ML": "red", "Rule-based": "orange"}
    )
    fig.update_traces(marker=dict(size=10), selector=dict(mode='markers'))
    fig.update_layout(legend_title_text="Alert Type", height=400)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No alert data available yet.")

# Table View
st.subheader("📋 Detailed Alerts")
st.dataframe(data.tail(25).sort_values(by="timestamp", ascending=False), use_container_width=True)

# Refresh Hint
st.markdown(f"<small>Refreshing every {REFRESH_INTERVAL} seconds...</small>", unsafe_allow_html=True)
