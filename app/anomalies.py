from app.database import SessionLocal
from app.models import EventModel


def get_store_anomalies(store_id: str):
    db = SessionLocal()

    try:
        events = (
            db.query(EventModel)
            .filter(
                EventModel.store_id == store_id,
                EventModel.is_staff == False
            )
            .all()
        )
    finally:
        db.close()

    anomalies = []
    anomaly_score = 0

    if len(events) == 0:
        return {
            "store_id": store_id,
            "anomalies": [{
                "type": "DEAD_STORE",
                "severity": "WARN",
                "suggested_action": "Check ingestion pipeline"
            }],
            "anomaly_score": 100
        }

    billing = [e for e in events if "BILLING" in (e.event_type or "").upper()]
    entry = [e for e in events if (e.event_type or "").upper() == "ENTRY"]
    abandon = [e for e in events if "ABANDON" in (e.event_type or "").upper()]
    zone = [e for e in events if "ZONE" in (e.event_type or "").upper()]

    # -------------------------
    # 1. CONVERSION DROP
    # -------------------------
    if len(entry) > 0 and len(billing) == 0:
        anomalies.append({
            "type": "CONVERSION_DROP",
            "severity": "WARN",
            "suggested_action": "Checkout failure suspected"
        })
        anomaly_score += 35

    # -------------------------
    # 2. QUEUE SPIKE
    # -------------------------
    if len(billing) > 10:
        anomalies.append({
            "type": "QUEUE_SPIKE",
            "severity": "CRITICAL",
            "suggested_action": "Add billing counters"
        })
        anomaly_score += 30

    # -------------------------
    # 3. ABANDONMENT
    # -------------------------
    if len(billing) > 0:
        rate = len(abandon) / len(billing) * 100

        if rate > 50:
            anomalies.append({
                "type": "HIGH_ABANDONMENT",
                "severity": "CRITICAL",
                "suggested_action": "Reduce queue wait time"
            })
            anomaly_score += 35

        elif rate > 25:
            anomalies.append({
                "type": "BILLING_FRICTION",
                "severity": "WARN",
                "suggested_action": "Improve checkout flow"
            })
            anomaly_score += 15

    # -------------------------
    # 4. FUNNEL BREAK
    # -------------------------
    if len(zone) > 10 and len(billing) == 0:
        anomalies.append({
            "type": "FUNNEL_BREAK",
            "severity": "CRITICAL",
            "suggested_action": "High engagement, no conversion"
        })
        anomaly_score += 40

    anomaly_score = min(100, anomaly_score)

    return {
        "store_id": store_id,
        "anomalies": anomalies,
        "anomaly_score": anomaly_score
    }