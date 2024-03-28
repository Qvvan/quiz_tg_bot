class UserManager:
    """Класс для управления пользователями бота."""

    def __init__(self, db_handler, bot):
        self.db_handler = db_handler
        self.bot = bot

    def is_user_exists(self, tg_id):
        """Проверка существования пользователя в базе данных.

        Args:
            tg_id: Идентификатор чата пользователя.

        Returns:
            bool: True, если пользователь существует, False в противном случае.
        """
        cursor = self.db_handler.execute_query(f"SELECT COUNT(*) FROM public.user WHERE tg_id = '{tg_id}'")
        count = cursor.fetchone()[0]
        return count > 0

    def add_user(self, tg_id, name):
        """Добавление нового пользователя в базу данных.

        Args:
            tg_id: Идентификатор чата пользователя.
            name (str): Имя пользователя.

        Returns:
            bool: True, если пользователь успешно добавлен, False в противном случае.
        """
        try:
            self.db_handler.execute_query(f"INSERT INTO public.user(name, tg_id) VALUES ('{name}', '{tg_id}')")
            self.db_handler.db_conn.commit()
            self.bot.send_message(323993202, f'Зарегистрирован: {name}')
            return True
        except Exception as e:
            self.bot.send_message(323993202, f"Ошибка работы с базой данных: {e}")
            self.db_handler.db_conn.rollback()
            return False

    def delete_user(self, tg_id):
        """Удаление пользователя из базы данных.

        Args:
            tg_id: Идентификатор чата пользователя.
        """
        cursor = self.db_handler.execute_query(f"DELETE FROM public.now WHERE tg_id = {tg_id};")
        cursor.execute(f"DELETE FROM public.user WHERE tg_id = '{tg_id}';")
        cursor.execute(f"DELETE FROM public.user_question WHERE tg_id = {tg_id};")
        cursor.execute(f"DELETE FROM public.wrong_list WHERE tg_id = {tg_id};")
        self.db_handler.db_conn.commit()
        self.bot.send_message(323993202, 'Пользователь успешно удален!')
