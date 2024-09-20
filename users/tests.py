from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

User = get_user_model()


class UserAuthTests(APITestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(
            email='testuser@example.com',
            #username='testuser',
            password='password'
        )

        # Получаем JWT токен для пользователя
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_user_can_login_and_access_protected_view(self):
        # Передаем токен в заголовок
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Выполняем GET-запрос к защищенному ресурсу
        response = self.client.get('/api/protected-resource/')

        # Проверяем, что доступ разрешен (HTTP 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
