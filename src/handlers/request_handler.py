from telebot import types
from ..core.bot_instance import bot
from ..helpers.queue import add_song

# Временное хранилище для данных пользователя
user_requests = {}

def register_handlers():
    @bot.message_handler(commands=['add'])
    def handle_add_command(message):
        msg = bot.send_message(message.chat.id, "Введите название песни:")
        bot.register_next_step_handler(msg, process_song_name)

    def process_song_name(message):
        try:
            user_id = message.from_user.id
            user_requests[user_id] = {
                'song_name': message.text,
                'chat_id': message.chat.id
            }
            
            msg = bot.send_message(message.chat.id, "Введите ссылку на песню:")
            bot.register_next_step_handler(msg, process_song_url)
        except Exception as e:
            bot.reply_to(message, f"Ошибка: {str(e)}")
            del user_requests[user_id]

    def process_song_url(message):
        try:
            user_id = message.from_user.id
            if user_id not in user_requests:
                return bot.send_message(message.chat.id, "Сессия устарела, начните заново")
            
            user_requests[user_id]['song_url'] = message.text
            
            # Создаем клавиатуру с кнопками подтверждения
            markup = types.InlineKeyboardMarkup()
            yes_btn = types.InlineKeyboardButton(
                text="✅ Да", 
                callback_data=f"confirm_{user_id}"
            )
            no_btn = types.InlineKeyboardButton(
                text="❌ Нет", 
                callback_data=f"cancel_{user_id}"
            )
            markup.add(yes_btn, no_btn)
            
            bot.send_message(
                message.chat.id,
                "Подтвердите добавление песни:\n\n"
                f"Название: {user_requests[user_id]['song_name']}\n"
                f"Ссылка: {user_requests[user_id]['song_url']}",
                reply_markup=markup
            )
        except Exception as e:
            bot.reply_to(message, f"Ошибка: {str(e)}")
            del user_requests[user_id]

    @bot.callback_query_handler(func=lambda call: call.data.startswith(('confirm_', 'cancel_')))
    def handle_confirmation(call):
        try:
            user_id = int(call.data.split('_')[1])
            action = call.data.split('_')[0]
            
            if user_id not in user_requests:
                return bot.answer_callback_query(
                    call.id, 
                    "Сессия устарела, начните заново", 
                    show_alert=True
                )
            
            data = user_requests[user_id]
            
            if action == 'confirm':
                success = add_song(
                    user_id=user_id,
                    session_id=data['chat_id'],
                    song_name=data['song_name'],
                    song_url=data['song_url']
                )
                
                if success:
                    response = "✅ Песня успешно добавлена в очередь!"
                else:
                    response = "❌ Ошибка при добавлении песни"
            else:
                response = "❌ Добавление отменено"
            
            bot.edit_message_text(
                response,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
            del user_requests[user_id]
            
        except Exception as e:
            bot.answer_callback_query(
                call.id, 
                f"Произошла ошибка: {str(e)}", 
                show_alert=True
            )