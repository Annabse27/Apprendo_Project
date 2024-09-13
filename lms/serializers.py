from rest_framework import serializers
from .models import Course, Lesson
from users.models import Payment


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
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
            model = Course
            fields = ['id', 'title', 'preview', 'description', 'lessons_count', 'lessons']

    def get_lessons_count(self, obj):
        """
                Метод для подсчёта количества уроков, связанных с курсом.

                Args:
                    obj (Course): Экземпляр курса.

                Returns:
                    int: Количество уроков в данном курсе.
        """
        return obj.lessons.count()



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'payment_date', 'paid_course', 'paid_lesson', 'amount', 'payment_method']
