"""
URL configuration for habitrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.dashboard, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("habits/", views.habits_page, name="habits"),
    path("habits/<int:habit_id>/edit/", views.edit_habit, name="edit_habit"),
    path("habits/<int:habit_id>/delete/", views.delete_habit, name="delete_habit"),
    path("register/", views.register, name="register"),
    path("habits/<int:habit_id>/log/", views.log_habit, name="log_habit"),
    path("history/", views.history, name="history"),
    path("history/<int:year>/<int:month>/<int:day>/", views.day_details, name="day_details"),
    path("save-mood-gratitude/", views.save_mood_gratitude, name="save_mood_gratitude"),
]
