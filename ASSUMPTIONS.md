
---

# ✅ `ASSUMPTIONS.md` (FINAL – VERY IMPORTANT)

```md
# Assumptions & Design Decisions

This document explains the key assumptions and technical decisions
made while building the system.

The system is designed to be evaluated **entirely through automation**.

---

## General Assumptions
- The evaluator will deploy the system in a Linux environment.
- The evaluator will interact with the system only through the `/query` API.
- The system must prioritize **graceful failure** over crashes or hallucinations.

---

## GA4 Analytics Agent

- GA4 credentials are expected to be provided at runtime via `credentials.json`.
- The system must start successfully even if GA4 credentials are missing.
- If credentials are not present:
  - Analytics queries return a clear explanatory message.
  - The service does not crash.
- GA4 metrics and dimensions are validated against allowlists to prevent invalid queries.
- Default date range is **last 7 days** if none is specified.
- Page-level queries are handled using `pagePath` filters.
- Time-series vs aggregate behavior is inferred deterministically.

---

## SEO Agent & Data Handling

- SEO analysis is based on Screaming Frog crawl data provided via Google Sheets.
- The system accepts the **exact Google Sheets URL** shared in the problem statement.
- Google Sheets URLs are automatically converted internally to CSV export URLs.
- The system does not assume:
  - Local files
  - Manual data preprocessing
- If SEO data is inaccessible or incomplete:
  - The system responds gracefully.
  - No SEO data is hallucinated.

---

## LLM Usage

- LLMs are used only for:
  - Intent detection
  - GA4 query planning
  - High-level summarization
- LLMs are **never** used for direct data execution.
- All LLM outputs are validated or constrained by deterministic logic.

---

## Scope & Intent

- The system is intentionally scoped to demonstrate:
  - Multi-agent orchestration
  - Safe LLM integration
  - Production-grade backend design
- It is not intended to be a full marketing automation platform.

---

## Guiding Principle

> “LLMs reason. Code enforces. Systems fail gracefully.”

This principle guided all architectural decisions.
