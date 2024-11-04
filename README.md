# Apprendo Project

## Описание проекта

**Apprendo** - это образовательная платформа, предоставляющая пользователям возможность создавать, подписываться и управлять курсами. Система поддерживает многопользовательские роли, такие как преподаватели, студенты и модераторы, и включает в себя функции рассылки уведомлений и асинхронных задач с использованием Celery и Redis.

## Функциональные возможности

- Регистрация и управление пользователями с различными ролями (Администратор, Преподаватель, Студент, Модератор).
- Создание, управление и подписка на курсы.
- Периодические задачи с использованием Celery (например, отправка уведомлений, блокировка неактивных пользователей).
- Асинхронные операции через Redis.
- Поддержка PostgreSQL для хранения данных.

## Установка и запуск

### Локальная установка

1. Убедитесь, что Python 3.12 установлен.
2. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/Annabse27/Apprendo_Project
   cd Apprendo Project
   ```
Проект использует **Poetry** для управления зависимостями. Убедитесь, что Poetry установлен, затем выполните:

```bash
poetry install
```

4. Настройте переменные окружения.
Скопируйте .env.example и заполните его необходимыми данными

5. Примените миграции:
   ```bash
   python manage.py migrate
   ```
6. Запустите сервер разработки:
   ```bash
   python manage.py runserver
   ```

### Запуск в Docker

1. Убедитесь, что Docker и Docker Compose установлены.
2. Запустите контейнеры:
   ```bash
   docker-compose up --build
   ```
3. Для запуска тестов с покрытием:
   ```bash
   docker-compose run tests
   ```

## Использование

### Регистрация и вход

- Зарегистрируйтесь или войдите в систему через интерфейс или с использованием API.

### Управление курсами

- преподаватели: создавайте курсы, добавляйте уроки
- студенты: подписывайтесь на курсы, проходите учебные тесты

### Асинхронные задачи

- Периодические задачи, такие как рассылка уведомлений, автоматически обрабатываются Celery.

## Тестирование

1. Для запуска тестов локально:
   ```bash
   pytest --cov=. --cov-report=html
   ```
2. В Docker:
   ```bash
   docker-compose run tests
   ```

## Развертывание

Для развертывания на сервере убедитесь, что все переменные окружения настроены, и используйте Docker Compose для запуска всех сервисов.

## Документация

- **Установка**: Инструкции по установке и запуску проекта локально и в Docker.
- **Использование**: Описание основных функций приложения.
- **API Документация**: Встроенная документация доступна по адресу `/api/docs/` после запуска сервера.

## Контакты

Для вопросов и предложений, пожалуйста, напишите по адресу annabse27@gmail.com.

```

Этот `README.md` предоставляет инструкции по установке, запуску, использованию и тестированию проекта. Вы можете адаптировать его под свои конкретные требования.
