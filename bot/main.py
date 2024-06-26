import os
import threading

import telebot
from telebot import types

from database_handler import DatabaseHandler
from question_manager import QuestionManager
from quiz_scheduler import QuizScheduler
from user_manager import UserManager


class TelegramBotHandler:
    def __init__(self, token, db_params):
        telebot.apihelper.SESSION_TIME_TO_LIVE = 60 * 5
        self.bot = telebot.TeleBot(token)
        self.db_handler = DatabaseHandler(db_params, self.bot)
        self.user_manager = UserManager(self.db_handler, self.bot)
        self.question_manager = QuestionManager(self.db_handler, self.bot)
        self.quiz_scheduler = QuizScheduler(self.bot, self.user_manager, self.question_manager)

    def get_keyboard_students(self):
        keyboard = types.InlineKeyboardMarkup()
        cursor = self.db_handler.execute_query('SELECT name,tg_id FROM public.user')
        tg_ids = cursor.fetchall()
        for name, tg_id in tg_ids:
            keyboard.add(types.InlineKeyboardButton(text=name, callback_data=tg_id))
        keyboard.add(types.InlineKeyboardButton(text='Назад', callback_data='back'))
        return keyboard

    def get_menu_keyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Удалить', callback_data='delete'))
        keyboard.add(types.InlineKeyboardButton(text='Скрыть', callback_data='hide'))
        return keyboard

    def connect_to_db(self):
        """Установка соединения с базой данных."""
        self.db_handler.connect()

    def close_db_connection(self):
        """Закрытие соединения с базой данных."""
        self.db_handler.close_connection()

    def start(self):
        """Запуск бота и обработка команды /start."""

        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.connect_to_db()
            name = message.chat.first_name
            tg_id = message.chat.id
            if self.user_manager.is_user_exists(tg_id):
                self.bot.send_message(tg_id, f'Вы уже зарегистрированы, {name}!')
            elif self.user_manager.add_user(tg_id, name):
                if self.question_manager.add_new_user_questions(tg_id):
                    self.bot.send_message(tg_id,
                                          f'Вы успешно зарегистрировались, {name}!\nПосле 18:00 вам придут первые 3 вопроса!')
                else:
                    self.bot.send_message(tg_id, 'Что-то пошло не так, попробуйте позже')
            self.close_db_connection()

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_query(call):

            if call.data == 'hide':
                self.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
            elif call.data == 'delete':
                self.bot.edit_message_text(chat_id=call.message.chat.id,
                                           message_id=call.message.id,
                                           text='Ваши ученики',
                                           reply_markup=self.get_keyboard_students())
            elif call.data == 'back':
                self.bot.edit_message_text(chat_id=call.message.chat.id,
                                           message_id=call.message.id,
                                           text='Что хотим?',
                                           reply_markup=self.get_menu_keyboard())
            else:
                self.user_manager.delete_user(call.data)
                self.bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id,
                                                   reply_markup=self.get_keyboard_students())

        @self.bot.message_handler(content_types=['text'])
        def handle_answer(message):
            self.connect_to_db()
            tg_id = message.chat.id
            if message.text.lower() == 'все' and message.chat.id == 323993202:
                self.question_manager.delete_all()
                self.bot.send_message(message.chat.id, 'Я все удалил!')
                return

            elif message.text == 'обновить' and message.chat.id == 323993202:
                self.bot.send_message(323993202, self.question_manager.process_message())
                return

            elif message.text.replace(' ', '').lower() == 'ученики' and message.chat.id == 323993202:
                self.bot.send_message(323993202, text='Что хотим?', reply_markup=self.get_menu_keyboard())
                return

            elif not self.user_manager.is_user_exists(tg_id):
                self.bot.send_message(tg_id, 'Нажмите /start, чтобы начать')
                return

            now = self.question_manager.get_current_question(tg_id)
            if now:
                quest_id, tg_id = now[0], now[1]
                response = self.question_manager.get_question_by_id(quest_id)[0]
                print(message.chat.first_name + ' ответил: ', message.text)
                answer = message.text.replace(' ', '')
                if answer in response['answer'].replace(' ', '').split('|'):
                    self.bot.send_message(tg_id, 'Отлично, это правильный ответ! 🔥')
                else:
                    self.bot.send_message(tg_id,
                                          'К сожалению, ответ неверный. Стоит ещё раз повторить эту тему, так как этот вопрос придёт тебе завтра! ⏰')
                    self.question_manager.add_wrong_question(quest_id, tg_id)
                self.bot.send_message(323993202,
                                      f"На вопрос\n {response['question']}\n{message.chat.first_name} ответил: {message.text}")
                self.question_manager.delete_current_question(tg_id)
                self.question_manager.get_question(tg_id)
            self.close_db_connection()

        try:
            self.bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            self.bot.send_message(323993202, f'Бот вылетел\nОшибка: {e}')

    def start_scheduled_tasks(self):
        """Запуск планировщика задач в отдельном потоке."""
        self.quiz_scheduler.start_scheduled_tasks()


if __name__ == "__main__":
    os.system('echo Бот запущен!')

    token = os.environ.get('API_TOKEN')
    db_params = {
        "database": os.environ.get('DB_NAME'),
        "user": os.environ.get('DB_USER'),
        "password": os.environ.get('DB_PASSWORD'),
        "host": os.environ.get('DB_HOST'),
        "port": os.environ.get('DB_PORT')
    }
    quiz_bot = TelegramBotHandler(token, db_params)
    quiz_bot.quiz_scheduler.schedule_reset_questions()

    # Запускаем планировщик в отдельном потоке
    scheduler_thread = threading.Thread(target=quiz_bot.start_scheduled_tasks)
    scheduler_thread.start()
    while True:
        try:
            quiz_bot.start()
        except Exception as e:
            print('Ошибка: ', e)
            print('Бот перезапускается...')
            continue
