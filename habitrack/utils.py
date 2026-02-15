from datetime import timedelta
from django.utils import timezone

def calculate_streak(habit):
    today = timezone.localdate()
    streak = 0

    while True:
        day = today - timedelta(days=streak)
        if habit.logs.filter(date=day, completed=True).exists():
            streak += 1
        else:
            break

    return streak


def calculate_overall_streak(user):
    habit_count = user.habit_set.count()
    if habit_count == 0:
        return 0

    today = timezone.localdate()
    streak = 0

    while True:
        day = today - timedelta(days=streak)
        completed_count = user.habit_set.filter(
            logs__date=day,
            logs__completed=True,
        ).distinct().count()
        if completed_count == habit_count:
            streak += 1
        else:
            break

    return streak
