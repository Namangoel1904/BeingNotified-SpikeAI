from app.llm.client import LiteLLMClient
from app.schemas.ga4_plan import GA4QueryPlan

def plan_ga4_query(query: str) -> GA4QueryPlan:
    """
    Deterministic GA4 query planner.
    Uses LLM if available, otherwise safe fallback.
    """

    try:
        llm = LiteLLMClient()
        raw = llm.chat([
            {"role": "system", "content": "You are a GA4 query planner."},
            {"role": "user", "content": query},
        ])

        return GA4QueryPlan.model_validate_json(raw)

    except Exception:
        # SAFE deterministic fallback
        return GA4QueryPlan(
            metrics=["activeUsers"],
            dimensions=[],
            start_date="7daysAgo",
            end_date="today",
        )
