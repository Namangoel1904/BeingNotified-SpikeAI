from app.llm.client import LiteLLMClient
from app.llm.prompts import GA4_SUMMARY_PROMPT

llm = LiteLLMClient()


def summarize_ga4_result(query: str, result: dict) -> str:
    rows = result.get("rows", [])

    if not rows:
        return explain_empty_result(query)

    messages = [
        {"role": "system", "content": GA4_SUMMARY_PROMPT},
        {"role": "user", "content": f"Query: {query}\nData: {rows[:10]}"},
    ]

    try:
        return llm.chat(messages)
    except Exception:
        return "GA4 data retrieved successfully."


def is_time_series(dimensions: list[str]) -> bool:
    return "date" in dimensions

def explain_empty_result(query: str) -> str:
    return (
        "No GA4 data was found for this query. "
        "This can happen if there was no traffic during the selected date range "
        "or if the specified page did not receive any visits."
    )
