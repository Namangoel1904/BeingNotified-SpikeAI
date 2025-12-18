# Assumptions & Design Decisions

This document outlines the assumptions and technical decisions made
while building the system.

The system is designed to be evaluated **entirely through automation**
in a headless Linux environment.

---

## General Assumptions

- The evaluator will deploy the system in a Linux environment.
- The evaluator will interact with the system only through the `/query` API.
- The system prioritizes **graceful failure** over crashes or hallucinated output.
- Absence of data is treated as a valid runtime state.

---

## GA4 Analytics Agent

- GA4 credentials are expected to be provided at runtime via `credentials.json`.
- The system starts successfully even if GA4 credentials are missing.
- If credentials are not present:
  - Analytics queries return a clear explanatory message.
  - The service does not crash or fabricate metrics.
- GA4 queries are planned deterministically using validated metrics and dimensions.
- Default date range is **last 7 days** if none is specified.
- Page-level queries use `pagePath` filtering.
- Time-series vs aggregate responses are inferred deterministically.

---

## SEO Agent & Data Handling

- SEO analysis is based on Screaming Frog–style crawl data.
- The system **attempts** to ingest SEO data from the Google Sheets URL
  provided in the problem statement.
- Google Sheets URLs are internally converted to export formats suitable
  for programmatic access.
- Due to known restrictions on unauthenticated Google Sheets exports:
  - Live data ingestion may fail in automated environments.
- When live ingestion fails:
  - The system falls back to a local snapshot (`seo_fallback.csv`).
  - No SEO insights are hallucinated.
  - The system continues to operate deterministically.

---

## LLM Usage

- LLMs are used only for:
  - Intent detection
  - GA4 query planning
  - High-level summarization
- LLMs are **never** used for direct data execution.
- All LLM outputs are constrained by deterministic logic.

---

## Scope & Intent

- The system demonstrates:
  - Multi-agent orchestration
  - Safe LLM integration
  - Production-grade backend design
- It is not intended to be a full marketing automation platform.

---

## Guiding Principle

> “LLMs reason. Code enforces. Systems fail gracefully.”
