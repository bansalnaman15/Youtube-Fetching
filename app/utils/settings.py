from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "YOUTUBE-FETCHER"
    APP_ENV: str = "DEV"
    SCHEDULER_JOB_ID: str = "FETCH_DATA"


settings = Settings()
