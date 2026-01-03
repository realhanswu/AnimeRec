from fastapi import FastAPI
from app.api.v1 import recommendations
from app.core.config import settings
from app.core.lifespan import lifespan

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# FORCE INITIALIZATION: Ensure the attribute exists immediately
app.state.ml_models = {}

app.include_router(
    recommendations.router,
    prefix=f"{settings.API_V1_STR}/recommendations",
    tags=["recommendations"]
)
