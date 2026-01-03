import asyncio
import time
import uuid
from typing import List
from redis.asyncio import Redis
from app.schemas.rec import UserContext, RecItem
from app.ml.model_loader import WideAndDeepRanker
from app.core.config import settings

class RecBatchService:
    def __init__(self, ranker: WideAndDeepRanker, redis: Redis):
        self.ranker = ranker
        self.redis = redis
        self.queue = asyncio.Queue()
        self._running = True
        self._task = asyncio.create_task(self._worker())

    async def get_recommendations(self, context: UserContext, k: int) -> List[RecItem]:
        future = asyncio.get_running_loop().create_future()
        await self.queue.put({
            "context": context,
            "k": k,
            "future": future
        })
        return await future

    async def _worker(self):
        while self._running:
            batch = []
            try:
                # 1. Fetch first item
                item = await self.queue.get()
                batch.append(item)

                # 2. Fill batch
                deadline = time.time() + settings.BATCH_TIMEOUT
                while len(batch) < settings.BATCH_SIZE:
                    remaining = deadline - time.time()
                    if remaining <= 0: break
                    try:
                        item = await asyncio.wait_for(self.queue.get(), timeout=remaining)
                        batch.append(item)
                    except (asyncio.TimeoutError, asyncio.QueueEmpty):
                        break

                if batch:
                    await self._process_batch(batch)
                    for _ in range(len(batch)):
                        self.queue.task_done()

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Batch Error: {e}")

    async def _process_batch(self, batch: List[dict]):
        # Mocking Candidate Retrieval (e.g. from Qdrant)
        # Assuming 100 candidates per user
        candidates_list = [[f"item_{i}" for i in range(100)] for _ in batch]

        # Flatten features for batch inference (1 user * 100 items)
        flat_features = []
        for _ in range(len(batch) * 100):
            flat_features.append({"feature_1": 0.5}) # Dummy features

        # Run Inference
        scores_flat = await asyncio.to_thread(self.ranker.predict_batch, flat_features)

        # Map results back to requests
        ptr = 0
        for i, req in enumerate(batch):
            candidates = candidates_list[i]
            count = len(candidates)

            user_scores = scores_flat[ptr : ptr + count]
            ptr += count

            # Sort
            ranked = sorted(zip(candidates, user_scores), key=lambda x: x[1], reverse=True)[:req["k"]]

            response = [
                RecItem(item_id=iid, score=s, rank=r+1)
                for r, (iid, s) in enumerate(ranked)
            ]

            if not req["future"].done():
                req["future"].set_result(response)

    async def shutdown(self):
        self._running = False
        self._task.cancel()
