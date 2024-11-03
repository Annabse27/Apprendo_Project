from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from lms.models import Course, Subscription


# Tесты для API подписок
class SubscriptionTest(TestCase):
    def setUp(self):
        # Создаем пользователя и курс для тестов
        self.user = User.objects.create_user(email='user@example.com', password='password')
        self.course = Course.objects.create(
            title='Курс 1',
            description='Описание курса',
            owner=self.user,
            status='approved'
        )

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

    def test_create_subscription(self):
        # Проверка успешного создания подписки через модель
        subscription = Subscription.objects.create(user=self.user, course=self.course)
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.course, self.course)
        self.assertIsNotNone(subscription.created_at)

    def test_subscription_uniqueness(self):
        # Проверка уникальности подписки
        Subscription.objects.create(user=self.user, course=self.course)
        with self.assertRaises(Exception):
            Subscription.objects.create(user=self.user, course=self.course)

    def test_subscription_deletion(self):
        # Проверка корректного удаления подписки через модель
        subscription = Subscription.objects.create(user=self.user, course=self.course)
        subscription_id = subscription.id
        subscription.delete()
        self.assertFalse(Subscription.objects.filter(id=subscription_id).exists())
