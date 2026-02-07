from django.test import TestCase
from django.contrib.auth.models import User
from .models import Habit
from django.urls import reverse

class HabitModelTest(TestCase):
    def test_habit_creation(self):
        user = User.objects.create_user(username="u", password="p")
        habit = Habit.objects.create(user=user, name="Test")
        self.assertEqual(habit.name, "Test")
        self.assertEqual(habit.user, user)
        
    def test_habit_string_representation(self):
        user = User.objects.create_user(username="u", password="p")
        habit = Habit.objects.create(user=user, name="Read")

        self.assertEqual(str(habit), "Read")

class AuthTest(TestCase):
    def test_login_required(self):
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 302)