import pytest
from datetime import date, timedelta
from tasks.forms import TaskForm


class TestTaskFormObjectStyle:
    def test_valid_form(self):
        data = {
            'title': 'Test task',
            'description': 'A task',
            'due_date': date.today() + timedelta(days=1),
        }
        form = TaskForm(data)
        assert form.is_valid()

    def test_missing_required_fields(self):
        form = TaskForm({})
        assert not form.is_valid()
        assert 'title' in form.errors
        assert 'due_date' in form.errors

    def test_due_date_cannot_be_past(self):
        data = {
            'title': 'Past task',
            'description': 'Past',
            'due_date': date.today() - timedelta(days=1),
        }
        form = TaskForm(data)
        assert not form.is_valid()
        assert 'due_date' in form.errors


def test_task_form_functional_valid():
    data = {
        'title': 'Func task',
        'description': 'Functional',
        'due_date': date.today() + timedelta(days=2),
    }
    form = TaskForm(data)
    assert form.is_valid()


def test_task_form_functional_invalid_due_date():
    data = {
        'title': 'Func task',
        'description': 'Functional',
        'due_date': date.today() - timedelta(days=2),
    }
    form = TaskForm(data)
    assert not form.is_valid()
    assert 'due_date' in form.errors
