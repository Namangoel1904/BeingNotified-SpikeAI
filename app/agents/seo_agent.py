from typing import Dict, Any, Optional
import pandas as pd

from app.utils.seo_rules import SEO_RULES
from app.utils.seo_loader import load_seo_data


class SEOAgent:
    """
    SEO Agent for Tier-2 evaluation.

    - Supports Google Sheets or CSV as data source
    - Does NOT assume data availability
    - Fails gracefully without hallucination
    """

    def __init__(self, data_source: Optional[str] = None):
        """
        data_source:
        - Google Sheets CSV URL (preferred)
        - Local CSV path (dev fallback)
        - None (graceful no-data mode)
        """
        self.data_source = data_source
        self.df = load_seo_data(data_source)

    def run(self, rule_key: str) -> Dict[str, Any]:
        """
        Execute an SEO rule against loaded data.
        """

        # 🔒 No data available
        if self.df.empty:
            return {
                "answer": "SEO data source not available. Unable to analyze SEO issues.",
                "data": None,
            }

        if rule_key not in SEO_RULES:
            return {
                "answer": "Unsupported SEO analysis request.",
                "data": None,
            }

        rule = SEO_RULES[rule_key]

        try:
            column = rule["column"]
            operator = rule["operator"]
            threshold = rule.get("threshold")

            df = self.df

            # Normalize column presence
            if column not in df.columns:
                return {
                    "answer": f"Required SEO column '{column}' not found in data.",
                    "data": None,
                }

            # Apply rule
            if operator == ">":
                result = df[df[column] > threshold]

            elif operator == "!=":
                result = df[df[column] != threshold]

            elif operator == "isnull":
                result = df[df[column].isna()]

            else:
                result = df

            urls = (
                result.get("address")
                if "address" in result.columns
                else result.iloc[:, 0]
            )

            return {
                "answer": rule["description"],
                "data": urls.head(50).tolist(),
            }

        except Exception as e:
            return {
                "answer": "Failed to process SEO analysis.",
                "data": {"error": str(e)},
            }
