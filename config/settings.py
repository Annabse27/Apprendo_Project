from pathlib import Path
from decouple import config
from datetime import timedelta
from dotenv import load_dotenv
import os

if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    raise RuntimeError("DJANGO_SETTINGS_MODULE is not set. Please check your configuration.")

# Загружаем переменные окружения
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ
SECRET_KEY = config('SECRET_KEY')

# Секретный ключ для Stripe
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='sk_test_default_key')

DEBUG = True
ALLOWED_HOSTS = []

# Пользовательская модель пользователя
AUTH_USER_MODEL = 'users.User'

# Приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    'rest_framework',
    'django_filters',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'django_celery_beat',  # Celery Beat
    'nested_admin',
    'users',
    'lms',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'lms.paginators.CustomPageNumberPagination',
    'PAGE_SIZE': 10,  # Устанавливаем размер страницы по умолчанию

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB', default='apprendo_db'),
        'USER': config('POSTGRES_USER', default='user'),
        'PASSWORD': config('POSTGRES_PASSWORD', default='password'),
        'HOST': config('POSTGRES_HOST', default='localhost'),
        'PORT': config('POSTGRES_PORT', default='5432'),
    }
}

# Валидаторы паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Интернационализация
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True

# Статика
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки Redis для Celery
#CELERY_BROKER_URL = config('CELERY_BROKER_URL')
CELERY_BROKER_URL = f'redis://{config("REDIS_HOST", default="redis")}:{config("REDIS_PORT", default="6379")}/0'
CELERY_RESULT_BACKEND = f'redis://{config("REDIS_HOST", default="redis")}:{config("REDIS_PORT", default="6379")}/0'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Paris'

CELERY_BEAT_SCHEDULE = {
    'block-inactive-users-every-day': {
        'task': 'users.tasks.block_inactive_users',
        'schedule': timedelta(days=1),
        'options': {'timezone': 'Europe/Paris'},
    },
}

# Настройки для отправки email через SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@yourdomain.com')

# `access`-токен будет действовать 30 минут, а `refresh`-токен — 7 дней
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

CORS_ALLOW_ALL_ORIGINS = True # или указать конкретные допустимые домены (React, Vue, или другое) порт три тысячи/ домен продакшена
CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
]

SPECTACULAR_SETTINGS = {
    'TITLE': 'Approndo API',
    'DESCRIPTION': 'API Documentation for Approndo',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
    },
    'SECURITY': [{'Bearer': []}],  # только эта схема
}
