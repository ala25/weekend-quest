from pydantic import BaseModel, Field


class Brief(BaseModel):
    title: str
    steps: list[str] = Field(min_length=3, max_length=3)
    deadline: str | None