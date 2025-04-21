from .core.bot_instance import bot
from .handlers import sql_handler, start_handler

if __name__ == '__main__':
    sql_handler.register_handlers()
    start_handler.register_handlers()
    bot.polling(none_stop=True)