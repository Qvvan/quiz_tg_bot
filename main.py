import telebot
import threading

from database_handler import DatabaseHandler
from question_manager import QuestionManager
from quiz_scheduler import QuizScheduler
from user_manager import UserManager


class TelegramBotHandler:
    def __init__(self, token, db_params):
        telebot.apihelper.SESSION_TIME_TO_LIVE = 60 * 5
        self.bot = telebot.TeleBot(token)
        self.db_handler = DatabaseHandler(db_params)
        self.user_manager = UserManager(self.db_handler, self.bot)
        self.question_manager = QuestionManager(self.db_handler, self.bot)
        self.quiz_scheduler = QuizScheduler(self.bot, self.user_manager, self.question_manager)

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

            elif message.text.replace(' ', '').split('-')[0] == 'удали' and message.chat.id == 323993202:
                self.user_manager.delete_user(message.text.replace(' ', '').split('-')[1])
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
            self.bot.polling(none_stop=True, interval=0)
        except Exception as e:
            self.bot.send_message(323993202, f'Бот вылетел\nОшибка: {e}')
            self.start()

    def start_scheduled_tasks(self):
        """Запуск планировщика задач в отдельном потоке."""
        self.quiz_scheduler.start_scheduled_tasks()


if __name__ == "__main__":

    print('Начало наботы')

    token = '5278804872:AAGh40DpEzAUs1FcjJJ8oCQTWm7LJ5qkFXQ'
    db_params = {
        "database": "tg_db",
        "user": "postgres",
        "password": "123",
        "host": "localhost",
        "port": '5432'
    }
    quiz_bot = TelegramBotHandler(token, db_params)
    quiz_bot.quiz_scheduler.schedule_reset_questions()

    # Запускаем планировщик в отдельном потоке
    scheduler_thread = threading.Thread(target=quiz_bot.start_scheduled_tasks)
    scheduler_thread.start()

    quiz_bot.start()
