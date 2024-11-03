from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from lms.models import Course

from lms.models import Test, Question, Answer
from rest_framework import status
from django.contrib.auth.models import Group


# ТЕСТЫ ДЛЯ УЧЕБНЫХ ТЕСТОВ


class TestViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Создаем user1 и добавляем в группу 'Преподаватель'
        self.user1 = User.objects.create_user(email="user1@example.com", password="password")
        teacher_group, _ = Group.objects.get_or_create(name='Преподаватель')
        self.user1.groups.add(teacher_group)

        # Создаем user2 и добавляем в группу 'Студент'
        self.user2 = User.objects.create_user(email="user2@example.com", password="password")
        student_group, _ = Group.objects.get_or_create(name='Студент')
        self.user2.groups.add(student_group)

        # Аутентификация под user1
        self.client.force_authenticate(user=self.user1)

        # Создаем курс
        self.course = Course.objects.create(title="Sample Course", description="Course Description", owner=self.user1)

    def test_create_test(self):
        data = {'title': 'Test Title', 'description': 'Test Description', 'course': self.course.id}
        print("Отправка POST запроса для создания теста с данными:", data)
        response = self.client.post(reverse('lms:test-list'), data)
        print("Код статуса ответа:", response.status_code)
        print("Данные ответа:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Test.objects.count(), 1)
        self.assertEqual(Test.objects.first().owner, self.user1)

    def test_view_test(self):
        # Создание теста
        response = self.client.post(reverse('lms:test-list'), {
            'title': 'Test Title',
            'description': 'Test Description',
            'course': self.course.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        test_id = response.data['id']

        # Проверка URL и данных теста
        url = reverse('lms:test-detail', args=[test_id])
        print(f"Generated URL: {url}")

        # Проверка доступа к тесту для user1
        response = self.client.get(url)
        print(f"Response status for user1: {response.status_code}, Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка содержания данных
        expected_data = {
            'id': test_id,
            'title': 'Test Title',
            'description': 'Test Description',
            'course': self.course.id,
            'questions': [],
            'owner': self.user1.id
        }
        self.assertEqual(response.data, expected_data, "Response data does not match expected data")

        # Проверка отказа в доступе для user2
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(url)
        print(f"Response status for user2: {response.status_code}, Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_edit_test(self):
        test = Test.objects.create(title="Test Title", description="Test Description", course=self.course,
                                   owner=self.user1)
        self.assertTrue(Test.objects.filter(id=test.id).exists(), "Test should exist before editing.")

        response = self.client.patch(reverse('lms:test-detail', args=[test.id]), {'title': 'Updated Title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Test.objects.get(id=test.id).title, 'Updated Title')

        print(f"Attempting to edit Test with ID: {test.id}")
        response = self.client.patch(reverse('lms:test-detail', args=[test.id]), {'title': 'Updated Title'})
        print(f"Edit response status code: {response.status_code}, response data: {response.data}")


    def test_delete_test(self):
        test = Test.objects.create(title="Test Title", description="Test Description", course=self.course,
                                   owner=self.user1)
        self.assertTrue(Test.objects.filter(id=test.id).exists(), "Test should exist before deletion.")

        response = self.client.delete(reverse('lms:test-detail', args=[test.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Test.objects.filter(id=test.id).exists(), "Test should be deleted.")

        print(f"Attempting to delete Test with ID: {test.id}")
        response = self.client.delete(reverse('lms:test-detail', args=[test.id]))
        print(f"Delete response status code: {response.status_code}, response data: {response.data}")


class QuestionViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(email="user1@example.com", password="password")
        self.user2 = User.objects.create_user(email="user2@example.com", password="password")
        self.client.force_authenticate(user=self.user1)

        # Создаем курс и тест
        self.course = Course.objects.create(title="Sample Course", description="Course Description", owner=self.user1)
        self.test = Test.objects.create(title="Test Title", description="Test Description", course=self.course,
                                        owner=self.user1)
        # Добавляем отладочные выводы URL
        print("Test list URL:", reverse('lms:test-list'))
        print("Question list URL:", reverse('lms:question-list'))
        print("Answer list URL:", reverse('lms:answer-list'))

    def test_create_question(self):
        data = {'text': 'Sample Question', 'test': self.test.id, 'question_type': 'multiple_choice'}
        print("Отправка POST запроса для создания вопроса с данными:", data)
        response = self.client.post(reverse('lms:question-list'), data)
        print("Код статуса ответа:", response.status_code)
        print("Данные ответа:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Question.objects.first().owner, self.user1)

    def test_edit_question(self):
        # Создаем вопрос
        question = Question.objects.create(text="Original Question", test=self.test, owner=self.user1)
        print(f"Созданный вопрос: {question}, ID: {question.id}")  # Отладочный вывод

        # Пытаемся отредактировать вопрос
        response = self.client.patch(reverse('lms:question-detail', args=[question.id]), {'text': 'Updated Question'})
        print(
            f"Ответ на запрос PATCH для обновления вопроса: статус {response.status_code}, данные ответа: {response.data}")  # Отладка

        # Проверяем, что обновление прошло успешно
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Question.objects.get(id=question.id).text, 'Updated Question')

        # Проверка на отказ в доступе для другого пользователя
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(reverse('lms:question-detail', args=[question.id]), {'text': 'Another Question'})
        print(
            f"Ответ на запрос PATCH от другого пользователя: статус {response.status_code}, данные ответа: {response.data}")  # Отладка
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_question(self):
        question = Question.objects.create(text="Sample Question", test=self.test, owner=self.user1)
        print(f"Created question: {question}, ID: {question.id}")  # Отладка

        response = self.client.delete(reverse('lms:question-detail', args=[question.id]))
        print(f"Delete response status code: {response.status_code}, response data: {response.data}")  # Отладка

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Question.objects.count(), 0)


class AnswerViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(email="user1@example.com", password="password")
        self.user2 = User.objects.create_user(email="user2@example.com", password="password")  # добавляем user2
        self.client.force_authenticate(user=self.user1)

        # Создаем курс, тест и вопрос с указанием owner
        self.course = Course.objects.create(title="Sample Course", description="Course Description", owner=self.user1)
        self.test = Test.objects.create(title="Test Title", description="Test Description", course=self.course,
                                        owner=self.user1)

        # Указываем `owner` при создании вопроса
        self.question = Question.objects.create(
            text="Sample Question", test=self.test, question_type="multiple_choice", owner=self.user1
        )

    def test_create_answer(self):
        print("Answer list URL:", reverse('lms:answer-list'))
        response = self.client.post(reverse('lms:answer-list'), {
            'text': 'Sample Answer',
            'question': self.question.id,  # Проверьте, что `self.question` определена корректно
            'is_correct': True
        })
        print("Response status code:", response.status_code)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Answer.objects.count(), 1)
        self.assertEqual(Answer.objects.first().question, self.question)

    def test_edit_answer(self):
        # Создаем ответ и указываем владельца
        answer = Answer.objects.create(
            text="Original Answer",
            question=self.question,
            is_correct=False,
            owner=self.user1  # Указываем владельца вручную
        )

        # Выполняем изменение от имени user1
        response = self.client.patch(reverse('lms:answer-detail', args=[answer.id]), {'text': 'Updated Answer'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Answer.objects.get(id=answer.id).text, 'Updated Answer')

        # Проверяем, что другой пользователь (user2) не может редактировать ответ
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(reverse('lms:answer-detail', args=[answer.id]), {'text': 'Another Answer'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_answer(self):
        answer = Answer.objects.create(
            text="Sample Answer",
            question=self.question,
            is_correct=True,
            owner=self.user1  # Указываем владельца вручную
        )

        response = self.client.delete(reverse('lms:answer-detail', args=[answer.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Answer.objects.count(), 0)
