from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST, require_http_methods

from .forms import RegisterForm, HabitForm
from .models import Habit, HabitLog
from .utils import calculate_streak, calculate_overall_streak

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
    return render(request, "habitrack/register.html", {"form": form})

@login_required
def dashboard(request):
    habits = Habit.objects.filter(user=request.user).order_by("created_at")
    today = timezone.localdate()
    for habit in habits:
        habit.streak = calculate_streak(habit)
        habit.done_today = habit.logs.filter(date=today, completed=True).exists()
    overall_streak = calculate_overall_streak(request.user)
    return render(
        request,
        "habitrack/dashboard.html",
        {
            "habits": habits,
            "current_date": today,
            "overall_streak": overall_streak,
        },
    )

@login_required
@require_http_methods(["GET", "POST"])
def habits_page(request):
    if request.method == "POST":
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect("habits")
    else:
        form = HabitForm()

    habits = Habit.objects.filter(user=request.user).order_by("created_at")
    return render(
        request,
        "habitrack/habits.html",
        {
            "habits": habits,
            "form": form,
        },
    )

@login_required
@require_http_methods(["GET", "POST"])
def edit_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if request.method == "POST":
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = HabitForm(instance=habit)
    return render(
        request,
        "habitrack/edit_habit.html",
        {"form": form, "habit": habit},
    )

@require_POST
@login_required
def delete_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    habit.delete()
    return redirect("habits")

@require_POST
@login_required
def log_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    today = timezone.localdate()
    log, created = HabitLog.objects.get_or_create(
        habit=habit,
        date=today,
        defaults={"completed": True},
    )
    if not created and not log.completed:
        log.completed = True
        log.save()
    return JsonResponse(
        {
            "status": "logged",
            "streak": calculate_streak(habit),
            "overall_streak": calculate_overall_streak(request.user),
        }
    )
