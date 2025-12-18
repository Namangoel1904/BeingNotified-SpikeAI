# app/utils/seo_planner.py

def is_seo_query(query: str) -> bool:
    seo_keywords = [
        "title",
        "meta",
        "h1",
        "seo",
        "index",
        "noindex",
        "canonical",
        "redirect",
        "https",
        "status",
        "crawl",
    ]
    q = query.lower()
    return any(k in q for k in seo_keywords)


def map_query_to_seo_rule(query: str) -> str | None:
    q = query.lower()

    if "title" in q and ("60" in q or "long" in q):
        return "long_title"

    if "https" in q:
        return "non_https"

    if "noindex" in q or ("index" in q and "no" in q):
        return "noindex"

    if "redirect" in q:
        return "redirects"

    return None
