# Incident Report

## What happened

To test my observability features, I purposely changed the summary prompt to an empty string. When I ran the program, the OU LiteLLM Sandbox returned a 400 Bad Request error because there wasn't a valid user prompt.

## How the trace helped

The trace made it easy to see where the problem happened. The plan and answers steps both finished successfully. The summary step failed and logged the error along with the prompt size, response size, latency, and the RuntimeError message. That told me the problem was with the summary prompt and not something earlier in the program.

## How I fixed it

I changed the summary prompt back to the correct version and kept the try/except block around the summary step. Now if that step fails again, the error is written to the trace instead of crashing without any information. After fixing it, I ran the program again and confirmed everything worked correctly.

## Cost Reconciliation

The program tracked token usage using common.llm.STATS. I also checked the OpenClaw gateway logs. The gateway was running correctly, but the logs in this environment did not include request-level token or cost information. Because of that, I used the STATS values to track token usage for the run.
