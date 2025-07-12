def apply_rules(event):
    """Checks if an event violates any hardcoded alert rules."""
    alerts = []

    if event["cpu"] > 90:
        alerts.append(f"High CPU usage: {event['cpu']}%")

    if event["memory"] > 85:
        alerts.append(f"High Memory usage: {event['memory']}%")

    if event["disk_io"] > 90:
        alerts.append(f"High Disk I/O: {event['disk_io']}%")

    return alerts
