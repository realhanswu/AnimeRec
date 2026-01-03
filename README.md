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
app/
│
├── .env                        # Local environment variables (not committed to git)
├── .gitignore                  # Git ignore rules (e.g., __pycache__, .env)
├── Dockerfile                  # Instructions to build the API container
├── docker-compose.yml          # Orchestration for API, Redis, and Qdrant
├── requirements.txt            # Python dependencies (fastapi, redis, etc.)
│
├── app/                        # Main Application Code
│   ├── __init__.py             # Makes 'app' a Python package
│   ├── main.py                 # Application entry point (FastAPI app init)
│   │
│   ├── api/                    # API Layer (Controllers)
│   │   ├── __init__.py
│   │   ├── deps.py             # Dependency Injection (getting the RecService)
│   │   └── v1/                 # Version 1 API routes
│   │       ├── __init__.py
│   │       └── recommendations.py  # Endpoint logic (POST /predict)
│   │
│   ├── core/                   # Core Configuration & Infrastructure
│   │   ├── __init__.py
│   │   ├── config.py           # Pydantic Settings (Environment variables)
│   │   └── lifespan.py         # Startup/Shutdown logic (Redis connection, Model loading)
│   │
│   ├── ml/                     # Machine Learning Specifics
│   │   ├── __init__.py
│   │   └── model_loader.py     # Wrapper for the ONNX/Wide&Deep model
│   │
│   ├── schemas/                # Pydantic Models (Data Transfer Objects)
│   │   ├── __init__.py
│   │   └── rec.py              # Request/Response schemas (UserContext, RecItem)
│   │
│   └── services/               # Business Logic Layer
│       ├── __init__.py
│       └── batch_engine.py     # The "Engine": Batching, Retrieval, and Ranking logic
│
└── artifacts/                  # Static files needed at runtime
    └── dummy_model             # Placeholder file for the ML model
```


## 🏁 Getting Started

### Prerequisites

* **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)


### 1. Installation \& Run

No local Python installation is required if using Docker.

```bash
# 1. Clone the repository
git clone https://github.com/realhanswu/AnimeRec.git
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

