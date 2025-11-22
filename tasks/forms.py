from django import forms
from .models import Task
from django.core.exceptions import ValidationError
from datetime import date


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']

    def clean_due_date(self):
        due = self.cleaned_data.get('due_date')
        if due and due < date.today():
            raise ValidationError('Due date cannot be in the past')
        return due
