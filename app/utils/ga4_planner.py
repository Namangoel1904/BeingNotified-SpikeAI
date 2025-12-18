import json
from datetime import date, timedelta
from app.llm.client import LiteLLMClient
from app.llm.prompts import GA4_PLANNER_PROMPT
from app.schemas.ga4_plan import GA4QueryPlan

llm = LiteLLMClient()


def default_last_7_days():
    end = date.today()
    start = end - timedelta(days=7)
    return start.isoformat(), end.isoformat()


def plan_ga4_query(query: str) -> GA4QueryPlan:
    messages = [
        {"role": "system", "content": GA4_PLANNER_PROMPT},
        {"role": "user", "content": query},
    ]

    try:
        raw = llm.chat(messages)
        parsed = json.loads(raw)
        return GA4QueryPlan(**parsed)

    except Exception:
        # Safe fallback: minimal valid GA4 query
        start, end = default_last_7_days()
        return GA4QueryPlan(
            metrics=["users"],
            dimensions=["date"],
            start_date=start,
            end_date=end,
        )

def extract_page_path(query: str) -> str | None:
    q = query.lower()

    if "homepage" in q or "home page" in q:
        return "/"

    for token in q.split():
        if token.startswith("/"):
            return token

    if "pricing" in q:
        return "/pricing"

    return None
