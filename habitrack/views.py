from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Habit

@login_required
def dashboard(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, "habitrack/dashboard.html", {"habits": habits})