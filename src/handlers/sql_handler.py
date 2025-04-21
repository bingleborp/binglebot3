from ..core.bot_instance import bot
from ..core.database_connection import connect_to_db
from ..helpers.is_admin_helper import is_admin

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

        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            query = message.text
            
            # Выполняем запрос
            cursor.execute(query)

            if cursor.description:
                # SELECT-запрос
                result = cursor.fetchall()
                response = "Результат:\n" + "\n".join(str(row) for row in result)
            else:
                # UPDATE/INSERT/DELETE
                conn.commit()
                response = f"Успешно. Затронуто строк: {cursor.rowcount}"

        except Exception as e:
            response = f"Ошибка: {str(e)}"
            
        finally:
            # Закрываем соединение
            if 'conn' in locals():
                cursor.close()
                conn.close()

        # Отправляем результат
        bot.send_message(message.chat.id, response)