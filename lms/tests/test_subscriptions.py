import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from lms.models import Course, Subscription


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(email='user@example.com', password='password')


@pytest.fixture
def course(user):
    return Course.objects.create(title='Курс 1', description='Описание курса', owner=user, status='approved')


@pytest.mark.django_db
def test_subscribe_and_unsubscribe(api_client, user, course):
    api_client.force_authenticate(user=user)
    response = api_client.post(reverse('lms:course-subscription'), {'course_id': course.id})
    assert response.status_code == 200
    assert Subscription.objects.filter(user=user, course=course).exists()
    response = api_client.post(reverse('lms:course-subscription'), {'course_id': course.id})
    assert response.status_code == 200
    assert not Subscription.objects.filter(user=user, course=course).exists()
