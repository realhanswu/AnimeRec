***

# Scalable Recommendation Engine (FastAPI + Redis + Docker)

A high-performance, asynchronous recommendation backend designed to handle **10k+ requests per second**. This project implements a **Retrieval-Ranking** architecture using **FastAPI** for orchestration, **Redis** for feature caching, and a **Wide \& Deep** model architecture for scoring.

## 🚀 Key Features

* **Scalable Architecture:** Async/Sync hybrid design with specialized Batch Processing logic to handle high-throughput inference.
* **Production Ready:** Dockerized setup with `gunicorn` + `uvicorn` workers.
* **Low Latency:** Uses Redis Pipeline for sub-millisecond feature fetching.
* **Clean Design:** Follows "Clean Architecture" principles (Service Layer, Dependency Injection, Pydantic Schemas).
* **Wide \& Deep Support:** Logic in place to handle sparse (categorical) and deep (dense) features.


## 🛠 Tech Stack

* **Framework:** FastAPI
* **Cache / Feature Store:** Redis (Alpine)
* **Vector DB:** Qdrant (Integrated \& Ready)
* **Containerization:** Docker \& Docker Compose
* **ML Runtime:** ONNX Runtime (Mocked for demo)


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
```


## 🏁 Getting Started

### Prerequisites

* **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)


### 1. Installation \& Run

No local Python installation is required if using Docker.

```bash
# 1. Clone the repository
git clone https://github.com/realhanswu/recommendation-engine.git
cd recommendation-engine

# 2. Build and Start Services
docker-compose up --build
```

Wait until you see the log:
`🚀 [LIFESPAN] READY FOR TRAFFIC`

### 2. Testing the API

The API will be available at `http://localhost:8000`.

#### Option A: Interactive Documentation (Swagger UI)

Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

#### Option B: cURL / Terminal

```bash
curl -X POST "http://localhost:8000/api/v1/recommendations/predict" \
     -H "Content-Type: application/json" \
     -d '{
           "context": {
             "user_id": "user_123", 
             "device": "mobile"
           }, 
           "k": 5
         }'
```


#### Option C: Python Client

```python
import requests

payload = {
    "context": {"user_id": "u1", "device": "mobile"},
    "k": 3
}
res = requests.post("http://localhost:8000/api/v1/recommendations/predict", json=payload)
print(res.json())
```


## ⚙️ Configuration

Environment variables are managed in `app/core/config.py` and `docker-compose.yml`.


| Variable | Default | Description |
| :-- | :-- | :-- |
| `REDIS_URL` | `redis://redis_db:6379/0` | Connection string for Feature Store |
| `MODEL_PATH` | `/code/artifacts/dummy_model` | Path to ONNX model artifact |
| `BATCH_SIZE` | `64` | Max requests processed in one inference pass |
| `BATCH_TIMEOUT` | `0.01` | Max wait time (seconds) to fill a batch |

## 🧪 Development Notes

* **Hot Reloading:** The `app` directory is mounted as a volume. Changes to the code will auto-reload the server without restarting Docker.
* **Mocking:** The project currently runs with a **Mock Ranker** (`app/ml/model_loader.py`) to allow running without a physical `.onnx` file. To use a real model, uncomment the ONNX Runtime code in that file.


## 📄 License

[MIT](LICENSE)

