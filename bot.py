from flask import Flask, request, abort
import telebot
from telebot import types
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

API_TOKEN = os.environ.get('API_TOKEN')
if not API_TOKEN:
    logging.error("Токен бота не найден.")
    raise ValueError("Токен бота не найден.")

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    WEBHOOK_URL = 'https://' + RENDER_EXTERNAL_HOSTNAME
else:
    WEBHOOK_URL = 'https://pearplerus-render.onrender.com'
    logging.warning("RENDER_EXTERNAL_HOSTNAME не установлен, используется дефолтный WEBHOOK_URL")

# Инициализация telebot для webhook (threaded=False, parse_mode='HTML')
bot = telebot.TeleBot(API_TOKEN, threaded=False, parse_mode='HTML')

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello, this is your Telegram bot!"


user_data = {}


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        if request.headers.get('content-type') == 'application/json':
            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return 'ok', 200
        else:
            abort(403)
    except Exception as err:
        logging.exception(f"Ошибка в webhook: {err}")
        return 'error', 500


if __name__ == '__main__':


    @bot.message_handler(commands=['start'])
    def start(message):
        text = (
            "Сегодня вы отправитесь в опасное, таинственное приключение по старинным "
            "местам города Барнаула, тайны которого тщательно охраняются призраками прошлого. В Барнауле много мистичес"
            "ких мест, где можно встретить привидения. Привидения Барнаула вполне дружелюбны и очень коммуникабельны, "
            "по ночам любят открывать холодильники в поисках чего-то вкусненького, отключать Интернет, прятать носки и"
            " вводить горожан в состояние временной амнезии."
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('В путь!', callback_data='v put'))
        markup.add(types.InlineKeyboardButton('Ни дня без приключений!', callback_data='v put'))
        markup.add(types.InlineKeyboardButton('Ой, что-то я боюсь...', callback_data='otkaz'))
        bot.send_message(message.chat.id, text, reply_markup=markup)


    @bot.callback_query_handler(func=lambda call: True)
    def answer(call):
        if call.data == 'v put':
            text = (
                "Вы пройдёте по следам барнаульских привидений и разгадаете их "
                "послания из прошлого. Только в этом случае вы получите настоящее письмо из прошлого и сможете усмирить"
                " разыгравшихся духов. Вы готовы отправиться в мистическое путешествие?"
            )
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup_inline = types.InlineKeyboardMarkup()
            first_arg = types.InlineKeyboardButton(text="Всегда готов!", callback_data='put2')
            sec_arg = types.InlineKeyboardButton(text="Вперёд за привидениями!", callback_data="put2")
            third_arg = types.InlineKeyboardButton(text="Может, не надо...", callback_data="otkaz")
            markup_inline.add(first_arg)
            markup_inline.add(sec_arg)
            markup_inline.add(third_arg)
            bot.send_message(call.message.chat.id, text, reply_markup=markup_inline)
        elif call.data == 'otkaz':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, 'Расходимся! Здесь кто-то боится привидений!')
        elif call.data == "put2":
            photo = open('img/svo.jpg', 'rb')
            text = (
                'Тогда следуйте подсказкам от привидений, которые будут появляться в этом мистическом сервисе. '
                'Отправляйтесь к старту нашего приключения – на старейшую площадь города, ровесницу Барнаула, которая '
                'много лет была административным и культурным центром города. Свое историческое название – Соборная – '
                'площадь утратила в 1917 году. Главная достопримечательность площади – Петропавловский собор – была '
                'разрушена в 1935 году. Напишите современное название этой площади.'
            )
            bot.send_photo(call.message.chat.id, photo, caption=text)
            user_data[call.message.chat.id] = "waiting_for_message_one"
        elif call.data == 'cmh':
            photo = open('img/meria.jpg', 'rb')
            text = (
                'Сфотографируйтесь так, чтобы на заднем плане вашего селфи был виден деревянный фасад бывшего '
                'Управления Алтайского горного округа. Это деревянное здание было построено в 1898 году в стиле '
                'классицизма, с его любовью к симметрии, строгим геометрическим формам, к светлым пилястрам, '
                'разделяющим фасад. '
            )
            markup_inline = types.InlineKeyboardMarkup()
            first_arg = types.InlineKeyboardButton(text="Я сделал!", callback_data='one')
            markup_inline.add(first_arg)
            bot.send_photo(call.message.chat.id, photo, caption=text, reply_markup=markup_inline)
        elif call.data == 'one':
            photo = open('img/miller.jpg', 'rb')
            text = (
                "Вы находитесь в самом мистическом, самом таинственном месте старин"
                "ного горного города Барнаула. Здесь до сих пор обитают привидения, которые тщательно хранят тайны "
                "прошлого."
                " Одной из самых загадочных историй Барнаула является история аптекаря, который, по преданиям, изготовил"
                " эликсир "
                "жизни. Говорят, что вместе со своей юной дочерью он действительно стал бессмертным и их тени до сих пор "
                "можно"
                "увидеть на этой улице. Расшифруйте имя аптекаря, и он приведет вас к месту своей работы. \n"
                "23-18-10-19-20-10-1-15 14-10-13-13-6-18."
            )
            bot.send_photo(call.message.chat.id, photo, caption=text)
            user_data[call.message.chat.id] = "waiting_for_message_1"
        elif call.data == 'z3':
            photo = open('img/apteka.jpg', 'rb')
            text = "Место назначения - ул.Ползунова 42, Горная Аптека."
            markup_inline = types.InlineKeyboardMarkup()
            first_arg = types.InlineKeyboardButton(text="Я здесь!", callback_data='lida')
            markup_inline.add(first_arg)
            bot.send_photo(call.message.chat.id, photo, caption=text, reply_markup=markup_inline)
        elif call.data == 'lida':
            text = (
                "Христиан Миллер жил и работал в здан"
                "ии Горной Аптеки. Сейчас здесь создан туристический центр с музеем, рестораном и магазином, а 200 лет "
                "назад "
                "здесь производились лекарства. Раньше Барнаул был центром фармацевтической деятельности, и лекарства "
                "отсюда по"
                "ставлялись по всей губернии. При реконструкции аптеки в 2010 году здесь были обнаружены таинственные "
                "подземелья"
                ", в которых были спрятаны различные аптечные склянки и ампулы с неизвестной жидкостью. Кто знает, может"
                " это и "
                "есть тот самый эликсир жизни? Вы можете заглянуть в музей и убедиться в этом самостоятельно. Стоимость"
                " билета 80 рублей."
            )
            bot.send_message(call.message.chat.id, text)
            photo = open('img/street.jpg', 'rb')
            text = (
                "Сейчас, Христиан Миллер и его дочь приглашают  вас прогуляться по "
                "Петропаловской улице. Так она называлась раньше, а вот новое название улицы связано и известным " 
                "барнаульским изобретателем, разработчиком первой паровой машины.\nВопрос: Как называется Петропавловская "
                "улица сейчас?"
            )
            bot.send_photo(call.message.chat.id, photo, caption=text)
            user_data[call.message.chat.id] = "waiting_for_message_2"
        elif call.data == 'z4':
            photo = open('img/museum.jpg', 'rb')
            text = (
                "Призраки прошлого приглашают вас разгадать следующую загадку. Най"
                "ти ее можно у здания Горной лаборатории – главной химической лаборатории Алтайских заводов. Именно здесь"
                " проводились анализы добытых на рудниках сплавов серебра, меди и золота до их отправки в Санкт-Петербург. "
                "Это каменное здание было построено в 1851 году (172 года назад!), а узнать его можно по пяти высаженным "
                "перед фасадом деревьям маньчжурского ореха.\nВопрос: Что в настоящий момент находится в здании Горной"
                " лаборатории?"
            )
            bot.send_photo(call.message.chat.id, photo, caption=text)
            user_data[call.message.chat.id] = "waiting_for_message_3"
        elif call.data == 'z5':
            photo = open('img/demid.jpg', 'rb')
            text = (
                "Вы находитесь у краеведческого музея, который в 2023 году отмечает "
                "свое 200летие. Но изначально на этом месте была горная лаборатория, в которой производился химический "
                "анализ "
                "добытой руды и выплавленных металлов. Горная лаборатория появилась гораздо позже строительства самого"
                " завода,"
                " появление которого тесно связывают с историей появления Барнаула.  Имя какого российского предпринимателя"
                ", о"
                "снователя горнодобывающей промышленности на Урале и в Сибири, связано с основанием города Барнаула?\n"
                "Площадь"
                ", в центральной части которого установлен столп в честь 100-летия горнорудного дела на Алтае, названа "
                "в его честь."
            )
            bot.send_photo(call.message.chat.id, photo, caption=text)
            user_data[call.message.chat.id] = "waiting_for_message_4"
        elif call.data == 'z6':
            photo = open('img/stolp.jpg', 'rb')
            text = (
                "Самым мистическим и одновременно величественным местом города по п"
                "раву считается Демидовская площадь. Это место, где до сих пор ощущается тень демидовского проклятья. "
                "Акинфий Дем"
                "идов никогда не был на Алтае, но здесь его хорошо знают и чтут, бережно сохраняя образ родоначальника "
                "алтайской"
                " промышленности в памяти поколений. Именно его усилиями был основан Барнаул, второй в России (после "
                "Екатеринб"
                "урга) горный город, и новый источник государственной казны. Перед смертью Акинфий Демидов проклял Барнаул"
                " и всех его жителей. В чем же заключается это проклятье? И как с ним справиться?"
            )
            bot.send_photo(call.message.chat.id, photo, caption=text)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Открыть видео", url="https://www.youtube.com/watch?v=5N9eUgfcL90"))
            text = (
                "Прослушайте историю создания Демидовской площади и ответьте на "
                "вопрос: Что помогло справиться с проклятьем Демидова?"
            )
            bot.send_message(call.message.chat.id, text, reply_markup=markup)
            user_data[call.message.chat.id] = "waiting_for_message_5"
        elif call.data == 'z7':
            photo = open('img/alex_1.jpg', 'rb')
            text = (
                "Существует примета: если обойти Демидовский столп три раза и кажд"
                "ый раз оставлять у его основания по монете, вы можете стать богатым человеком. Только имейте в виду, что"
                " богат"
                "ство каждый понимает по-своему! Обойдите вокруг столпа три раза да смотрите внимательно! В царствование"
                " какого"
                " императора был установлен этот памятник в честь 100-летия горнорудного дела на Алтае.\nНапишите в чат "
                "имя этого российского императора"
            )
            bot.send_photo(call.message.chat.id, photo, caption=text)
            user_data[call.message.chat.id] = "waiting_for_message_6"
        elif call.data == 'z8':
            photo = open('img/silver.jpg', 'rb')
            text = (
                "В 1771 году Барнаул получил статус «Горный город» и все здания и "
                "сооружения, которые строились здесь для целей горнорудного производства. Так здесь на Демидовской площади"
                " появ"
                "ились горное училище, горный госпиталь, богадельня для инвалидов Сереброплавильного завода. Приглядитесь"
                " внимат"
                "ельнее, все здания похожи друг на друга по архитектуре: двухэтажные, приземистые, с прочным фундаментом, "
                "наверн"
                "яка они могут выдержать даже очень сильное землетрясение. Все они создавались питерским архитектором. "
                "Недаром "
                "это место называют уголком Петербурга. \nВопрос: Что находилось на месте Демидовской площади 300 лет "
                "назад? По"
                "говаривают, что именно там спрятано около 700 килограммов чистого серебра времен Акинфия Демидова."
            )
            bot.send_photo(call.message.chat.id, photo, caption=text)

            user_data[call.message.chat.id] = "waiting_for_message_7"
        elif call.data == 'z9':
            text = (
                "Согласно легендам, серебро в Барнауле не только глубоко под землей"
                ", но и на поверхности. Фактически мы ходим по улицам, усыпанным серебром. Почему? Раньше центральные улицы"
                " Барн"
                "аула мостили шлаком, остававшимся после переработки серебра. Но так как технологический процесс был "
                "несовершене"
                "н, в шлаке оставались частички драгоценного металла. \nРасшифруйте послание тени Демидова – это "
                "первоначальное " 
                "название завода  – и сам Демидов проводит вас к уникальному историческому памятнику, построенному в "
                "1739 году."
            )
            bot.send_message(call.message.chat.id, text)
            text = (
                "VTLTGKFDBKMYSQPFDJL"
            )
            bot.send_message(call.message.chat.id, text)
            user_data[call.message.chat.id] = "waiting_for_message_8"
        elif call.data == 'z10':
            text = (
                "Отлично! Вы отправляетесь на территорию известнейшего сереброплав"
                "ильного завода. На самом деле завод изначально был предназначен для выплавки меди, а после обнаружения в "
                "алтайс"
                "кой руде серебра в 1746 году был переоборудован для выплавки серебра и стал крупнейшим сереброплавильным"
                " заводом Сибири."
            )
            bot.send_message(call.message.chat.id, text)
            photo = open('img/mirror.jpg', 'rb')
            text = (
                "Закройте глаза… Прислушайтесь… Говорят, что души рабочих этого зав"
                "ода до сих пор не могут покинуть этого места и по сей день бродят по заводу. По вечерам здесь появляется"
                " тень "
                "мужчины в темных одеждах. Возможно, это дух самого Акинфия Демидова, которому изначально и принадлежали"
                " эти з"
                "аводы. Поговаривают, что при жизни Демидов спрятал немало монет из серебра в вырытых под заводом штольнях"
                " и се"
                "йчас пытается защитить его от посторонних глаз. А какой предмет издревле связывали с потусторонним миром?"
            )
            bot.send_photo(call.message.chat.id, photo, caption=text)
            photo = open('img/spich.jpg', 'rb')
            text = (
                "Найдите этот предмет, он поможет вам ответить на вопрос Акинфия "
                "Демидова, что располагалось в этом здании в советские годы. То, что так тревожит души рабочих завода..."
                "\nАКИРБАФЯАНЧЕЧИПСЯАКСЬЛУАНРАБ"
            )
            bot.send_photo(call.message.chat.id, photo, caption=text)
            user_data[call.message.chat.id] = "waiting_for_message_9"
        elif call.data == 'z11':
            photo = open('img/phil.jpg', 'rb')
            text = (
                "Жители Барнаула всегда трудились на славу, любили и отдохнуть. Воз"
                "вращайтесь на улицу известного изобретателя и отправляйтесь к красивому зданию, построенному в "
                "псевдорусском ст"
                "иле более 100 лет назад. Количество окон на фасаде этого здания указывает на год постройки. Узнайте, "
                "что находи"
                "тся в этом здании в настоящее время."
            )
            bot.send_photo(call.message.chat.id, photo, caption=text)
            user_data[call.message.chat.id] = "waiting_for_message_10"
        elif call.data == 'z12':
            photo1 = open('img/img.png', 'rb')
            text = (
                "Здесь проводили балы, концерты, собрания, ставили спекта"
                "кли. Но и это красивое здание не обходится без тайн и загадок. До 1900 года здесь находилось совсем другое"
                " соор"
                "ужение. Разгадайте ребус – послание от призраков прошлого – и узнайте, на фундаменте какого здания был "
                "построен Народный Дом."
            )
            bot.send_photo(call.message.chat.id, photo1, caption=text)
            user_data[call.message.chat.id] = "waiting_for_message_11"
        elif call.data == 'z13':
            text = (
                "Постепенно Барнаул становился крупным промышленным городом, местом "
                "притяжения переселенцев со всей Российской Империи. Некоторые улицы сохраняют в своем названии "
                "исторические ге"
                "ографические названия, однако многие улицы были переименованы. Например, Московский проспект стал "
                "проспектом Л"
                "енина, Тобольская – улицей Льва Толстого, Томская улица – улицей Короленко, Иркутская – улицей Пушкина. "
                "Однако "
                "одна из таких улиц сохранила свое историческое название. Это одна из старейших улиц города, расположена у "
                "бер"
                "егов реки Барнаулки. Поселенцы – известные в те времена работники в части металлургии - прибыли сюда из "
                "Олоне"
                "цкого края, с реки Олонси (это район между Ладожским и Онежским озерами, в Карелии). Сейчас существуют "
                "две ул"
                "ицы  – Большая и Малая – сохранившие это название. Эти улицы хранят тайны прошлого и не спешат с ними "
                "расстав"
                "аться. Найдите на карте эти улицы и вы получите послание от привидений.\nНапишите в чат название улиц"
            )
            bot.send_message(call.message.chat.id, text)
            user_data[call.message.chat.id] = "waiting_for_message_12"
        elif call.data == 'z14':
            photo1 = open('img/img_3.jpg', 'rb')
            text = (
                "На Большой улице, где во времена Акинфия Демидова прожива"
                "ли выходц"
                "ы с русского севера, вам предстоит отыскать еще один дом с привидениями.  Номер этого дома вы узнаете, "
                "решив головоломку."
            )
            bot.send_photo(call.message.chat.id, photo1, caption=text)
            user_data[call.message.chat.id] = "waiting_for_message_13"
        elif call.data == 'z15':
            photo = open('img/38.jpg', 'rb')
            text = (
                "На этом месте по адресу Большая Олонская 38 стоял дом купца Зубова"
                ", где во время своей сибирской ссылки часто бывал известный русский писатель Федор Михайлович "
                "Достоевский. Возм"
                "ожно, их тени из прошлого до сих пор живут в этом доме.\nВозможно, их тени можно встретить и в самом "
                "мистическом "
                "и неоднозначном месте города. Расшифруйте его название, и смело отправляйтесь на встречу с привидениями!"
            )
            bot.send_photo(call.message.chat.id, photo, caption=text)
            text = (
                "ОБДПСОЬКРБСЛ"
            )
            bot.send_message(call.message.chat.id, text)
            user_data[call.message.chat.id] = "waiting_for_message_14"
        elif call.data == 'z16':
            photo = open('img/park.jpg', 'rb')
            text = (
                "Вы находитесь у подножия Нагорного парка – самого неоднозначного"
                " места в городе. В 1772 году было принято решение об открытии в этом месте Нагорного кладбища. За полтора "
                "века "
                "здесь были похоронены многие известные горожане, учёные, общественные деятели, купцы, исследователи Алтая."
                " Поднявшись по лестнице и сосчитав количество пролётов, вы вспомните и навсегда запомните год основания "
                "Барнаула в 18 веке."
            )
            markup_inline = types.InlineKeyboardMarkup()
            first_arg = types.InlineKeyboardButton(text="ОК", callback_data='ok1')
            markup_inline.add(first_arg)
            bot.send_photo(call.message.chat.id, photo, caption=text, reply_markup=markup_inline)
        elif call.data == 'ok1':
            text = (
                "Нагорный парк бережно хранит историю города. Здесь нашли вечный п"
                "окой известный русский публицист, писатель, исследователь Алтая Николай Ядринцев (его именем названы улицы"
                " в "
                "Барнауле, Омске, Новосибирске, Иркутске);  врач, выдающийся естествоиспытатель, географ, исследователь "
                "Алтая, "
                "член-корреспондент РАН Фридрих Геблер (его именем назван переулок в Барнауле и самый большой ледник горы "
                "Белух"
                "а), русский общественный деятель, народный просветитель Василий Штильке и многие другие."
            )
            markup_inline = types.InlineKeyboardMarkup()
            first_arg = types.InlineKeyboardButton(text="ОК", callback_data='ok2')
            markup_inline.add(first_arg)
            bot.send_message(call.message.chat.id, text, reply_markup=markup_inline)
        elif call.data == 'ok2':
            photo = open('img/grave.jpg', 'rb')
            text = (
                "Найдите восстановленную могилу горного инженера, изобретателя-меха"
                "ника, гидротехника Козьмы Фролова. Именно он с середины 18 века возглавлял все золотые промыслы на Урале "
                "и в Си"
                "бири, был руководителем работ на всех рудниках Алтая. У могилы Козьмы Фролова вы и получите послание от "
                "призраков прошлого."
            )
            markup_inline = types.InlineKeyboardMarkup()
            first_arg = types.InlineKeyboardButton(text="Я здесь!", callback_data='ok3')
            markup_inline.add(first_arg)
            bot.send_photo(call.message.chat.id, photo, caption=text, reply_markup=markup_inline)
        elif call.data == 'ok3':
            photo = open('img/leter.jpg', 'rb')
            text = (
                'Дорогiя потомки! '
                'На бѣрѣгу этой замѣчатѣльной рѣки мы построили чудѣсный городъ. ' 
                'Завѣщаемъ вамъ хранiть и обѣрѣгать богатства нашаго крыя. '
                'Помнiтѣ о насъ, мы вложили свою душу въ этотъ город. '
                'Хранiтѣ исторiю, чтитѣ своихъ прѣдковъ! '
                'Мы ѻбѣщаѥмъ больше не тревожить жителей города и бꙋдемъ помогать прїꙋмножать ваше богатство! '
            )
            bot.send_photo(call.message.chat.id, photo, caption=text)
            user_data[call.message.chat.id] = "waiting_for_message_15"

        bot.answer_callback_query(call.id)


    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        global user_data
        chat_id = message.chat.id
        if user_data.get(chat_id) == "waiting_for_message_1":
            if (message.text.lower()).strip() == "христиан миллер":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Идём дальше!", callback_data="z3"))
                markup.add(types.InlineKeyboardButton(text="Всё! По домам!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Верно! привидения на вашей стороне!', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Неправильный ответ! Видимо, привидения не на вашей стороне...")
        elif user_data.get(chat_id) == "waiting_for_message_2":
            if (message.text.lower()).strip() == "ползунова":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Идём дальше!", callback_data="z4"))
                markup.add(types.InlineKeyboardButton(text="Всё! По домам!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Верно! привидения на вашей стороне!', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(message.chat.id, 'Неправильный ответ! Видимо, привидения не на вашей стороне...')
        elif user_data.get(chat_id) == "waiting_for_message_one":
            if (message.text.lower()).strip() == "площадь свободы":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Идём дальше!", callback_data="cmh"))
                markup.add(types.InlineKeyboardButton(text="Всё! По домам!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Верно! привидения на вашей стороне!', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(message.chat.id, 'Неправильный ответ! Видимо, привидения не на вашей стороне...')
        elif user_data.get(chat_id) == "waiting_for_message_3":
            if (message.text.lower()).strip() == "алтайский государственный краеведческий музей" or \
                    (message.text.lower()).strip() == "краеведческий музей" or (message.text.lower()).strip() == "агкм":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Идём дальше!", callback_data="z5"))
                markup.add(types.InlineKeyboardButton(text="Всё! По домам!", callback_data="otkaz"))
                text = (
                    'Верно! привидения на вашей стороне! Ваш путь лежит к Горной Аптеке'
                    ' на улицу Ползунова дом 42.'
                )
                bot.send_message(message.chat.id, text, reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Неправильный ответ! Видимо, привидения не на вашей стороне...")
        elif user_data.get(chat_id) == "waiting_for_message_4":
            if (message.text.lower()).strip() == "демидов":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Идём дальше!", callback_data="z6"))
                markup.add(types.InlineKeyboardButton(text="Всё! По домам!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Верно! привидения на вашей стороне!', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Неправильный ответ! Видимо, привидения не на вашей стороне...")
        elif user_data.get(chat_id) == "waiting_for_message_5":
            if (message.text.lower()).strip() == "строительство демидовского столпа" or \
                    (message.text.lower()).strip() == "демидовский столп" or (message.text.lower()).strip() == "агкм":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Идём дальше!", callback_data="z7"))
                markup.add(types.InlineKeyboardButton(text="Всё! По домам!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Верно! привидения на вашей стороне!', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Неверно. Послушайте ещё раз про историю создания Демидовской площади")
        elif user_data.get(chat_id) == "waiting_for_message_6":
            if (message.text.lower()).strip() == "александр 1" or (message.text.lower()).strip() == 'александр первый':
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Идём дальше!", callback_data="z8"))
                markup.add(types.InlineKeyboardButton(text="Всё! По домам!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Верно! привидения на вашей стороне!', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Неправильный ответ! Видимо, привидения не на вашей стороне...")
        elif user_data.get(chat_id) == "waiting_for_message_7":
            if (message.text.lower()).strip() == "искусственное озеро" or (message.text.lower()).strip() == 'болото':
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Идём дальше!", callback_data="z9"))
                markup.add(types.InlineKeyboardButton(text="Всё! По домам!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Верно! привидения на вашей стороне!.', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Неправильный ответ! Видимо, привидения не на вашей стороне...")
        elif user_data.get(chat_id) == "waiting_for_message_8":
            if (message.text.lower()).strip() == "медеплавильный завод":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Идём дальше!", callback_data="z10"))
                markup.add(types.InlineKeyboardButton(text="Всё! По домам!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Верно! привидения на вашей стороне!.', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Неправильный ответ! Видимо, привидения не на вашей стороне...")
        elif user_data.get(chat_id) == "waiting_for_message_9":
            if (message.text.lower()).strip() == "барнаульская спичечная фабрика":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Идём дальше!", callback_data="z11"))
                markup.add(types.InlineKeyboardButton(text="Всё! По домам!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Верно! Привидения на вашей стороне!', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Неправильный ответ! Видимо, привидения не на вашей стороне...")
        elif user_data.get(chat_id) == "waiting_for_message_10":
            if (message.text.lower()).strip() == "филармония" or (message.text.lower()).strip() == "государственная филарм\
            ония алтайского края":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Идём дальше!", callback_data="z12"))
                markup.add(types.InlineKeyboardButton(text="Всё! По домам!", callback_data="otkaz"))
                text = (
                    'Всё верно. Государственная филармония Алтайского края. 17 декабря '
                    '1900 года здесь был открыт Народный дом, который очень быстро стал центром культурно-просветительской'
                    ' жизни города.'
                )
                bot.send_message(message.chat.id, text, reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Неправильный ответ! Видимо, привидения не на вашей стороне...")
        elif user_data.get(chat_id) == "waiting_for_message_11":
            if (message.text.lower()).strip() == "гауптвахта":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Идём дальше!", callback_data="z13"))
                markup.add(types.InlineKeyboardButton(text="Всё! По домам!", callback_data="otkaz"))
                text = (
                    'Действительно, на месте постройки современной Филармонии располагала'
                    'сь гауптвахта – городская тюрьма – сереброплавильного завода. Здание тюрьмы, канцелярии и '
                    'инструментального'
                    ' магазина, расположенных по одной линии Петропавловской улицы, соединялись в те времена глухими '
                    'каменными '
                    'оградами с декоративными портиками.'
                )
                bot.send_message(message.chat.id, text, reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Неправильный ответ! Видимо, привидения не на вашей стороне...")
        elif user_data.get(chat_id) == "waiting_for_message_12":
            if (message.text.lower()).strip() == "большая олонская, малая олонская":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Идём дальше!", callback_data="z14"))
                markup.add(types.InlineKeyboardButton(text="Всё! По домам!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Верно! Привидения на вашей стороне!', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Неправильный ответ! Видимо, привидения не на вашей стороне...")
        elif user_data.get(chat_id) == "waiting_for_message_13":
            if (message.text.lower()).strip() == "38":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Идём дальше!", callback_data="z15"))
                markup.add(types.InlineKeyboardButton(text="Всё! По домам!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Верно! Привидения на вашей стороне!', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Неправильный ответ! Видимо, привидения не на вашей стороне...")
        elif user_data.get(chat_id) == "waiting_for_message_14":
            if (message.text.lower()).strip() == "нагорный парк":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Идём дальше!", callback_data="z16"))
                markup.add(types.InlineKeyboardButton(text="Всё! По домам!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Верно! Привидения на вашей стороне!', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Неправильный ответ! Видимо, привидения не на вашей стороне...")


    try:
        bot.remove_webhook()
        bot.set_webhook(url=WEBHOOK_URL + '/webhook')
        logging.info(f"Webhook установлен на: {WEBHOOK_URL + '/webhook'}")
    except Exception as e:
        logging.error(f"Ошибка при установке вебхука: {e}")

    # Запуск Flask
    port = int(os.environ.get('PORT', 5000))
    logging.info(f"Запуск Flask на порту: {port}")
    app.run(host='0.0.0.0', port=port)