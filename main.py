import telebot
import psycopg2
from telebot import types
import random
import schedule
import time
import threading

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
        self.id = 323993202

    def start(self):
        """Запускает бота и устанавливает обработчики сообщений."""
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            name = message.chat.first_name
            chat_id = message.chat.id
            if self.is_user_exists(chat_id):
                self.bot.send_message(chat_id, f'Вы уже зарегистрированы!\n{name}')
            elif self.add_user(chat_id, name):
                if self.add_new_user_questions(chat_id):
                    self.bot.send_message(chat_id, f'Вы успешно зарегистрировались, {name}!\nНачинаем же!')
                    self.get_question()
                else:
                    self.bot.send_message(chat_id, 'Что-то пошло не так, попробуйте позже')

        @self.bot.message_handler(content_types=['text'])
        def handle_answer(message):
            chat_id = message.chat.id
            if not self.is_user_exists(chat_id):
                self.bot.send_message(chat_id, 'Нажмите /start, чтобы начать')
                return
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
                self.get_question()
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


    def is_user_exists(self, chat_id):
        """Проверяет наличие пользователя в базе данных по chat_id.

        Args:
            chat_id (int): Идентификатор чата пользователя.

        Returns:
            bool: True, если пользователь с указанным chat_id существует, иначе False.
        """
        cursor = self.db_conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM public.user WHERE tg_id = '{chat_id}'")
        count = cursor.fetchone()[0]
        return count > 0

    def add_user(self, chat_id, name):
        """Добавляет пользователя в таблицу 'user'.

        Args:
            chat_id (int): Идентификатор чата пользователя (tg_id).
            name (str): Имя пользователя.

        Returns:
            bool: True, если пользователь успешно добавлен, иначе False.
        """
        cursor = self.db_conn.cursor()
        try:
            cursor.execute(f"INSERT INTO public.user(name, tg_id) VALUES ('{name}', '{chat_id}');")
            self.db_conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при добавлении пользователя: {e}")
            return False

    def get_question(self):
        now = self.get_current_question()
        cursor = self.db_conn.cursor()
        cursor.execute('SELECT tg_id FROM public.user')
        user_id = cursor.fetchone()[0]
        if now:
            quest_id = now[1]
            quest = self.get_question_by_id(quest_id)
        else:
            self.bot.send_message(user_id, 'На сегодня вопросов больше нет.')
            return
            # result = self.get_unanswered_question()
            # if result:
            #     quest_id, user_id = result[1], result[2]
            #     self.update_question_status(quest_id, user_id)
            #     self.insert_current_question(quest_id, user_id)
            #     quest = self.get_question_by_id(quest_id)
            # else:
            #     self.bot.send_message(message.chat.id, 'На сегодня вопросов больше нет.')
            #     return

        # Перемешиваем варианты ответов
        options = quest['wrong'] + [quest['answer']]
        random.shuffle(options)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for option in options:
            markup.add(option)
        self.bot.send_message(user_id, quest['question'], reply_markup=markup)

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


    def reset_questions(self):
        cursor = self.db_conn.cursor()
        # Переносим все текущие вопросы в таблицу wrong_list со статусом 'NO'
        cursor.execute("INSERT INTO public.wrong_list SELECT * FROM public.now;")
        cursor.execute("UPDATE public.wrong_list SET status='NO';")
        # Удаляем все текущие вопросы
        cursor.execute("DELETE FROM public.now;")
        # Выбираем 3 новых вопроса и добавляем их в таблицу now
        cursor.execute("INSERT INTO public.now(quest_id, user_id) SELECT quest_id, user_id FROM (" \
                       "SELECT quest_id, user_id, ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY RANDOM()) AS rn " \
                       "FROM public.user_question " \
                       "WHERE status = 'NO') sub WHERE rn <= 3;")
        self.db_conn.commit()
        # После сброса вопросов, присылаем новые вопросы пользователю
        self.get_question()

    def add_new_user_questions(self, user_id):
        """Добавляет вопросы из таблицы 'question' в таблицу 'user_question' для нового пользователя.

        Args:
            user_id (int): Идентификатор нового пользователя.

        Returns:
            bool: True, если вопросы успешно добавлены, иначе False.
        """
        cursor = self.db_conn.cursor()
        try:
            # Выбираем все вопросы из таблицы 'question'
            cursor.execute("SELECT id FROM public.question;")
            questions = cursor.fetchall()

            # Проверяем, какие из этих вопросов уже есть в таблице 'user_question' для нового пользователя
            for question_id in questions:
                cursor.execute(
                    f"SELECT COUNT(*) FROM public.user_question WHERE user_id = {user_id} AND quest_id = {question_id[0]};")
                count = cursor.fetchone()[0]
                # Если вопроса еще нет в 'user_question', добавляем его со статусом 'NO'
                if count == 0:
                    print('Что-то было добавлено', question_id[0])
                    cursor.execute(
                        f"INSERT INTO public.user_question(quest_id, user_id, status) VALUES ({question_id[0]}, {user_id}, 'NO');")
                    self.db_conn.commit()

            return True
        except Exception as e:
            print(f"Ошибка при добавлении вопросов для нового пользователя: {e}")
            return False

    def schedule_reset_questions(self):
        # Расписание: выполнение check_and_reset_questions каждый день в 16:01
        schedule.every().day.at("16:33").do(self.reset_questions)

    def start_scheduled_tasks(self):
        while True:
            schedule.run_pending()
            time.sleep(1)


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
    quiz_bot.schedule_reset_questions()

    # Запускаем планировщик в отдельном потоке
    scheduler_thread = threading.Thread(target=quiz_bot.start_scheduled_tasks)
    scheduler_thread.start()

    quiz_bot.start()
