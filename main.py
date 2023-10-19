import telebot
import psycopg2
from telebot import types
import random

class QuizBot:
    def __init__(self, token, db_params):
        """
        Инициализирует объект QuizBot.

        Args:
            token (str): Токен Telegram-бота.
            db_params (dict): Параметры подключения к базе данных PostgreSQL.
        """
        self.bot = telebot.TeleBot(token)
        self.db_conn = psycopg2.connect(**db_params)

    def start(self):
        """Запускает бота и устанавливает обработчики сообщений."""
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.get_question(message)

        @self.bot.message_handler(content_types=['text'])
        def handle_answer(message):
            chat_id = message.chat.id
            now = self.get_current_question()
            if now:
                quest_id, user_id = now[1], now[2]
                quest = self.get_question_by_id(quest_id)

                if message.text == quest['answer']:
                    self.bot.send_message(chat_id, 'Правильно!')
                else:
                    self.bot.send_message(chat_id, 'Неправильно!')
                    add_wrong_question(quest_id, user_id)  # Добавляем вопрос в wrong_list
                self.delete_current_question()
                self.get_question(message)
            else:
                self.bot.send_message(chat_id, 'На сегодня вопросов больше нет.')

        def add_wrong_question(quest_id, user_id):
            """Добавляет вопрос с неправильным ответом в таблицу wrong_list.

            Args:
                quest_id (int): Идентификатор вопроса.
                user_id (int): Идентификатор пользователя.
            """
            cursor = self.db_conn.cursor()
            cursor.execute(
                f"INSERT INTO public.wrong_list(quest_id, user_id, status) VALUES ({quest_id}, {user_id}, 'YES');")
            self.db_conn.commit()

        self.bot.polling(none_stop=True)

    def get_question(self, message):
        now = self.get_current_question()
        if now:
            quest_id, user_id = now[1], now[2]
            quest = self.get_question_by_id(quest_id)
        else:
            result = self.get_unanswered_question()
            if result:
                quest_id, user_id = result[1], result[2]
                self.update_question_status(quest_id, user_id)
                self.insert_current_question(quest_id, user_id)
                quest = self.get_question_by_id(quest_id)
            else:
                self.bot.send_message(message.chat.id, 'На сегодня вопросов больше нет.')
                return

        # Перемешиваем варианты ответов
        options = quest['wrong'] + [quest['answer']]
        print(quest['answer'])
        random.shuffle(options)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for option in options:
            markup.add(option)
        self.bot.send_message(message.chat.id, quest['question'], reply_markup=markup)

    def get_current_question(self):
        """Получает текущий вопрос из базы данных.

        Returns:
            tuple: Кортеж с информацией о текущем вопросе.
        """
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM public.now LIMIT 1")
        return cursor.fetchone()

    def get_question_by_id(self, quest_id):
        """Получает вопрос по идентификатору из базы данных.

        Args:
            quest_id (int): Идентификатор вопроса.

        Returns:
            dict: Словарь с информацией о вопросе.
        """
        cursor = self.db_conn.cursor()
        cursor.execute(f"SELECT question FROM public.question WHERE id = {quest_id}")
        return cursor.fetchone()[0]

    def get_unanswered_question(self):
        """Получает следующий неотвеченный вопрос из базы данных.

        Returns:
            tuple: Кортеж с информацией о следующем вопросе для ответа.
        """
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM public.user_question WHERE status = 'NO' ORDER BY quest_id LIMIT 1;")
        return cursor.fetchone()

    def update_question_status(self, quest_id, user_id):
        """Обновляет статус вопроса на 'YES' после ответа пользователя.

        Args:
            quest_id (int): Идентификатор вопроса.
            user_id (int): Идентификатор пользователя.
        """
        cursor = self.db_conn.cursor()
        cursor.execute(f"UPDATE public.user_question SET status='YES' WHERE quest_id = {quest_id} and user_id = {user_id};")
        self.db_conn.commit()

    def insert_current_question(self, quest_id, user_id):
        """Вставляет текущий вопрос в таблицу 'now'.

        Args:
            quest_id (int): Идентификатор вопроса.
            user_id (int): Идентификатор пользователя.
        """
        cursor = self.db_conn.cursor()
        cursor.execute(f"INSERT INTO public.now(quest_id, user_id) VALUES ({quest_id}, {user_id});")
        self.db_conn.commit()

    def delete_current_question(self):
        """Удаляет текущий вопрос из таблицы 'now'."""
        now = self.get_current_question()
        if now:
            quest_id, user_id = now[1], now[2]
            cursor = self.db_conn.cursor()
            cursor.execute(f"DELETE FROM public.now WHERE quest_id = {quest_id} and user_id = {user_id};")
            self.db_conn.commit()

    def get_user_tg_id(self, user_id):
        """Получает идентификатор Telegram пользователя из базы данных.

        Args:
            user_id (int): Идентификатор пользователя.

        Returns:
            int: Идентификатор Telegram пользователя.
        """
        cursor = self.db_conn.cursor()
        cursor.execute(f"SELECT tg_id FROM public.user WHERE id = {user_id}")
        return cursor.fetchone()

if __name__ == "__main__":
    token = '5278804872:AAHKD4HyQhwt9FBMb_GpX005_fwdva1A3qs'
    db_params = {
        "database": "tg",
        "user": "postgres",
        "password": "123",
        "host": "localhost",
        "port": '5432'
    }
    quiz_bot = QuizBot(token, db_params)
    quiz_bot.start()
