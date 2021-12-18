import telebot
import psycopg2
from telebot import TeleBot
import datetime

conn = psycopg2.connect(database="postgres",
                        user="postgres",
                        password="1234",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

token = '2106295702:AAH1GOCcX6QkAwohVqEycGlfLSozLgQtswk'
z=''
bot: TeleBot = telebot.TeleBot(token)
def ned(days,weeks):
    t='Верхняя-Нижняя'
    cursor.execute("SELECT start_time,timetable.subject,room_numb, teacher.full_name FROM timetable JOIN teacher ON timetable.subject=teacher.subject and day=%s and (week=%s or week=%s) ;",(str(days),str(weeks), (str(t))))
    records = list(cursor.fetchall())
    z=str(days + '\n')
    for i in range(0,len(records)):
        for j in range(0,len(records[i])):
            z=str(z+str(records[i][j]) + ' ')
        z=z+str('\n')
    return z
year = datetime.datetime.now()
wee = datetime.date(year.year, year.month, year.day).strftime("%V")
if (int(wee) % 2 == 0):
    weeks = 'Нижняя'
else:
    weeks = 'Верхняя'
t ='Верхняя-Нижняя'
@bot.message_handler(commands=['start'])
def start(message):
    print(message.chat.id)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Понедельник",
                 "Вторник",)
    keyboard.row("Среда",
                 "Четверг",
                 "Пятница",)
    keyboard.row("Расписание на эту неделю",
                 "Расписание на следующую неделю",)
    keyboard.row("День недели",
                 '/help')
    bot.send_message(message.chat.id, "Привет, подскажу, какое у вас расписание,для этого выберите следующие кнопки", reply_markup=keyboard)
@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == 'понедельник':
        x='Понедельник'
        z = ned(x,weeks)
        bot.send_message(message.chat.id,z)

    elif message.text.lower() == 'вторник':
        x='Вторник'
        z = ned(x,weeks)
        bot.send_message(message.chat.id,z)

    elif message.text.lower() == 'среда':
        x='Среда'
        z = ned(x, weeks)
        bot.send_message(message.chat.id,z)

    elif message.text.lower() == 'четверг':
        x='Четверг'
        z = ned(x,weeks)
        bot.send_message(message.chat.id,z)

    elif message.text.lower() == 'пятница':
        x='Пятница'
        z = ned(x,weeks)
        bot.send_message(message.chat.id,z)

    elif (message.text.lower() == 'расписание на эту неделю'):
        x = 'Понедельник'
        z = ned(x, weeks)
        x = 'Вторник'
        z = z + ned(x, weeks)
        x = 'Среда'
        z = z + ned(x, weeks)
        x = 'Четверг'
        z = z + ned(x, weeks)
        x = 'Пятница'
        z = z + ned(x, weeks)
        bot.send_message(message.chat.id, z)
    elif (message.text.lower() == 'расписание на следующую неделю'):
        if (int(wee) % 2 == 0):
            we = 'Верхняя'
        else:
            we = 'Нижняя'
        x = 'Понедельник'
        z = ned(x, we)
        x = 'Вторник'
        z = z + ned(x, we)
        x = 'Среда'
        z = z + ned(x, we)
        x = 'Четверг'
        z = z + ned(x, we)
        x = 'Пятница'
        z = z + ned(x, we)
        bot.send_message(message.chat.id, z)
    elif message.text.lower() == 'день недели':
        bot.send_message(message.chat.id,str('Это неделя - '+weeks))
    elif message.text.lower() == '/mtuci':
        bot.send_message(message.chat.id, str('Это наш офисиальный сайт htpps://mtuci.ru'))
    elif message.text.lower() == '/help':
        bot.send_message(message.chat.id, str('/start запускает бот\n'+'Расписание на эту ниделю - это '))
    else:
        bot.send_message(message.chat.id, str('Извините я вас не понял'))
bot.infinity_polling()