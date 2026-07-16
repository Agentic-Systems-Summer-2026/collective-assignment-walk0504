"""
Fixed pipeline (not an agent):
  1. Extract action items from notes.txt
  2. Flag items with MISSING owner or deadline
  3. Write a 3-sentence status summary
"""
import sys
import pathlib

# sys.path trick so 'from common.llm import ...' resolves from the repo root
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from common.llm import chat, STATS

# ---------------------------------------------------------------------------
# Read notes
# ---------------------------------------------------------------------------
notes_path = pathlib.Path(__file__).resolve().parent / "notes.txt"
notes = notes_path.read_text()

# ---------------------------------------------------------------------------
# Call 1 – Extract action items
# ---------------------------------------------------------------------------
action_items_raw = chat([
    {
        "role": "system",
        "content": (
            "You are a precise assistant that extracts action items from meeting notes. "
            "Ignore ideas that were explicitly parked or deferred."
        ),
    },
    {
        "role": "user",
        "content": (
            f"Extract every action item from the meeting notes below.\n"
            f"Output a numbered list. For each item use this exact format:\n"
            f"  Task: <description> | Owner: <name or MISSING> | Deadline: <deadline or MISSING>\n\n"
            f"NOTES:\n{notes}"
        ),
    },
])

# ---------------------------------------------------------------------------
# Call 2 – Flag items with MISSING owner or deadline
# ---------------------------------------------------------------------------
flagged_raw = chat([
    {
        "role": "user",
        "content": (
            f"Below is a list of action items. "
            f"Output ONLY the items that have 'MISSING' as the owner OR the deadline "
            f"(or both). Keep the same format. If none qualify, say 'None'.\n\n"
            f"ACTION ITEMS:\n{action_items_raw}"
        ),
    },
])

# ---------------------------------------------------------------------------
# Call 3 – 3-sentence status summary
# ---------------------------------------------------------------------------
summary_raw = chat([
    {
        "role": "user",
        "content": (
            f"Using the action items and the flagged incomplete items below, "
            f"write a 3-sentence status summary suitable for a project manager. "
            f"Be concise and factual.\n\n"
            f"ACTION ITEMS:\n{action_items_raw}\n\n"
            f"FLAGGED (MISSING owner or deadline):\n{flagged_raw}"
        ),
    },
])

# ---------------------------------------------------------------------------
# Print results
# ---------------------------------------------------------------------------
print("=" * 60)
print("ACTION ITEMS")
print("=" * 60)
print(action_items_raw)

print()
print("=" * 60)
print("FLAGGED ITEMS (MISSING owner or deadline)")
print("=" * 60)
print(flagged_raw)

print()
print("=" * 60)
print("STATUS SUMMARY")
print("=" * 60)
print(summary_raw)

print()
print("=" * 60)
print("STATS")
print("=" * 60)
print(STATS)
