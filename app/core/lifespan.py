import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from redis.asyncio import Redis
from app.core.config import settings
from app.ml.model_loader import WideAndDeepRanker
from app.services.batch_engine import RecBatchService

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n" + "="*50)
    print("🚀 [LIFESPAN] STARTUP SEQUENCE INITIATED")
    print("="*50 + "\n")

    try:
        # STEP 1: CHECK CONFIG
        print(f"🔍 [LIFESPAN] Config Check: REDIS_URL={settings.REDIS_URL}")

        # STEP 2: CONNECT REDIS
        print("🔌 [LIFESPAN] Connecting to Redis...")
        redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True, socket_timeout=5)

        # Force a ping to ensure it's actually alive
        await redis_client.ping()
        print("✅ [LIFESPAN] Redis Connected Successfully!")

        # STEP 3: LOAD MODEL
        print("🧠 [LIFESPAN] Loading Model...")
        ranker = WideAndDeepRanker(settings.MODEL_PATH)
        ranker.load()
        print("✅ [LIFESPAN] Model Loaded!")

        # STEP 4: START ENGINE
        print("⚙️ [LIFESPAN] Starting Batch Engine...")
        service = RecBatchService(ranker, redis_client)
        print("✅ [LIFESPAN] Batch Engine Created!")

        # STEP 5: ATTACH TO STATE (The Critical Step)
        print("📌 [LIFESPAN] Attaching to App State...")
        app.state.ml_models["rec_service"] = service
        app.state.ml_models["redis"] = redis_client

        # Verify it attached
        if "rec_service" in app.state.ml_models:
             print("✅ [LIFESPAN] Service attached to state successfully!")
        else:
             print("❌ [LIFESPAN] FAILED TO ATTACH TO STATE!")

        print("\n" + "="*50)
        print("🚀 [LIFESPAN] READY FOR TRAFFIC")
        print("="*50 + "\n")

        yield  # <--- App runs here

    except Exception as e:
        print("\n" + "!"*50)
        print(f"🔥 [LIFESPAN] CRITICAL STARTUP ERROR: {type(e).__name__}: {e}")
        print("!"*50 + "\n")
        # Don't silence it. Let it crash so we see the log.
        raise e

    finally:
        # Cleanup (runs on shutdown)
        print("🛑 [LIFESPAN] SHUTTING DOWN...")
