# Store Intelligence System – Design Overview

## 1. System Objective

The goal of this system is to simulate a real-time retail intelligence platform that processes in-store customer activity and converts raw event streams into meaningful business insights. The system supports ingestion of multi-camera events, zone-based movement tracking, billing queue analysis, and POS-based purchase mapping. It exposes APIs that allow retrieval of metrics, funnel analytics, heatmaps, and anomaly detection results.

## 2. High-Level Architecture

The system follows a modular backend pipeline:

Event Sources → FastAPI Ingestion Layer → SQLite Database → Analytics Layer → REST APIs

### Components

- FastAPI Application: Handles ingestion and analytics APIs
- SQLite Database (via SQLAlchemy): Stores normalized event data
- Pipeline Layer: Transforms raw JSONL events into structured schema
- Analytics Layer: Computes metrics, funnels, heatmaps, anomalies

## 3. Data Flow

1. Raw events are ingested via `/events/ingest`
2. Events are normalized into a unified schema
3. Stored in SQLite database
4. Analytics endpoints query stored data
5. POS CSV is used for purchase inference

## 4. Metrics System

- Unique Visitors: Distinct non-staff visitor IDs
- Total Events: Count of all valid events
- Conversion Rate: Purchases / Unique Visitors * 100
- Abandonment Rate: Billing drop-offs / Billing entries * 100

## 5. Funnel Logic

Customer journey stages:
Entry → Zone Visit → Billing Queue → Purchase

This helps identify drop-off points in the store journey.

## 6. Heatmap Logic

Heatmaps are generated using:
- Zone entry frequency
- Time spent in zone
- Revenue zone weighting

This highlights high engagement areas.

## 7. Anomaly Detection

Rule-based anomaly detection is implemented:
- Conversion drop detection
- Billing queue spike detection
- Stale feed detection

Each anomaly returns severity and recommended action.

## 8. Design Trade-offs

- SQLite used for simplicity
- Rule-based analytics instead of ML
- Replay-based pipeline instead of real streaming
- No external dependencies like Kafka or Spark

## 9. Scalability

System can be extended to:
- PostgreSQL for scale
- Kafka for streaming ingestion
- Redis for caching metrics
- Spark/Flink for real-time processing

## 10. Summary

This system is a lightweight retail intelligence pipeline that simulates real-world analytics using modular and extensible design principles.