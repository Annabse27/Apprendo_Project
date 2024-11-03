from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from lms.models import Course
from django.contrib.auth.models import Group


# Тесты на наличие корректных полей пагинации в ответе


class PaginationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='student@example.com', password='password')

        # Назначаем пользователя в группу студентов
        student_group, _ = Group.objects.get_or_create(name='Студент')
        self.user.groups.add(student_group)

        self.client.force_authenticate(user=self.user)

        # Создаем 15 утвержденных курсов
        for i in range(15):
            Course.objects.create(title=f'Курс {i + 1}', description=f'Описание курса {i + 1}', owner=self.user,
                                  status='approved')

        # Проверка количества утвержденных курсов
        print(f"Created Courses: {Course.objects.filter(status='approved').count()}")

    def test_course_pagination(self):
        response = self.client.get(reverse('lms:course-list'))

        # Отладочный вывод
        print("Response status code:", response.status_code)
        print("Response data keys:", response.data.keys())
        print("Number of courses returned:", len(response.data.get('results', [])))
        print("Response data (first page):", response.data.get('results'))

        # Проверки
        self.assertEqual(response.status_code, 200)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(len(response.data['results']), 10)  # Убедитесь, что на странице 10 курсов
