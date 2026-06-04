from app.database import SessionLocal
from app.models import EventModel
from app.pos import get_purchase_count


def get_store_metrics(store_id: str):

    db = SessionLocal()

    events = db.query(EventModel).filter(
        EventModel.store_id == store_id
    ).all()

    db.close()

    visitors = set()
    billing_visitors = set()
    abandoned_visitors = set()

    total_events = 0

    for e in events:

        if e.is_staff:
            continue

        total_events += 1

        if e.visitor_id:
            visitors.add(e.visitor_id)

        if e.event_type in [
            "QUEUE_COMPLETED",
            "BILLING_QUEUE_JOIN"
        ]:
            billing_visitors.add(e.visitor_id)

        if e.event_type in [
            "QUEUE_ABANDONED",
            "BILLING_QUEUE_ABANDON"
        ]:
            abandoned_visitors.add(e.visitor_id)

    unique_visitors = len(visitors)

    purchases = get_purchase_count()

    conversion_rate = 0

    if unique_visitors > 0:
        conversion_rate = round(
            (purchases / unique_visitors) * 100,
            2
        )

    abandonment_rate = 0

    if len(billing_visitors) > 0:
        abandonment_rate = round(
            (len(abandoned_visitors) / len(billing_visitors)) * 100,
            2
        )

    return {
        "store_id": store_id,
        "unique_visitors": unique_visitors,
        "conversion_rate": conversion_rate,
        "abandonment_rate": abandonment_rate,
        "total_events": total_events,
        "purchases": purchases
    }