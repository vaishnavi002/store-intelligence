# Design Choices and Engineering Decisions-> Technical Choices Document

## 1. Model Selection

### Why lightweight ML instead of deep learning?

We selected a lightweight feature-based scoring model because:

- Real-time inference requirement
- Limited labeled dataset
- Need for interpretability
- Faster execution in API layer

The model uses:
- entry count
- zone activity
- billing interactions

This produces a probabilistic conversion score.

---

## 2. Schema Design

### Event Schema

Each event contains:

- event_id (UUID)
- store_id
- camera_id
- visitor_id
- event_type
- timestamp
- is_staff
- confidence

### Design Rationale

- Unified schema supports all event types:
  - ENTRY
  - ZONE_ENTERED
  - BILLING
  - QUEUE_ABANDONED
- Enables easy filtering and aggregation

---

## 3. API Architecture

### FastAPI was chosen because:

- High performance async framework
- Native Pydantic validation
- Easy testing with TestClient
- Production-ready simplicity

---

## 4. Metrics Design Decisions

### Conversion Rate

We define conversion as:

> POS-based purchase visitors / unique visitors

This avoids inflated conversion metrics from event-only systems.

---

### Abandonment Rate

Calculated as:

> abandoned visitors / billing visitors

This reflects real checkout friction.

---

## 5. Anomaly System Design

We implemented a rule-based anomaly engine:

### Why rule-based?

- Interpretability is critical
- Retail stakeholders need clear reasons
- Faster than training ML classifiers

### Anomalies detected:

- Conversion drop
- Queue spike
- Billing abandonment
- Funnel breakdown

Each anomaly contributes to a cumulative:

> anomaly_score (0–100)

---

## 6. POS Integration Choice

We used CSV-based POS ingestion because:

- Hackathon constraint-friendly
- Easy integration with pandas
- Reliable batch processing

---

## 7. Database Choice

SQLite was selected because:

- Zero setup required
- Fast local development
- Sufficient for evaluation scale

Can be replaced with PostgreSQL in production.

---

## 8. Trade-offs

| Decision | Trade-off |
|----------|----------|
| Rule-based anomalies | Less adaptive than ML |
| SQLite | Not scalable for large traffic |
| Batch POS | Not real-time |

---

## 9. Summary

The system balances:
- interpretability
- performance
- modularity
- extensibility

making it suitable for production extension.