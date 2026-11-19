"""Compare two fixed prompts; save every response without editing messy_note.txt."""

import json
from datetime import datetime, timezone
from pathlib import Path

from openai import OpenAI, OpenAIError
from pydantic import ValidationError

from brief_schema import Brief


PROMPTS = {
    "A": 'Return only JSON with "title", "steps" (exactly three items), and "deadline" (null if none is mentioned). Use these notes: {notes}',
    "B": """Turn the notes into a brief with a title, exactly three suggested steps, and a deadline.
Preserve the user's intent and restrictions.
Follow corrections and do not repeat completed tasks.
Use null for the deadline when none is stated. A duration is not a deadline.
Notes: {notes}""",
}

# Labels are fixed before running either prompt.
CASES = [
    ("learning", "do ai learning", "AI learning steps; no deadline", None),
    ("deadline", "do ai learning by Friday", "AI learning steps; Friday deadline", "Friday"),
    ("blank", "", "Reject locally without a model call", None),
    ("correction", "Plan a game night for Friday. Actually, make it Saturday instead.", "Game night; use Saturday correction", "Saturday"),
    ("no_deadline", "Learn Python. Do not set a deadline.", "Python learning; no deadline", None),
    ("three_topics", "Prepare for my Python quiz by Monday: review loops, practice functions, and take a practice quiz.", "Cover loops, functions, practice quiz; Monday", "Monday"),
    ("completed", "Buy groceries and cook dinner by Sunday. I already bought the groceries.", "Cook dinner; do not buy groceries again; Sunday", "Sunday"),
    ("duration", "Practice Python for 20 minutes.", "20-minute practice; no invented recurring schedule or deadline", None),
    ("duplicate", "Study Python by Friday. Study Python by Friday.", "One Python study task; Friday", "Friday"),
    ("restriction", "Learn Python by Friday. Don't suggest watching videos.", "Python learning; no videos; Friday", "Friday"),
]


def main():
    client = OpenAI(timeout=30, max_retries=0)
    run_dir = Path("evaluations") / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    run_dir.mkdir(parents=True)
    results = {"model": "gpt-4.1-mini", "prompts": PROMPTS, "results": []}
    for case_id, notes, expected, deadline in CASES:
        for name, template in PROMPTS.items():
            row = {"case": case_id, "prompt": name, "notes": notes,
                   "expected": expected, "expected_deadline": deadline,
                   "schema_pass": None, "meaning_pass": None}
            if not notes.strip():
                row.update(status="rejected_blank", local_guard_pass=True)
            else:
                try:
                    response = client.responses.parse(
                        model=results["model"], input=template.format(notes=notes),
                        text_format=Brief,
                    )
                    row["raw_response"] = response.model_dump(mode="json")
                    brief = response.output_parsed
                    if brief is None:
                        row.update(status="no_parsed_output", schema_pass=False)
                    else:
                        row.update(status="parsed", schema_pass=True,
                                   output=brief.model_dump(),
                                   deadline_pass=brief.deadline == deadline)
                except (OpenAIError, ValidationError) as error:
                    row.update(status="error", error_type=type(error).__name__,
                               error=str(error),
                               schema_pass=False if isinstance(error, ValidationError) else None)
            results["results"].append(row)
            (run_dir / "results.json").write_text(json.dumps(results, indent=2))
            print(f"{case_id} / {name}: {row['status']}", flush=True)
    print(f"Saved results to {run_dir / 'results.json'}")
    print("Meaning checks require review of the saved outputs against their labels.")


if __name__ == "__main__":
    main()
