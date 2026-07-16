Create day2-minibuild/workflow.py. It must be a FIXED PIPELINE, not an agent:

- Import the course client with a plain: from common.llm import chat, STATS
- Read notes.txt from the SAME FOLDER as the script.
- Make exactly THREE chat() calls, in this fixed order:
  1. Extract every action item from the notes as a list of task / owner / deadline. Use "MISSING" when an owner or deadline is absent. Ignore ideas that were explicitly parked.
  2. Given that list, output only the items that have a MISSING owner or deadline.
  3. Given the list and the flags, write a 3-sentence status summary.
- The Python code decides every step. The model must never choose what happens next. No loops of any kind, no tools, no retries.
- At the end, print the action-item list, the flagged items, the summary, and STATS.
