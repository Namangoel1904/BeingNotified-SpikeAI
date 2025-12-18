SEO_RULES = {
    "long_title": {
        "description": "Title tags longer than recommended length",
        "column": "title 1 length",
        "operator": ">",
        "threshold": 60,
    },
    "missing_meta": {
        "description": "Pages missing meta descriptions",
        "column": "meta description 1",
        "operator": "isnull",
    },
    "non_indexable": {
        "description": "Non-indexable pages",
        "column": "indexability",
        "operator": "!=",
        "threshold": "Indexable",
    },
}
