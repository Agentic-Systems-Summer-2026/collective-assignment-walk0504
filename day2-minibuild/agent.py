"""
Agent-style pipeline (day2-minibuild/agent.py)

Uses a simple text protocol to drive an LLM agent through:
  1. read_notes()   – read notes.txt next to this script
  2. count_items()  – count action-item lines in a given text
  3. save_output()  – write the final answer to agent_output.txt

The model replies each turn with either:
  ACTION: tool_name(arguments)
  DONE: <final answer>
"""

import pathlib
import re

from common.llm import chat, STATS

# ---------------------------------------------------------------------------
# Paths (all resolved relative to THIS script file)
# ---------------------------------------------------------------------------
HERE = pathlib.Path(__file__).resolve().parent
NOTES_PATH = HERE / "notes.txt"
OUTPUT_PATH = HERE / "agent_output.txt"

# ---------------------------------------------------------------------------
# Tool functions
# ---------------------------------------------------------------------------

def read_notes() -> str:
    """Return the text of notes.txt (next to this script)."""
    return NOTES_PATH.read_text()


def count_items(text: str) -> int:
    """Count action items: lines that start with a digit, '-', or '*'."""
    count = 0
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and (stripped[0].isdigit() or stripped[0] in ("-", "*", "•")):
            count += 1
    return count


def save_output(text: str) -> str:
    """Write text to agent_output.txt next to this script; return 'saved'."""
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    return "saved"


# ---------------------------------------------------------------------------
# Tool dispatcher
# ---------------------------------------------------------------------------
TOOLS = {
    "read_notes": read_notes,
    "count_items": count_items,
    "save_output": save_output,
}

def dispatch(tool_name: str, args_str: str):
    """Call a tool by name, parsing simple string/no-arg signatures."""
    fn = TOOLS.get(tool_name)
    if fn is None:
        return f"ERROR: unknown tool '{tool_name}'"

    # Strip outer quotes or whitespace from args_str
    args_str = args_str.strip()

    if tool_name == "read_notes":
        return fn()
    elif tool_name == "count_items":
        # Argument is the text to count — strip surrounding quotes if present
        text_arg = args_str.strip("\"'")
        return fn(text_arg)
    elif tool_name == "save_output":
        text_arg = args_str.strip("\"'")
        return fn(text_arg)
    else:
        return f"ERROR: unhandled tool '{tool_name}'"


# ---------------------------------------------------------------------------
# Reply parser — forgiving version
# ---------------------------------------------------------------------------
# Matches ACTION: or DONE: anywhere in the reply (case-insensitive),
# tolerating preamble, extra whitespace, and markdown code fences.

ACTION_RE = re.compile(
    r"action\s*:\s*(\w+)\s*\(([^)]*)\)",
    re.IGNORECASE | re.DOTALL,
)
DONE_RE = re.compile(
    r"done\s*:\s*(.*)",
    re.IGNORECASE | re.DOTALL,
)

def parse_reply(reply: str):
    """
    Returns ('action', tool_name, args_str) or ('done', final_text) or (None, None).
    Strips markdown fences before searching.
    """
    # Remove markdown code fences
    cleaned = re.sub(r"```[^\n]*\n?", "", reply).strip()

    # Search for DONE first (it terminates the loop)
    done_m = DONE_RE.search(cleaned)
    if done_m:
        return ("done", done_m.group(1).strip())

    # Search for ACTION
    action_m = ACTION_RE.search(cleaned)
    if action_m:
        return ("action", action_m.group(1).strip(), action_m.group(2).strip())

    return (None,)


# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """\
You are a project-management assistant. Your GOAL is to:
  1. Produce a numbered list of every action item from the meeting notes, \
with format: Task: <desc> | Owner: <name or MISSING> | Deadline: <date or MISSING>
  2. List all items that have MISSING owner or MISSING deadline (flag them).
  3. Write a concise 3-sentence status summary for a project manager.
  4. Save the full final answer (action items + flagged gaps + summary) to disk.

You have exactly three tools available. Each turn reply with EXACTLY ONE of:

  ACTION: tool_name(arguments)
  DONE: <your complete final answer>

Tool descriptions:
  read_notes()          — reads and returns the meeting notes text
  count_items(text)     — counts the number of action-item lines in the given text; \
pass the action-item list as the argument
  save_output(text)     — writes text to agent_output.txt and returns "saved"; \
call this with your full final answer before replying DONE

Rules:
- Only ONE directive per reply; no extra text before it except brief reasoning if needed.
- Use ACTION to call tools, DONE when the work is finished.
- You MUST call save_output before replying DONE.
- Do not embed newlines inside an ACTION call's argument; keep arguments concise.
"""

REMINDER = (
    "\n[SYSTEM] Your last reply did not contain a valid ACTION: or DONE: directive. "
    "Please reply with exactly one of:\n"
    "  ACTION: tool_name(arguments)\n"
    "  DONE: <final answer>\n"
)

# ---------------------------------------------------------------------------
# Agent loop
# ---------------------------------------------------------------------------
MAX_TURNS = 8

def run_agent():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.append({"role": "user", "content": "Please begin."})

    final_answer = None
    turns_used = 0

    for turn in range(1, MAX_TURNS + 1):
        turns_used = turn
        reply = chat(messages, max_tokens=1200)
        messages.append({"role": "assistant", "content": reply})

        parsed = parse_reply(reply)

        if parsed[0] == "done":
            final_answer = parsed[1]
            break

        elif parsed[0] == "action":
            _, tool_name, args_str = parsed
            result = dispatch(tool_name, args_str)
            tool_msg = f"Tool result for {tool_name}:\n{result}"
            messages.append({"role": "user", "content": tool_msg})

        else:
            # Neither keyword found — remind the model
            messages.append({"role": "user", "content": REMINDER})

    if final_answer is None:
        final_answer = "(Agent did not produce a DONE reply within the turn limit.)"

    return final_answer, turns_used


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    final_answer, turns_used = run_agent()

    print("=" * 60)
    print("FINAL ANSWER")
    print("=" * 60)
    print(final_answer)
    print()
    print(f"Turns used: {turns_used} / {MAX_TURNS}")
    print()
    print("=" * 60)
    print("STATS")
    print("=" * 60)
    print(STATS)
