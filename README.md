# Store Intelligence API

Store Intelligence platform built for the Purplle Engineering Hiring Challenge.

The system processes retail store behavioral events and exposes analytics APIs for visitor tracking, conversion analysis, funnel analysis, heatmaps, and anomaly detection.

---

## Architecture

Raw CCTV Footage
        ↓
Detection Pipeline
        ↓
Structured Events
        ↓
Event Ingestion API
        ↓
SQLite Database
        ↓
Analytics Endpoints

---

## Project Structure

store-intelligence/

├── app/

│   ├── main.py

│   ├── database.py

│   ├── models.py

│   ├── schemas.py

│   ├── metrics.py

│   ├── funnel.py

│   ├── heatmap.py

│   ├── anomalies.py

│   └── pos.py

│

├── pipeline/

│   └── replay_events.py

│

├── tests/

│   └── test_api.py

│

├── data/

│   ├── videos/

│   ├── layouts/

│   ├── pos/

│   └── sample_events/

│

├── requirements.txt

├── docker-compose.yml

├── Dockerfile

└── README.md

---

## Installation

Create virtual environment

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the API

```bash
uvicorn app.main:app --reload
```

Open:

http://127.0.0.1:8000/docs

---

## Running Event Replay

Replay sample events into the API.

```bash
python pipeline/replay_events.py
```

Expected output:

```json
{
  "status": "success",
  "inserted": 13
}
```

---

## API Endpoints

### Health

GET

```text
/health
```

Example response:

```json
{
  "status": "healthy"
}
```

---

### Event Ingestion

POST

```text
/events/ingest
```

Accepts batches of events.

Supports idempotent inserts using event_id.

---

### Metrics

GET

```text
/stores/{store_id}/metrics
```

Returns:

- Unique Visitors
- Conversion Rate
- Abandonment Rate
- Total Events

---

## 📦 Metrics Output Example

```json
{
  "store_id": "ST1076",
  "unique_visitors": 3,
  "conversion_rate": 66.67,
  "abandonment_rate": 33.33,
  "total_events": 9,
  "purchases": 2,
  "ml_conversion_score": 0.82,
  "anomaly_score": 45,
  "anomalies": [
    {
      "type": "CONVERSION_DROP",
      "severity": "WARN"
    }
  ]
}

### Funnel

GET

```text
/stores/{store_id}/funnel
```

Returns:

- Entry Count
- Zone Visits
- Billing Visits
- Purchases

---

### Heatmap

GET

```text
/stores/{store_id}/heatmap
```

Returns zone activity scores.

---

### Anomalies

GET

```text
/stores/{store_id}/anomalies
```

Returns operational anomalies.

---

## Running Tests

```bash
pytest -v
```

Expected:

```text
5 passed
```

---

## Technologies

- FastAPI
- SQLAlchemy
- SQLite
- Pandas
- Pytest
- OpenCV
- Ultralytics YOLO

---

## Notes

The challenge dataset contains:

- Entry Camera Footage
- Zone Camera Footage
- Billing Camera Footage
- Store Layouts
- POS Transactions
- Sample Events

The current implementation supports event replay and analytics computation from structured event streams.
