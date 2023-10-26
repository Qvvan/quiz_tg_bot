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

    def start(self):
        """Запускает бота и устанавливает обработчики сообщений."""
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            name = message.chat.first_name
            chat_id = message.chat.id
            if self.is_user_exists(chat_id):
                self.bot.send_message(chat_id, f'Вы уже зарегистрированы, {name}!')
            elif self.add_user(chat_id, name):
                if self.add_new_user_questions(chat_id):
                    self.bot.send_message(chat_id, f'Вы успешно зарегистрировались, {name}!\nПосле 18:00 вам придут первые 3 вопроса!')
                else:
                    self.bot.send_message(chat_id, 'Что-то пошло не так, попробуйте позже')

        @self.bot.message_handler(content_types=['text'])
        def handle_answer(message):
            print(message.text)
            print(type(message.chat.id))
            if message.text == 'все' and message.chat.id == 323993202:
                cursor = self.db_conn.cursor()
                cursor.execute("DELETE FROM public.user;")
                cursor.execute("DELETE FROM public.wrong_list;")
                cursor.execute("DELETE FROM public.now;")
                cursor.execute("DELETE FROM public.user_question;")
                self.db_conn.commit()
                print('Я тут')
                self.bot.send_message(message.chat.id, 'Я все удалил!')
                return
            chat_id = message.chat.id
            if not self.is_user_exists(chat_id):
                self.bot.send_message(chat_id, 'Нажмите /start, чтобы начать')
                return
            now = self.get_current_question(chat_id)
            if now:
                quest_id, user_id = now[1], now[2]
                quest = self.get_question_by_id(quest_id)
                print(message.chat.first_name + ' ответил: ', message.text)
                answer = message.text.replace(' ', '').lower()
                if answer == quest['answer'].replace(' ', ''):
                    self.bot.send_message(chat_id, 'Отлично, это правильный ответ! 🔥')
                else:
                    self.bot.send_message(chat_id, 'К сожалению, ответ неверный. Стоит ещё раз повторить эту тему, так как этот вопрос придёт тебе завтра! ⏰')
                    add_wrong_question(quest_id, user_id)  # Добавляем вопрос в wrong_list
                self.delete_current_question(chat_id)
                self.get_question(chat_id)

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

        self.bot.polling(none_stop = True, interval = 0)


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

    def get_question(self, tg_id):
        now = self.get_current_question(tg_id)
        if now:
            quest_id = now[1]
            quest = self.get_question_by_id(quest_id)
        else:
            self.bot.send_message(tg_id, 'На сегодня вопросов больше нет.')
            return

        # Перемешиваем варианты ответов
        # options = quest['wrong'] + [quest['answer']]
        # random.shuffle(options)
        # markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        # for option in options:
        #     markup.add(option)
        # self.bot.send_message(user_id, quest['question'], reply_markup=markup)
        self.bot.send_message(tg_id, quest['question'])

    def get_current_question(self, tg_id):
        """Получает текущий вопрос из базы данных.

        Returns:
            tuple: Кортеж с информацией о текущем вопросе.
        """
        cursor = self.db_conn.cursor()
        cursor.execute(f"SELECT * FROM public.now WHERE user_id = {tg_id} LIMIT 1")
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



    def insert_current_question(self, quest_id, user_id):
        """Вставляет текущий вопрос в таблицу 'now'.

        Args:
            quest_id (int): Идентификатор вопроса.
            user_id (int): Идентификатор пользователя.
        """
        cursor = self.db_conn.cursor()
        cursor.execute(f"INSERT INTO public.now(quest_id, user_id) VALUES ({quest_id}, {user_id});")
        self.db_conn.commit()


    def delete_current_question(self, tg_id):
        """Удаляет текущий вопрос из таблицы 'now'."""
        now = self.get_current_question(tg_id)
        if now:
            quest_id, user_id = now[1], now[2]
            cursor = self.db_conn.cursor()
            cursor.execute(f"DELETE FROM public.now WHERE quest_id = {quest_id} and user_id = {user_id};")
            self.db_conn.commit()

    def add_questions_to_now_for_all_users(self):
        """Добавляет первые три вопроса в таблицу 'now' для всех пользователей и обновляет статус."""
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT tg_id FROM public.user")
        user_ids = cursor.fetchall()

        for user_id in user_ids:
            # Добавляем первые три вопроса в таблицу 'now' для текущего пользователя
            cursor.execute("INSERT INTO public.now(quest_id, user_id) " \
                           "SELECT quest_id, user_id " \
                           "FROM (" \
                           "SELECT quest_id, user_id, ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY quest_id) AS rn " \
                           "FROM public.user_question " \
                           "WHERE status = 'NO' AND user_id = %s) sub " \
                           "WHERE rn <= 3;", (user_id,))
            self.db_conn.commit()

            # Обновляем статус выбранных вопросов в user_question на 'YES'
            cursor.execute("UPDATE public.user_question SET status = 'YES' " \
                           "WHERE user_id = %s AND quest_id IN (SELECT quest_id FROM public.now WHERE user_id = %s);",
                           (user_id, user_id))
            self.db_conn.commit()


    def reset_questions(self):
        cursor = self.db_conn.cursor()
        # Переносим все текущие вопросы в таблицу wrong_list со статусом 'NO'
        cursor.execute("INSERT INTO public.wrong_list SELECT * FROM public.now;")
        # Удаляем все текущие вопросы
        cursor.execute("DELETE FROM public.now;")
        # Выбираем 3 новых вопроса и добавляем их в таблицу now
        self.add_questions_to_now_for_all_users()
        cursor.execute("INSERT INTO public.now(quest_id, user_id) " \
                       "SELECT quest_id, user_id " \
                       "FROM public.wrong_list;")
        cursor.execute("DELETE FROM public.wrong_list;")
        self.db_conn.commit()
        # После сброса вопросов, присылаем новые вопросы пользователю
        self.send_first_question_to_users()

    def send_first_question_to_users(self):
        """Рассылает первый вопрос из таблицы 'now' каждому пользователю из таблицы 'user'."""
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT tg_id FROM public.user")
        users = cursor.fetchall()
        print(users)
        for tg_id in users:
            tg_id = tg_id[0]
            # Получите первый вопрос из таблицы 'now' для текущего пользователя
            cursor.execute("SELECT quest_id FROM public.now WHERE user_id = %s LIMIT 1;", (tg_id,))
            question_id = cursor.fetchone()

            if question_id:
                # Получите текст вопроса по его идентификатору
                cursor.execute("SELECT question FROM public.question WHERE id = %s;", (question_id,))
                question_text = cursor.fetchone()[0]
                if question_text:
                    # Отправьте вопрос пользователю
                    self.bot.send_message(tg_id, 'Вопросы дня! 💯')
                    self.bot.send_message(tg_id, question_text['question'])

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
        schedule.every().day.at("16:58").do(self.reset_questions)

    def start_scheduled_tasks(self):
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    token = '6882354049:AAFyIi0qwlK8WPtWjYngFwU-ncZ2qs0WR3Q'
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
