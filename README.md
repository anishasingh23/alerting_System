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

## Sample Real Time Synthetic Data Generation Demo


![ScreenRecording2025-07-12205454-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/f49e8cee-8d78-4eab-8378-33126c841c7b)


---

## Streamlit Dashboard Screenshot


<img width="1898" height="735" alt="Screenshot 2025-07-12 205705" src="https://github.com/user-attachments/assets/360dbc6c-fd22-4d2d-ad47-d562ab8dd646" />

<img width="1896" height="539" alt="Screenshot 2025-07-12 205715" src="https://github.com/user-attachments/assets/d8c88ed5-487f-4125-9a34-45223b18d65a" />


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



