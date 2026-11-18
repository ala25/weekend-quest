# Weekend Quest

A Python program that picks the first activity that fits your free time.

## Run

From the `quest` folder:

```bash
uv run python quest.py
```

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
