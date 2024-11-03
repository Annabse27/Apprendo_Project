import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from lms.models import Course
from django.contrib.auth.models import Group


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def student_user():
    user = User.objects.create_user(email='student@example.com', password='password')
    group, _ = Group.objects.get_or_create(name='Студент')
    user.groups.add(group)
    return user


@pytest.fixture
def create_courses(student_user):
    for i in range(15):
        Course.objects.create(title=f'Курс {i + 1}', description=f'Описание курса {i + 1}', owner=student_user, status='approved')


@pytest.mark.django_db
def test_course_pagination(api_client, student_user, create_courses):
    api_client.force_authenticate(user=student_user)
    response = api_client.get(reverse('lms:course-list'))

    assert response.status_code == 200
    assert 'count' in response.data
    assert len(response.data['results']) == 10

    # Проверка сортировки по id
    course_ids = [course['id'] for course in response.data['results']]
    assert course_ids == sorted(course_ids)
