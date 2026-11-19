from openai import OpenAI, APIError
from pathlib import Path
from brief_schema import Brief

notes = Path("messy_note.txt").read_text()
if not notes.strip():
    print("please add a note to the file")
    raise SystemExit

client = OpenAI()

activities = [
    {"name": "Explore a hidden garden", "minutes": 15},
    {"name": "Visit a wizard's market", "minutes": 30},
    {"name": "Search for a lost dragon", "minutes": 60},
]

try:
    available_minutes = int(input("How many minutes do you have? "))
except ValueError:
    print("Please enter a whole number, like 30.")
    raise SystemExit

found_activity = False

for activity in activities:
    if activity["minutes"] <= available_minutes:
        print(activity["name"])
        found_activity = True
        prompt = f'Return only JSON with "title", "steps" (exactly three items), and "deadline" (null if none is mentioned). Use these notes: {notes}'
        #prompt = f"""Turn the notes into a brief with a title, exactly three suggested steps, and a deadline.
#Preserve the user's intent and restrictions.
#Follow corrections and do not repeat completed tasks.
#Use null for the deadline when none is stated. A duration is not a deadline.
#Notes: {notes}"""
        print(prompt)
        try:
            response = client.responses.parse(
                model="gpt-4.1-mini",
                input=prompt,
                text_format=Brief,
            )
    
            brief = response.output_parsed
            if brief is not None:
                print(brief.title)
                for step in brief.steps:
                    print(step)
                print(brief.deadline)
            else:
                print("No brief was returned")
        except APIError:
            print("The briefing is unavailable. You can still enjoy your quest!")
        break

if not found_activity:
    print("No quests fit your time. Come back when you have 15 minutes!")