from rest_framework import serializers
from .models import Course, Lesson

class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Course.

    Поля:
        id (int): Уникальный идентификатор курса.
        title (str): Название курса.
        preview (str): Путь к изображению превью курса.
        description (str): Описание курса.
    """
    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description']


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Lesson.

    Поля:
        id (int): Уникальный идентификатор урока.
        title (str): Название урока.
        description (str): Описание урока.
        preview (str): Путь к изображению превью урока.
        video_url (str): URL-адрес видеоурока.
        course (int): Идентификатор курса, к которому относится урок.
    """
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_url', 'course']
