   # Используем официальный образ Python
   FROM python:3.12-slim

   # Устанавливаем рабочую директорию
   WORKDIR /app

   # Устанавливаем зависимости для PostgreSQL и сборки
   RUN apt-get update && apt-get install -y libpq-dev gcc

   # Копируем pyproject.toml и poetry.lock для установки зависимостей
   COPY pyproject.toml poetry.lock /app/

   # Устанавливаем Poetry
   RUN pip install poetry

   # Устанавливаем зависимости без разработки
   RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

   # Копируем все файлы проекта в контейнер
   COPY . .

