import json
import uuid
import requests

API_URL = "http://127.0.0.1:8000/events/ingest"

EVENT_FILE = "data\sample_events\sample_eventsbe42122.jsonl"

events_to_send = []

with open(EVENT_FILE, "r", encoding="utf-8") as f:

    for line in f:

        raw = json.loads(line)

        timestamp = (
            raw.get("event_timestamp")
            or raw.get("event_time")
            or raw.get("queue_join_ts")
        )

        store_id = (
            raw.get("store_id")
            or raw.get("store_code")
            or "STORE_UNKNOWN"
        )

        visitor_id = (
            raw.get("id_token")
            or str(raw.get("track_id"))
            or "UNKNOWN"
        )

        transformed = {
            "event_id": str(uuid.uuid4()),
            "store_id": store_id,
            "camera_id": raw.get("camera_id", "UNKNOWN"),
            "visitor_id": visitor_id,
            "event_type": raw.get("event_type", "UNKNOWN").upper(),
            "timestamp": timestamp,
            "is_staff": raw.get("is_staff", False),
            "confidence": 0.90
        }

        events_to_send.append(transformed)

response = requests.post(
    API_URL,
    json=events_to_send
)

print(response.status_code)
print(response.json())