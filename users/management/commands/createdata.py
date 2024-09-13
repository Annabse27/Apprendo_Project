from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from lms.models import Course, Lesson
from users.models import Payment

class Command(BaseCommand):
    help = 'Создание тестовых данных для модели Payment'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        user = User.objects.first()
        course = Course.objects.first()
        lesson = Lesson.objects.first()

        Payment.objects.create(user=user, payment_date="2024-09-12", paid_course=course, amount=100, payment_method='cash')
        Payment.objects.create(user=user, payment_date="2024-09-12", paid_lesson=lesson, amount=50, payment_method='transfer')

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно созданы!'))
