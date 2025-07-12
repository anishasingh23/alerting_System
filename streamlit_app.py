import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load alert data
@st.cache_data
def load_alerts():
    filepath = "logs/alert_data.csv"
    if os.path.exists(filepath):
        return pd.read_csv(filepath, parse_dates=["timestamp"])
    return pd.DataFrame(columns=["timestamp", "source", "type", "value", "message"])

# Title
st.title(" Real-Time Alerting Dashboard")

# Load data
alerts = load_alerts()

if alerts.empty:
    st.warning("No alert data found yet. Run the main alert system first.")
    st.stop()

# Filters
sources = alerts["source"].unique().tolist()
types = alerts["type"].unique().tolist()

selected_sources = st.multiselect("Filter by Source", sources, default=sources)
selected_types = st.multiselect("Filter by Alert Type", types, default=types)

# Filtered data
filtered = alerts[
    (alerts["source"].isin(selected_sources)) &
    (alerts["type"].isin(selected_types))
]

# Summary
st.subheader(" Alert Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Alerts", len(filtered))
col2.metric("ML Anomalies", filtered["type"].str.contains("ML").sum())
col3.metric("Unique Sources", filtered["source"].nunique())

# Color Mapping
def classify_type(alert_type):
    return "ML" if "ML" in alert_type else "Rule"

filtered["category"] = filtered["type"].apply(classify_type)
color_map = {"Rule": "red", "ML": "blue"}
colors = filtered["category"].map(color_map)

# Plot
st.subheader(" Alert Timeline")

fig, ax = plt.subplots()
ax.scatter(filtered["timestamp"], filtered["source"], c=colors, alpha=0.7)

ax.set_xlabel("Time")
ax.set_ylabel("Source")
ax.set_title("Alert Events Timeline")
ax.grid(True)
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', label='Rule-based Alert', markerfacecolor='red', markersize=8),
    plt.Line2D([0], [0], marker='o', color='w', label='ML Anomaly', markerfacecolor='blue', markersize=8),
]
ax.legend(handles=legend_elements)
st.pyplot(fig)

# Table
st.subheader(" Raw Alert Data")
st.dataframe(filtered.sort_values(by="timestamp", ascending=False), use_container_width=True)
