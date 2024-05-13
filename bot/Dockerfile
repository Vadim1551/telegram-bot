# Используем официальный базовый образ Python
FROM python:3.9-slim-buster

# Устанавливаем необходимые пакеты для работы SSH
RUN apt-get update && apt-get install -y \
    openssh-client \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы проекта в рабочую директорию контейнера
COPY . /app

# Устанавливаем зависимости проекта
RUN pip install --no-cache-dir -r requirements.txt


# Определяем переменные окружения
ENV TOKEN=""
ENV CHAT_ID=""
ENV DB_HOST=""
ENV DB_PORT=""
ENV DB_NAME=""
ENV DB_USERNAME=""
ENV DB_PASSWORD=""
ENV SSH_HOST=""
ENV SSH_USER=""
ENV SSH_PASSWORD=""
ENV SSH_PORT=""
ENV PATH_TO_LOGS=""

# Команда для запуска приложения
CMD ["python", "main.py"]
