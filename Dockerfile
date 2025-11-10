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

# Копируем файлы проекта
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости через Poetry без установки текущего проекта
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY app ./app

EXPOSE 5000

CMD ["python", "-m", "app.main"]
