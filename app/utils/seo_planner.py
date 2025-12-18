# app/utils/seo_planner.py

def map_query_to_seo_rule(query: str) -> str | None:
    """
    Deterministic mapping from natural language query to SEO rule key.
    """

    q = query.lower()

    # Long title tags
    if "title" in q and ("60" in q or "long" in q):
        return "long_title"

    # Missing meta descriptions
    if "meta" in q and ("missing" in q or "empty" in q):
        return "missing_meta"

    # Non-indexable pages
    if "non indexable" in q or "non-indexable" in q:
        return "non_indexable"

    # Noindex pages (explicit)
    if "noindex" in q:
        return "non_indexable"

    return None
