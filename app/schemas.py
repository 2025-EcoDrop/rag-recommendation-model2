from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    query: str
    user_id: int | None = None

class QueryResponse(BaseModel):
    answer: List[List[str]]