from pydantic import BaseModel
from typing import List

class GA4QueryPlan(BaseModel):
    metrics: List[str]
    dimensions: List[str]
    start_date: str
    end_date: str
