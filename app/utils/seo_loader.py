import pandas as pd
import re


def _convert_google_sheet_to_csv(url: str) -> str:
    """
    Converts a Google Sheets 'edit' URL to a CSV export URL.
    """
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
    gid_match = re.search(r"gid=([0-9]+)", url)

    if not match:
        raise ValueError("Invalid Google Sheets URL")

    sheet_id = match.group(1)
    gid = gid_match.group(1) if gid_match else "0"

    return (
        f"https://docs.google.com/spreadsheets/d/"
        f"{sheet_id}/export?format=csv&gid={gid}"
    )


def load_seo_data(source: str | None):
    """
    Load SEO data from:
    - Google Sheets (edit URL or CSV export URL)
    - Local CSV
    - None (graceful fallback)
    """

    if not source:
        return pd.DataFrame()

    try:
        # Handle Google Sheets edit URL
        if "docs.google.com/spreadsheets" in source:
            source = _convert_google_sheet_to_csv(source)

        df = pd.read_csv(source, low_memory=False)
        df.columns = [c.strip().lower() for c in df.columns]
        return df

    except Exception:
        # Graceful degradation (no crash)
        return pd.DataFrame()
