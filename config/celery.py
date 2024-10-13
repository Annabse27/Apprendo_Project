import os
from celery import Celery

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создаем объект Celery
app = Celery('config')

# Загружаем настройки Celery из переменных окружения
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем задачи из всех зарегистрированных приложений
app.autodiscover_tasks()


