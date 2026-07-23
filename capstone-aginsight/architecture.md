# AgInsight: A Trustworthy AI Farm Monitoring Agent

## Capstone Design Review and Progress Checkpoint

**Student:** Jolie Walker  
**Course:** Agentic Systems  
**Project:** AgInsight  
**Date:** July 23, 2026  

---

## 1. Project Overview

AgInsight is an agentic AI system designed to help farmers monitor important weather conditions and commodity prices. The system reviews incoming farm-related data, creates an alert, checks the alert against the original data, and only approves the alert if the information is supported.

The purpose of AgInsight is not only to provide useful information, but also to reduce the risk of sending farmers inaccurate or misleading alerts. Agricultural decisions can affect crop health, livestock safety, operating costs, and income. Because of this, an alert should not be treated as trustworthy only because it was written by an AI model.

The current working version of AgInsight uses sample weather and commodity data to demonstrate one complete end-to-end workflow. It reads the source data, generates an alert, checks each statement, removes an unsupported statement, checks the corrected alert again, and saves a record of the process.

---

## 2. Problem Statement

Farmers make decisions using information from several different sources, including weather forecasts, commodity markets, government announcements, and farm records. Monitoring all of these sources can take time, especially when conditions change quickly.

An AI monitoring agent could help by reviewing information and creating timely alerts. However, AI systems can also generate statements that are not supported by the source data. In agriculture, an inaccurate alert could cause a farmer to delay work unnecessarily, misunderstand market conditions, or make a decision based on false information.

AgInsight addresses this problem by adding a grounding check before an alert is approved. Each statement in the alert is compared with the original weather or commodity data. Unsupported statements are flagged instead of being shown as normal, trusted information.

---

## 3. Project Goals

The main goals of the current AgInsight design are:

1. Monitor weather and commodity information relevant to a farm.
2. Generate a clear alert based on the available data.
3. Check every alert statement against the original source data.
4. Rewrite the alert one time when unsupported information is found.
5. Hold or discard an alert if it still fails after the rewrite.
6. Record the source data, checks, decisions, and final result.
7. Keep important decisions visible to the farmer.
8. Support future review of past alerts and system performance.

---

# 4. System Architecture

The current AgInsight prototype is organized into six major components.

### Data Collection

The current prototype uses sample weather and commodity data to demonstrate the complete workflow. This allows the alert generation, grounding check, and observability features to be tested without requiring live API connections. Future versions of AgInsight will replace the sample data with live weather and commodity market APIs.

### Alert Generation

The agent reviews the available data and creates a natural language alert for the farmer. The alert summarizes important conditions such as extreme heat, high wind, or commodity prices.

### Grounding Check

Before the alert is approved, every statement is checked against the original source data. Statements that cannot be supported by the available data are marked as failed. This reduces the chance that incorrect AI-generated information reaches the farmer.

### Unsupported Statement Removal

If unsupported information is found, the system removes unsupported statements from the alert. The updated alert is then checked one additional time before a final approval decision is made. Limiting the process to a single additional check prevents endless correction loops while ensuring that only supported information is included in the final alert.

### Observability

Every execution is recorded in a log file. The log includes the original source data, generated alert, grounding results, rewritten alert, and final approval status. This provides a complete history of system behavior for debugging and future evaluation.

### Human Oversight

The farmer remains responsible for making final decisions. AgInsight is designed to support decision making rather than replace human judgment.

---

# 5. Agent Workflow

The workflow implemented in the current prototype is shown below.

```
Weather Data
        │
Commodity Prices
        │
        ▼
Generate Alert
        │
        ▼
Grounding Check
        │
 ┌──────┴──────┐
 │             │
PASS         FAIL
 │             │
 │        Rewrite Once
 │             │
 └──────┬──────┘
        ▼
Second Grounding Check
        │
        ▼
Approve or Hold Alert
        │
        ▼
Save Log
```
---

# 6. Design Trade-Offs

Several design decisions were made during the development of AgInsight to improve reliability while keeping the system simple enough for a working prototype.

### Single Rewrite Limit

AgInsight only attempts one rewrite if unsupported information is detected. Allowing unlimited rewrites could cause the system to enter an endless correction loop. A single rewrite keeps the workflow predictable while still giving the agent an opportunity to correct mistakes.

### Grounding Before Delivery

The grounding check occurs before an alert is delivered to the farmer. This design choice prioritizes accuracy over speed. While this adds one additional processing step, it greatly reduces the chance of unsupported AI-generated statements reaching the user.

### Human-in-the-Loop

AgInsight is designed to support farmers rather than replace them. The system provides recommendations, but the farmer remains responsible for making operational decisions. Future self-improvement suggestions will also require farmer approval before being adopted.

### Comprehensive Logging

Every alert, including successful alerts, rewritten alerts, and failed alerts, is recorded. Keeping a complete history makes it easier to evaluate system performance, identify recurring problems, and improve future versions of the agent.

### Limited Initial Scope

The current prototype focuses only on weather conditions and commodity prices. Limiting the scope allowed the core workflow to be implemented and tested before adding additional data sources such as USDA reports, grants, equipment maintenance, or local farm records.
---

# 7. Risk and Observability Plan

Several risks were identified during the design of AgInsight.

| Risk | Mitigation |
|------|------------|
| Unsupported AI statements | Grounding check validates every alert before delivery. |
| Infinite correction loop | The system only performs one rewrite attempt. |
| False alerts | Unsupported alerts are held instead of being approved. |
| Missing audit trail | Every execution is written to a log file. |
| Future model drift | Historical logs can be reviewed to identify recurring problems. |

Observability is supported through detailed logging. Each execution records:

- Source weather data
- Source commodity data
- Initial alert
- Grounding check results
- Rewritten alert
- Final approval status
- Timestamp

These records provide evidence for evaluation and future system improvements.
---

# 8. Alignment with Instructor Feedback

During the proposal review, feedback was provided recommending that AgInsight perform a grounding check before presenting alerts to the farmer. This recommendation became one of the primary design goals for the project.

The current prototype demonstrates this behavior by validating every generated statement against the available weather and commodity data. If unsupported information is identified, the system performs one rewrite and checks the revised alert again before making a final decision.

The instructor also recommended keeping detailed records of each alert so the system can later review its own performance. The prototype records the source data, generated alert, grounding results, rewritten alert, and final status in an observability log. These records provide the foundation for the future self-review capability planned for the final version of AgInsight.

The future self-review component will analyze historical alerts, identify recurring mistakes or false alarms, and recommend improvements. Any suggested changes will remain human-approved before they become part of the system. This keeps the farmer in control while allowing the agent to improve over time.
---

# 9. Current Prototype Status

The current prototype demonstrates one complete end-to-end workflow.

The prototype currently supports:

- Weather monitoring
- Commodity price monitoring
- Natural language alert generation
- Statement-by-statement grounding validation
- One automatic rewrite attempt
- Final approval or rejection of alerts
- Observability logging
- Multiple evaluation scenarios

The following capabilities are planned for future versions:
These capabilities are not included in the current prototype but represent planned enhancements for future development.
- Live weather APIs
- Live commodity market APIs
- USDA announcements
- Grant opportunities
- Equipment maintenance reminders
- Historical trend analysis
- Farmer feedback collection
- Self-review and improvement recommendations
---

# 10. Conclusion

AgInsight demonstrates how an agentic AI system can improve trust in automated agricultural decision support by validating its own output before presenting information to the user.

The current prototype successfully implements an end-to-end workflow that includes data collection, alert generation, grounding validation, limited rewriting, approval decisions, and observability logging. Evaluation results showed that the system responded correctly to different weather conditions and prevented unsupported statements from appearing in approved alerts.

Future work will expand AgInsight by connecting live data sources, increasing the number of monitored agricultural resources, and implementing a human-approved self-review process that allows the system to recommend improvements based on historical performance.

Overall, this project establishes a reliable foundation for a trustworthy agricultural monitoring agent while maintaining transparency, accountability, and human oversight.
