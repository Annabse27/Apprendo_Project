import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from lms.models import Course, Lesson
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
    return Course.objects.create(title='Test Course', description='Description', owner=teacher_user)


@pytest.fixture
def lesson(teacher_user, course):
    return Lesson.objects.create(
        title="Test Lesson",
        description="Lesson Description",
        video_url="https://www.youtube.com/watch?v=abc123",
        course=course,
        owner=teacher_user
    )


@pytest.mark.django_db
def test_teacher_can_create_lesson(api_client, teacher_user, course):
    api_client.force_authenticate(user=teacher_user)
    response = api_client.post(reverse('lms:lesson-list-create'), {
        'title': 'New Lesson',
        'description': 'Lesson description',
        'video_url': 'https://www.youtube.com/watch?v=abc123',
        'course': course.id
    })
    assert response.status_code == 201
