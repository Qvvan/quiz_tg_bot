FROM python:3.11.4-slim-buster

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /bot

# Устанавливаем переменные среды Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy entrypoint.dev.sh
COPY entrypoint.sh .
RUN sed -i 's/\r$//g' /bot/entrypoint.sh
RUN chmod +x /bot/entrypoint.sh

COPY . .

# run entrypoint.dev.sh
ENTRYPOINT ["/bot/entrypoint.sh"]