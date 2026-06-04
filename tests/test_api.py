# PROMPT:
# Generate FastAPI API tests for ingest, metrics, funnel and health endpoints.
#
# CHANGES MADE:
# Adjusted assertions for challenge schema and local project structure.
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root():

    response = client.get("/")

    assert response.status_code == 200


def test_ingest_event():

    payload = [
        {
            "event_id": "TEST_001",
            "store_id": "TEST_STORE",
            "camera_id": "CAM1",
            "visitor_id": "VIS1",
            "event_type": "ENTRY",
            "timestamp": "2026-03-03T14:22:10Z",
            "is_staff": False,
            "confidence": 0.95
        }
    ]

    response = client.post(
        "/events/ingest",
        json=payload
    )

    assert response.status_code == 200


def test_metrics():

    response = client.get(
        "/stores/ST1076/metrics"
    )

    assert response.status_code == 200


def test_funnel():

    response = client.get(
        "/stores/ST1076/funnel"
    )

    assert response.status_code == 200