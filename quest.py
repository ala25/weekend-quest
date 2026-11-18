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
        break

if not found_activity:
    print("No quests fit your time. Come back when you have 15 minutes!")