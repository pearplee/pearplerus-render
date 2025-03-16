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
    WEBHOOK_URL = 'https://pearpleeng-render.onrender.com'
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
    except Exception as e:
        logging.exception(f"Ошибка в webhook: {e}")
        return 'error', 500


if __name__ == '__main__':


    @bot.message_handler(commands=['start'])
    def start(message):
        text = (
            'Today you will embark on a dangerous, mysterious adventure through the ancient places of Barnaul, the secrets '
            'of which are carefully guarded by the ghosts of the past. In Barnaul, there are many mystical places where '
            'you can encounter ghosts. The ghosts of Barnaul are quite friendly and very sociable; at night, they like to '
            'open refrigerators in search of something tasty, turn off the Internet, hide socks, and put townspeople into '
            'a state of temporary amnesia.'
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Let's go!", callback_data='v put'))
        markup.add(types.InlineKeyboardButton("I'm fond of adventures!", callback_data='v put'))
        markup.add(types.InlineKeyboardButton("OMG! I'm scared", callback_data='otkaz'))
        bot.send_message(message.chat.id, text, reply_markup=markup)


    # @bot.message_handler(func=lambda message: True)
    # def echo_all(message):
    #     logging.info(f"Получено сообщение от пользователя {message.chat.id}: {message.text}")
    #     try:
    #         bot.reply_to(message, message.text)
    #     except Exception as e:
    #         logging.exception(f"Ошибка в обработчике echo_all: {e}")


    @bot.callback_query_handler(func=lambda call: True)
    def answer(call):
        if call.data == 'v put':
            text = (
                "You will follow the footsteps of Barnaul's ghosts and decipher their messages from the past. Only in this "
                "case will you receive a real letter from the past and be able to calm the mischievous spirits. Are you "
                "ready to embark on a mystical journey?"
            )
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup_inline = types.InlineKeyboardMarkup()
            first_arg = types.InlineKeyboardButton(text="I'm always ready!", callback_data='put2')
            sec_arg = types.InlineKeyboardButton(text="Let's go!", callback_data="put2")
            third_arg = types.InlineKeyboardButton(text="I'm not sure... Maybe go home...", callback_data="otkaz")
            markup_inline.add(first_arg)
            markup_inline.add(sec_arg)
            markup_inline.add(third_arg)
            bot.send_message(call.message.chat.id, text, reply_markup=markup_inline)
        elif call.data == 'otkaz':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, 'Finish it! Someone is afraid of ghosts!')
        elif call.data == "put2":
            text = (
                "Head to the starting "
                "point of our adventure — the oldest square in the city, which for many years "
                "was the administrative and cultural center of the city. The square lost its historical name Sobornaya in 1917. The "
                "main attraction of the square — the Peter and Paul Cathedral — was destroyed in 1935."
                "What is the contemporary name of this square?"
            )
            bot.send_message(call.message.chat.id, text)
            user_data[call.message.chat.id] = "new_1"
        elif call.data == 'n1':
            text = (
                "Take a selfie so that the wooden facade of the former Administration of the Altai Mining District "
                "is visible in the background. This wooden building was built in 1898 in the classical style, with "
                "its love for symmetry, strict geometric forms, and light pilasters dividing the facade."
            )
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text="I did it!", callback_data="z2"))
            bot.send_message(call.message.chat.id, text, reply_markup=markup)
        elif call.data == 'z2':
            text = (
                "You are in the most mystical, most mysterious place of the ancient mining city of Barnaul. Ghosts still "
                "inhabit this place, carefully guarding the secrets of the past. One of the most mysterious stories of "
                "Barnaul is the story of the pharmacist who, according to legends, created the elixir of life. It is said "
                "that together with his young daughter, he indeed became immortal, and their shadows can still be seen on "
                "this street. Decipher the name of the pharmacist, and he will lead you to his workplace.\n"
                "3-8-18-9-19-20-9-1-14   13-9-12-12-5-18."
            )
            bot.send_message(call.message.chat.id, text)
            user_data[call.message.chat.id] = "waiting_for_message_1"
        elif call.data == 'z3':
            text = (
                "Hint: Polzunova St. 42, Mountain Pharmacy"
            )
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text="I'm here'!", callback_data="n2"))
            bot.send_message(call.message.chat.id, text, reply_markup=markup)
        elif call.data == 'n2':
            text = (
                "Christian Miller lived and worked in the building of the "
                "Mountain Pharmacy. Now it houses a tourist center with a museum, restaurant, and shop, but 200 years ago, "
                "medicines were produced here. Barnaul used to be the center of pharmaceutical activity, and medicines "
                "from here were supplied throughout the province. During the reconstruction of the pharmacy in 2010, "
                "mysterious dungeons were discovered here, where various pharmacy bottles and ampoules with an unknown "
                "liquid were hidden. Who knows, maybe this is the elixir of life? You can visit the museum and see for "
                "yourself. The ticket price is 80 rubles."
            )
            bot.send_message(call.message.chat.id, text)
            text = (
                "Now, Christian Miller and his daughter invite you to take a walk along Petropavlovskaya Street. That's "
                "what it used to be called, but the new name of the street is associated with a famous Barnaul inventor, "
                "the developer of the first steam engine.\nQuestion: What is Petropavlovskaya Street called now?"
            )
            bot.send_message(call.message.chat.id, text)
            user_data[call.message.chat.id] = "waiting_for_message_2"
        elif call.data == 'z4':
            text = (
                "The ghosts of the past invite you to solve the next riddle. You can find it near the building of the "
                "Mining Laboratory — the main chemical laboratory of the Altai plants. This is where analyses of the mined "
                "alloys of silver, copper, and gold were conducted before they were sent to St. Petersburg. This stone "
                "building was constructed in 1851 (172 years ago!), and you can recognize it by the five Manchurian walnut "
                "trees planted in front of its facade.\nQuestion: What is currently located in the building of the Mining "
                "Laboratory?"

            )
            bot.send_message(call.message.chat.id, text)
            user_data[call.message.chat.id] = "waiting_for_message_3"
        elif call.data == 'z5':
            text = (
                "You are now at the local history museum, which is celebrating its 200th anniversary in 2023. However, "
                "this site originally housed the mining laboratory, where chemical analyses of mined ore and smelted "
                "metals were conducted. The mining laboratory appeared much later than the construction of the plant "
                "itself, the establishment of which is closely tied to the history of Barnaul's founding.\nQuestion: Which "
                "Russian entrepreneur, the founder of the mining industry in the Urals and Siberia, is associated with the "
                "founding of Barnaul? The square, in the center of which stands a pillar commemorating the 100th "
                "anniversary of mining in Altai, is named after him."
            )
            bot.send_message(call.message.chat.id, text)
            user_data[call.message.chat.id] = "waiting_for_message_4"
        elif call.data == 'z6':
            text = (
                "The most mystical and majestic place in the city is undoubtedly Demidovskaya Square. This is a place "
                "where the shadow of the Demidov curse can still be felt.Akinfiy Demidov never visited Altai, but he is "
                "well-known and respected here, with his image as the founder of the Altai industry carefully preserved in "
                "the memory of generations. It was through his efforts that Barnaul, the second mining city in Russia "
                "(after Yekaterinburg), was founded, becoming a new source of state revenue. Before his death, Akinfiy "
                "Demidov cursed Barnaul and all its inhabitants. What is this curse? And how was it overcome?"
            )
            bot.send_message(call.message.chat.id, text)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Open video", url="https://www.youtube.com/watch?v=5N9eUgfcL90"))
            text = (
                "Listen to "
                "the story of the creation of Demidovskaya Square and answer the question: What helped overcome Demidov's "
                "curse"
            )
            bot.send_message(call.message.chat.id, text, reply_markup=markup)
            user_data[call.message.chat.id] = "waiting_for_message_5"
        elif call.data == 'z7':
            text = (
                "There is a belief: if you walk around the Demidov pillar three times and leave a coin at its base each "
                "time, you may become a wealthy person. Just keep in mind that wealth is understood differently by "
                "everyone! Walk around the pillar three times and look carefully! During the reign of which emperor was "
                "this monument erected to commemorate the 100th anniversary of mining in Altai?\nWrite the name of this "
                "Russian emperor in the chat."
            )
            bot.send_message(call.message.chat.id, text)
            user_data[call.message.chat.id] = "waiting_for_message_6"
        elif call.data == 'z8':
            text = (
                "In 1771, Barnaul received the status of a 'Mining City,' and all buildings and structures constructed here"
                "were for mining purposes. Thus, the Mining School, Mining Hospital, and an almshouse for disabled workers "
                "of the Silver Smelting Plant appeared on Demidovskaya Square. Take a closer look—all the buildings "
                "resemble each other in architecture: two-story, squat, with a solid foundation, likely capable of "
                "withstanding even a strong earthquake. They were all designed by a St. Petersburg architect. No wonder "
                "this place is called a corner of St. Petersburg.\nQuestion: What was located on the site of Demidovskaya "
                "Square 300 years ago? Rumors say that about 700 kilograms of pure silver from the time of Akinfiy Demidov "
                "are hidden there."
            )
            bot.send_message(call.message.chat.id, text)

            user_data[call.message.chat.id] = "waiting_for_message_7"
        elif call.data == 'z9':
            text = (
                "According to legends, silver in Barnaul is not only deep underground but also on the surface. In fact, we"
                "walk on streets paved with silver. Why? In the past, the central streets of Barnaul were paved with slag "
                "left after silver processing. However, due to imperfect technology, particles of the precious metal "
                "remained in the slag.Decipher the message from the shadow of Demidov – this is the original name of the "
                "plant - and Demidov himself will guide you to a unique historical monument built in 1739."
            )
            bot.send_message(call.message.chat.id, text)
            text = (
                "FRSSU VPHOWLQI SODQW"
            )
            bot.send_message(call.message.chat.id, text)
            user_data[call.message.chat.id] = "waiting_for_message_8"
        elif call.data == 'z10':
            text = (
                "Great! You are heading to the territory of the most famous silver smelting plant. In fact, the plant was "
                "initially intended for copper smelting, but after the discovery of silver in Altai ore in 1746, it was "
                "repurposed for silver smelting and became the largest silver smelting plant in Siberia."
            )
            bot.send_message(call.message.chat.id, text)
            text = (
                "Close your eyes… Listen… It is said that the souls of the workers of this plant still cannot leave this "
                "place and wander the plant to this day. In the evenings, the shadow of a man in dark clothing appears "
                "here. Perhaps it is the spirit of Akinfiy Demidov himself, who originally owned these plants. Rumors say "
                "that during his lifetime, Demidov hid many silver coins in the tunnels dug under the plant and is now "
                "trying to protect them from prying eyes.\nQuestion: Which object has long been associated with the "
                "otherworldly? This object has the ability to preserve the energies of people and things around it. It is "
                "said that you can see the reflection of a ghost in it…"
            )
            bot.send_message(call.message.chat.id, text)
            text = (
                "Find this object—it will help you answer Akinfiy Demidov's question: What was located in this building "
                "during the Soviet years?\nCipher: YROTCAFHCTAMLUANRAB"
            )
            bot.send_message(call.message.chat.id, text)
            user_data[call.message.chat.id] = "waiting_for_message_9"
        elif call.data == 'z11':
            text = (
                "The residents of Barnaul have always worked hard and loved to relax. Return to the street of the famous "
                "inventor and head to a beautiful building constructed in the pseudo-Russian style over 100 years ago. The "
                "number of windows on its facade indicates the year of construction. Find out what is currently located in "
                "this building."
            )
            bot.send_message(call.message.chat.id, text)
            user_data[call.message.chat.id] = "waiting_for_message_10"
        elif call.data == 'z12':
            photo = open('img/img_1.png', 'rb')
            text = (
                "Balls, concerts, meetings, and theatrical performances were held here. But even this beautiful building "
                "is not without its secrets and mysteries. Before 1900, a completely different structure stood here. Solve "
                "the rebus—a message from the ghosts of the past—and find out on the foundation of which building the "
                "People's House was built."
            )
            bot.send_photo(call.message.chat.id, photo, caption=text)
            photo.close()
            user_data[call.message.chat.id] = "waiting_for_message_11"
        elif call.data == 'z13':
            text = (
                "Gradually, Barnaul became a major industrial city, attracting settlers from all over the Russian Empire. "
                "Some streets have retained historical geographical names, but many were renamed. For example, Moskovsky "
                "Prospekt became Lenin Prospekt, Tobolskaya Street became Leo Tolstoy Street, Tomskaya Street became "
                "Korolenko Street, and Irkutskaya Street became Pushkin Street. However, one such street has preserved its "
                "historical name. It is one of the oldest streets in the city, located near the banks of the Barnaulka "
                "River. The settlers – well-known metallurgy workers of that time—came here from the Olonets region, from "
                "the Olonka River (an area between Lake Ladoga and Lake Onega in Karelia). Today, there are two streets – "
                "Bolshaya (Big) and Malaya (Small) – that have retained this name. These streets hold secrets of the past "
                "and are in no hurry to part with them. Find these streets on the map, and you will receive a message from "
                "the ghosts.\nWrite the names of the streets in the chat."
            )
            bot.send_message(call.message.chat.id, text)
            user_data[call.message.chat.id] = "waiting_for_message_12"
        elif call.data == 'z14':
            photo = open('img/img_3.jpg', 'rb')
            text = (
                "On Bolshaya Olonskaya Street, where settlers from the Russian North lived during the time of Akinfiy "
                "Demidov, you must find another haunted house. You will learn the number of this house by solving a puzzle."
            )
            bot.send_photo(call.message.chat.id, photo, caption=text)
            photo.close()
            user_data[call.message.chat.id] = "waiting_for_message_13"
        elif call.data == 'z15':
            text = (
                "At this location, at the address Bolshaya Olonskaya 38, stood the house of the merchant Zubov, where the "
                "famous Russian writer Fyodor Mikhailovich Dostoevsky often visited during his Siberian exile. Perhaps "
                "their shadows from the past still linger in this house. Perhaps their shadows can also be found in the "
                "most mystical and ambiguous place in the city. Decipher its name, and boldly set off to meet the ghosts!"
            )
            bot.send_message(call.message.chat.id, text)
            text = (
                "OBHPSOZ QBSL"
            )
            bot.send_message(call.message.chat.id, text)
            user_data[call.message.chat.id] = "waiting_for_message_14"
        elif call.data == 'z16':
            text = (
                "You are at the foot of Nagorny Park—the most ambiguous place in the city. In 1772, it was decided to open "
                "a Nagorny Cemetery here. Over a century and a half, many famous townspeople, scientists, public figures, "
                "merchants, and explorers of Altai were buried here. Climbing the stairs and counting the number of "
                "flights, you will recall and forever remember the year of Barnaul's founding in the 18th century."
            )
            bot.send_message(call.message.chat.id, text)
            text = (
                "Nagorny Park carefully preserves the history of the city. Here lie the eternal rest of the famous Russian "
                "publicist, writer, and explorer of Altai, Nikolai Yadrintsev (streets in Barnaul, Omsk, Novosibirsk, and "
                "Irkutsk are named after him); the physician, outstanding naturalist, geographer, and explorer of Altai, "
                "Friedrich Gebler (a lane in Barnaul and the largest glacier of Mount Belukha are named after him); the "
                "Russian public figure and folk educator Vasily Shtilke; and many others."
            )
            bot.send_message(call.message.chat.id, text)
            text = (
                "Find the restored grave of the mining engineer, inventor-mechanic, and hydraulic engineer Kozma Frolov. "
                "It was he who, from the mid-18th century, headed all gold mining operations in the Urals and Siberia and "
                "supervised work at all Altai mines. At Kozma Frolov's grave, you will receive a message from the ghosts "
                "of the past."
            )
            bot.send_message(call.message.chat.id, text)
            text = (
                '"Dear descendants!\nOn the banks of this remarkable river, we built a wonderful city.We bequeath to you '
                'to preserve and protect the riches of our land.Remember us—we poured our souls into this city.Preserve '
                'history, honor your ancestors!We promise to no longer disturb the residents of the city and will help you '
                'multiply  your wealth!"'
            )
            bot.send_message(call.message.chat.id, text)
            user_data[call.message.chat.id] = "waiting_for_message_15"

        bot.answer_callback_query(call.id)


    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        global user_data
        chat_id = message.chat.id
        if user_data.get(chat_id) == "waiting_for_message_1":
            if (message.text.lower()).strip() == "christian miller":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Let's go!", callback_data="z3"))
                markup.add(types.InlineKeyboardButton(text="We're shrinking! Bye!!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Great! The ghosts are on your side!', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Incorrect! The ghosts don't support you today...")
        elif user_data.get(chat_id) == "new_1":
            if (message.text.lower()).strip() == "sovetov square" or (message.text.lower()).strip() == "sovetov":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Let's go!", callback_data="n1"))
                markup.add(types.InlineKeyboardButton(text="We're shrinking! Bye!!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Great! The ghosts are on your side!', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(message.chat.id, "Incorrect! The ghosts don't support you today...")
        elif user_data.get(chat_id) == "waiting_for_message_2":
            if (message.text.lower()).strip() == "polzunova street" or (message.text.lower()).strip() == "polzunova":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Let's go!", callback_data="z4"))
                markup.add(types.InlineKeyboardButton(text="We're shrinking! Bye!!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Great! The ghosts are on your side!', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(message.chat.id, "Incorrect! The ghosts don't support you today...")
        elif user_data.get(chat_id) == "waiting_for_message_3":
            if (message.text.lower()).strip() == "the altai state local history museum" or \
                    (message.text.lower()).strip() == "taslhm":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Let's go!", callback_data="z5"))
                markup.add(types.InlineKeyboardButton(text="We're shrinking! Bye!!", callback_data="otkaz"))
                text = (
                    'Great! The ghosts are on your side!'
                )
                bot.send_message(message.chat.id, text, reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Incorrect! The ghosts don't support you today...")
        elif user_data.get(chat_id) == "waiting_for_message_4":
            if (message.text.lower()).strip() == "demidov":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Let's go!", callback_data="z6"))
                markup.add(types.InlineKeyboardButton(text="We're shrinking! Bye!!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Great! The ghosts are on your side!', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Incorrect! The ghosts don't support you today...")
        elif user_data.get(chat_id) == "waiting_for_message_5":
            if (message.text.lower()).strip() == "construction demidov pillar on the square" or \
                    (message.text.lower()).strip() == "demidov pillar" or (message.text.lower()).strip() == \
                    "demidov square":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Let's go!", callback_data="z7"))
                markup.add(types.InlineKeyboardButton(text="We're shrinking! Bye!!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Great! The ghosts are on your side!', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Incorrect. Listen again.")
        elif user_data.get(chat_id) == "waiting_for_message_6":
            if (message.text.lower()).strip() == "alexander 1" or (message.text.lower()).strip() == 'alexandr 1' or \
                    (message.text.lower()).strip() == 'alexander the first':
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Let's go!", callback_data="z8"))
                markup.add(types.InlineKeyboardButton(text="We're shrinking! Bye!!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Great! The ghosts are on your side!', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Incorrect! The ghosts don't support you today...")
        elif user_data.get(chat_id) == "waiting_for_message_7":
            if (message.text.lower()).strip() == "artificial lake" or (message.text.lower()).strip() == 'swamp':
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Let's go!", callback_data="z9"))
                markup.add(types.InlineKeyboardButton(text="We're shrinking! Bye!!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Great! The ghosts are on your side!', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Incorrect! The ghosts don't support you today...")
        elif user_data.get(chat_id) == "waiting_for_message_8":
            if (message.text.lower()).strip() == "copper smelting plant":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Let's go!", callback_data="z10"))
                markup.add(types.InlineKeyboardButton(text="We're shrinking! Bye!!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Great! The ghosts are on your side!', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Incorrect! The ghosts don't support you today...")
        elif user_data.get(chat_id) == "waiting_for_message_9":
            if (message.text.lower()).strip() == "barnaul match factory":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Let's go!", callback_data="z11"))
                markup.add(types.InlineKeyboardButton(text="We're shrinking! Bye!!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Great! The ghosts are on your side!', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Incorrect! The ghosts don't support you today...")
        elif user_data.get(chat_id) == "waiting_for_message_10":
            if (message.text.lower()).strip() == "philharmonic" or (message.text.lower()).strip() == "the state \
            philharmonic of the altai territory":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Let's go!", callback_data="z12"))
                markup.add(types.InlineKeyboardButton(text="We're shrinking! Bye!!", callback_data="otkaz"))
                text = (
                    "Correct. The State Philharmonic of the Altai Territory. On December 17, 1900, the People's House was "
                    "opened here, which quickly became the center of cultural and educational life in the city."
                )
                bot.send_message(message.chat.id, text, reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Incorrect! The ghosts don't support you today...")
        elif user_data.get(chat_id) == "waiting_for_message_11":
            if (message.text.lower()).strip() == "guardhouse":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Let's go!", callback_data="z13"))
                markup.add(types.InlineKeyboardButton(text="We're shrinking! Bye!!", callback_data="otkaz"))
                text = (
                    'Indeed, the site of the modern Philharmonic was once occupied by the guardhouse—the city prison of the'
                    'silver smelting plant. The prison building, office, and tool shop, located along Petropavlovskaya '
                    'Street, were connected at that time by solid stone fences with decorative porticos.'
                )
                bot.send_message(message.chat.id, text, reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Incorrect! The ghosts don't support you today...")
        elif user_data.get(chat_id) == "waiting_for_message_12":
            if (message.text.lower()).strip() == "bolshaya olonskaya, malaya olonskaya":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Let's go!", callback_data="z14"))
                markup.add(types.InlineKeyboardButton(text="We're shrinking! Bye!!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Great! The ghosts are on your side!', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Incorrect! The ghosts don't support you today...")
        elif user_data.get(chat_id) == "waiting_for_message_13":
            if (message.text.lower()).strip() == "38":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Let's go!", callback_data="z15"))
                markup.add(types.InlineKeyboardButton(text="We're shrinking! Bye!!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Great! The ghosts are on your side!', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Incorrect! The ghosts don't support you today...")
        elif user_data.get(chat_id) == "waiting_for_message_14":
            if (message.text.lower()).strip() == "nagorny park":
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text="Let's go!", callback_data="z16"))
                markup.add(types.InlineKeyboardButton(text="We're shrinking! Bye!!", callback_data="otkaz"))
                bot.send_message(message.chat.id, 'Great! The ghosts are on your side!', reply_markup=markup)
                user_data[chat_id] = None
            else:
                bot.send_message(chat_id, "Incorrect! The ghosts don't support you today...")


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