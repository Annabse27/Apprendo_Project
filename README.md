# Devoirs24Project

## Описание проекта

Проект Devoirs24Project — это Django приложение с поддержкой Celery и Redis, упакованное в Docker для удобного развёртывания. В проекте используется база данных PostgreSQL, брокер сообщений Redis и Celery для выполнения фоновых задач.

## Требования

- [Docker](https://docs.docker.com/get-docker/) (версия 20.10.0 и выше)
- [Docker Compose](https://docs.docker.com/compose/install/) (версия 1.27.0 и выше)

## Шаги для запуска проекта

### 1. Клонирование репозитория

Сначала склонируйте репозиторий на свой локальный компьютер:

```bash
git clone https://https://github.com/Annabse27/Devoirs24Project.git
cd Devoirs24Project
```

### 2. Настройка переменных окружения

Создайте файл `.env` в корне проекта (там же, где находится файл `docker-compose.yaml`), и добавьте следующие переменные:

```env
DJANGO_SECRET_KEY='ваш-секретный-ключ'
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Настройки базы данных
POSTGRES_DB=Devoirs24Project
POSTGRES_USER=postgres
POSTGRES_PASSWORD=ваш-пароль
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Настройки Redis
REDIS_URL=redis://redis:6379/0

# Настройки электронной почты (если используется)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=ваш-емейл@gmail.com
EMAIL_HOST_PASSWORD=пароль-для-емейл
```

Убедитесь, что переменные `POSTGRES_USER`, `POSTGRES_PASSWORD` и `POSTGRES_DB` совпадают с настройками, указанными в вашем Docker Compose.

### 3. Запуск проекта

Для запуска всех контейнеров (Django, PostgreSQL, Redis, Celery и Celery Beat) выполните команду:

```bash
docker-compose up -d --build
```

Параметр `--build` нужен только при первом запуске или если вы изменили конфигурацию контейнеров.

### 4. Выполнение миграций и сбор статических файлов

После того как контейнеры запустятся, выполните миграции и соберите статические файлы:

```bash
docker-compose exec app python manage.py migrate
docker-compose exec app python manage.py collectstatic --noinput
```

### 5. Доступ к проекту

После успешного выполнения миграций и сборки статических файлов, проект будет доступен по адресу:

```plaintext
http://localhost:8000
```

### 6. Команды для управления контейнерами

- Остановка контейнеров:
  ```bash
  docker-compose down
  ```

- Перезапуск контейнеров (без пересборки):
  ```bash
  docker-compose up -d
  ```

- Перезапуск контейнеров с пересборкой:
  ```bash
  docker-compose up -d --build
  ```

### 7. Работа с Celery

Celery используется для фоновых задач. В проекте два процесса: Celery Worker и Celery Beat. Они автоматически запускаются с `docker-compose up`.

Если вы хотите вручную запустить или остановить Celery:

- Запуск Celery Worker:
  ```bash
  docker-compose exec celery celery -A config worker --loglevel=info
  ```

- Запуск Celery Beat:
  ```bash
  docker-compose exec celery-beat celery -A config beat --loglevel=info
  ```

### 8. Остановка проекта

Если вы хотите остановить все контейнеры, выполните:

```bash
docker-compose down
```

Это завершит работу всех контейнеров, но сохранит данные базы данных и другие настройки.

## Структура проекта

```
Devoirs24Project/
├── config/                # Основные настройки проекта
├── lms/                   # Django-приложение
├── users/                 # Пользовательские модели и управление пользователями
├── manage.py              # Управление проектом Django
├── docker-compose.yaml    # Конфигурация Docker Compose
├── Dockerfile             # Dockerfile для сборки приложения
├── .env                   # Переменные окружения (создайте этот файл)
└── README.md              
```

## Полезные команды

- **Миграции базы данных**:
  ```bash
  docker-compose exec app python manage.py migrate
  ```

- **Создание суперпользователя**:
  ```bash
  docker-compose exec app python manage.py createsuperuser
  ```

- **Доступ к контейнеру с приложением**:
  ```bash
  docker-compose exec app sh
  ```

- **Просмотр логов**:
  ```bash
  docker-compose logs -f
  ```

## Заключение

Этот проект настроен для простого развёртывания с использованием Docker и Docker Compose. Убедитесь, что все необходимые переменные окружения правильно заданы в файле `.env` перед запуском проекта. Если у вас возникли вопросы или проблемы с запуском, обратитесь к документации Django, Docker или Celery.
