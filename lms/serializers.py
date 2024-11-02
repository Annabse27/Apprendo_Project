from rest_framework import serializers
from .models import Course, Lesson, Subscription
from users.models import Payment
from .validators import validate_youtube_url  # Импортируем валидатор
from .models import Test, Question, Answer  # УЧЕБНЫЕ ТЕСТЫ


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Lesson.
    """
    video_url = serializers.URLField(validators=[validate_youtube_url])  # Добавляем валидатор
    owner = serializers.ReadOnlyField(source='owner.id')  # Указываем owner как только для чтения

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_url', 'course', 'owner']


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'status', 'owner', 'price', 'lessons_count', 'lessons', 'is_subscribed']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=obj).exists()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'payment_date', 'paid_course', 'paid_lesson', 'amount', 'payment_method']


# УЧЕБНЫЕ ТЕСТЫ
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct', 'question', 'owner']
        extra_kwargs = {
            'owner': {'read_only': True}  # Делаем owner только для чтения
        }


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)  # Делаем поле только для чтения

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'test', 'answers', 'owner']
        extra_kwargs = {
            'owner': {'read_only': True}  # Устанавливаем только для чтения
        }


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)  # Поле только для чтения

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'course', 'questions', 'owner']
        extra_kwargs = {
            'owner': {'read_only': True}  # Только для чтения
        }
