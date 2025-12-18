import json

from app.llm.client import LiteLLMClient
from app.llm.prompts import INTENT_DETECTION_PROMPT
from app.schemas.intent import IntentPlan

# GA4 imports
from app.agents.ga4_agent import GA4Agent
from app.utils.ga4_planner import plan_ga4_query, extract_page_path
from app.utils.ga4_postprocess import (
    is_time_series,
    summarize_ga4_result,
)

# SEO imports
from app.agents.seo_agent import SEOAgent
from app.utils.seo_intent_mapper import map_seo_query_to_rule

# -------------------------
# Global singletons
# -------------------------
llm = LiteLLMClient()
ga4_agent = GA4Agent()

# Default SEO data source (from problem statement PDF)
SEO_DATA_SOURCE = (
    "https://docs.google.com/spreadsheets/d/"
    "1zzf4ax_H2WiTBVrJigGjF2Q3Yz-qy2qMCbAMKvl6VEE/edit#gid=1438203274"
)
seo_agent = SEOAgent(data_source=SEO_DATA_SOURCE)


# -------------------------
# Intent Detection
# -------------------------
def detect_intent(query: str) -> IntentPlan:
    """
    Detect whether the query is analytics, seo, or multi-agent.
    Applies deterministic SEO override before LLM usage.
    """

    # Deterministic SEO override (domain guarantees)
    seo_keywords = [
        "title tag", "title tags",
        "meta description",
        "indexability", "indexable",
        "https", "canonical",
        "robots", "sitemap",
        "hreflang", "alt text", "images",
    ]

    lowered = query.lower()
    if any(k in lowered for k in seo_keywords):
        return IntentPlan(
            intent="seo",
            requires_property_id=False,
            tasks=[{"agent": "seo", "goal": query}],
        )

    messages = [
        {"role": "system", "content": INTENT_DETECTION_PROMPT},
        {"role": "user", "content": query},
    ]

    try:
        raw = llm.chat(messages)
        parsed = json.loads(raw)
        return IntentPlan(**parsed)

    except Exception:
        # Safe fallback
        return IntentPlan(
            intent="analytics",
            requires_property_id=True,
            tasks=[{"agent": "analytics", "goal": query}],
        )


# -------------------------
# Main Orchestrator
# -------------------------
def orchestrate(query: str, property_id: str | None):
    """
    Main orchestration function.
    Routes requests to GA4 (Tier-1) or SEO (Tier-2).
    """

    intent_plan = detect_intent(query)

    # ==================================================
    # 🔹 ANALYTICS (GA4 — Tier-1)
    # ==================================================
    if intent_plan.intent == "analytics":

        if not property_id:
            return {
                "answer": "GA4 propertyId is required for analytics queries.",
                "data": None,
            }

        plan = plan_ga4_query(query)
        page_path = extract_page_path(query)

        try:
            result = ga4_agent.run_report(
                property_id=property_id,
                metrics=plan.metrics,
                dimensions=plan.dimensions,
                start_date=plan.start_date,
                end_date=plan.end_date,
                page_path=page_path,
            )

        except FileNotFoundError as e:
            return {
                "answer": str(e),
                "data": None,
            }

        except Exception as e:
            return {
                "answer": "Failed to fetch GA4 data.",
                "data": {"error": str(e)},
            }

        summary = summarize_ga4_result(query, result)

        return {
            "answer": summary,
            "data": {
                "query_plan": plan.dict(),
                "page_path_filter": page_path,
                "time_series": is_time_series(plan.dimensions),
                "result": result,
            },
        }

    # ==================================================
    # 🔹 SEO (Tier-2)
    # ==================================================
    if intent_plan.intent == "seo":
        rule_key = map_seo_query_to_rule(query)

        if not rule_key:
            return {
                "answer": "SEO analysis request not supported.",
                "data": None,
            }

        return seo_agent.run(rule_key)

    # ==================================================
    # 🔹 FALLBACK
    # ==================================================
    return {
        "answer": f"Intent detected: {intent_plan.intent}",
        "data": intent_plan.dict(),
    }
