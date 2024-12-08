from pydantic import BaseModel, Field


class CurrentUser(BaseModel):
    id: int = Field(None, description="User ID")

    class Config:
        validate_assignment = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
