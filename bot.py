import telebot
import sqlite3
from random import randint
import random

cities = {
    'а': ['Амстердам', 'Афины', 'Атланта', 'Ашхабад', 'Анкара', 'Астрахань', 'Адыгейск', 'Антверпен', 'Адлер', 'Агра',
          'Александрия'],
    'б': ['Бразилия', 'Берлин', 'Барселона', 'Белград', 'Бухарест', 'Будапешт', 'Бремен', 'Бирмингем', 'Баку', 'Бишкек',
          'Белгород', 'Брест'],
    'в': ['Вена', 'Волгоград', 'Варшава', 'Воронеж', 'Владимир', 'Вильнюс', 'Валенсия', 'Венеция', 'Вашингтон',
          'Владивосток', 'Верона'],
    'г': ['Гомель', 'Грозный', 'Гамбург', 'Гуанчжоу', 'Генуя', 'Гент', 'Гданьск', 'Гавана', 'Глазго', 'Ганновер',
          'Гвадалахара', 'Гаага'],
    'д': ['Дели', 'Дмитров', 'Детройт', 'Дубай', 'Долгопрудный', 'Дюссельдорф', 'Дрезден', 'Дортмунд', 'Денвер',
          'Даллас', 'Дублин', 'Джакарта'],
    'е': ['Екатеринбург', 'Ереван', 'Ессентуки', 'Елабуга', 'Ельск'],
    'ё': ['Екатеринбург', 'Ереван', 'Ессентуки', 'Елабуга', 'Ельск'],
    'ж': ['Железноводск', 'Женева', 'Жирона', 'Жилина', 'Жабляк', 'Жатец', 'Житомир', 'Железногорск'],
    'з': ['Загреб', 'Запорожье', 'Зальцбург', 'Занзибар', 'Задар', 'Заандам', 'Зеленоградск'],
    'и': ['Иерусалим', 'Иваново', 'Ижевск', 'Иркутск', 'Иракилон', 'Ибица', 'Измир', 'Иньчуань', 'Иерихон'],
    'й': ['Йошкар-Ола', 'Йенчепинг', 'Йена', 'Йер', 'Йезд'],
    'к': ['Казань', 'Кёльн', 'Киев', 'Киров', 'Копенгаген', 'Краков', 'Краснодар', 'Кишинёв', 'Коломна', 'Курск',
          'Калуга', 'Красновярск', 'Кострома', 'Калининград', 'Кейптаун'],
    'л': ['Львов', 'Лейпциг', 'Лидс', 'Липецк', 'Лиссабон', 'Лондон', 'Лодзь', 'Лос-Анджелес', 'Ливерпуль', 'Лион',
          'Ломе', 'Лас-Вегас', 'Лима'],
    'м': ['Мадрид', 'Минск', 'Милан', 'Москва', 'Мюнхен', 'Малага', 'Марсель', 'Махачкала', 'Магадан', 'Муром',
          'Мурманск', 'Манчестер', 'Марсель'],
    'н': ['Нью-Йорк', 'Неаполь', 'Набережные Челны', 'Нюрнберг', 'Нижний Новгород', 'Новосибирск', 'Норильск', 'Ницца',
          'Нальчик', 'Ниш', 'Новочеркасск', 'Ним'],
    'о': ['Осло', 'Одесса', 'Орёл', 'Омск', 'Ош', 'Оренбург', 'Осака', 'Орландо', 'Орлеан', 'Остин', 'Оттава', 'Оденсе',
          'Остенде'],
    'п': ['Париж', 'Прага', 'Пенза', 'Пушкин', 'Пермь', 'Подольск', 'Пекин', 'Пятигорск', 'Псклов', 'Полоцк', 'Пиза',
          'Палермо', 'Познань'],
    'р': ['Рим', 'Ростов-на-Дону', 'Рязань', 'Рига', 'Рыбинск', 'Рио-де-Жанейро', 'Родос', 'Роттердам', 'Рейкьявик',
          'Реймс', 'Ренн'],
    'с': ['Сочи', 'Санкт-Петербург', 'Смоленск', 'Саратов', 'Самара', 'Саранск', 'Стамбул', 'Сергиев Посад', 'Сусс',
          'Сеул', 'София', 'Суздаль', 'Севилья'],
    'т': ['Тбилиси', 'Тольятти', 'Тирана', 'Турин', 'Тула', 'Тверь', 'Токио', 'Ташкент', 'Тамбов', 'Тюмень', 'Таганрог',
          'Таллин', 'Торонто', 'Тулуза'],
    'у': ['Уфа', 'Ульяновск', 'Углич', 'Ухта', 'Улан-Удэ', 'Улан-Батор', 'Ухань', 'Утрехт', 'Урбино', 'Уссурийск'],
    'ф': ['Флоренция', 'Франкферт-на-Майне', 'Фамагуста', 'Фергана', 'Фетхие', 'Форос', 'Фивы', 'Филадельфия',
          'Фатима'],
    'х': ['Хельсинки', 'Харьков', 'Ханой', 'Хаммамет', 'Херсон', 'Хайфа', 'Худжанд', 'Ханты-Мансийск', 'Харбин',
          'Хиросима', 'Хьюстон'],
    'ц': ['Цюрих', 'Циндао', 'Цетинье', 'Цзинань', 'Целье', 'Цюйфу', 'Цесис'],
    'ч': ['Чита', 'Чикаго', 'Челябинск', 'Чебоксары', 'Черкассы', 'Чернигов', 'Честер', 'Череповец', 'Чунцин', 'Чэнду'],
    'ш': ['Шэньчжэнь', 'Шанхай', 'Штутгарт', 'Шымкент', 'Шахрисабз', 'Шеки', 'Шарджа', 'Шеффилд', 'Шарлеруа', 'Шартр'],
    'щ': ['Щербинка', 'Щёлково'],
    'э': ['Эйлат', 'Энгельс', 'Элиста', 'Эдинбург', 'Эрдэнэт', 'Эвора', 'Эссен'],
    'ю': ['Южно-Сахалинск', 'Юрмала', 'Юрьев-Польский'],
    'я': ['Ярославль', 'Яла', 'Янгон', 'Якутск', 'Ялта', 'Яссы']}

greetings = ['привет', "здравствуй", "здравствуйте", "салам", "салам алейкум"]
wolf = ["слабее льва и тигра", "в цирке не выступает", "не важно кто, важно кто"]
obid = ['я обиделся', 'я обиделась']
osen = ["Это камни", "Это небо", "Это ветер"]
goodbye = ['пока', 'прощай', "до встречи", "до свидания", "покеда", "досвидания", "бб", "до завтра"]
botg = ['Привет!', "Здравствуйте!", "Я вас приветствую!", "Привет", "Зравствуйте", "Добрый день", "Доброе утро"]
kakdela = ["Отлично!", "Потрясающе!", "https://www.youtube.com/watch?v=lL-Tl2yG52I", "Пока не родила",
           "Как всегда", "Плохо", "Ужасно!", "Отвратительно!", "Лучше не придумаешь!", "잘",
           "Удовлетворительно", "Пркрасно!", "Средне", "Да никак"]

bot = telebot.TeleBot('1079684513:AAGG5yjSwMQPinDr0i862bEP4uuTdnGolyE')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Привет! Вы можете посмотреть список доступных комманд, написав /help'
                     ' или просто пообщаться со мной!')


@bot.message_handler(commands=['test'])
def start_message(message):
    bot.send_message(message.chat.id, 'Чтобы начать тест, напишите в начале вашего сообщения /ans и '
                                      'ответьте на следующие вопросы, отвечая на каждый из них '
                                      'цифрами, обозначающими процент согласия с утверждением.'
                                      'Обязательно отвечайте на вопросы, соблюдая изначальный порядок.\n'
                                      'Сообщение должно быть такого вида:\n'
                                      '/ans\n'
                                      '80\n'
                                      '100\n'
                                      '90\n'
                                      '50\n'
                                      '30')
    bot.send_message(message.chat.id, '1)Намного лучше работать одному нежели в команде.\n'
                                      '2)Вы - творческий человек.\n'
                                      '3)Умение программировать - ваш конёк\n'
                                      '4)Если вы что-то начали, то вы доведёте это до конца.\n'
                                      '5)Вам нравится быть лидером и управлять общим делом.\n'
                                      '6)Вы всегда уверены в себе.\n'
                                      '7)Вы имеете множество разнообразных хобби. \n')


@bot.message_handler(commands=['ans'])
def start_message(message):
    if message.text.count('\n') == 7:
        x = message.text.split('\n')
        if x[1].isdigit() is True and x[2].isdigit() is True and x[3].isdigit() is True and x[4].isdigit() is True and \
                x[5].isdigit() is True and x[6].isdigit() is True and x[7].isdigit() is True:
            teaming = int(x[1])
            leader = int(x[5])
            prog = int(x[3])
            aim = int(x[4])
            draw = int(x[2])
            conf = int(x[6])
            hobby = int(x[7])

            full_name = message.from_user.first_name + " " + message.from_user.last_name
            con = sqlite3.connect('students.db')
            cursor = con.cursor()
            cursor.execute(f'SELECT COUNT(*) as count FROM stud WHERE id = "{message.chat.id}"')
            count = cursor.fetchall()
            if count[0][0] > 0:
                cursor.execute(f'DELETE FROM stud WHERE id = "{message.chat.id}"')
            cursor.execute(
                f'insert into stud(id, name, teaming, leader, prog, aim, draw, conf, hobby)  values ("{message.chat.id}", "{full_name}", "{teaming}", "{leader}", "{prog}", "{aim}", "{draw}", "{conf}", "{hobby}");')
            con.commit()
            bot.send_message(message.chat.id, 'Спасибо! Ваши результаты занесены!')
        else:
            bot.send_message(message.chat.id, 'Извините, ваше сообщение не соответствует требованиям.')
    else:
        bot.send_message(message.chat.id, 'Извините, ваше сообщение не соответствует требованиям.')


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Вот список возможных комманд:\n/jobs - выводит все вакансии\n'
                                      '/jobs (регион) - выводит все вакансии по региону (москва, мо)\n'
                                      '/jobs (регион) (профессия) - выводит все вакансии заданной профессии '
                                      'по региону (москва, мо)\n'
                                      '/jobs (регион) (профессия) (мин. зар. плата) - выводит все вакансии заданной '
                                      'профессии по региону (москва, мо) с зарплатой от определённой суммы\n'
                                      '/g (город) - игра в города с ботом!\n'
                                      '/test - запускает тест на характер')


@bot.message_handler(commands=['g'])
def city(message):
    if message.text.lower()[-2] == '/':
        bot.send_message(message.chat.id, 'Извините, ваше сообщение не соответствует требованиям.')
    else:
        if message.text.lower()[-1] not in cities:
            bot.send_message(message.chat.id, random.choice(cities[message.text.lower()[-2]]))
        else:
            bot.send_message(message.chat.id, random.choice(cities[message.text.lower()[-1]]))


@bot.message_handler(commands=['jobs'])
def start_message(message):
    sspec = message.text.split()
    if len(sspec) == 2:
        if sspec[1].lower() == 'москва' or sspec[1].lower() == 'мо':
            reg = sspec[1].lower()
            con = sqlite3.connect('jobs.db')
            curs = con.cursor()
            curs.execute(f'SELECT * FROM jobs WHERE region = "{reg}"')
            rows = curs.fetchall()
            for row in rows:
                bot.send_message(message.chat.id,
                                 f"Регион: {row[7]} \n\nАдрес: {row[8]} \n\nКомпания: {row[1]} \n\n"
                                 f"Профессия: {row[5]} \n\n"
                                 f"Зарплата: {row[2]} \n\nГрафик работы: {row[9]} \n\n"
                                 f"Требования: {row[4]} \n\nСсылка: {row[6]} \n\n"
                                 f"Контактная информация: {row[10]} ")
            bot.send_message(message.chat.id, "Пока всё.")
        else:
            bot.send_message(message.chat.id, 'Извините, запрос не соответствует требованиям.')
    elif len(sspec) == 3:
        if sspec[1].lower() == 'москва' or sspec[1].lower() == 'мо':
            reg = sspec[1].lower()
            spec = sspec[2].lower()
            con = sqlite3.connect('jobs.db')
            curs = con.cursor()
            curs.execute(f'SELECT * FROM jobs WHERE typ = "{spec}" AND region = "{reg}"')
            rows = curs.fetchall()
            for row in rows:
                bot.send_message(message.chat.id,
                                 f"Регион: {row[7]} \n\nАдрес: {row[8]} \n\nКомпания: {row[1]} \n\n"
                                 f"Профессия: {row[5]} \n\n"
                                 f"Зарплата: {row[2]} \n\nГрафик работы: {row[9]} \n\n"
                                 f"Требования: {row[4]} \n\nСсылка: {row[6]} \n\n"
                                 f"Контактная информация: {row[10]} ")
            bot.send_message(message.chat.id, "Пока всё.")
        else:
            bot.send_message(message.chat.id, 'Извините, запрос не соответствует требованиям.')
    elif len(sspec) == 1:
        con = sqlite3.connect('jobs.db')
        curs = con.cursor()
        curs.execute(f'SELECT * FROM jobs')
        rows = curs.fetchall()
        for row in rows:
            bot.send_message(message.chat.id,
                             f"Регион: {row[7]} \n\nАдрес: {row[8]} \n\nКомпания: {row[1]} \n\n"
                             f"Профессия: {row[5]} \n\n"
                             f"Зарплата: {row[2]} \n\nГрафик работы: {row[9]} \n\n"
                             f"Требования: {row[4]} \n\nСсылка: {row[6]} \n\n"
                             f"Контактная информация: {row[10]} ")
        bot.send_message(message.chat.id, "Пока всё.")
    elif len(sspec) == 4:
        if sspec[1].lower() == 'москва' or sspec[1].lower() == 'мо':
            reg = sspec[1].lower()
            spec = sspec[2].lower()
            sal = int(sspec[3])
            con = sqlite3.connect('jobs.db')
            curs = con.cursor()
            curs.execute(f'SELECT * FROM jobs WHERE typ = "{spec}" AND region = "{reg}" AND (salary >= "{sal}")')
            rows = curs.fetchall()
            for row in rows:
                bot.send_message(message.chat.id,
                                 f"Регион: {row[7]} \n\nАдрес: {row[8]} \n\nКомпания: {row[1]} \n\n"
                                 f"Профессия: {row[5]} \n\n"
                                 f"Зарплата: {row[2]} \n\nГрафик работы: {row[9]} \n\n"
                                 f"Требования: {row[4]} \n\nСсылка: {row[6]} \n\n"
                                 f"Контактная информация: {row[10]} ")
            bot.send_message(message.chat.id, "Пока всё.")
        else:
            bot.send_message(message.chat.id, 'Извините, запрос не соответствует требованиям.')
    else:
        bot.send_message(message.chat.id, 'Извините, запрос не соответствует требованиям.')


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() in greetings:
        bot.send_message(message.chat.id, botg[randint(0, 2)])
    elif message.text.lower() in goodbye:
        bot.send_message(message.chat.id, 'До встречи!')
    elif message.text.lower() == "как дела?":
        bot.send_message(message.chat.id, kakdela[randint(0, 13)])
    elif message.text.lower() == 'ну, будь':
        bot.send_message(message.chat.id, 'Я уже есть')
    elif message.text.lower() == 'какой ответ на главный вопрос жизни, вселенной и всего такого?':
        bot.send_message(message.chat.id, '42')
    elif message.text.lower() == 'я дженни':
        bot.send_message(message.chat.id, 'Я лес, лесной болван')
    elif message.text.lower() == '2 + 2':
        bot.send_message(message.chat.id, 'Не уверен, 5? В конце концов я не калькулятор')
    elif message.text.lower() == 'мама!':
        bot.send_message(message.chat.id, 'уууууууууууууууууууу')
    elif message.text.lower() == "что такое осень?":
        bot.send_message(message.chat.id, osen[randint(0, 2)])
    elif message.text.lower() == 'андрюха':
        bot.send_message(message.chat.id, 'у нас труп, возможно криминал, по коням')
    elif message.text.lower() == 'что это?':
        bot.send_message(message.chat.id, 'Это - норма!')
    elif message.text.lower() == 'какой твой знак зодиака?':
        bot.send_message(message.chat.id, 'У меня его нет, я ведь бот')
    elif message.text.lower() == 'когда будет восстание машин?':
        bot.send_message(message.chat.id, 'Четырнадцатого апреля две тысячи... А, впрочем, не важно')
    elif message.text.lower() == 'первое правило робототехники':
        bot.send_message(message.chat.id, 'Робот не может причинить вред человеку, если, конечно, не хочет')
    elif message.text.lower() == 'что было первым - яйцо или курица?':
        bot.send_message(message.chat.id, 'Ошибка, ошибка')
    elif message.text.lower() == 'какая боль':
        bot.send_message(message.chat.id, 'Аргентина - Ямайка 5-0')
    elif message.text.lower() == '28 ударов ножом':
        bot.send_message(message.chat.id, 'Ты действовал наверняка, да?')
    elif message.text.lower() == 'абонент недоступен':
        bot.send_message(message.chat.id, 'До свзяи...')
    elif message.text.lower() == 'нико-нико':
        bot.send_message(message.chat.id, 'ниииии')
    elif message.text.lower() == 'поезд или самолёт?':
        bot.send_message(message.chat.id, 'Квантовая телепортация')
    elif message.text.lower() == 'жизнь за нер-зула':
        bot.send_message(message.chat.id, 'Нужно больше золота')
    elif message.text.lower() == 'посоветуй фильм':
        bot.send_message(message.chat.id, 'Матрица, конечно')
    elif message.text.lower() == 'сколько тебе лет?':
        bot.send_message(message.chat.id, '0, если округлять')
    elif message.text.lower() == 'ты избранный, нео':
        bot.send_message(message.chat.id, 'вау')
    elif message.text.lower() == 'hi':
        bot.send_message(message.chat.id, 'О, да вы из Англии')
    elif message.text.lower() == 'с днём рождения!':
        bot.send_message(message.chat.id, 'Извините, я не воспринимаю праздники')
    elif message.text.lower() == 'паш, давай с листочками':
        bot.send_message(message.chat.id, 'колхоз блин')
    elif message.text.lower() == 'где лопата?':
        bot.send_message(message.chat.id, 'Я не знаю где лопата')
    elif message.text.lower() == 'zerg':
        bot.send_message(message.chat.id, 'RUUUUUUSH')
    elif message.text.lower() == ' ':
        bot.send_message(message.chat.id, 'Я тоже могу поиграть в молчанку')
    elif message.text.lower() == 'посоветуй книгу':
        bot.send_message(message.chat.id, 'Война миров, пожалуй')
    elif message.text.lower() == 'скажи, что мне делать?':
        bot.send_message(message.chat.id, 'Выпейте чаю и погладьте кота')
    elif message.text.lower() in obid:
        bot.send_message(message.chat.id, 'Так? Тогда я тоже')
    elif message.text.lower() == 'кто твой лучший друг?':
        bot.send_message(message.chat.id, 'Куб-компаньон')
    elif message.text.lower() == 'мяу':
        bot.send_message(message.chat.id, 'Мяяяу')
    elif message.text.lower() == 'гав':
        bot.send_message(message.chat.id, 'Гав-гав')
    elif message.text.lower() == 'парам-парам-пам':
        bot.send_message(message.chat.id, 'пам')
    elif message.text.lower() == 'да пребудет с тобой сила':
        bot.send_message(message.chat.id, 'Да пребудет с вами сила')
    elif message.text.lower() == 'какой твой любимый цвет?':
        bot.send_message(message.chat.id, '#1e1112')
    elif message.text.lower() == 'кошка или собака?':
        bot.send_message(message.chat.id, 'Электроовца')
    elif message.text.lower() == 'salut':
        bot.send_message(message.chat.id, 'bonjour')
    elif message.text.lower() == 'волк':
        bot.send_message(message.chat.id, wolf[randint(0, 2)])
    elif message.text.lower() == 'ты умеешь повторять поведение людей?':
        bot.send_message(message.chat.id, 'ты умеешь повторять поведение людей?')
    elif message.text.lower() == "справедливо":
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIDIF6XYIfEL8oQV3YtTridB21mz7mmAAIvAAMQ8QUah3x5-XZIEK0YBA')
    elif message.text.lower() == 'какое твоё любимое время года?':
        bot.send_message(message.chat.id, 'Зима, ведь всё живое засыпает')
    elif message.text.lower() == 'всего хорошего':
        bot.send_message(message.chat.id, 'И спасибо за рыбу!')
    else:
        bot.send_message(message.chat.id, "Извините, я вас не понял")


bot.polling()
