from fastapi import FastAPI
from typing import List

from app.schemas import Event
from app.database import engine, SessionLocal
from app.models import Base, EventModel
from app.metrics import get_store_metrics
from app.funnel import get_store_funnel
from app.heatmap import get_store_heatmap
from app.anomalies import get_store_anomalies

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Store Intelligence API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "Store Intelligence API Running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/events/ingest")
def ingest_events(events: List[Event]):

    db = SessionLocal()

    inserted = 0

    for event in events:

        existing = db.get(EventModel, event.event_id)

        if existing:
            continue

        row = EventModel(
            event_id=event.event_id,
            store_id=event.store_id,
            camera_id=event.camera_id,
            visitor_id=event.visitor_id,
            event_type=event.event_type,
            timestamp=event.timestamp,
            is_staff=event.is_staff,
            confidence=event.confidence
        )

        db.add(row)
        inserted += 1

    db.commit()
    db.close()

    return {
        "status": "success",
        "inserted": inserted
    }

@app.get("/stores/{store_id}/metrics")
def store_metrics(store_id: str):
    return get_store_metrics(store_id)

@app.get("/stores/{store_id}/funnel")
def store_funnel(store_id: str):
    return get_store_funnel(store_id)

@app.get("/stores/{store_id}/heatmap")
def store_heatmap(store_id: str):
    return get_store_heatmap(store_id)

@app.get("/stores/{store_id}/anomalies")
def store_anomalies(store_id: str):
    return get_store_anomalies(store_id)

@app.get("/debug/events")
def debug_events():

    db = SessionLocal()

    events = db.query(EventModel).all()

    result = []

    for e in events:
        result.append({
            "event_type": e.event_type,
            "visitor_id": e.visitor_id,
            "store_id": e.store_id
        })

    db.close()

    return result