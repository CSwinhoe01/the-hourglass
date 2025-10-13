from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "due_date", "status", "category"]
        widgets = {
            "due_date": forms.DateTimeInput(
                attrs={
                    "placeholder": "0000-00-00 00:00:00",  # example format
                    "autocomplete": "off",
                },
                format="%Y-%m-%d %H:%M:%S",
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # accept the same format when posting back
        self.fields["due_date"].input_formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d",
        ]