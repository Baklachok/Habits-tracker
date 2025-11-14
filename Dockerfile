FROM python:3.12-slim

# Устанавливаем зависимости для mysqlclient и curl для Poetry
RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Копируем только файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости через Poetry без установки текущего проекта
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копируем весь проект
COPY app ./app

# Устанавливаем переменные среды для Flask
ENV FLASK_APP=app.main
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

# Запуск с autoreload
CMD ["flask", "run", "--reload"]
