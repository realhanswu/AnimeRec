# Scalable Recommendation Engine (FastAPI + Redis + Docker)

A high-performance, asynchronous recommendation backend designed to handle **10k+ requests per second**. This project implements a **Retrieval-Ranking** architecture using **FastAPI** for orchestration, **Redis** for feature caching, and a **Wide & Deep** model architecture for scoring.

## 🚀 Key Features

*   **Scalable Architecture:** Async/Sync hybrid design with specialized Batch Processing logic to handle high-throughput inference.
*   **Production Ready:** Dockerized setup with `gunicorn` + `uvicorn` workers.
*   **Low Latency:** Uses Redis Pipeline for sub-millisecond feature fetching.
*   **Clean Design:** Follows "Clean Architecture" principles (Service Layer, Dependency Injection, Pydantic Schemas).
*   **Wide & Deep Support:** Logic in place to handle sparse (categorical) and deep (dense) features.

## 🛠 Tech Stack

*   **Framework:** FastAPI
*   **Cache / Feature Store:** Redis (Alpine)
*   **Vector DB:** Qdrant (Integrated & Ready)
*   **Containerization:** Docker & Docker Compose
*   **ML Runtime:** ONNX Runtime (Mocked for demo)

## 📂 Project Structure

```text
recommendation_engine/
├── app/
│   ├── api/          # Route handlers & Dependency Injection
│   ├── core/         # Config & Lifespan (Startup) logic
│   ├── ml/           # Model wrappers & ONNX interaction
│   ├── services/     # Business logic (Batching, Retrieval)
│   └── schemas/      # Pydantic data models
├── artifacts/        # Model files (dummy_model)
├── Dockerfile        # Multi-stage build
└── docker-compose.yml
