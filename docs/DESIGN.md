# Store Intelligence Architecture

## Overview

Raw CCTV Clips
→ Detection Layer
→ Event Stream
→ FastAPI Ingestion
→ SQLite
→ Metrics API

## Detection Layer

Sample events are replayed through replay_events.py.

Future production design:
YOLOv8 + ByteTrack.

## Event Stream

JSON events.

## Intelligence API

FastAPI.

## Database

SQLite.

## Anomaly Detection

Conversion drop.
Queue spike.
Dead zone.

## AI-Assisted Decisions

Used ChatGPT for:

- Event schema design
- FastAPI structure
- Funnel calculation

Accepted:
...

Rejected:
...