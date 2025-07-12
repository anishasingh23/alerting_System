# Real-Time Anomaly Detection & Alerting System

---

## Overview

This project implements a real-time, multithreaded alerting system that processes simulated event data streams and detects anomalies using both rule-based logic and a machine learning model (Isolation Forest). The system includes a responsive Streamlit dashboard for live visualization of detected alerts.

---

## Features

- Real-time data generation for CPU, memory, latency, and other metrics  
- Multithreaded event processing using Python `threading`  
- Rule-based alerting system with customizable logic  
- ML-based anomaly detection using Isolation Forest  
- Alerts logged to both terminal and structured CSV files  
- Streamlit dashboard with:
  - Color-coded timeline of alerts
  - Filtering by source or alert type
  - Rule-based vs ML-based alert visualization  

---

## Architecture

```
                 ┌──────────────────────┐
                 │   Event Generator    │
                 └────────┬─────────────┘
                          ↓
             ┌─────────────────────────────┐
             │   Shared Thread-Safe Queue  │◄────────────┐
             └────────────┬────────────────┘             │
                          ↓                              │
           ┌────────────────────────────┐                │
           │    Worker Thread (× N)     │                │
           │ - Rule-Based Alerting      │                │
           │ - ML Anomaly Detection     │                │
           └────────────┬───────────────┘                │
                        ↓                                │
                ┌───────────────┐         ┌────────────┐ │
                │  Logging CSV  │◄────────┤ Alert Writer│─┘
                └───────────────┘         └────────────┘

                                 ↓
                       ┌────────────────────┐
                       │   Streamlit UI     │
                       └────────────────────┘
```

---

## Sample Project Demo

> Add a demo walkthrough of the Streamlit dashboard in `.gif` format.

📁 Save your GIF in `assets/demo.gif`

```
[ Insert GIF showcasing Streamlit dashboard in action ]
```

---

## Streamlit Dashboard Screenshot

📁 Save a static screenshot as `assets/dashboard.png`

```
[ Insert dashboard screenshot here ]
```

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/realtime-alerting-system.git
cd realtime-alerting-system
```

### 2. Create & Activate Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## How to Run

### 1. Start the Real-Time System

```bash
python main.py
```

- Simulates event streams  
- Applies rule-based and ML-based detection  
- Logs alerts to `logs/alert_data.csv` and `logs/alerts.log`

### 2. Run the Dashboard

```bash
streamlit run streamlit_app.py
```

---

## Machine Learning Model

The anomaly detection uses **Isolation Forest**, an unsupervised machine learning algorithm. The model is trained on synthetic, normal data and detects deviations in CPU, memory, and latency metrics in real-time.

---

## Future Enhancements

- Integration with Kafka or Redis for distributed ingestion  
- Docker-based containerization and deployment  
- Integration with Slack or email for real-time alerts  
- Hosting via Streamlit Cloud or similar  
- Use of deep learning for more advanced anomaly detection  
- Replay mode for historical data investigation

---



