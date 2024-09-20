from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from lms.models import Course
from django.contrib.auth.models import Group

class ModeratorPermissionsTest(TestCase):
    def setUp(self):
        # Создаем пользователя модератора и администратора
        self.moderator = User.objects.create_user(email='moderator@example.com', password='passwordmoderator')
        self.admin = User.objects.create_superuser(email='admin@example.com', password='passwordadmin')

        # Создаем группу модераторов и добавляем пользователя
        self.moderator_group, _ = Group.objects.get_or_create(name='Модераторы')
        self.moderator.groups.add(self.moderator_group)
        self.moderator.save()

        # Устанавливаем клиент
        self.client = APIClient()

    def test_moderator_create_course_forbidden(self):
        # Аутентифицируемся как модератор
        self.client.force_authenticate(user=self.moderator)
        response = self.client.post(reverse('lms:course-list'), {
            'title': 'New Course',
            'description': 'Course description'  # Добавляем обязательное поле
        })
        self.assertEqual(response.status_code, 403)  # Модератору должно быть запрещено создавать курс

    def test_admin_create_course_success(self):
        # Аутентифицируемся как администратор
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(reverse('lms:course-list'), {
            'title': 'New Course',
            'description': 'Course description'  # Добавляем обязательное поле
        })
        self.assertEqual(response.status_code, 201)  # Администратор должен иметь возможность создать курс
