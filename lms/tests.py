from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from lms.models import Course, Lesson, Subscription
from django.contrib.auth.models import Group

# Импорты для валидатора
from django.core.exceptions import ValidationError
from lms.validators import validate_youtube_url


class ModeratorPermissionsTest(TestCase):
    def setUp(self):
        # Создаем пользователя модератора и администратора
        self.moderator = User.objects.create_user(email='moderator@example.com', password='passwordmoderator')
        self.admin = User.objects.create_superuser(email='admin@example.com', password='passwordadmin')

        # Создаем группу модераторов и добавляем пользователя
        self.moderator_group, _ = Group.objects.get_or_create(name='Модераторы')
        self.moderator.groups.add(self.moderator_group)
        self.moderator.save()

        # Создаем курс для тестов
        self.course = Course.objects.create(title='Test Course', description='Description', owner=self.admin)

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

    def test_moderator_delete_course_forbidden(self):
        # Аутентифицируемся как модератор
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(reverse('lms:course-detail', args=[self.course.id]))
        self.assertEqual(response.status_code, 403)  # Модератору должно быть запрещено удалять курс

    def test_admin_create_course_success(self):
        # Аутентифицируемся как администратор
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(reverse('lms:course-list'), {
            'title': 'New Course',
            'description': 'Course description'  # Добавляем обязательное поле
        })
        self.assertEqual(response.status_code, 201)  # Администратор должен иметь возможность создать курс

    def test_admin_delete_course_success(self):
        # Аутентифицируемся как администратор
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(reverse('lms:course-detail', args=[self.course.id]))
        self.assertEqual(response.status_code, 204)  # Администратор должен иметь возможность удалить курс



#Тесты на фильтрацию курсов и уроков для обычных пользователей
class CourseFilterTest(TestCase):
    def setUp(self):
        # Создаем двух пользователей
        self.user1 = User.objects.create_user(email='user1@example.com', password='password1')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password2')

        # Создаем курс от имени user1 и user2
        self.course1 = Course.objects.create(title='User1 Course', description='Description', owner=self.user1)
        self.course2 = Course.objects.create(title='User2 Course', description='Description', owner=self.user2)

        # Устанавливаем клиент для API
        self.client = APIClient()

    def test_user1_can_see_only_own_courses(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse('lms:course-list'))
        self.assertEqual(response.status_code, 200)
        # Убедитесь, что возвращается только курс user1
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'User1 Course')

    def test_user2_can_see_only_own_courses(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(reverse('lms:course-list'))
        self.assertEqual(response.status_code, 200)
        # Убедитесь, что возвращается только курс user2
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'User2 Course')



#Owner Тесты
class OwnerPermissionsTest(TestCase):
    def setUp(self):
        # Создаем двух пользователей
        self.user1 = User.objects.create_user(email='user1@example.com', password='password1')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password2')

        # Создаем курс от имени user1
        self.course = Course.objects.create(title='User1 Course', description='Description', owner=self.user1)

        # Устанавливаем клиент для API
        self.client = APIClient()

    def test_owner_can_edit_own_course(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(reverse('lms:course-detail', args=[self.course.id]), {'title': 'Updated Title'})
        self.assertEqual(response.status_code, 200)

    #Злобный тест
    def test_non_owner_cannot_edit_course(self):
        # Авторизуем пользователя, который НЕ является владельцем и НЕ является модератором
        self.client.force_authenticate(user=self.user2)

        # Проверяем, что курс существует в базе данных
        course_exists = Course.objects.filter(id=self.course.id).exists()
        print(f"Course exists in the database: {course_exists}")
        self.assertTrue(course_exists)

        # Проверяем данные курса
        course = Course.objects.get(id=self.course.id)
        print(f"Course ID: {course.id}, Owner: {course.owner.email}, Title: {course.title}")

        # Пытаемся изменить курс, который принадлежит другому пользователю (user1)
        response = self.client.patch(reverse('lms:course-detail', args=[self.course.id]), {'title': 'New title'})

        # Выводим статус и тело ответа для отладки
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.content}")

        # Ожидаем статус 403 Forbidden
        self.assertEqual(response.status_code, 403)

    def test_owner_can_delete_own_course(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(reverse('lms:course-detail', args=[self.course.id]))
        self.assertEqual(response.status_code, 204)  # Владелец должен иметь возможность удалить свой курс

    def test_non_owner_cannot_delete_course(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(reverse('lms:course-detail', args=[self.course.id]))
        self.assertEqual(response.status_code, 403)  # Другой пользователь не может удалить чужой курс


# Тесты для проверки валидатора
class ValidatorTest(TestCase):

    def test_valid_youtube_url(self):
        # Проверяем валидную ссылку на YouTube
        valid_url = 'https://www.youtube.com/watch?v=abc123'
        try:
            validate_youtube_url(valid_url)
        except ValidationError:
            self.fail("Валидная ссылка YouTube вызвала ValidationError.")

    def test_invalid_url(self):
        # Проверяем невалидную ссылку (не YouTube)
        invalid_url = 'https://www.example.com'
        with self.assertRaises(ValidationError):
            validate_youtube_url(invalid_url)

    def test_shortened_youtube_url(self):
        # Проверяем валидную сокращённую ссылку на YouTube
        valid_url = 'https://youtu.be/abc123'
        try:
            validate_youtube_url(valid_url)
        except ValidationError:
            self.fail("Валидная сокращённая ссылка YouTube вызвала ValidationError.")



#Тесты на права модератора при работе с уроками
class LessonModeratorPermissionsTest(TestCase):
    def setUp(self):
        # Создаем пользователя модератора и владельца
        self.moderator = User.objects.create_user(email='moderator@example.com', password='passwordmoderator')
        self.owner = User.objects.create_user(email='owner@example.com', password='passwordowner')

        # Создаем группу модераторов и добавляем пользователя
        self.moderator_group, _ = Group.objects.get_or_create(name='Модераторы')
        self.moderator.groups.add(self.moderator_group)

        # Создаем курс и урок для тестов
        self.course = Course.objects.create(title='Test Course', description='Description', owner=self.owner)
        self.lesson = Lesson.objects.create(title='Test Lesson', description='Lesson Description', owner=self.owner, course=self.course)

        # Устанавливаем клиент
        self.client = APIClient()

    def test_moderator_cannot_delete_lesson(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(reverse('lms:lesson-detail', args=[self.lesson.id]))
        self.assertEqual(response.status_code, 403)  # Модератору должно быть запрещено удалять урок

    def test_moderator_can_edit_lesson(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.patch(reverse('lms:lesson-detail', args=[self.lesson.id]), {'title': 'Updated Title'})
        self.assertEqual(response.status_code, 200)  # Модератор может редактировать урок



# Tесты для API подписок
class SubscriptionTest(TestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(email='user@example.com', password='password')

        # Создаем курс от имени пользователя
        self.course = Course.objects.create(title='Курс 1', description='Описание курса', owner=self.user)

        # Устанавливаем клиент для API
        self.client = APIClient()


    def test_subscribe_and_unsubscribe(self):
        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

        # Подписка на курс
        response = self.client.post(reverse('lms:course-subscription'), {'course_id': self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Подписка добавлена')

        # Проверяем, что подписка существует
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # Отписка от курса
        response = self.client.post(reverse('lms:course-subscription'), {'course_id': self.course.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Подписка удалена')

        # Проверяем, что подписка удалена
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())


# Тесты на наличие корректных полей пагинации в ответе
class PaginationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='user@example.com', password='password')
        self.client.force_authenticate(user=self.user)

        # Создаем несколько курсов
        for i in range(15):
            Course.objects.create(title=f'Курс {i+1}', description=f'Описание курса {i+1}', owner=self.user)

    def test_course_pagination(self):
        # Проверяем первый запрос с пагинацией по умолчанию
        response = self.client.get(reverse('lms:course-list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(len(response.data['results']), 10)  # Убедитесь, что на странице 10 курсов
