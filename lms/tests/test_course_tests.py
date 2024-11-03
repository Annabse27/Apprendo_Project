import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from lms.models import Course, QuizModel, Question, Answer
from django.contrib.auth.models import Group


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def teacher_user():
    user = User.objects.create_user(email='teacher@example.com', password='passwordteacher')
    group, _ = Group.objects.get_or_create(name='Преподаватель')
    user.groups.add(group)
    return user


@pytest.fixture
def course(teacher_user):
    return Course.objects.create(title="Sample Course", description="Course Description", owner=teacher_user)


@pytest.mark.django_db
def test_create_test(api_client, teacher_user, course):
    api_client.force_authenticate(user=teacher_user)
    data = {'title': 'Test Title', 'description': 'Test Description', 'course': course.id}
    response = api_client.post(reverse('lms:test-list'), data)
    assert response.status_code == 201
    assert QuizModel.objects.count() == 1
