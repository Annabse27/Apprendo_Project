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
        lessons_count (int): Количество уроков в данном курсе.
    """
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'lessons_count']

    def get_lessons_count(self, obj):
        """
        Метод для подсчёта количества уроков, связанных с курсом.

        Args:
            obj (Course): Экземпляр курса.

        Returns:
            int: Количество уроков в данном курсе.
        """
        return obj.lessons.count()


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
