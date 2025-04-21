from src.core.bot_instance import bot

def register_handlers():
    @bot.message_handler(commands=["start"])
    def start(m, res=False):
        bot.send_message(m.chat.id, 'Я на связи! Напиши мне что-нибудь )')