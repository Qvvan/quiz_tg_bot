# Используем базовый образ Python
FROM python:3.8

# Добавляем ключ репозитория PostgreSQL и сам репозиторий
RUN apt-get update && apt-get install -y wget gnupg
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ bookworm-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'

# Устанавливаем PostgreSQL клиентские утилиты с версией 16
RUN apt-get update && apt-get install -y postgresql-client-16

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы из текущей директории в контейнер
COPY . .

# Добавляем пути к папкам с модулями и файлами конфигурации в переменную окружения PYTHONPATH
ENV PYTHONPATH=/app

WORKDIR /app/bot


# Команда для запуска скрипта (ваш скрипт должен быть заменён на app.py)
CMD ["python", "main.py"]