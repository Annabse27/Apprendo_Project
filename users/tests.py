import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from users.models import User
from lms.models import Course
from users.models import Payment


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    def _create_user(email, password):
        user = User.objects.create_user(email=email, password=password)
        return user
    return _create_user


@pytest.fixture
def access_token(create_user):
    user = create_user(email='testuser@example.com', password='password')
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


@pytest.mark.django_db
def test_user_can_register(api_client):
    data = {
        'email': 'newuser@example.com',
        'password': 'newpassword123',
        'phone': '1234567890',
        'city': 'Test City'
    }
    response = api_client.post('/api/users/register/', data)
    assert response.status_code == status.HTTP_201_CREATED
    assert 'email' in response.data['user']


@pytest.mark.django_db
def test_user_can_login_and_access_protected_view(api_client, access_token):
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    response = api_client.get('/api/protected-resource/')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_cannot_access_protected_view_without_token(api_client):
    response = api_client.get('/api/protected-resource/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_user_cannot_login_with_wrong_password(api_client, create_user):
    create_user(email='testuser@example.com', password='password')
    data = {
        'email': 'testuser@example.com',
        'password': 'wrongpassword'
    }
    response = api_client.post('/api/users/token/', data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'detail' in response.data


@pytest.mark.django_db
def test_create_payment(api_client, create_user):
    user = create_user(email='testuser@example.com', password='password')
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    course = Course.objects.create(
        title='Test Course',
        description='Test Description',
        price=100,
        owner=user
    )
    data = {'course_id': course.id}
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = api_client.post(reverse('users:create-payment'), data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'payment_url' in response.data


    payment = Payment.objects.latest('id')
    assert payment is not None
    print(f"Stripe Session ID: {payment.stripe_session_id}")
    print(f"Stripe Payment URL: {payment.stripe_payment_url}")
