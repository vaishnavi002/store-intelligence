# Design Choices and Engineering Decisions

## 1. Framework Choice – FastAPI

FastAPI was chosen for:
- High performance
- Easy API development
- Built-in validation with Pydantic
- Excellent testing support

It allowed fast implementation within tight deadlines.

## 2. Database Choice – SQLite

SQLite was selected because:
- Zero configuration required
- Lightweight and portable
- Suitable for evaluation environments
- Easy integration with SQLAlchemy

## 3. ORM – SQLAlchemy

SQLAlchemy provides:
- Clean schema definition
- Easy migration to PostgreSQL
- Structured query handling

## 4. Event Processing Strategy

A replay-based pipeline was used instead of real-time streaming:
- Faster development
- Deterministic testing
- Simulated production-like ingestion

## 5. Metrics Approach

Metrics are computed using:
- Set-based visitor tracking
- Event-type classification
- POS CSV integration for purchases

## 6. Conversion Logic

Conversion rate is calculated as:
Purchases / Unique Visitors * 100

Ensures:
- No division by zero
- Proper percentage scaling

## 7. Anomaly Detection

Rule-based system used due to simplicity:
- Conversion drop detection
- Queue spike detection
- Missing/stale data detection

## 8. Heatmap Strategy

Heatmaps are built using:
- Zone visit frequency
- Dwell time approximation
- Revenue zone weighting

## 9. File Structure

- app/ → core API logic
- pipeline/ → ingestion scripts
- docs/ → documentation
- tests/ → API tests
- data/ → dataset storage

## 10. Docker

Docker setup is included for reproducibility:
- Dockerfile for API containerization
- docker-compose for orchestration

## 11. Trade-offs

- No ML models due to time constraints
- No distributed systems
- No caching layer
- Simplified schema for speed

## 12. Summary

The system prioritizes correctness, clarity, and modularity while simulating a real-world retail intelligence pipeline within limited time constraints.