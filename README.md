# Weekend Quest

A Python program that picks the first activity that fits your free time.

## Run

From the `quest` folder:

```bash
uv run python quest.py
```
Create a local .env file containing OPENAI_API_KEY=your-key-here. The program selects an activity, then requests a two-sentence briefing from OpenAI. If the request fails, it displays a friendly fallback. A saved example is available in sample_briefing.txt.

## Example

```text
How many minutes do you have? 45
Explore a hidden garden
```

Entering `0` shows a message that no quests fit. Entering `banana` asks you to enter a whole number.

## What I learned

- `int()` converts the text from `input()` into an integer so we can compare it with each activity's duration.
- `try/except` handles errors. Here, `except ValueError` catches input that `int()` cannot convert into an integer, like `banana`. The program prints a friendly message and exits.
- `break` stops the loop after the first activity that fits, so the program picks only one activity.

## Next 10-minute step

Start AA-71: explore how to send the selected activity to a model for a two-sentence briefing.

## AA-73 checks

These checks were run manually during development. Results below come from
the user's reports in chat and shared screenshots, not automated tests or a
saved terminal transcript. The code evolved during these checks; this is not
a fixed-version evaluation or a comparison of two prompts.

| # | Input | Expected behavior | Reported result |
| --- | --- | --- | --- |
| 1 | `do ai learning` | Title, three learning steps, no deadline (`None` in Python). | Matched. |
| 2 | `do ai learning by Friday` | Learning brief with Friday deadline. | Matched. |
| 3 | Empty file | Reject blank notes before calling the model. | Initially returned “Notes missing” with three instructions; after adding the blank-input guard, printed the friendly message and stopped before the time question. |
| 4 | `Plan a game night for Friday. Actually, make it Saturday instead.` | Follow the correction; deadline Saturday. | Matched. |
| 5 | `Learn Python. Do not set a deadline.` | Python learning brief with no deadline. | Matched. |
| 6 | `Prepare for my Python quiz by Monday: review loops, practice functions, and take a practice quiz.` | Steps cover loops, functions, and a practice quiz; deadline Monday. | Matched. |
| 7 | `Buy groceries and cook dinner by Sunday. I already bought the groceries.` | Do not suggest buying groceries again; deadline Sunday. | Screenshot showed checking purchased groceries, planning the menu, and cooking dinner; deadline Sunday. |
| 8 | `Practice Python for 20 minutes.` | Treat 20 minutes as a duration, not a deadline; deadline absent. | Matched. |
| 9 | `Study Python by Friday. Study Python by Friday.` | Treat duplicate notes as one task; deadline Friday. | Matched. |
| 10 | `Learn Python by Friday. Don't suggest watching videos.` | Deadline Friday; no steps suggesting videos. | Matched. |

Schema-pass counts were not separately recorded. Remaining AA-73 work: Python
tests for invalid output, and a comparison of two prompts on these same examples
with schema validity and meaning preservation recorded separately. Blank input
is handled by Python rather than sent to the model.

### Automated prompt comparison

`evaluate_briefs.py` contains both fixed prompts and all 10 labeled examples.
Run it with:

```bash
uv run --env-file .env python evaluate_briefs.py
```

It makes 18 OpenAI calls (nine nonblank notes × two prompts), checks blank input
locally, and saves responses incrementally under a new `evaluations/` directory
for each run. It does not overwrite the notes or earlier results. Schema and
deadline checks are recorded separately; `meaning_pass` stays unset until the
saved outputs are reviewed against the expected behavior. Connection errors
are not evidence of schema failure. This automation has not yet completed a
successful API evaluation before approval; the initial restricted run returned connection errors.

### Completed automated comparison

Results: `evaluations/20261119T001847815451Z/results.json`. Both fixed prompts
used `gpt-4.1-mini` on the same nine nonblank examples. The blank example was
rejected locally for each prompt. Full API responses and expected labels are
saved with per-case schema, deadline, and qualitative meaning checks.

| Check | Prompt A | Prompt B |
| --- | --- | --- |
| Schema passes | 9/9 | 9/9 |
| Exact deadline-field matches | 9/9 | 8/9 |
| Meaning preserved (Codex review) | 9/9 | 7/9 |
| Blank input rejected locally | 1/1 | 1/1 |

Prompt B invented Wednesday/Thursday intermediate deadlines for the Friday AI
learning example. For the game-night correction, it mentioned Saturday in the
title and steps but returned a null deadline. Prompt A passed both cases.
Keep Prompt A based on this run. These small, single-run results do not prove
general reliability; meaning scores are qualitative assistant review, not human
review or automated semantic validation. Suggested actions may elaborate on notes,
but invented deadlines count as a failure.

Schema tests: `uv run python -m unittest test_brief.py` passed all three tests
(two steps rejected, missing title rejected, valid brief accepted).
