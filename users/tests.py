from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

# Импорты для тестирования платежей
from django.urls import reverse
from django.contrib.auth.models import User
from lms.models import Course
from .models import Payment


User = get_user_model()


class UserAuthTests(APITestCase):

    def setUp(self):
        # Создаем пользователя для тестов авторизации
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='password'
        )

        # Получаем JWT токен для пользователя
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_user_can_register(self):
        """
        Тест на регистрацию нового пользователя
        """
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'phone': '1234567890',
            'city': 'Test City'
        }

        # Отправляем POST-запрос на регистрацию
        response = self.client.post('/api/users/register/', data)

        # Проверяем, что регистрация успешна
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('email', response.data['user'])

        # Проверяем, что пользователь действительно создан
        user = User.objects.get(email='newuser@example.com')
        self.assertIsNotNone(user)

        # Проверяем, что пароль был захеширован
        self.assertTrue(user.check_password('newpassword123'))

    def test_user_can_login_and_access_protected_view(self):
        """
        Тест на авторизацию и доступ к защищённому ресурсу
        """
        # Передаем токен в заголовок
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Выполняем GET-запрос к защищенному ресурсу
        response = self.client.get('/api/protected-resource/')

        # Проверяем, что доступ разрешен (HTTP 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_access_protected_view_without_token(self):
        """
        Тест на проверку доступа к защищённому ресурсу без токена
        """
        # Выполняем GET-запрос к защищенному ресурсу без токена
        response = self.client.get('/api/protected-resource/')

        # Проверяем, что доступ запрещен (HTTP 401)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cannot_login_with_wrong_password(self):
        """
        Тест на проверку логина с неверным паролем
        """
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }

        # Отправляем POST-запрос на получение токена с неправильным паролем
        response = self.client.post('/api/users/token/', data)

        # Проверяем, что доступ запрещен (HTTP 401)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)


class PaymentTestCase(APITestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(email='testuser@example.com', password='password')

        # Генерируем JWT токен для пользователя
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        # Создаем тестовый курс
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            price=100,
            owner=self.user
        )

    def test_create_payment(self):
        data = {'course_id': self.course.id}

        # Отправляем POST запрос с JWT токеном в заголовке
        response = self.client.post(
            reverse('users:create-payment'),
            data,
            format='json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}'  # Передаем JWT токен в заголовке
        )

        # Проверяем, что статус ответа 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что в ответе есть поле 'payment_url'
        self.assertIn('payment_url', response.data)

        # Проверяем, что объект Payment был создан
        payment = Payment.objects.latest('id')  # Получаем последний созданный платеж
        self.assertIsNotNone(payment)  # Убеждаемся, что объект не пустой

        # Выводим информацию о session_id и payment_url
        print(f"Stripe Session ID: {payment.stripe_session_id}")
        print(f"Length of Stripe Session ID: {len(payment.stripe_session_id)}")

        print(f"Stripe Payment URL: {payment.stripe_payment_url}")
        print(f"Length of Stripe Payment URL: {len(payment.stripe_payment_url)}")
