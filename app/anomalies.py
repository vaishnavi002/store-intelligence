from app.database import SessionLocal
from app.models import EventModel
from datetime import datetime, timedelta


def get_store_anomalies(store_id: str):

    db = SessionLocal()

    events = (
        db.query(EventModel)
        .filter(
            EventModel.store_id == store_id,
            EventModel.is_staff == False
        )
        .all()
    )

    db.close()

    anomalies = []

    if len(events) == 0:
        anomalies.append({
            "type": "DEAD_STORE",
            "severity": "WARN",
            "suggested_action": "Check camera feed and event pipeline"
        })

    billing_events = [
        e for e in events
        if "BILLING" in e.event_type.upper()
    ]

    if len(billing_events) > 10:
        anomalies.append({
            "type": "QUEUE_SPIKE",
            "severity": "CRITICAL",
            "suggested_action": "Open additional billing counter"
        })

    entry_events = [
        e for e in events
        if e.event_type.upper() == "ENTRY"
    ]

    if len(entry_events) > 0 and len(billing_events) == 0:
        anomalies.append({
            "type": "CONVERSION_DROP",
            "severity": "WARN",
            "suggested_action": "Investigate customer drop-off"
        })

    return {
        "store_id": store_id,
        "anomalies": anomalies
    }