from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from lms.models import Course
from django.contrib.auth.models import Group


# Тесты для модератора КУРСЫ


class ModeratorPermissionsTest(TestCase):
    def setUp(self):
        self.moderator = User.objects.create_user(email='moderator@example.com', password='passwordmoderator')
        self.teacher = User.objects.create_user(email='teacher@example.com', password='passwordteacher')

        moderator_group, _ = Group.objects.get_or_create(name='Модераторы')
        self.moderator.groups.add(moderator_group)

        self.course = Course.objects.create(title='Test Course', description='Test Description', owner=self.teacher)
        self.client = APIClient()

    def test_moderator_can_edit_course(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.patch(reverse('lms:course-detail', args=[self.course.id]), {'title': 'Updated Title'})
        self.assertEqual(response.status_code, 200)

    def test_moderator_cannot_delete_course(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(reverse('lms:course-detail', args=[self.course.id]))
        self.assertEqual(response.status_code, 403)


# Owner тесты КУРСЫ
class OwnerPermissionsTest(TestCase):
    def setUp(self):
        # Создаем пользователей
        self.user1 = User.objects.create_user(email='user1@example.com', password='password1')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password2')

        # Назначаем user1 в группу Преподавателей
        teacher_group, _ = Group.objects.get_or_create(name='Преподаватель')
        self.user1.groups.add(teacher_group)

        # Создаем курс от имени user1 с неутвержденным статусом
        self.unapproved_course = Course.objects.create(
            title="User1 Unapproved Course",
            description="Description",
            owner=self.user1,
            status="unapproved"
        )

        # Создаем курс от имени user1 с утвержденным статусом
        self.approved_course = Course.objects.create(
            title="User1 Approved Course",
            description="Approved Description",
            owner=self.user1,
            status="approved"
        )

        # Устанавливаем клиент для API
        self.client = APIClient()

    def test_teacher_can_delete_own_unapproved_course(self):

        print(f"Unapproved Course Status: {self.unapproved_course.status}, Owner: {self.unapproved_course.owner}")

        # Авторизуемся как user1, владелец неутвержденного курса
        self.client.force_authenticate(user=self.user1)

        # Пробуем удалить неутвержденный курс
        response = self.client.delete(reverse('lms:course-detail', args=[self.unapproved_course.id]))

        # Ожидаем успешное удаление с кодом 204
        self.assertEqual(response.status_code, 204)

    def test_teacher_cannot_delete_approved_course(self):
        print(f"Approved Course Status: {self.approved_course.status}, Owner: {self.approved_course.owner}")

        # Авторизуемся как user1, владелец утвержденного курса
        self.client.force_authenticate(user=self.user1)

        # Пробуем удалить утвержденный курс
        response = self.client.delete(reverse('lms:course-detail', args=[self.approved_course.id]))

        # Ожидаем отказ с кодом 403
        self.assertEqual(response.status_code, 403)

    def test_teacher_can_edit_own_unapproved_course(self):
        print(f"Unapproved Course Status: {self.unapproved_course.status}, Owner: {self.unapproved_course.owner}")

        # Авторизуемся как user1, владелец неутвержденного курса
        self.client.force_authenticate(user=self.user1)

        # Пробуем редактировать неутвержденный курс
        response = self.client.patch(reverse('lms:course-detail', args=[self.unapproved_course.id]),
                                     {'title': 'Updated Title'})

        # Ожидаем успешное редактирование с кодом 200
        self.assertEqual(response.status_code, 200)

    def test_teacher_cannot_edit_approved_course(self):
        print(f"Approved Course Status: {self.approved_course.status}, Owner: {self.approved_course.owner}")

        # Авторизуемся как user1, владелец утвержденного курса
        self.client.force_authenticate(user=self.user1)

        # Пробуем редактировать утвержденный курс
        response = self.client.patch(reverse('lms:course-detail', args=[self.approved_course.id]),
                                     {'title': 'Attempted Edit'})

        # Ожидаем отказ с кодом 403
        self.assertEqual(response.status_code, 403)


# Тесты для студентов КУРСЫ
class StudentPermissionsTest(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(email='student@example.com', password='passwordstudent')
        self.client = APIClient()

    def test_student_cannot_create_course(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.post(reverse('lms:course-list'), {'title': 'Student Course', 'description': 'Student Test Course'})
        self.assertEqual(response.status_code, 403)
