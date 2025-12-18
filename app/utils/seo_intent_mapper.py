def map_seo_query_to_rule(query: str) -> str | None:
    q = query.lower()

    if "title" in q and "length" in q:
        return "long_title"

    if "meta description" in q and ("missing" in q or "empty" in q):
        return "missing_meta"

    if "indexable" in q or "indexability" in q:
        return "non_indexable"

    return None
