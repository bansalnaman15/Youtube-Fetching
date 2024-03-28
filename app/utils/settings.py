from pydantic.v1 import BaseSettings
from decouple import config


class Settings(BaseSettings):
    PROJECT_NAME: str = "YOUTUBE-FETCHER"
    APP_ENV: str = "DEV"
    SCHEDULER_JOB_ID: str = "FETCH_DATA"
    POSTGRES_USER: str = config('POSTGRES_USER')
    POSTGRES_PASSWORD: str = config('POSTGRES_PASSWORD')
    POSTGRES_DB: str = config('POSTGRES_DB')
    PAGE_SIZE: int = 5
    YOUTUBE_API_KEYS: str = config('YOUTUBE_API_KEYS')


settings = Settings()
