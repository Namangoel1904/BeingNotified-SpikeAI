import json
from app.schemas.intent import IntentPlan
from app.llm.client import LiteLLMClient

from app.agents.ga4_agent import GA4Agent
from app.utils.ga4_planner import plan_ga4_query, extract_page_path
from app.utils.ga4_postprocess import summarize_ga4_result, is_time_series

from app.agents.seo_agent import SEOAgent
from app.utils.seo_planner import map_query_to_seo_rule

# -------------------------
# Agents (SAFE)
# -------------------------
ga4_agent = GA4Agent()

SEO_DATA_SOURCE = (
    "https://docs.google.com/spreadsheets/d/"
    "1zzf4ax_H2WiTBVrJigGjF2Q3Yz-qy2qMCbAMKvl6VEE/edit#gid=1438203274"
)
seo_agent = SEOAgent(data_source=SEO_DATA_SOURCE)

# -------------------------
# Intent Detection
# -------------------------
def detect_intent(query: str) -> IntentPlan:
    seo_keywords = [
        "title", "meta", "index", "seo", "canonical",
        "redirect", "crawl", "https"
    ]

    lowered = query.lower()
    if any(k in lowered for k in seo_keywords):
        return IntentPlan(
            intent="seo",
            requires_property_id=False,
            tasks=[{"agent": "seo", "goal": query}],
        )

    try:
        llm = LiteLLMClient()
        raw = llm.chat([
            {"role": "system", "content": "Detect intent: analytics or seo."},
            {"role": "user", "content": query},
        ])
        return IntentPlan(**json.loads(raw))

    except Exception:
        return IntentPlan(
            intent="analytics",
            requires_property_id=True,
            tasks=[{"agent": "analytics", "goal": query}],
        )

# -------------------------
# Main Orchestrator
# -------------------------
def orchestrate(query: str, property_id: str | None):
    intent_plan = detect_intent(query)

    # -------------------------
    # GA4 (Tier 1)
    # -------------------------
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
            return {"answer": str(e), "data": None}

        except Exception as e:
            return {"answer": "Failed to fetch GA4 data.", "data": {"error": str(e)}}

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

    # -------------------------
    # SEO (Tier 2)
    # -------------------------
    if intent_plan.intent == "seo":
        rule_key = map_query_to_seo_rule(query)

        if not rule_key:
            return {
                "answer": "Unsupported SEO analysis request.",
                "data": None,
            }

        return seo_agent.run(rule_key)

    # -------------------------
    # Fallback
    # -------------------------
    return {
        "answer": f"Intent detected: {intent_plan.intent}",
        "data": intent_plan.dict(),
    }
