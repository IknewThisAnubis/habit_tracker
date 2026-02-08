from datetime import timedelta
from django.utils.timezone import now

def calculate_streak(habit):
    today = now().date()
    streak = 0

    while True:
        day = today - timedelta(days=streak)
        if habit.logs.filter(date=day, completed=True).exists():
            streak += 1
        else:
            break

    return streak