from alert_engine import AlertEngine

if __name__ == "__main__":
    engine = AlertEngine(num_workers=4, run_duration=25)
    engine.start()
