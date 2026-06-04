
# System Design Document – Store Intelligence API

## 1. Overview

The Store Intelligence system is designed to process multi-source retail events including camera-based tracking data, queue events, zone-level interactions, and POS transactions. The system transforms raw event streams into actionable retail insights such as conversion rates, customer engagement patterns, and operational anomalies.

The primary goal is to provide real-time, scalable, and interpretable analytics for retail optimization.

---

## 2. Architecture

The system follows a modular pipeline architecture:

### 2.1 Data Ingestion Layer
- FastAPI endpoint receives event batches
- Deduplication via event_id
- Stores structured data into SQLite database

### 2.2 Metrics Engine
- Computes:
  - Unique visitors
  - Total events
  - Conversion rate (POS validated)
  - Abandonment rate (queue-based)

### 2.3 Funnel Engine
Tracks customer journey stages:
- Entry → Zone Visit → Billing → Purchase

### 2.4 POS Integration Layer
- Reads transactional CSV data
- Maps purchases to visitor IDs
- Ensures real conversion validation

### 2.5 Anomaly Detection Engine
- Rule-based system that detects:
  - Conversion drops
  - Queue spikes
  - Billing abandonment
  - Funnel breakdowns
- Outputs anomaly severity score (0–100)

### 2.6 ML Scoring Layer
- Lightweight predictive model
- Uses features:
  - Entry count
  - Zone engagement
  - Billing interactions
- Outputs ML conversion score

---

## 3. AI-Assisted Decision Making (MANDATORY SECTION)

AI techniques in this system are applied in a hybrid manner:

### 3.1 Rule-Based Intelligence
Instead of relying on a heavy ML model, interpretable rules are used for:
- anomaly detection
- funnel validation
- threshold-based alerts

This ensures transparency and explainability.

### 3.2 Feature-Based ML Layer
A lightweight predictive model estimates conversion probability using:
- entry frequency
- zone engagement intensity
- billing activity

This acts as a behavioral scoring system rather than a black-box model.

### 3.3 Why Hybrid Approach?
- Retail systems require explainability
- Business users need actionable insights
- Pure ML models are difficult to interpret in real-time systems

Thus, combining rule-based logic with ML scoring ensures both accuracy and usability.

---

## 4. Design Decisions

- SQLite chosen for simplicity and portability
- FastAPI for async-ready performance
- Event-driven architecture for extensibility
- Modular design for easy scaling (Kafka-ready)

---

## 5. Scalability Considerations

- Stateless API design enables horizontal scaling
- Event ingestion can be replaced with streaming systems (Kafka/Kinesis)
- Database can migrate to PostgreSQL for production workloads

---

## 6. Limitations

- Current ML model is lightweight (non-deep learning)
- No real-time streaming pipeline yet
- POS integration is batch-based

---

## 7. Future Improvements

- Real-time Kafka ingestion
- Deep learning-based footfall prediction
- Computer vision integration for live tracking
- Retail recommendation engine

---