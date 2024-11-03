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
def moderator_user():
    user = User.objects.create_user(email='moderator@example.com', password='passwordmoderator')
    group, _ = Group.objects.get_or_create(name='Модераторы')
    user.groups.add(group)
    return user


@pytest.fixture
def teacher_user():
    user = User.objects.create_user(email='teacher@example.com', password='passwordteacher')
    group, _ = Group.objects.get_or_create(name='Преподаватель')
    user.groups.add(group)
    return user


@pytest.fixture
def course(teacher_user):
    return Course.objects.create(title='Test Course', description='Test Description', owner=teacher_user)


@pytest.mark.django_db
def test_moderator_can_edit_course(api_client, moderator_user, course):
    api_client.force_authenticate(user=moderator_user)
    response = api_client.patch(reverse('lms:course-detail', args=[course.id]), {'title': 'Updated Title'})
    assert response.status_code == 200


@pytest.mark.django_db
def test_moderator_cannot_delete_course(api_client, moderator_user, course):
    api_client.force_authenticate(user=moderator_user)
    response = api_client.delete(reverse('lms:course-detail', args=[course.id]))
    assert response.status_code == 403
