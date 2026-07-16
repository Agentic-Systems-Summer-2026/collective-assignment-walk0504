Create day2-minibuild/agent.py that solves the SAME task agent-style:

- Same course client, plain import: from common.llm import chat, STATS
- Define exactly three plain Python tool functions:
  read_notes() -> returns the text of notes.txt next to the script
  count_items(text) -> returns how many action items appear in the given text
  save_output(text) -> writes text to agent_output.txt next to the script and returns "saved"
- System prompt: give the model the GOAL, describe the three tools, and require replies using either:
  ACTION: tool_name(arguments)
  or
  DONE: <final answer>
- Make the reply parsing forgiving: tolerate case differences, extra whitespace, conversational wording, and markdown code fences.
- The loop sends the conversation, parses the reply, runs the selected tool on ACTION, and stops on DONE or after a maximum of 8 turns.
- If neither keyword appears, append a protocol reminder and count it as a turn.
- At the end, print the final answer, turns used, and STATS.
