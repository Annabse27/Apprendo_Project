from celery import shared_task
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings


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

