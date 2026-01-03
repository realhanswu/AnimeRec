from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "RecSys Engine"
    API_V1_STR: str = "/api/v1"

    REDIS_URL: str = "redis://redis_db:6379/0"
    MODEL_PATH: str = "./artifacts/dummy_model"

    CANDIDATE_COUNT: int = 100
    BATCH_SIZE: int = 64
    BATCH_TIMEOUT: float = 0.01

    class Config:
        env_file = ".env"

settings = Settings()
