from app.database import SessionLocal
from app.models import EventModel
from app.pos import get_purchase_visitors
from app.ml_model import predict_conversion
from app.anomalies import get_store_anomalies


def get_store_metrics(store_id: str):
    db = SessionLocal()

    try:
        events = (
            db.query(EventModel)
            .filter(EventModel.store_id == store_id)
            .all()
        )
    finally:
        db.close()

    visitors = set()
    billing_visitors = set()
    abandoned_visitors = set()

    entry_count = 0
    zone_count = 0
    billing_count = 0

    for e in events:
        if e.is_staff:
            continue

        if not e.visitor_id:
            continue

        visitors.add(e.visitor_id)
        entry_count += 1

        etype = (e.event_type or "").upper()

        if "ZONE" in etype:
            zone_count += 1

        if "BILLING" in etype or "QUEUE_COMPLETED" in etype:
            billing_visitors.add(e.visitor_id)
            billing_count += 1

        if "ABANDON" in etype:
            abandoned_visitors.add(e.visitor_id)

    purchase_visitors = set(get_purchase_visitors())
    valid_purchases = visitors.intersection(purchase_visitors)

    unique_visitors = len(visitors)

    conversion_rate = (
        (len(valid_purchases) / unique_visitors) * 100
        if unique_visitors > 0 else 0
    )

    abandonment_rate = (
        (len(abandoned_visitors) / len(billing_visitors)) * 100
        if len(billing_visitors) > 0 else 0
    )

    ml_score = predict_conversion(entry_count, zone_count, billing_count)

    # -------------------------
    # CONNECT ANOMALIES HERE
    # -------------------------
    anomaly_data = get_store_anomalies(store_id)

    return {
        "store_id": store_id,
        "unique_visitors": unique_visitors,
        "conversion_rate": round(conversion_rate, 2),
        "abandonment_rate": round(abandonment_rate, 2),
        "total_events": entry_count,
        "purchases": len(valid_purchases),
        "ml_conversion_score": ml_score,

        # NEW
        "anomaly_score": anomaly_data["anomaly_score"],
        "anomalies": anomaly_data["anomalies"]
    }