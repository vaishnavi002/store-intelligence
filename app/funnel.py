from app.database import SessionLocal
from app.models import EventModel


def get_store_funnel(store_id: str):

    db = SessionLocal()

    events = db.query(EventModel).filter(
        EventModel.store_id == store_id
    ).all()

    db.close()

    entry_visitors = set()
    zone_visitors = set()
    billing_visitors = set()
    purchasers = set()

    for e in events:

        if e.is_staff:
            continue

        if e.event_type == "ENTRY":
            entry_visitors.add(e.visitor_id)

        if "ZONE" in e.event_type:
            zone_visitors.add(e.visitor_id)

        if e.event_type in [
            "QUEUE_COMPLETED",
            "QUEUE_ABANDONED"
        ]:
            billing_visitors.add(e.visitor_id)

        if e.event_type == "QUEUE_COMPLETED":
            purchasers.add(e.visitor_id)

    entry_count = len(entry_visitors)

    purchase_count = len(purchasers)

    dropoff_percent = 0

    if entry_count > 0:
        dropoff_percent = round(
            ((entry_count - purchase_count) / entry_count) * 100,
            2
        )

    return {
        "entry": entry_count,
        "zone_visit": len(zone_visitors),
        "billing": len(billing_visitors),
        "purchase": purchase_count,
        "dropoff_percent": dropoff_percent
    }