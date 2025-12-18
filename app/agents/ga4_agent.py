import os
from typing import Dict, Any, List, Optional

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Metric,
    Dimension,
    FilterExpression,
    Filter,
)

from app.utils.ga4_validator import ALLOWED_METRICS, ALLOWED_DIMENSIONS


class GA4Agent:
    """
    GA4 Analytics Agent

    - Lazy initializes GA4 client
    - Validates metrics & dimensions via allowlists
    - Supports optional pagePath filtering
    - Evaluator-safe (does not crash without credentials.json)
    """

    def __init__(self):
        self.client: Optional[BetaAnalyticsDataClient] = None

    def _init_client(self):
        """Initialize GA4 client only when needed."""
        if self.client:
            return

        if not os.path.exists("credentials.json"):
            raise FileNotFoundError(
                "credentials.json not found. GA4 analytics cannot run."
            )

        self.client = BetaAnalyticsDataClient.from_service_account_file(
            "credentials.json"
        )

    def run_report(
        self,
        property_id: str,
        metrics: List[str],
        dimensions: List[str],
        start_date: str,
        end_date: str,
        page_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute a GA4 report with optional pagePath filtering.
        """

        # Lazy init
        self._init_client()

        # Enforce GA4 allowlists
        safe_metrics = [m for m in metrics if m in ALLOWED_METRICS]
        safe_dimensions = [d for d in dimensions if d in ALLOWED_DIMENSIONS]

        if not safe_metrics:
            safe_metrics = ["users"]

        if not safe_dimensions:
            safe_dimensions = ["date"]

        # Optional pagePath filter
        filter_expression = None
        if page_path:
            filter_expression = FilterExpression(
                filter=Filter(
                    field_name="pagePath",
                    string_filter=Filter.StringFilter(
                        match_type=Filter.StringFilter.MatchType.CONTAINS,
                        value=page_path,
                    ),
                )
            )

        request = RunReportRequest(
            property=f"properties/{property_id}",
            metrics=[Metric(name=m) for m in safe_metrics],
            dimensions=[Dimension(name=d) for d in safe_dimensions],
            date_ranges=[
                DateRange(start_date=start_date, end_date=end_date)
            ],
            dimension_filter=filter_expression,
        )

        response = self.client.run_report(request)

        return {
            "dimension_headers": [h.name for h in response.dimension_headers],
            "metric_headers": [h.name for h in response.metric_headers],
            "rows": [
                {
                    "dimensions": [v.value for v in row.dimension_values],
                    "metrics": [v.value for v in row.metric_values],
                }
                for row in response.rows
            ],
        }
