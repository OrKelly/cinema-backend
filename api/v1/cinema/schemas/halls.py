from pydantic import BaseModel, Field


class CreateHallSchema(BaseModel):
    title: str
    description: str


class CreateHallCompleteSchema(BaseModel):
    id: int
    title: str
