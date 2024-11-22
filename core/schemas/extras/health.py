from pydantic import BaseModel, Field


class HealthSchema(BaseModel):
    status: str = Field(..., example="OK")
