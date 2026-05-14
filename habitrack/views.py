from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST, require_http_methods
from calendar import monthcalendar
from datetime import datetime, timedelta

from .forms import RegisterForm, HabitForm, MoodGratitudeForm
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
    
    # Get today's mood and gratitude
    today_log = HabitLog.objects.filter(habit__user=request.user, date=today).first()
    
    return render(
        request,
        "habitrack/dashboard.html",
        {
            "habits": habits,
            "current_date": today,
            "overall_streak": overall_streak,
            "today_log": today_log,
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
    if not created:
        # Toggle the completed status
        log.completed = not log.completed
        log.save()
    return JsonResponse(
        {
            "status": "logged",
            "streak": calculate_streak(habit),
            "overall_streak": calculate_overall_streak(request.user),
        }
    )

@login_required
def history(request):
    """Display calendar history view"""
    today = timezone.localdate()
    year = request.GET.get("year", today.year)
    month = request.GET.get("month", today.month)
    
    try:
        year = int(year)
        month = int(month)
    except ValueError:
        year = today.year
        month = today.month
    
    # Validate month/year
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1
    
    habits = Habit.objects.filter(user=request.user).order_by("created_at")
    
    # Get calendar for the month
    cal = monthcalendar(year, month)
    
    # Get all habit logs for this month
    start_date = datetime(year, month, 1).date()
    if month == 12:
        end_date = datetime(year + 1, 1, 1).date() - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1).date() - timedelta(days=1)
    
    logs = HabitLog.objects.filter(
        habit__user=request.user,
        date__gte=start_date,
        date__lte=end_date
    ).values_list('date', 'habit_id', 'completed', 'mood', 'gratitude')
    
    # Build calendar data
    calendar_data = []
    for week in cal:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append(None)
            else:
                date_obj = datetime(year, month, day).date()
                # Check if all habits are completed on this day
                day_logs = HabitLog.objects.filter(
                    habit__user=request.user,
                    date=date_obj,
                    completed=True
                ).count()
                all_completed = day_logs == habits.count() and habits.count() > 0
                
                week_data.append({
                    "day": day,
                    "date": date_obj,
                    "all_completed": all_completed
                })
        calendar_data.append(week_data)
    
    # Calculate navigation
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    context = {
        "calendar": calendar_data,
        "year": year,
        "month": month,
        "month_name": datetime(year, month, 1).strftime("%B"),
        "habits": habits,
        "prev_month": prev_month,
        "prev_year": prev_year,
        "next_month": next_month,
        "next_year": next_year,
    }
    
    return render(request, "habitrack/history.html", context)

@login_required
@require_http_methods(["GET"])
def day_details(request, year, month, day):
    """Get details for a specific day"""
    try:
        date_obj = datetime(int(year), int(month), int(day)).date()
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid date"}, status=400)
    
    # Check if date is in future
    if date_obj > timezone.localdate():
        return JsonResponse({"error": "Cannot view future dates"}, status=400)
    
    habits = Habit.objects.filter(user=request.user).order_by("created_at")
    
    # Get all logs for this day
    day_logs = HabitLog.objects.filter(
        habit__user=request.user,
        date=date_obj
    )
    
    log_data = {}
    for log in day_logs:
        log_data[log.habit_id] = {
            "completed": log.completed,
            "mood": log.mood,
            "gratitude": log.gratitude,
        }
    
    habits_list = []
    for habit in habits:
        habit_log = log_data.get(habit.id, {})
        habits_list.append({
            "id": habit.id,
            "name": habit.name,
            "completed": habit_log.get("completed", False),
        })
    
    # Get mood and gratitude (take from first log with this data)
    mood_log = day_logs.exclude(mood__isnull=True).first()
    mood = mood_log.mood if mood_log else None
    gratitude = mood_log.gratitude if mood_log else None
    
    return JsonResponse({
        "date": str(date_obj),
        "habits": habits_list,
        "mood": mood,
        "gratitude": gratitude,
    })

@require_POST
@login_required
def save_mood_gratitude(request):
    """Save mood and gratitude for today"""
    today = timezone.localdate()
    mood = request.POST.get("mood")
    gratitude = request.POST.get("gratitude", "").strip()
    
    # Get or create a log entry for today (use first habit as reference)
    habit = Habit.objects.filter(user=request.user).first()
    if not habit:
        return JsonResponse({"error": "No habits found"}, status=400)
    
    log, _ = HabitLog.objects.get_or_create(
        habit=habit,
        date=today,
        defaults={"completed": False, "mood": mood, "gratitude": gratitude}
    )
    
    # Update mood and gratitude
    if mood:
        log.mood = int(mood)
    log.gratitude = gratitude
    log.save()
    
    return JsonResponse({
        "status": "saved",
        "mood": log.mood,
        "gratitude": log.gratitude,
    })
