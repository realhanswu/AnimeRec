from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <--- IMPORT THIS
from app.api.v1 import recommendations
from app.core.config import settings
from app.core.lifespan import lifespan

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# --- ADD THIS SECTION ---
# Set this to the specific domains of your frontend in production
# e.g., origins = ["https://my-frontend.com", "http://localhost:3000"]
origins = ["*"]  # "*" allows ALL external sources (good for dev, be careful in prod)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Allows all headers (Auth tokens, etc.)
)
# ------------------------

# Initialize state
app.state.ml_models = {}

app.include_router(
    recommendations.router,
    prefix=f"{settings.API_V1_STR}/recommendations",
    tags=["recommendations"]
)

if __name__ == "__main__":
    import uvicorn
    # Host "0.0.0.0" is already correct for external access
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
