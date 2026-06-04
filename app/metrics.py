from app.database import SessionLocal
from app.models import EventModel
from app.pos import get_purchase_visitors


def get_store_metrics(store_id: str):
    db = SessionLocal()

    events = db.query(EventModel).filter(
        EventModel.store_id == store_id
    ).all()

    db.close()

    visitors = set()
    total_events = 0

    billing_visitors = set()
    abandoned_visitors = set()

    for e in events:
        if e.is_staff:
            continue

        total_events += 1

        if e.visitor_id:
            visitors.add(e.visitor_id)

        if e.event_type in ["QUEUE_COMPLETED", "queue_completed"]:
            billing_visitors.add(e.visitor_id)

        if e.event_type in ["QUEUE_ABANDONED", "queue_abandoned"]:
            abandoned_visitors.add(e.visitor_id)

    # ✅ REAL PURCHASE LOGIC
    purchase_visitors = get_purchase_visitors()

    # Only count purchases for THIS store's visitors
    valid_purchases = visitors.intersection(purchase_visitors)

    unique_visitors = len(visitors)

    conversion_rate = (
        (len(valid_purchases) / unique_visitors) * 100
        if unique_visitors > 0
        else 0
    )

    abandonment_rate = (
        (len(abandoned_visitors) / len(billing_visitors)) * 100
        if len(billing_visitors) > 0
        else 0
    )

    return {
        "store_id": store_id,
        "unique_visitors": unique_visitors,
        "conversion_rate": round(conversion_rate, 2),
        "abandonment_rate": round(abandonment_rate, 2),
        "total_events": total_events,
        "purchases": len(valid_purchases)
    }