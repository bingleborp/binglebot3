import os
from .sql import do

admin_id = os.getenv("TG_BOT_ADMIN_IDS")

def is_admin(user_id):
    return str(admin_id) == str(user_id)

def is_moderator(user_id):
    return do("SELECT * FROM users WHERE is_moderator = true")