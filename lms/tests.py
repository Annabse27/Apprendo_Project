from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Course, Lesson

#Написание тестов для модели курса (Viewsets)
class CourseTests(APITestCase):

   def setUp(self):
      # Создаём курс для тестов
      self.course = Course.objects.create(
         title="Python for Beginners",
         description="Learn Python programming"
      )

   def test_create_course(self):
      """
      Тест для создания курса
      """
      url = reverse('course-list')  # маршрут для создания
      data = {'title': 'New Course', 'description': 'New course description'}
      response = self.client.post(url, data, format='json')
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)
      self.assertEqual(Course.objects.count(), 2)
      self.assertEqual(Course.objects.get(id=response.data['id']).title, 'New Course')

   def test_get_courses(self):
      """
      Тест для получения списка курсов
      """
      url = reverse('course-list')
      response = self.client.get(url, format='json')
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(len(response.data), 1)

   def test_get_course(self):
      """
      Тест для получения одного курса
      """
      url = reverse('course-detail', kwargs={'pk': self.course.id})
      response = self.client.get(url, format='json')
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(response.data['title'], 'Python for Beginners')

   def test_update_course(self):
      """
      Тест для обновления курса
      """
      url = reverse('course-detail', kwargs={'pk': self.course.id})
      data = {'title': 'Updated Course', 'description': 'Updated description'}
      response = self.client.put(url, data, format='json')
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(Course.objects.get(id=self.course.id).title, 'Updated Course')

   def test_delete_course(self):
      """
      Тест для удаления курса
      """
      url = reverse('course-detail', kwargs={'pk': self.course.id})
      response = self.client.delete(url, format='json')
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
      self.assertEqual(Course.objects.count(), 0)



#Написание тестов для модели урока (Generic-классы)
class LessonTests(APITestCase):
   def setUp(self):
      # Создаём курс и урок для тестов
      self.course = Course.objects.create(title="Python for Beginners", description="Learn Python programming")
      self.lesson = Lesson.objects.create(
         title="Lesson 1",
         description="Introduction to Python",
         video_url="https://example.com",
         course=self.course
      )


   def test_create_lesson(self):
      """
      Тест для создания урока
      """
      url = reverse('lesson-list-create')
      data = {
         'title': 'New Lesson',
         'description': 'New lesson description',
         'video_url': 'https://example.com',
         'course': self.course.id
      }
      response = self.client.post(url, data, format='json')
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)
      self.assertEqual(Lesson.objects.count(), 2)
      self.assertEqual(Lesson.objects.get(id=response.data['id']).title, 'New Lesson')


   def test_get_lessons(self):
      """
      Тест для получения списка уроков
      """
      url = reverse('lesson-list-create')
      response = self.client.get(url, format='json')
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(len(response.data), 1)


   def test_get_lesson(self):
      """
      Тест для получения одного урока
      """
      url = reverse('lesson-detail', kwargs={'pk': self.lesson.id})
      response = self.client.get(url, format='json')
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(response.data['title'], 'Lesson 1')


   def test_update_lesson(self):
      """
      Тест для обновления урока
      """
      url = reverse('lesson-detail', kwargs={'pk': self.lesson.id})
      data = {
         'title': 'Updated Lesson',
         'description': 'Updated description',
         'video_url': 'https://example.com',
         'course': self.course.id
      }
      response = self.client.put(url, data, format='json')
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(Lesson.objects.get(id=self.lesson.id).title, 'Updated Lesson')


   def test_delete_lesson(self):
      """
      Тест для удаления урока
      """
      url = reverse('lesson-detail', kwargs={'pk': self.lesson.id})
      response = self.client.delete(url, format='json')
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
      self.assertEqual(Lesson.objects.count(), 0)


