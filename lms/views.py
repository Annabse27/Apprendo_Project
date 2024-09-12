from rest_framework import viewsets
from .models import Course
from .serializers import CourseSerializer
from rest_framework import generics
from .models import Lesson
from .serializers import LessonSerializer

class CourseViewSet(viewsets.ModelViewSet):
    """
    Viewset для модели Course.

    Обеспечивает CRUD операции для курсов:
    - Список курсов.
    - Получение одного курса.
    - Создание нового курса.
    - Обновление курса.
    - Удаление курса.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListCreateView(generics.ListCreateAPIView):
    """
    Представление для списка уроков и создания нового урока.

    Методы:
    - GET: Возвращает список всех уроков.
    - POST: Создает новый урок.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления и удаления одного урока.

    Методы:
    - GET: Возвращает данные одного урока.
    - PUT: Полностью обновляет данные урока.
    - PATCH: Частично обновляет данные урока.
    - DELETE: Удаляет урок.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
