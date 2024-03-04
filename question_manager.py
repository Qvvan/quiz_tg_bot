import random

from telebot import types


class QuestionManager:
    """Класс для управления вопросами и заданиями пользователям."""

    def __init__(self, db_handler, bot):
        self.db_handler = db_handler
        self.bot = bot

    def get_question(self, tg_id):
        """Получение текущего вопроса для пользователя и отправка ему сообщения.

        Args:
            tg_id: Идентификатор чата пользователя.
        """
        now = self.get_current_question(tg_id)
        if now:
            quest_id = now[0]
            response = self.get_question_by_id(quest_id)[0]
            answer = response['answer']
            wrong = response['wrong']
            quest = response['question']
            path = response['path_img']
        else:
            self.bot.send_message(tg_id, 'На сегодня вопросов больше нет.✅')
            return

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        s = '\n'
        if wrong:
            # Перемешиваем варианты ответов
            options = wrong + [answer]
            random.shuffle(options)
            for i, option in enumerate(options, start=1):
                markup.add(f'{option}')
                s += f'\n{i}. {option}'
        if path:
            with open(path, 'rb') as photo:
                self.bot.send_photo(tg_id, photo, quest + s,
                                    reply_markup=markup if wrong else types.ReplyKeyboardRemove())
        else:
            self.bot.send_message(tg_id, quest + s, reply_markup=markup if wrong else types.ReplyKeyboardRemove())

    def get_current_question(self, tg_id):
        """Получение текущего задания пользователя.

        Args:
            tg_id: Идентификатор чата пользователя.

        Returns:
            tuple: Кортеж с информацией о текущем вопросе пользователя.
        """
        cursor = self.db_handler.execute_query(f"SELECT * FROM public.now WHERE tg_id = {tg_id} LIMIT 1")
        return cursor.fetchone()

    def get_question_by_id(self, quest_id):
        """Получение текста вопроса по его идентификатору.

            quest_id: Идентификатор вопроса.

        Returns:
            str: Текст вопроса.
        """
        cursor = self.db_handler.execute_query(
            f"SELECT jsonb_build_object('question', question, 'answer', answer, 'wrong', wrong, 'path_img', path_img) FROM public.question WHERE id = {quest_id}")
        return cursor.fetchone()

    def add_new_user_questions(self, tg_id):
        """Добавление новых вопросов для пользователя.

        Args:
            tg_id: Идентификатор пользователя.

        Returns:
            bool: True, если вопросы успешно добавлены, False в противном случае.
        """
        cursor = self.db_handler.execute_query("SELECT id FROM public.question;")
        questions = cursor.fetchall()

        for question_id in questions:
            cursor.execute(
                f"SELECT COUNT(*) FROM public.user_question WHERE tg_id = {tg_id} AND quest_id = {question_id[0]};")
            count = cursor.fetchone()[0]

            if count == 0:
                print('Что-то было добавлено', question_id[0])
                cursor.execute(
                    f"INSERT INTO public.user_question(quest_id, tg_id, status) VALUES ({question_id[0]}, {tg_id}, 'NO');")
                self.db_handler.db_conn.commit()

        return True

    def send_first_question_to_users(self):
        """Отправка первого вопроса всем зарегистрированным пользователям."""
        cursor = self.db_handler.execute_query("SELECT tg_id FROM public.user")
        users = cursor.fetchall()

        for tg_id in users:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            s = '\n'
            tg_id = tg_id[0]

            now = self.get_current_question(tg_id)

            if now:
                quest_id = now[0]
                response = self.get_question_by_id(quest_id)[0]
                answer = response['answer']
                wrong = response['wrong']
                quest = response['question']
                path = response['path_img']
                self.bot.send_message(tg_id, 'Вопросы дня! 💯')
                if wrong:
                    # Перемешиваем варианты ответов
                    options = wrong + [answer]
                    random.shuffle(options)
                    for i, option in enumerate(options, start=1):
                        markup.add(f'{option}')
                        s += f'\n{i}. {option}'
                if path:
                    with open(path, 'rb') as photo:
                        self.bot.send_photo(tg_id, photo, quest + s,
                                            reply_markup=markup if wrong else types.ReplyKeyboardRemove())
                else:
                    self.bot.send_message(tg_id, quest + s,
                                          reply_markup=markup if wrong else types.ReplyKeyboardRemove())


    def reminder(self):
        """Отправка напоминания пользователям об оставшихся вопросах."""
        self.db_handler.connect()
        cursor = self.db_handler.execute_query("SELECT DISTINCT tg_id FROM public.now;")
        users = cursor.fetchall()

        for tg_id in users:
            self.bot.send_message(tg_id[0],
                                  'Время поджимает!⏰\nОтветьте на оставшиеся вопросы до 18:00, чтобы не упустить ни одного')
        self.db_handler.close_connection()

    def reset_questions(self):
        """Сброс текущих вопросов и добавление новых."""
        self.db_handler.connect()
        cursor = self.db_handler.execute_query("INSERT INTO public.wrong_list SELECT * FROM public.now;")
        cursor.execute("DELETE FROM public.now;")
        self.add_questions_to_now_for_all_users()
        cursor.execute("INSERT INTO public.now(quest_id, tg_id) SELECT quest_id, tg_id FROM public.wrong_list;")
        cursor.execute("DELETE FROM public.wrong_list;")
        self.db_handler.db_conn.commit()
        self.send_first_question_to_users()
        self.db_handler.close_connection()

    def add_questions_to_now_for_all_users(self):
        """Добавление вопросов для всех пользователей."""
        cursor = self.db_handler.execute_query("SELECT tg_id FROM public.user")
        tg_ids = cursor.fetchall()

        for tg_id in tg_ids:
            cursor.execute("INSERT INTO public.now(quest_id, tg_id) "
                           "SELECT quest_id, tg_id "
                           "FROM (SELECT quest_id, tg_id, ROW_NUMBER() OVER(PARTITION BY tg_id ORDER BY quest_id) AS rn "
                           "FROM public.user_question WHERE status = 'NO' AND tg_id = %s) sub "
                           "WHERE rn <= 3;", (tg_id,))
            self.db_handler.db_conn.commit()

            cursor.execute("UPDATE public.user_question SET status = 'YES' "
                           "WHERE tg_id = %s AND quest_id IN (SELECT quest_id FROM public.now WHERE tg_id = %s);",
                           (tg_id, tg_id))
            self.db_handler.db_conn.commit()

    def add_wrong_question(self, quest_id, tg_id):
        """Добавление вопроса в список неправильных ответов пользователя.

        Args:
            quest_id: Идентификатор вопроса.
            tg_id: Идентификатор пользователя.
        """
        self.db_handler.execute_query(
            f"INSERT INTO public.wrong_list(quest_id, tg_id) VALUES ({quest_id}, {tg_id});")
        self.db_handler.db_conn.commit()

    def delete_current_question(self, tg_id):
        """Удаление текущего вопроса пользователя.

        Args:
            tg_id: Идентификатор чата пользователя.
        """
        now = self.get_current_question(tg_id)
        if now:
            quest_id, tg_id = now[0], now[1]
            self.db_handler.execute_query(
                f"DELETE FROM public.now WHERE quest_id = {quest_id} and tg_id = {tg_id};")
            self.db_handler.db_conn.commit()

    def process_message(self):
        """Обработка сообщения и обновление базы данных с вопросами."""
        self.db_handler.execute_query("""
            INSERT INTO public.user_question (tg_id, quest_id, status)
            SELECT CAST(u.tg_id AS BIGINT), q.id, 'NO'
            FROM public.user AS u
            CROSS JOIN (
                SELECT q.id 
                FROM public.question AS q
                LEFT JOIN public.user_question AS uq ON q.id = uq.quest_id
                WHERE uq.quest_id IS NULL
            ) q;
        """)
        self.db_handler.db_conn.commit()
        return "Таблица обновлена!"

    def delete_all(self):
        self.db_handler.execute_query("DELETE FROM public.user;")
        self.db_handler.execute_query("DELETE FROM public.wrong_list;")
        self.db_handler.execute_query("DELETE FROM public.now;")
        self.db_handler.execute_query("DELETE FROM public.user_question;")
        self.db_handler.db_conn.commit()
