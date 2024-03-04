import psycopg2


class DatabaseHandler:
    def __init__(self, db_params):
        self.db_params = db_params
        self.db_conn = None

    def connect(self):
        """Установка соединения с базой данных."""
        self.db_conn = psycopg2.connect(**self.db_params)

    def close_connection(self):
        """Закрытие соединения с базой данных."""
        if self.db_conn is not None:
            self.db_conn.close()
            self.db_conn = None

    def execute_query(self, query, values=None):
        """Выполнение SQL-запроса.

        Args:
            query (str): SQL-запрос.
            args: Параметры для подстановки в запрос.

        Returns:
            psycopg2.extensions.cursor: Объект курсора для работы с результатами запроса.
        """
        cursor = self.db_conn.cursor()
        cursor.execute(query, values)
        return cursor
