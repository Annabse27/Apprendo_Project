from celery import shared_task
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings

from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from users.models import User


@shared_task
def sample_task():
    print(f'Периодическая задача выполнена: {datetime.now()}')


@shared_task
def send_course_update_email(course_title, emails):
    """
    Асинхронная задача для отправки email при обновлении курса.
    """
    subject = f"Обновление курса: {course_title}"
    message = f"Курс {course_title} был обновлен. Проверьте новые материалы."

    # Отправляем письмо каждому подписчику
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        emails,  # список email подписчиков
        fail_silently=False,
    )


@shared_task
def block_inactive_users():
    """
    Фоновая задача для блокировки пользователей, которые не заходили более 30 дней.
    """
    one_month_ago = timezone.now() - timedelta(days=30)

    # Находим пользователей, которые не заходили более месяца
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)

    # Деактивируем таких пользователей
    inactive_users.update(is_active=False)

    return f'Заблокировано пользователей: {inactive_users.count()}'
