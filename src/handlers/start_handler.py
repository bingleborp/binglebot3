from ..core.bot_instance import bot
from ..helpers.users import register

def register_handlers():
    @bot.message_handler(commands=["start"])
    def start(m, res=False):
        register(m.chat.id, m.from_user.first_name)
        bot.send_message(m.chat.id, 'Я на связи! Напиши /help для списка команд')