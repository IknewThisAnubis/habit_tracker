from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django import forms
from .models import Habit
from django.utils.timezone import now

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "password"]

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def dashboard(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, "habitrack/dashboard.html", {"habits": habits})

@require_POST
@login_required
def create_habit(request):
    name = request.POST.get("name")
    habit = Habit.objects.create(user=request.user, name=name)
    return JsonResponse({"id": habit.id, "name": habit.name})

@login_required
def log_habit(request, habit_id):
    habit = Habit.objects.get(id=habit_id, user=request.user)
    log, _ = HabitLog.objects.get_or_create(habit=habit, date=now().date())
    log.completed = True
    log.save()
    return JsonResponse({"status": "logged"})

from .utils import calculate_streak

@login_required
def dashboard(request):
    habits = Habit.objects.filter(user=request.user)
    for h in habits:
        h.streak = calculate_streak(h)
    return render(request, "tracker/dashboard.html", {"habits": habits})