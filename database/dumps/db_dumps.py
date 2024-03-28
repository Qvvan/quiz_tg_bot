import datetime
import os
from dotenv import load_dotenv


def create_database_dump(host, port, username, password, database):
    # Формируем имя файла для дампа с текущей датой
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dump_file = f"{database}_dump_{current_datetime}.sql"

    # Устанавливаем переменную среды PGPASSWORD
    os.environ['PGPASSWORD'] = password

    os.system(
        f"pg_dump -h {host} -p {port} -U {username} -d {database} -f {dump_file}")


if __name__ == "__main__":
    load_dotenv('../../config/.env.prod')

    # Параметры подключения к базе данных
    db = {
        "database": os.environ.get('DB_NAME'),
        "user": os.environ.get('DB_USER'),
        "password": os.environ.get('DB_PASSWORD'),
        "host": os.environ.get('DB_HOST'),
        "port": os.environ.get('DB_PORT')
    }

    # Создаем дамп базы данных
    create_database_dump(db['host'], db['port'], db['user'], db['password'], db['database'])
