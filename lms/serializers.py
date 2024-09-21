from rest_framework import serializers
from .models import Course, Lesson, Subscription
from users.models import Payment
from .validators import validate_youtube_url  # Импортируем валидатор


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
    video_url = serializers.URLField(validators=[validate_youtube_url])  # Добавляем валидатор

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_url', 'course', 'owner']



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

    is_subscribed = serializers.SerializerMethodField()  # Поле для проверки подписки

    class Meta:
            model = Course
            fields = ['id', 'title', 'preview', 'description', 'lessons_count', 'lessons', 'is_subscribed']

    def get_lessons_count(self, obj):
        """
                Метод для подсчёта количества уроков, связанных с курсом.

                Args:
                    obj (Course): Экземпляр курса.

                Returns:
                    int: Количество уроков в данном курсе.
        """
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        # Получаем текущего пользователя из контекста запроса
        user = self.context['request'].user
        # Проверяем, есть ли подписка на этот курс у пользователя
        return Subscription.objects.filter(user=user, course=obj).exists()




class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'payment_date', 'paid_course', 'paid_lesson', 'amount', 'payment_method']
