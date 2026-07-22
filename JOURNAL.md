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