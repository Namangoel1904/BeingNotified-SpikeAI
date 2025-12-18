# app/utils/seo_planner.py

def map_query_to_seo_rule(query: str) -> str | None:
    """
    Deterministic mapping from natural language query to SEO rule key.
    """

    q = query.lower()

    # Long title tags
    if "title" in q and ("60" in q or "long" in q):
        return "long_title"

    # Non-HTTPS URLs
    if "https" in q:
        return "non_https"

    # Noindex pages
    if "noindex" in q or ("index" in q and "no" in q):
        return "noindex"

    # Redirect issues
    if "redirect" in q:
        return "redirects"

    return None
