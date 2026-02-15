from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Habit, HabitLog
from .utils import calculate_streak
from datetime import date, timedelta

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

    def test_dashboard_sets_done_today_flag(self):
        user = User.objects.create_user("u", password="p")
        habit = Habit.objects.create(user=user, name="A")

        self.client.login(username="u", password="p")
        response = self.client.get(reverse("dashboard"))

        habits = list(response.context["habits"])
        self.assertEqual(habits[0].id, habit.id)
        self.assertFalse(habits[0].done_today)
        self.assertEqual(response.context["overall_streak"], 0)

    def test_dashboard_overall_streak_counts_all_habits(self):
        user = User.objects.create_user("u", password="p")
        h1 = Habit.objects.create(user=user, name="A")
        h2 = Habit.objects.create(user=user, name="B")

        HabitLog.objects.create(habit=h1, date=date.today())
        HabitLog.objects.create(habit=h2, date=date.today())
        HabitLog.objects.create(habit=h1, date=date.today() - timedelta(days=1))
        HabitLog.objects.create(habit=h2, date=date.today() - timedelta(days=1))

        self.client.login(username="u", password="p")
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.context["overall_streak"], 2)

class CreateHabitTest(TestCase):
    def test_create_habit(self):
        User.objects.create_user("u", password="p")
        self.client.login(username="u", password="p")
        response = self.client.post(reverse("habits"), {"name": "X"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Habit.objects.count(), 1)

class RegisterTest(TestCase):
    def test_register(self):
        response = self.client.post(reverse("register"), {"username": "x", "password": "y"})
        self.assertEqual(response.status_code, 302)  # redirect to dashboard
        self.assertTrue(User.objects.filter(username="x").exists())

class StreakTest(TestCase):
    def test_streak(self):
        u = User.objects.create_user("a", password="x")
        h = Habit.objects.create(name="test", user=u)

        HabitLog.objects.create(habit=h, date=date.today())
        HabitLog.objects.create(habit=h, date=date.today() - timedelta(days=1))

        self.assertEqual(calculate_streak(h), 2)

class LogHabitTest(TestCase):
    def test_log_habit_creates_log_for_today(self):
        user = User.objects.create_user("u", password="p")
        habit = Habit.objects.create(user=user, name="Hydrate")
        self.client.login(username="u", password="p")

        response = self.client.post(reverse("log_habit", args=[habit.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            HabitLog.objects.filter(
                habit=habit,
                date=timezone.localdate(),
                completed=True,
            ).exists()
        )

    def test_log_habit_for_other_user_returns_404(self):
        owner = User.objects.create_user("owner", password="p")
        attacker = User.objects.create_user("attacker", password="p")
        habit = Habit.objects.create(user=owner, name="Read")

        self.client.login(username="attacker", password="p")
        response = self.client.post(reverse("log_habit", args=[habit.id]))
        self.assertEqual(response.status_code, 404)

    def test_log_habit_requires_post(self):
        user = User.objects.create_user("u", password="p")
        habit = Habit.objects.create(user=user, name="Run")
        self.client.login(username="u", password="p")

        response = self.client.get(reverse("log_habit", args=[habit.id]))
        self.assertEqual(response.status_code, 405)

class EditHabitTest(TestCase):
    def test_edit_habit_get(self):
        user = User.objects.create_user("u", password="p")
        habit = Habit.objects.create(user=user, name="Old")

        self.client.login(username="u", password="p")
        response = self.client.get(reverse("edit_habit", args=[habit.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Old")

    def test_edit_habit_post_updates(self):
        user = User.objects.create_user("u", password="p")
        habit = Habit.objects.create(user=user, name="Old")

        self.client.login(username="u", password="p")
        response = self.client.post(
            reverse("edit_habit", args=[habit.id]),
            {"name": "New"},
        )
        self.assertEqual(response.status_code, 302)
        habit.refresh_from_db()
        self.assertEqual(habit.name, "New")

    def test_edit_habit_other_user_returns_404(self):
        owner = User.objects.create_user("owner", password="p")
        attacker = User.objects.create_user("attacker", password="p")
        habit = Habit.objects.create(user=owner, name="Private")

        self.client.login(username="attacker", password="p")
        response = self.client.get(reverse("edit_habit", args=[habit.id]))
        self.assertEqual(response.status_code, 404)

class DeleteHabitTest(TestCase):
    def test_delete_habit_post(self):
        user = User.objects.create_user("u", password="p")
        habit = Habit.objects.create(user=user, name="ToDelete")

        self.client.login(username="u", password="p")
        response = self.client.post(reverse("delete_habit", args=[habit.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Habit.objects.filter(id=habit.id).exists())

    def test_delete_habit_get_not_allowed(self):
        user = User.objects.create_user("u", password="p")
        habit = Habit.objects.create(user=user, name="ToDelete")

        self.client.login(username="u", password="p")
        response = self.client.get(reverse("delete_habit", args=[habit.id]))
        self.assertEqual(response.status_code, 405)
