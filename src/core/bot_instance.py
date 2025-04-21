import os
import telebot

botToken = os.environ["TG_BOT_TOKEN"]
bot = telebot.TeleBot(botToken)