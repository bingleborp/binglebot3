from ..core.bot_instance import bot
from ..core.database_connection import connect_to_db
from ..helpers.is_admin_helper import is_admin

def register_handlers():
    @bot.message_handler(content_types=["text"])
    def handle_text(message):
        if is_admin(message.chat.id):
            try:
                conn = connect_to_db()
                cursor = conn.cursor()
                query = message.text
                cursor.execute(query)

                if cursor.description:
                    # Если это SELECT-запрос, получаем результаты
                    result = cursor.fetchall()
                    response = "Результат:\n" + "\n".join([str(row) for row in result])
                else:
                    # Если это UPDATE/INSERT/DELETE и т.д., коммитим изменения
                    conn.commit()
                    response = f"Успешно. Затронуто строк: {cursor.rowcount}"

                # Закрываем соединение
                cursor.close()
                conn.close()

            except Exception as e:
                response = f"Ошибка: {str(e)}"

            # Отправляем результат
            bot.send_message(message.chat.id, response)

        else:
            bot.send_message(message.chat.id, 'Доступ запрещён')