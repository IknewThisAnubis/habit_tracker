from django.contrib.auth.models import User
from django.db import models
from datetime import date

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class HabitLog(models.Model):
    MOOD_CHOICES = [
        (1, 'Very Sad'),
        (2, 'Sad'),
        (3, 'Neutral'),
        (4, 'Happy'),
        (5, 'Very Happy'),
    ]
    
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="logs")
    date = models.DateField(default=date.today)
    completed = models.BooleanField(default=True)
    mood = models.IntegerField(choices=MOOD_CHOICES, null=True, blank=True)
    gratitude = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ("habit", "date")