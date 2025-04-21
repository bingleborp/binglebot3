import telebot
import os
import psycopg2

# Инициализация бота
botToken = os.getenv("TG_BOT_TOKEN")
bot = telebot.TeleBot(botToken)
dbUser = os.getenv("DB_USER")
dbPass = os.getenv("DB_PASS")
dbName = os.getenv("DB_NAME")
adminId = os.getemv("TG_BOT_ADMIN_IDS")
DATABASE_URL = "postgres://" + dbUser + ":"+ dbPass +"@bingle_db:5432/" + dbName

def connect_to_db():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

# Ответ на /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я на связи! Напиши мне что-нибудь )')
# SQL
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.chat.id == adminId:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = message.text
        cursor.execute(query)
        conn.commit()
        cursor.close()
        response =
        bot.send_message(message.chat.id, 'Вот ответ базы: ', response)
    else:
        bot.send_message(message.chat.id, 'Пашол нафик')

# Запускаем бота
bot.polling(none_stop=True, interval=0)