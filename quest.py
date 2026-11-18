from openai import OpenAI, APIError

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
        prompt = f"Write a two-sentence briefing for this quest: {activity['name']}."
        print(prompt)
        try:
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt,
            )
            print(response.output_text)
        except APIError:
            print("The briefing is unavailable. You can still enjoy your quest!")
        break

if not found_activity:
    print("No quests fit your time. Come back when you have 15 minutes!")