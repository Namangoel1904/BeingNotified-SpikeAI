from pydantic import BaseModel
from typing import Any, Optional

class QueryResponse(BaseModel):
    answer: str
    data: Optional[Any] = None
