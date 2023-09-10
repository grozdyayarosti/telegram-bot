import telebot
from telebot import types
import config
import infoFile

# Инициализация бота с помощью специального токена
bot = telebot.TeleBot(config.TOKEN)

# Обработчик события при получении команды start
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(
        message.chat.id,
        "Доброго времени суток, {0.first_name}!\nЯ - <b>{1.first_name}</b>.\nХотите записаться на занятие или получить информацию о школе танцев?".format(
            message.from_user,
            bot.get_me()),
        parse_mode='html',
        # Вывод альтернативной клавиатуры для выбора предложенных ответов(в зависимости от параметра будут предложены разные варианты в клавиатуре)
        reply_markup=markUpSave('start')
    )

#Обработчик события при получении текстового сообщения
@bot.message_handler(content_types=['text'])
def dialog(message):
    if message.chat.type == 'private':
        # Бот смотрит на полученные сообщения и в зависимости от них отвечает
        match message.text:
            case 'Хочу записаться на занятие':
                mesg = bot.send_message(
                    message.chat.id,
                    "На какое имя вы хотите записаться?",
                    reply_markup=markUpSave('empty')
                )
                # Метод, который ждёт ответного сообщения от пользователя и запускает метод recordName
                bot.register_next_step_handler(mesg, recordName)

            case 'Хочу получить информацию':

                bot.send_message(
                    message.chat.id, "Какая информация вас интересует?",
                    reply_markup=markUpSave('info')
                )

            case 'Расписание занятий':
                photo = open('static/schedule.jpg', 'rb')
                bot.send_photo(
                    message.chat.id,
                    photo,
                    reply_markup=markUpSave('start')
                    )

            case 'Прейскурант':
                photo = open('../prog/tgBot2/static/pricelist.jpg', 'rb')
                bot.send_photo(
                    message.chat.id,
                    photo,
                    reply_markup=markUpSave('start')
                )

            case 'Узнать о стилях танцев':
                mesg = bot.send_message(
                    message.chat.id,
                    "О каком стиле танцев вы хотите узнать поподробнее?",
                    reply_markup=markUpSave('styleInfo')
                )
                bot.register_next_step_handler(mesg, moreInfo)

            case _:
                bot.send_message(message.chat.id, "К сожалению, я могу вам ответить только на предложенные команды🥺")
def moreInfo(message):
    # Если сообщение не "перейти обратно", то запрашивает ввыбранный стиль в файле infoFile и тот по ключу выдаёт подробный текст польхователю
    if message.text == 'Перейти обратно':
        welcome(message)
    else:
        mesg = bot.send_message(
            message.chat.id,
            infoFile.getInfoStyle(message.text),
            reply_markup=markUpSave('styleInfo')
        )
        bot.register_next_step_handler(mesg, moreInfo)
def recordName(message):
    # Записывает полученное имя пользователя в глобальную переменную под ключом name
    infoFile.info['name'] = message.text
    mesg = bot.send_message(
        message.chat.id,
        "На какой стиль танцев вы хотите записаться?",
        reply_markup=markUpSave('style')
    )
    # после ответа пользователя запускает функцию запроса стиля
    bot.register_next_step_handler(mesg, recordStyle)
def recordStyle(message):
    # Записывает полученное название стиля в глобальную переменную под ключом style
    infoFile.info['style'] = message.text
    mesg = bot.send_message(
        message.chat.id,
        "Укажите свой номер телефона для связи",
        reply_markup=markUpSave('empty')
    )
    # после ответа пользователя запускает функцию запроса телефона
    bot.register_next_step_handler(mesg, recordPhone)
def recordPhone(message):
    infoFile.info['phone'] = message.text
    bot.send_message(
        message.chat.id,
        "Вы успешно записаны!"
    )
    bot.send_message(
        message.chat.id,
        f"Данные будут переданы администратору\nИмя: {infoFile.info['name']}\nСтиль танцев: {infoFile.info['style']}\nНомер телефона: {infoFile.info['phone']}",
        reply_markup=markUpSave('start')
    )
    bot.send_message(
        # ID взят из файла config
        config.AdminChatID,
        f"Запись для администратора:\nИмя: {infoFile.info['name']}\nСтиль танцев: {infoFile.info['style']}\nНомер телефона: {infoFile.info['phone']}",
    )
# Функция, которая в зависимости от полученного параметра создаёт markup - альетарнативную клавиатуру с разными вариантами ответа
def markUpSave(mode):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if mode == 'start':
        item1 = types.KeyboardButton("Хочу записаться на занятие")
        item2 = types.KeyboardButton("Хочу получить информацию")
        markup.add(item1, item2)

    elif mode == 'info':
        item1 = types.KeyboardButton("Расписание занятий")
        item2 = types.KeyboardButton("Прейскурант")
        item3 = types.KeyboardButton("Узнать о стилях танцев")
        markup.add(item1, item2, item3)

    elif mode == 'style':
        item1 = types.KeyboardButton("HIP HOP NEW")
        item2 = types.KeyboardButton("JUZZ FUNK NEW")
        item3 = types.KeyboardButton("K POP NEW")
        item4 = types.KeyboardButton("JAZZ FUNK")
        item5 = types.KeyboardButton("K POP PRO")
        item6 = types.KeyboardButton("HIP HOP")
        item7 = types.KeyboardButton("UNIVERSE DANCE CREW")
        item8 = types.KeyboardButton("GIRL'S FLAVA")
        item9 = types.KeyboardButton("VOGUE")
        item10 = types.KeyboardButton("JAZZ FUNK 18+")
        item11 = types.KeyboardButton("TATTIERS")
        item12 = types.KeyboardButton("HIGH HEELLS NEW")
        item13 = types.KeyboardButton("HIGH HEELLS PRO")
        markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11, item12, item13)

    elif mode == 'styleInfo':
        item1 = types.KeyboardButton("VOGUE")
        item2 = types.KeyboardButton("K-POP")
        item3 = types.KeyboardButton("JAZZ-FUNK")
        item4 = types.KeyboardButton("HIP-HOP")
        item5 = types.KeyboardButton("HIGH-HEELS")
        item6 = types.KeyboardButton("Перейти обратно")
        markup.add(item1, item2, item3, item4, item5, item6)

    elif mode == 'empty':
        markup = types.ReplyKeyboardRemove()

    return markup
# Заставляет бота работать бесперебойно(пока на машине запущен код)
bot.polling(none_stop=True)
