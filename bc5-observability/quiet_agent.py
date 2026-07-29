#!/usr/bin/env python3
"""Build Challenge 5 starter — an agent with ZERO observability.

Run from the repo root:  python3 bc5-observability/quiet_agent.py

It plans a three-step research summary and usually produces something. But
when the output is wrong — and sometimes it is — you have nothing: no logs,
no trace, no cost data, no way to say WHICH step went sideways. On purpose.

YOUR JOB (see README.md): instrument this stack — structured trace logging
(JSONL: timestamp, step, model, tokens, latency, decision), a human-in-the-
loop checkpoint before anything is written to disk, and cost/usage pulled
from the gateway (~/.openclaw/gateway.log and/or common.llm.STATS). Then
break something on purpose, diagnose it FROM YOUR OWN TRACE, and write the
incident up: what happened, how the trace showed it, what you changed.
"""
import pathlib
import sys
import json
import time
from datetime import datetime

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common.llm import chat, STATS

HERE = pathlib.Path(__file__).resolve().parent
TOPIC = "why long-running agents need checkpoints"
TRACE_FILE = HERE / "trace.jsonl"


def log_trace(step, model, prompt_size, response_size, tokens, latency, decision):
    record = {
        "timestamp": datetime.now().isoformat(),
        "step": step,
        "model": model,
        "prompt_size": prompt_size,
        "response_size": response_size,
        "tokens": tokens,
        "latency_seconds": round(latency, 3),
        "decision": decision,
    }

    with TRACE_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")

def main():
    # ----- PLAN -----
    plan_prompt = f"List 3 short bullet questions someone should answer to explain: {TOPIC}"

    tokens_before = STATS["tokens"]
    start_time = time.perf_counter()

    plan = chat([
        {"role": "user", "content": plan_prompt}
    ])

    plan_latency = time.perf_counter() - start_time
    plan_tokens = STATS["tokens"] - tokens_before

    log_trace(
        step="plan",
        model="default",
        prompt_size=len(plan_prompt),
        response_size=len(plan),
        tokens=plan_tokens,
        latency=plan_latency,
        decision="Generated three research questions",
    )

    # ----- ANSWERS -----
    answers_prompt = "Answer each question in 2 sentences:\n" + plan

    tokens_before = STATS["tokens"]
    start_time = time.perf_counter()

    answers = chat([
        {"role": "user", "content": answers_prompt}
    ])

    answers_latency = time.perf_counter() - start_time
    answers_tokens = STATS["tokens"] - tokens_before

    log_trace(
        step="answers",
        model="default",
        prompt_size=len(answers_prompt),
        response_size=len(answers),
        tokens=answers_tokens,
        latency=answers_latency,
        decision="Generated answers for the research questions",
    )

        # ----- SUMMARY -----
    summary_prompt = "Compress this into a 4-sentence summary for a student:\n" + answers

    tokens_before = STATS["tokens"]
    start_time = time.perf_counter()

    try:
        summary = chat([
            {"role": "user", "content": summary_prompt}
        ])

        summary_latency = time.perf_counter() - start_time
        summary_tokens = STATS["tokens"] - tokens_before

        log_trace(
            step="summary",
            model="default",
            prompt_size=len(summary_prompt),
            response_size=len(summary),
            tokens=summary_tokens,
            latency=summary_latency,
            decision="Generated final student summary",
        )

    except Exception as error:
        summary_latency = time.perf_counter() - start_time

        log_trace(
            step="summary",
            model="default",
            prompt_size=len(summary_prompt),
            response_size=0,
            tokens=STATS["tokens"] - tokens_before,
            latency=summary_latency,
            decision=f"FAILED: {type(error).__name__}: {error}",
        )

        print("\nSummary step failed. Check trace.jsonl for details.")
        return

    estimated_cost = STATS["tokens"] * 0.000001
    print(f"\nCurrent token usage: {STATS['tokens']}")
    print(f"Estimated cost so far: ${estimated_cost:.6f}")

    approval = input("\nApprove this summary and write it to summary.md? (yes/no): ").strip().lower()

    if approval in {"yes", "y"}:
        (HERE / "summary.md").write_text(
            f"# {TOPIC}\n\n{summary}\n",
            encoding="utf-8",
        )

        log_trace(
            step="human_approval",
            model="human",
            prompt_size=0,
            response_size=len(approval),
            tokens=0,
            latency=0,
            decision="Approved summary and wrote summary.md",
        )

        print("\nApproved. summary.md was written.")
    else:
        log_trace(
            step="human_approval",
            model="human",
            prompt_size=0,
            response_size=len(approval),
            tokens=0,
            latency=0,
            decision="Rejected summary; summary.md was not written",
        )

        print("\nRejected. summary.md was not changed.")


if __name__ == "__main__":
    main()
