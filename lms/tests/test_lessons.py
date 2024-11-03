from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from lms.models import Course, Lesson
from django.contrib.auth.models import Group


# Тесты УРОКИ ВСЕ ПОЛЬЗОВАТЕЛИ/в зависимости от ролей пользователей

class LessonPermissionsTest(TestCase):
    def setUp(self):
        # Создаем пользователей: преподавателя, модератора, студента
        self.teacher = User.objects.create_user(email='teacher@example.com', password='passwordteacher')
        self.moderator = User.objects.create_user(email='moderator@example.com', password='passwordmoderator')
        self.student = User.objects.create_user(email='student@example.com', password='passwordstudent')

        # Назначаем роли пользователям
        teacher_group, _ = Group.objects.get_or_create(name='Преподаватель')
        self.teacher.groups.add(teacher_group)

        moderator_group, _ = Group.objects.get_or_create(name='Модераторы')
        self.moderator.groups.add(moderator_group)

        student_group, _ = Group.objects.get_or_create(name='Студент')
        self.student.groups.add(student_group)

        # Создаем курс для тестирования
        self.course = Course.objects.create(title='Test Course', description='Description', owner=self.teacher)

        # Создаем урок для тестирования
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Lesson Description",
            video_url="https://www.youtube.com/watch?v=abc123",
            course=self.course,
            owner=self.teacher
        )

        # Инициализируем APIClient
        self.client = APIClient()

    def test_teacher_can_create_lesson(self):
        # Аутентифицируемся как преподаватель
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(reverse('lms:lesson-list-create'), {
            'title': 'New Lesson',
            'description': 'Lesson description',
            'video_url': 'https://www.youtube.com/watch?v=abc123',
            'course': self.course.id
        })
        self.assertEqual(response.status_code, 201)  # Преподаватель может создать урок

    def test_moderator_cannot_create_lesson(self):
        # Аутентифицируемся как модератор
        self.client.force_authenticate(user=self.moderator)
        response = self.client.post(reverse('lms:lesson-list-create'), {
            'title': 'New Lesson',
            'description': 'Lesson description',
            'video_url': 'https://www.youtube.com/watch?v=abc123',
            'course': self.course.id
        })
        self.assertEqual(response.status_code, 403)  # Модератор не может создать урок

    def test_teacher_can_edit_own_lesson(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.patch(
            reverse('lms:lesson-detail', args=[self.lesson.id]),
            {'title': 'Updated Lesson'}
        )
        print(f"Response status code: {response.status_code}")  # Отладочный вывод
        print(f"Response data: {response.data}")
        self.assertEqual(response.status_code, 200)  # Преподаватель может редактировать свой урок

    def test_moderator_can_edit_lesson(self):
        # Аутентифицируемся как модератор
        self.client.force_authenticate(user=self.moderator)
        response = self.client.patch(reverse('lms:lesson-detail', args=[self.lesson.id]), {'title': 'Updated Lesson'})
        self.assertEqual(response.status_code, 200)  # Модератор может редактировать урок

    def test_student_cannot_edit_lesson(self):
        # Аутентифицируемся как студент
        self.client.force_authenticate(user=self.student)
        response = self.client.patch(reverse('lms:lesson-detail', args=[self.lesson.id]), {'title': 'Updated Lesson'})
        self.assertEqual(response.status_code, 403)  # Студент не может редактировать урок

    def test_teacher_can_delete_own_unapproved_lesson(self):
        self.client.force_authenticate(user=self.teacher)
        print(f"Lesson Status before deletion: {self.lesson.status}")
        response = self.client.delete(reverse('lms:lesson-detail', args=[self.lesson.id]))
        print(f"Response status code: {response.status_code}")  # Отладочный вывод
        self.assertEqual(response.status_code, 204)  # Преподаватель может удалить свой неутвержденный урок

    def test_moderator_cannot_delete_lesson(self):
        # Аутентифицируемся как модератор
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(reverse('lms:lesson-detail', args=[self.lesson.id]))
        self.assertEqual(response.status_code, 403)  # Модератор не может удалить урок

    def test_student_cannot_delete_lesson(self):
        # Аутентифицируемся как студент
        self.client.force_authenticate(user=self.student)
        response = self.client.delete(reverse('lms:lesson-detail', args=[self.lesson.id]))
        self.assertEqual(response.status_code, 403)  # Студент не может удалить урок
