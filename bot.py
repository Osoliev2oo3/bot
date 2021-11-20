import telebot
import psycopg2
# from telebot import TeleBot
import datetime

conn = psycopg2.connect(database="timetable",
                        user="postgres",
                        password="1234",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

token = '2143878695:AAHNOsHNp47GiGkq_gBu8FS0H3IpeSdtXyE'

bot: TeleBot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    print(message.chat.id)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("По дате", "Сегодня")
    keyboard.row("Завтра", "Вчера")
    keyboard.row('/help')

    bot.send_message(message.chat.id, "Привет, подскажу, какое у вас расписание,для этого выберите следующие кнопки", reply_markup=keyboard)
    print(datetime.datetime.now().time())

@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == 'сегодня':
        cursor.execute("SELECT nomer,sabgek  FROM Timetable WHERE data = date(now());")
        records = list(cursor.fetchall())
        q = records[0][1]
        w = records[1][1]
        e = records[2][1]
        r = records[3][1]
        if q == 'Нет':
            q = "9:30-11:05 - нет.\n"
        else:
            q = ('9:30-11:05 - ' + str(q) + '.\n')
        if w == 'Нет':
            w = "11:20-12:55 - нет.\n"
        else:
            w = ('11:20-12:55 - ' + str(w) + '.\n')
        if e == 'Нет':
            e = "13:10-14:45 - нет.\n"
        else:
            e = ('13:10-14:45 - ' + str(e) + '.\n')
        if r == 'Нет':
            r = "15:25-17:00 - нет.\n"
        else:
            r = ('15:25-17:00 - ' + str(r) + '.\n')
        t = str('Расписание на сегодня: \n' + q + w + e + r)
        bot.send_message(message.chat.id, t)

    elif message.text.lower() == 'завтра':
        cursor.execute("SELECT nomer, sabgek FROM Timetable WHERE data = (date(now()) + integer '1');")
        records = list(cursor.fetchall())
        print(records)
        q = records[0][1]
        w = records[1][1]
        e = records[2][1]
        r = records[3][1]
        if q == 'Нет':
            q = "9:30-11:05 - нет.\n"
        else:
            q = ('9:30-11:05 - ' + str(q) + '.\n')
        if w == 'Нет':
            w = "11:20-12:55 - нет.\n"
        else:
            w = ('11:20-12:55 - ' + str(w) + '.\n')
        if e == 'Нет':
            e = "13:10-14:45 - нет.\n"
        else:
            e = ('13:10-14:45 - ' + str(e) + '.\n')
        if r == 'Нет':
            r = "15:25-17:00 - нет.\n"
        else:
            r = ('15:25-17:00 - ' + str(r) + '.\n')
        t = str('Расписание на завтра: \n' + q + w + e + r)
        bot.send_message(message.chat.id, t)
        print(message.text)

    elif message.text.lower() == 'вчера':
        cursor.execute("SELECT nomer, sabgek FROM Timetable WHERE data = (date(now()) - integer '1');")
        records = list(cursor.fetchall())
        q = records[0][1]
        w = records[1][1]
        e = records[2][1]
        r = records[3][1]
        if q == 'Нет':
            q = "9:30-11:05 - нет.\n"
        else:
            q = ('9:30-11:05 - ' + str(q) + '.\n')
        if w == 'Нет':
            w = "11:20-12:55 - нет.\n"
        else:
            w = ('11:20-12:55 - ' + str(w) + '.\n')
        if e == 'Нет':
            e = "13:10-14:45 - нет.\n"
        else:
            e = ('13:10-14:45 - ' + str(e) + '.\n')
        if r == 'Нет':
            r = "15:25-17:00 - нет.\n"
        else:
            r = ('15:25-17:00 - ' + str(r) + '.\n')
        t = str('Вчерашнее расписание: \n' + q + w + e + r)
        bot.send_message(message.chat.id, t)

    elif message.text.lower() == 'по дате':
        bot.send_message(message.chat.id, 'Введите число в формате ГГГГ-ММ-ДД \n Например: 2021-01-01')

    elif message.text.__contains__('2021'):
        date1 = str(message.text)
        cursor.execute("SELECT nomer, sabgek FROM Timetable WHERE data = '{0}'".format(date1))
        records = list(cursor.fetchall())
        if not records:
            bot.send_message(message.chat.id, 'Пока расписания на это число нет, введите другую дату.')
        else:
            q = records[0][1]
            w = records[1][1]
            e = records[2][1]
            r = records[3][1]
            if q == 'Нет':
                q = "9:30-11:05 - нет.\n"
            else:
                q = ('9:30-11:05 - ' + str(q) + '.\n')
            if w == 'Нет':
                w = "11:20-12:55 - нет.\n"
            else:
                w = ('11:20-12:55 - ' + str(w) + '.\n')
            if e == 'Нет':
                e = "13:10-14:45 - нет.\n"
            else:
                e = ('13:10-14:45 - ' + str(e) + '.\n')
            if r == 'Нет':
                r = "15:25-17:00 - нет.\n"
            else:
                r = ('15:25-17:00 - ' + str(r) + '.\n')
            t = str('Расписание на ' + date1 + ':\n' + q + w + e + r)
            bot.send_message(message.chat.id, t)
    else:
        bot.send_message(message.chat.id, 'Вы ввели некоректные данные, пожалуйста убедитесь в достоверности, и повторите попытку')



    if message.text.lower() == '/help':
        bot.send_message(message.chat.id, '/start \n Команды будут добавляться :)')


bot.infinity_polling()