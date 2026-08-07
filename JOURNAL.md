# Build Journal

One short entry per build — all five Build Challenges plus the smaller daily
builds. Four to eight sentences each: this is a lab notebook, not an essay.
It is also your AI-use disclosure record for the course. Graded on
completeness and honesty about failures, not polish. (50 pts, due Aug 6.)

Template per entry:

## Day N — <build name>
- **What I built:**
- **What failed:**
- **What I changed:**
- **Where AI helped, and how I verified its output:**

-
## Day 2 – Mini-Build: Workflow vs. Agent
- **What I built:** Built two versions of the same meeting-notes processor. One was a fixed workflow with three model calls, and the other was an agent that decided which tools to use.
- **What failed:** I struggled getting the programs to run because I was in the wrong directory. Once I switched to the correct folder, both versions ran correctly.
- **What I changed:** I created the workflow and agent prompt files, verified both programs, and ran each version three times to compare performance.
- **Where AI helped, and how I verified its output:** AI helped generate both programs, but I verified the output by checking every run against the assignment answer key. Both versions consistently scored 7/7, and I compared the calls, tokens, and turns across all runs.
## Day 3 – Build Challenge 1

- **What I built:** I added three custom tools to my agent: a word counter, a calculator, and a compact search tool that returns matching lines instead of entire notes.

- **What failed:** My first version of the compact search tool still caused the agent to make extra tool calls, so the overall token count was sometimes higher than expected.

- **What I changed:** I updated the tool descriptions and improved the compact search tool so it returned fewer results and gave the model better guidance on when to stop searching.

- **Where AI helped, and how I verified its output:** I used AI to generate and revise the Python code, then verified everything myself by running multiple tests. I confirmed the model selected each of my custom tools automatically and checked the traces and STATS output after every run.
## Build Challenge 2

The original program overloaded the model by sending all 30 policy documents even though only three were needed. This caused context drift and incomplete answers while using nearly 25,000 tokens.

To fix it, I changed the program so it only retrieved the three relevant policies before sending them to the model. I also improved the analyst prompt so it ignored expired policies, verified every requirement was included, and cited every policy used.

The result was a correct answer while reducing token usage from about 24,787 tokens to 574 tokens.

## Build Challenge 3: Reliability and Rollback
For this build, I started with the provided broken agent and identified several reliability problems. The original program did not have a timeout or retry process for network calls, silently ignored errors, trusted model responses without validating the JSON, erased the previous report at the start of every run, and did not save progress. This meant a temporary network issue, an invalid model response, or a Codespace interruption could cause missing work, repeated token usage, or a damaged report.

I created `fixed_agent.py` and added request timeouts, three retries with exponential backoff, JSON validation, code-fence stripping, and a safe fallback that classifies an item as high risk when the model response cannot be trusted. I also added an atomic checkpoint file that saves progress after each request. The completed report is first written to a staged file, and the previous successful report is saved as a backup before the new report replaces it.

I tested the program by intentionally corrupting the model response for CR-103. The agent retried three times, used the safe fallback, and continued processing the remaining requests without damaging the report. I also interrupted the program after three requests and restarted it. The program resumed at request four instead of repeating the first three requests. Finally, I ran the completed program again and verified that it did not reprocess the queue.

## Build Challenge 4 — Evaluation

For this build, I created an evaluation harness for my AgInsight capstone. I connected the starter harness to the part of AgInsight that generates and validates alerts using fixed weather and commodity data. Using fixed data made the tests repeatable and kept the evaluation from depending on live API results.

I created eight test cases that covered normal conditions, heat, extreme heat, high wind, heavy rain, several risks at once, exact alert thresholds, and output formatting. The first evaluation run passed six out of eight cases. After reviewing the results, I found that the two failures were caused by the LLM judge criteria and not by AgInsight. I updated the criteria to match the actual system requirements, and the next run passed all eight cases for a 100% pass rate.

I also connected the harness to GitHub Actions so a small five-case evaluation runs on every push. The first GitHub Actions run failed because the workflow did not install the `requests` package used by AgInsight. I added that dependency, pushed again, and the next run passed. I then deliberately changed the pass threshold to 110% to prove the regression gate could catch a broken build. After confirming the failed run, I restored the threshold to 80% and pushed again so the repository ended in a passing state.

The biggest thing I learned was that an LLM judge still needs human review. A judge can fail a correct answer when the criteria are too vague or do not match the system design. I had to review the outputs myself and adjust the criteria before I could trust the final score.

## Build Challenge 5 — Observability and Oversight

For this build, I added structured JSON trace logging to each step of the agent. The trace records the timestamp, step name, model, prompt size, response size, latency, token usage, and the decision made. This made it much easier to see exactly what happened during each step of the program.

I also added a human approval step before the program writes the final summary to summary.md. The program now shows the summary, token usage, and estimated cost before asking if it should save the file. The user's decision is also added to the trace.

To test everything, I purposely broke the summary prompt by making it an empty string. The request failed, and the trace showed that the plan and answers steps worked while the summary step failed. After that, I fixed the prompt, ran the program again, and confirmed everything worked correctly.

ChatGPT helped me write parts of the trace logging code and troubleshoot problems like indentation and error handling. I tested every change myself by running the program, checking the trace, testing both the approval and rejection paths, creating a real failure, and making sure the final version worked correctly.

## Final Capstone Completion

What I built:
I completed the final version of AgInsight, an agentic AI system that monitors weather and commodity data, generates alerts, validates every important statement using grounding, and records each monitoring cycle through observability logging. I also completed teh project website, final report, presentation, evaluation evidence, and blameless postmortem. 

What failed:
The biggest challenges during the final phase involved making sure every part of the project worked together. I ran into issues with API rate limits, formatting, and making sure my evaluation results accurately reflected the system's behavior. Preparing all of the final deliverables also took much longer than I expected. 

What I changed:
I finalized the grounding workflow, improved fallback behavior for external APIs, completed teh automated evaluation suite, verified all eight evaluation scenarios passed, updated the documentation, and prepared the final presentation and demonstrations. I also reviewed the entire project to make sure the code, report, and presentation were consistent with one anohter. 

Where AI helped:
AI helped me to troubleshoot Python code, improve documentation, practice my presentation, and create the netfliy website. I verified everything by running the program myself, reviewing the alerts against the source data, confirming the results, and making sure the final version of AgInsight behaved as expeected before submission. 