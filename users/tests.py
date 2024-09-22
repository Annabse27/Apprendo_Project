from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


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
