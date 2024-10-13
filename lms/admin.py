from django.contrib import admin
from .models import Course, Lesson
from django_celery_beat.models import PeriodicTask, IntervalSchedule


admin.site.register(Course)
admin.site.register(Lesson)

def setup_periodic_tasks():
    # Настройка интервала (каждые 10 секунд)
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=10,
        period=IntervalSchedule.SECONDS,
    )

    # Создание периодической задачи
    PeriodicTask.objects.create(
        interval=schedule,
        name='Test Task',
        task='lms.tasks.sample_task',  # Путь к задаче
    )
