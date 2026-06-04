from app.database import SessionLocal
from app.models import EventModel
from sqlalchemy import func


def get_store_heatmap(store_id: str):

    db = SessionLocal()

    rows = (
        db.query(
            EventModel.event_type,
            func.count().label("count")
        )
        .filter(
            EventModel.store_id == store_id,
            EventModel.is_staff == False
        )
        .group_by(EventModel.event_type)
        .all()
    )

    db.close()

    total = sum(r.count for r in rows)

    result = []

    for r in rows:
        score = 0

        if total > 0:
            score = round((r.count / total) * 100, 2)

        result.append({
            "zone": r.event_type,
            "score": score
        })

    return {
        "store_id": store_id,
        "data_confidence": total >= 20,
        "heatmap": result
    }