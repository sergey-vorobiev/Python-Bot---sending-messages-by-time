import telebot
import time
import schedule
from datetime import datetime

bot = telebot.TeleBot('ID Telegram Bot')

# Многомерный объект с сообщениями
messages = {
    '05.2024': {
        '24': '',
        '25': '',
        '26': '',
    },
    '06.2024': {
        '01': '',
        '02': '',
    },
}

target_date = datetime(2024, 6, 6) # отчет времени до указанной даты

# Функция отправки сообщения
def send_message(chat_id, message, parse_mode='html', reply_markup=None):
    bot.send_message(chat_id, message, parse_mode=parse_mode, reply_markup=reply_markup)

# Функция сколько дней осталось до запланированной даты
def get_how_many_days_before(date):
    date_full = date.split('.')
    current_date = datetime(int(date_full[2]), int(date_full[1]), int(date_full[0]))
    difference = target_date - current_date
    return difference.days

# Функция обработки кол-ва дней, оставщихся до указанной даты
def get_days_text(days):
    if days == 0:
        return "Сегодня"
    elif days == 1:
        return "Завтра"
    elif 2 <= days <= 4:
        return f"Осталось: {days} дня 🤟"
    else:
        return f"Осталось: {days} дней 🤟"

# Функция отправки сообщения боту
def send_scheduled_messages(chat_id):
    current_month = datetime.now().strftime('%m.%Y')
    for month, messages_by_day in messages.items():
        if month == current_month:
            today = datetime.today().strftime('%d')
            for date, message in messages_by_day.items():
                if int(date) == int(today):
                    days_left = get_how_many_days_before(date + '.' + month)
                    days_text = get_days_text(days_left)
                    send_message(chat_id, f'{message}\n\n<b>{days_text}</b>')
                    return False


# Функция принудительной отправки сообещния всем, кто напишет /start
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    print(chat_id) # выводим в консоль ID пользователя
    send_scheduled_messages(chat_id)

def send_massage():
    send_scheduled_messages('ID User Telegram')

# Расскоментировать, если необходимо отправлять сообщение по времени
# schedule.every().day.at("08:11").do(send_massage)

if __name__ == '__main__':
    while True:
        # Расскоментировать, если необходимо отправлять сообщение по времени
        # schedule.run_pending()

        bot.polling()
        time.sleep(1)
