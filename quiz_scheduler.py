import schedule
import time


class QuizScheduler:
    """Класс для планирования задач по расписанию."""

    def __init__(self, bot, user_manager, question_manager):
        """Инициализация объекта QuizScheduler.

        Args:
            bot: Объект бота TeleBot.
            user_manager (UserManager): Менеджер пользователей.
            question_manager (QuestionManager): Менеджер вопросов.
        """
        self.bot = bot
        self.user_manager = user_manager
        self.question_manager = question_manager

    def schedule_reset_questions(self):
        """Запланировать сброс вопросов по расписанию."""
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

        for day in weekdays:
            remind = f"schedule.every().{day}.at('17:00').do(self.question_manager.reminder)"
            exec(remind)

        for day in weekdays:
            quest = f"schedule.every().{day}.at('18:00').do(self.question_manager.reset_questions)"
            exec(quest)

    def start_scheduled_tasks(self):
        """Запуск задач по расписанию в отдельном потоке."""
        while True:
            schedule.run_pending()
            time.sleep(1)
