from pydantic import BaseModel, Field

class SummarizeRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=50,
        max_length=10000
    )