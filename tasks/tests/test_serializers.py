import pytest
from datetime import date, timedelta
from tasks.serializers import TaskSerializer, TaskWithUserSerializer, UserSerializer
from django.contrib.auth import get_user_model


class TestTaskSerializerObjectStyle:
    def test_valid_serializer(self):
        data = {
            'title': 'Serialize task',
            'description': 'serialize',
            'due_date': (date.today() + timedelta(days=3)).isoformat(),
        }
        s = TaskSerializer(data=data)
        assert s.is_valid(), s.errors

    def test_missing_title(self):
        data = {
            'description': 'no title',
            'due_date': (date.today() + timedelta(days=3)).isoformat(),
        }
        s = TaskSerializer(data=data)
        assert not s.is_valid()
        assert 'title' in s.errors

    def test_due_date_not_in_past(self):
        data = {
            'title': 'past',
            'description': 'past',
            'due_date': (date.today() - timedelta(days=1)).isoformat(),
        }
        s = TaskSerializer(data=data)
        assert not s.is_valid()
        assert 'due_date' in s.errors


def test_task_serializer_functional_valid():
    data = {
        'title': 'Func serialize',
        'description': 'ok',
        'due_date': (date.today() + timedelta(days=5)).isoformat(),
    }
    s = TaskSerializer(data=data)
    assert s.is_valid()


def test_task_with_user_serializer_nested_valid(db):
    data = {
        'title': 'Nested',
        'description': 'with user',
        'due_date': (date.today() + timedelta(days=4)).isoformat(),
        'user': {'username': 'tester', 'email': 't@example.com'},
    }
    s = TaskWithUserSerializer(data=data)
    assert s.is_valid(), s.errors
    task = s.save()
    User = get_user_model()
    assert User.objects.filter(username='tester').exists()


def test_task_with_user_serializer_nested_invalid_user():
    data = {
        'title': 'Nested',
        'description': 'bad user',
        'due_date': (date.today() + timedelta(days=4)).isoformat(),
        'user': {'username': ''},
    }
    s = TaskWithUserSerializer(data=data)
    assert not s.is_valid()
    assert 'user' in s.errors
