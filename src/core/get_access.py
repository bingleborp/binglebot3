import os
from .database_connection import connect_to_db

admin_id = os.getenv("TG_BOT_ADMIN_IDS")

def is_admin(user_id):
    return str(admin_id) == str(user_id)

def is_moder(user_id: int) -> bool:
    with connect_to_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT EXISTS(SELECT 1 FROM users WHERE telegram_id = %s AND is_moder = %s)",
                (user_id, True))
            return cursor.fetchone()[0] 