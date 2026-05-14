from django import forms
from django.contrib.auth.models import User

from .models import Habit, HabitLog


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "password"]


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Habit name"}),
        }

    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()
        if not name:
            raise forms.ValidationError("Habit name cannot be blank.")
        return name


class MoodGratitudeForm(forms.ModelForm):
    class Meta:
        model = HabitLog
        fields = ["mood", "gratitude"]
        widgets = {
            "mood": forms.RadioSelect(),
            "gratitude": forms.Textarea(attrs={"rows": 3, "placeholder": "What are you grateful for today?"}),
        }
