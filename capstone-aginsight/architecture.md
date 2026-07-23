# AgInsight: A Trustworthy AI Farm Monitoring Agent

## Capstone Design Review and Progress Checkpoint

**Student:** Jolie Walker  
**Course:** Agentic Systems  
**Project:** AgInsight  
**Date:** July 23, 2026

---

# 1. Project Overview

AgInsight is an agentic AI system designed to help farmers monitor important weather conditions and commodity market information. The system collects data, generates alerts, validates every alert against the original source data, and only approves alerts that are supported by the available information.

The purpose of AgInsight is to improve trust in AI-generated alerts. Farmers often make important decisions based on weather and market conditions, so inaccurate information could lead to unnecessary costs or poor operational decisions. Instead of assuming AI-generated information is correct, AgInsight verifies every statement before it is presented to the user.

The current prototype demonstrates one complete monitoring cycle using live weather data, commodity market integration, grounding validation, automatic fallback behavior, and observability logging.

---

# 2. Problem Statement

Farmers rely on information from several different sources every day, including weather forecasts, commodity markets, government announcements, and farm records. Monitoring these sources manually can take time, especially when conditions change quickly.

AI systems can summarize this information, but they may also generate statements that are not supported by the available data. In agriculture, an inaccurate alert could cause a farmer to delay work unnecessarily, misunderstand market conditions, or make decisions based on incorrect information.

AgInsight addresses this problem by validating every alert before it is approved. Every generated statement is compared to the original source data, and unsupported information is removed before the alert reaches the farmer.

---

# 3. Project Goals

The current goals of AgInsight are:

1. Retrieve live weather information.
2. Retrieve commodity market information.
3. Generate alerts dynamically based on current conditions.
4. Validate every generated statement using grounding.
5. Remove unsupported statements when necessary.
6. Allow only one correction attempt.
7. Approve or hold alerts based on validation results.
8. Record every monitoring cycle in an observability log.
9. Provide a strong foundation for future agricultural automation.

---

# 4. System Architecture

The current AgInsight prototype is organized into six major components.

## Data Collection

The prototype retrieves live weather information for Weatherford, Oklahoma, using the Open-Meteo API. It also attempts to retrieve commodity market information from the Alpha Vantage API.

Because external services may become unavailable or temporarily rate-limit requests, AgInsight includes automatic fallback behavior. When an API cannot be reached, clearly labeled fallback values are used so the monitoring cycle can continue instead of failing.

## Alert Generation

Using the collected weather and commodity information, the system generates natural language alerts. Alerts are created dynamically based on the current conditions instead of using hardcoded messages.

## Grounding Validation

Every generated alert is checked against the original source data before approval. Each statement is individually validated to verify that it is supported by the available information.

## One Correction Attempt

If unsupported information is found, the system removes unsupported statements and performs one additional grounding check. Limiting the process to one correction attempt prevents endless correction loops while still improving reliability.

## Observability

Every monitoring cycle is written to an observability log. The log records:

- Source weather data
- Source commodity data
- Initial alert
- Grounding results
- Corrected alert
- Final approval status
- Timestamp

These records support debugging, evaluation, and future system improvements.

## Human Oversight

AgInsight supports farmer decision making but does not replace it. The farmer remains responsible for all operational decisions made on the farm.

---

# 5. Agent Workflow

The current workflow is shown below.

Live Weather API

+

Commodity Market API

↓

Dynamic Alert Generation

↓

Grounding Validation

↓

Unsupported Information Found?

↓

One Correction Attempt

↓

Final Approval or Hold

↓

Observability Log

---

# 6. Design Decisions

Several important design decisions were made while building AgInsight.

## Reliability Over Speed

The system prioritizes accurate information over fast delivery. Spending a little more time validating alerts helps reduce the chance of incorrect information reaching the farmer.

## Ground Before Delivery

Every alert must pass grounding validation before approval. This reduces hallucinations and increases trust in AI-generated information.

## One Correction Limit

Only one correction attempt is allowed. This prevents the workflow from entering endless rewrite loops while still allowing unsupported information to be removed.

## Graceful API Fallback

External APIs may occasionally fail or become rate-limited. Instead of stopping the workflow, AgInsight automatically switches to fallback data so monitoring can continue.

## Complete Observability

Every monitoring cycle is recorded. Keeping detailed logs makes it easier to evaluate system performance and identify future improvements.

---

# 7. Risk and Observability Plan

Several risks were considered during development.

| Risk | Mitigation |
|------|------------|
| Unsupported AI statements | Ground every alert before approval. |
| Endless correction loops | Limit corrections to one attempt. |
| External API failure | Use clearly labeled fallback data. |
| Missing audit trail | Record every monitoring cycle. |
| Future model drift | Review historical logs to identify recurring issues. |

The observability log records:

- Weather source data
- Commodity source data
- Generated alerts
- Grounding results
- Final approval decision
- Timestamp

These records provide evidence for evaluation and future improvements.

---

# 8. Alignment with Instructor Feedback

One of the primary recommendations received during the proposal review was to perform grounding validation before presenting alerts to the farmer. That recommendation became one of the central design goals for AgInsight.

The current prototype validates every generated statement against the original weather and commodity information. Unsupported statements are removed before approval, making the final alert more trustworthy.

Another recommendation was to maintain detailed records of system behavior. Every monitoring cycle is saved in an observability log so future versions of AgInsight can analyze previous alerts, identify recurring mistakes, and support future self-review capabilities.

---

# 9. Current Prototype Status

The current prototype successfully demonstrates one complete end-to-end monitoring cycle.

Current capabilities include:

- Live weather retrieval using the Open-Meteo API
- Commodity API integration
- Automatic fallback when APIs fail or become rate-limited
- Dynamic alert generation
- Grounding validation
- One correction attempt
- Final approval decisions
- Observability logging

Future development will include:

- Local elevator cash bids
- USDA market reports
- Equipment maintenance reminders
- SMS and mobile notifications
- Multi-farm monitoring
- Historical trend analysis
- Farmer feedback integration
- Human-approved self-review recommendations

---

# 10. Conclusion

AgInsight demonstrates how an agentic AI system can improve trust in automated agricultural decision support by validating its own output before presenting information to the user.

The current prototype successfully retrieves live weather information, integrates external commodity market data, generates alerts dynamically, validates every alert using grounding, handles API failures through automatic fallback behavior, and records every monitoring cycle for future evaluation.

Although the project is still under development, the current implementation provides a strong foundation for future autonomous agricultural monitoring. Future versions will expand the number of monitored data sources while maintaining transparency, reliability, and human oversight.