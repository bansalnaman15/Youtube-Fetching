from pydantic import BaseModel, Field, field_validator
from cron_validator import CronValidator


class StartCronRequest(BaseModel):
    cron_interval: str = Field(..., title="Cron Interval", description="Interval for the cron job")
    search_key: str = Field(..., title="Search Key", description="Search key for fetching data")

    @field_validator('cron_interval')
    def validate_cron_interval(cls, value):
        try:
            description = CronValidator.parse(value)
        except Exception as e:
            raise ValueError("Invalid cron interval format") from e
        return value

    @field_validator('search_key')
    def validate_search_key(cls, value):
        if not value.strip():
            raise ValueError("Search key cannot be empty or contain only whitespace")
        return value
