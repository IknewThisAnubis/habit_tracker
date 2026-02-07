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

class DashboardViewTest(TestCase):
    def test_user_sees_only_own_habits(self):
        u1 = User.objects.create_user("u1", password="p")
        u2 = User.objects.create_user("u2", password="p")
        Habit.objects.create(user=u1, name="A")
        Habit.objects.create(user=u2, name="B")

        self.client.login(username="u1", password="p")
        response = self.client.get(reverse("dashboard"))

        self.assertContains(response, "A")
        self.assertNotContains(response, "B")

class CreateHabitTest(TestCase):
    def test_create_habit(self):
        user = User.objects.create_user("u", password="p")
        self.client.login(username="u", password="p")
        response = self.client.post("/habits/create/", {"name": "X"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Habit.objects.count(), 1)

class RegisterTest(TestCase):
    def test_register(self):
        response = self.client.post("/register/", {"username": "x", "password": "y"})
        self.assertEqual(response.status_code, 302)  # redirect to dashboard
        self.assertTrue(User.objects.filter(username="x").exists())