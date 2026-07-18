# Prompt Changelog

Prompts are software artifacts. Every prompt lives as a file in `prompts/` —
never inline-only — and **every change gets a line here**: what changed, why,
and the observed effect. BC2's write-up must cite at least two entries.

Format: `YYYY-MM-DD · file · what changed · why · observed effect`

| Date | Prompt file | What changed | Why | Observed effect |
|---|---|---|---|---|
| 2026-07-13 | bc1-agent-system.txt | (seed) initial system prompt from template | starting point | agent answers but tool JSON occasionally wrapped in prose |
| 2026-07-15 | day2-workflow.md | Created Day 2 workflow prompt | Built fixed workflow version | Scored 7/7 consistently across three runs |
| 2026-07-15 | day2-agent.md | Created Day 2 agent prompt | Built agent version | Scored 7/7 consistently across three runs |
| 2026-07-15 | bc1-agent-system.txt | Added three custom tools and updated the search_notes_compact tool description | Help the model choose tools more effectively and make search results more token
| 2026-07-17 | bc2-analyst.txt | Updated the analyst prompt to identify only relevant policies, ignore expired/rescinded policies, and require policy citations. | Reduce context drift and improve accuracy. | Model correctly focused on AS-7, AS-18, and AS-24 while reducing token usage dramatically. |

| 2026-07-17 | bc2-analyst.txt | Added a verification checklist requiring every requirement to be included before answering. | Prevent omission of important policy details. | Final response included the on-call contact, 90-day retention, read-only credentials, and correct policy citations. |