import time
from fastapi import APIRouter, Depends, Body
from app.schemas.rec import RecRequest, RecResponse
from app.api.deps import get_rec_service
from app.services.batch_engine import RecBatchService

router = APIRouter()

@router.post("/predict", response_model=RecResponse)
async def predict(
    request: RecRequest = Body(...),
    service: RecBatchService = Depends(get_rec_service)
):
    t0 = time.time()
    items = await service.get_recommendations(request.context, request.k)
    return RecResponse(items=items, latency_ms=(time.time() - t0) * 1000)
