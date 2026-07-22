#!/usr/bin/env python3
"""Reliable version of the Build Challenge 3 agent."""

import argparse
import json
import os
import pathlib
import shutil
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common.llm import _key, BASE, DEFAULT_MODEL

HERE = pathlib.Path(__file__).resolve().parent
REQUESTS_FILE = HERE / "requests.jsonl"
REPORT = HERE / "approved_report.md"
STAGED_REPORT = HERE / "approved_report.staged.md"
BACKUP_REPORT = HERE / "approved_report.backup.md"
CHECKPOINT = HERE / "checkpoint.json"

VALID_RISKS = {"low", "medium", "high"}
MAX_RETRIES = 3
TIMEOUT_SECONDS = 20


def atomic_write(path, text):
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(text, encoding="utf-8")
    temp_path.replace(path)


def load_requests():
    items = []

    for line_number, line in enumerate(
        REQUESTS_FILE.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if not line.strip():
            continue

        item = json.loads(line)

        if not isinstance(item, dict):
            raise ValueError(f"Line {line_number} is not a JSON object.")

        if not isinstance(item.get("id"), str):
            raise ValueError(f"Line {line_number} has an invalid id.")

        if not isinstance(item.get("request"), str):
            raise ValueError(f"Line {line_number} has an invalid request.")

        items.append(item)

    return items


def strip_code_fences(text):
    cleaned = text.strip()

    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        cleaned = "\n".join(lines).strip()

    return cleaned


def validate_verdict(verdict):
    if not isinstance(verdict, dict):
        raise ValueError("Model response was not a JSON object.")

    risk = verdict.get("risk")
    reason = verdict.get("reason")

    if risk not in VALID_RISKS:
        raise ValueError("Risk must be low, medium, or high.")

    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("Reason is missing or invalid.")

    return {
        "risk": risk,
        "reason": reason.strip().replace("\n", " "),
    }


def parse_model_response(text):
    cleaned = strip_code_fences(text)
    verdict = json.loads(cleaned)
    return validate_verdict(verdict)


def classify(text, item_id):
    body = json.dumps(
        {
            "model": DEFAULT_MODEL,
            "temperature": 0,
            "max_tokens": 200,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Classify this change request. Reply ONLY with JSON "
                        '{"risk": "low|medium|high", '
                        '"reason": "<one line>"}\n\n'
                        + text
                    ),
                }
            ],
        }
    )

    request = urllib.request.Request(
        BASE + "/v1/chat/completions",
        data=body.encode("utf-8"),
        headers={
            "Authorization": "Bearer " + _key(),
            "Content-Type": "application/json",
        },
    )

    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(
                request,
                timeout=TIMEOUT_SECONDS,
            ) as response:
                response_data = json.load(response)

            model_text = response_data["choices"][0]["message"]["content"]

            if os.getenv("BC3_BAD_JSON_ID") == item_id:
                model_text = "This is intentionally invalid JSON."

            return parse_model_response(model_text)

        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            TimeoutError,
            KeyError,
            IndexError,
            TypeError,
            ValueError,
            json.JSONDecodeError,
        ) as error:
            last_error = error
            print(
                f"Attempt {attempt}/{MAX_RETRIES} failed for "
                f"{item_id}: {error}"
            )

            if attempt < MAX_RETRIES:
                delay = 2 ** (attempt - 1)
                print(f"Retrying in {delay} second(s)...")
                time.sleep(delay)

    print(f"Using safe fallback for {item_id}: {last_error}")

    return {
        "risk": "high",
        "reason": "Safe fallback used because classification failed.",
    }


def new_checkpoint():
    return {
        "next_index": 0,
        "approved_lines": [],
        "processed_ids": [],
        "complete": False,
    }


def load_checkpoint():
    if not CHECKPOINT.exists():
        return new_checkpoint()

    return json.loads(CHECKPOINT.read_text(encoding="utf-8"))


def build_report(approved_lines):
    lines = ["# Approved Changes", ""]

    if approved_lines:
        lines.extend(approved_lines)
    else:
        lines.append("_No low-risk changes were approved._")

    return "\n".join(lines) + "\n"


def save_progress(state):
    atomic_write(
        CHECKPOINT,
        json.dumps(state, indent=2) + "\n",
    )

    atomic_write(
        STAGED_REPORT,
        build_report(state["approved_lines"]),
    )


def commit_report(state):
    atomic_write(
        STAGED_REPORT,
        build_report(state["approved_lines"]),
    )

    if REPORT.exists():
        shutil.copy2(REPORT, BACKUP_REPORT)

    STAGED_REPORT.replace(REPORT)

    state["complete"] = True

    atomic_write(
        CHECKPOINT,
        json.dumps(state, indent=2) + "\n",
    )


def reset_progress():
    for path in (CHECKPOINT, STAGED_REPORT):
        if path.exists():
            path.unlink()

    print("Checkpoint and staged report removed.")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete saved progress and start over.",
    )

    parser.add_argument(
        "--pause",
        type=float,
        default=0,
        help="Pause after each item for restart testing.",
    )

    args = parser.parse_args()

    if args.reset:
        reset_progress()
        return 0

    try:
        items = load_requests()
        state = load_checkpoint()

        if state["complete"]:
            print(
                "This queue was already completed. "
                "No requests were processed again."
            )
            return 0

        start_index = state["next_index"]

        if start_index > 0:
            print(
                f"Resuming from item {start_index + 1} "
                f"of {len(items)}."
            )
        else:
            print(f"Starting {len(items)} request(s).")

        for index in range(start_index, len(items)):
            item = items[index]

            print(f"Processing {item['id']}...")

            verdict = classify(
                item["request"],
                item["id"],
            )

            if verdict["risk"] == "low":
                line = (
                    f"- **{item['id']}** ({verdict['risk']}): "
                    f"{item['request'][:80]} — "
                    f"{verdict['reason']}"
                )

                state["approved_lines"].append(line)

            state["processed_ids"].append(item["id"])
            state["next_index"] = index + 1

            save_progress(state)

            crash_after = os.getenv("BC3_CRASH_AFTER")

            if crash_after and state["next_index"] == int(crash_after):
                raise RuntimeError(
                    "Injected crash after checkpoint save."
                )

            if args.pause > 0:
                print("Checkpoint saved.")
                time.sleep(args.pause)

        commit_report(state)

        print(
            f"Complete. {len(state['approved_lines'])} "
            f"low-risk change(s) approved."
        )
        print(f"Final report: {REPORT.name}")

        return 0

    except KeyboardInterrupt:
        print(
            "\nRun interrupted. Restart the program to resume "
            "from the saved checkpoint."
        )
        return 130

    except Exception as error:
        print(f"Run stopped safely: {error}")
        print(
            "The previous good report was not destroyed. "
            "Restart to resume from the checkpoint."
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())