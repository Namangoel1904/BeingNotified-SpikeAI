from pydantic import BaseModel
from typing import List, Literal, Optional

class AgentTask(BaseModel):
    agent: Literal["analytics", "seo"]
    goal: str

class IntentPlan(BaseModel):
    intent: Literal["analytics", "seo", "multi"]
    requires_property_id: bool
    tasks: List[AgentTask]
