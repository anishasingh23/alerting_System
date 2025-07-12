import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load CSV
df = pd.read_csv("logs/alert_data.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp")

# Global aesthetics
sns.set(style="whitegrid")
plt.rcParams.update({
    "font.size": 12,
    "figure.autolayout": True,
    "axes.titlesize": 16,
    "axes.labelsize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "axes.titlepad": 20,
})

# Create directory for plots if needed
os.makedirs("logs/plots", exist_ok=True)

# 1️⃣ ALERT COUNT BY TYPE
plt.figure(figsize=(8, 5))
palette = {
    "CPU": "#e74c3c",
    "Memory": "#f1c40f",
    "Disk I/O": "#3498db",
    "ML": "#9b59b6",
    "Other": "#7f8c8d"
}
sns.countplot(data=df, x="type", palette=palette, order=df["type"].value_counts().index)
plt.title("🔔 Alert Frequency by Type")
plt.xlabel("Alert Type")
plt.ylabel("Count")
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.savefig("logs/plots/alert_type_counts.png", dpi=300)
plt.show()

# 2️⃣ ALERT TIMELINE SCATTER
plt.figure(figsize=(10, 5))
sns.scatterplot(
    data=df,
    x="timestamp",
    y="type",
    hue="type",
    palette=palette,
    s=100,
    edgecolor="black"
)
plt.title("📈 Alert Timeline by Type")
plt.xlabel("Time")
plt.ylabel("Alert Type")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("logs/plots/alerts_timeline.png", dpi=300)
plt.show()
