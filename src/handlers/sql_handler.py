from ..core.bot_instance import bot
from ..core.sql import operation
from ..core.is_admin_helper import is_admin

def register_handlers():
    # Обработчик команды /sql
    @bot.message_handler(commands=['sql'])
    def handle_sql_command(message):
        if not is_admin(message.chat.id):
            bot.send_message(message.chat.id, 'Доступ запрещён')
            return

        # Запрашиваем SQL-запрос
        msg = bot.send_message(message.chat.id, "Введите SQL-запрос:")
        bot.register_next_step_handler(msg, process_sql_query)

    # Обработчик SQL-запроса
    def process_sql_query(message):
        # Проверяем, что сообщение содержит текст
        if message.content_type != 'text':
            bot.send_message(message.chat.id, "Нужен текстовый запрос!")
            return
        response = operation(message.text)

        # Отправляем результат
        bot.send_message(message.chat.id, response)