# Используем базовый образ Python
FROM python:3.8

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