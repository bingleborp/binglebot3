import os
from ..core.sql import operation

admin_id = os.getenv("TG_BOT_ADMIN_IDS")

def is_admin(user_id):
    return str(admin_id) == str(user_id)

def is_moderator(user_id):
    return operation("SELECT * from")