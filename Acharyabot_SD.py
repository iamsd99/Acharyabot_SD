#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# A library that provides an Acharya interface to the Telegram Bot API
# Shubham Dumbre(SD) <shubhamdumbre99@gmail.com>
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].

from threading import Thread
import time

from telegram import Bot, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, CommandHandler, CallbackQueryHandler
from telegram.ext.filters import Filters
from pymongo import MongoClient

custom_keyboard = [['/About_Acharya_Institutions - About Us,Our Vision & Mission.'],
                   ['/Trustees - Our Support.'],
                   ['/Institutes - Brief About Our Institutes.'],
                   ['/Admissions - Details About Admissions.'],
                   ['/Contact_Us - Get In Touch.'],
                   ['/Gurukul_Hostel - Our Hostel Facility.'],
                   ['/Chat_bot - Details About Our Chat Bot.']]
reply_markup = ReplyKeyboardMarkup(custom_keyboard)
reply_markup1 = ReplyKeyboardRemove()


#########################
# All Classes Goes Here #
#########################

# Creating class for all operation related to bot.
class DataBase:
    def __init__(self, database='users', table='users_id'):
        self.client = MongoClient()
        self.db = self.client[database]  # 'users'
        self.table = self.db[table]  # 'users_id'

    def check_user(self, chat_id=None, username=None):
        if chat_id:
            try:
                details = self.table.find_one({'_id': chat_id})
                if details:
                    return True, details
                else:
                    return False, "User is not present in the database."
            except Exception as e:
                return False, e
        elif username:
            user = self.table.find_one({'username': username})
            if user:
                return True, user['_id']
            else:
                return False, "User not Present"

    def add_user(self, chat_id, name, username):
        try:
            self.table.insert_one({'_id': chat_id, 'name': name, 'username': username})
            return True,
        except Exception as e:
            return False, e

    def update_user(self, chat_id, *parameters):
        pass

    def remove_user(self, chat_id):
        try:
            self.table.remove({'_id': chat_id})
            return True,
        except Exception as e:
            return False, e

    def find(self, broadcast=False):
        if not broadcast:
            users = "\n\n".join(
                [str(
                    "Chat id = " + str(a['_id']) + "\nUsername = " + str(a['username'] + "\nName = " + str(a['name']))
                ) for a in self.table.find()])
            # print(users)
            return users
        else:
            chat_ids = list()
            for user in self.table.find():
                chat_id = user['_id']
                chat_ids.append(chat_id)
            return chat_ids


##############
# Admin Area #
##############

# /start threaded admin handler
def threaded_admin_start(bot, update):
    custom_keyboard1 = [['/start - To start the bot.'], ['/users - To get details about Users.']]
    rm = ReplyKeyboardMarkup(custom_keyboard1)
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="""
Control Panel 
/start - Normal start command to bot.
/users - to get details about users.
/msg - Send Message to particular user.
        e.g /msg <username> <Message>
/broadcast - Send Message Message to all.
        e.g /broadcast <Message>
""", reply_markup=rm)


# /start received by admin of this bot.
def admin_start(bot: Bot, update: Update):
    start_admin = Thread(target=threaded_admin_start, args=(bot, update))
    start_admin.start()


# Send List of Users to Admin.
def send_users(bot: Bot):
    bot.send_message(chat_id=619236446, text=db.find())


# Send Message to Particular User.
def send_msg(bot: Bot, update: Update):
    username = update.message.text.split()[1]
    msg = ' '.join(update.message.text.split()[2:])
    try:
        chat_id = int(username)
        result = db.check_user(chat_id=chat_id)
    except Exception as e:
        print(e)
        result = db.check_user(username=username)
    if result[0]:
        bot.send_message(chat_id=619236446, text="Message sent to: %s" % username)
        chat_id = result[1]["_id"]
        bot.send_message(chat_id=chat_id, text=msg)
    else:
        bot.send_message(chat_id=619236446, text=result[1])


# Broadcast message to all users.
def broadcast_msg(bot: Bot, update: Update):
    msg = " ".join(update.message.text.split()[1:])
    chat_ids = db.find(broadcast=True)
    for chat_id in chat_ids:
        bot.send_message(chat_id=chat_id, text=msg)


# When admin send command then this function will handle commands.
def admin(bot: Bot, update: Update):
    text = update.message.text
    if text.startswith("/users"):
        Thread(target=send_users, args=(bot,)).start()
    elif text.startswith("/msg"):
        Thread(target=send_msg, args=(bot, update)).start()
    elif text.startswith("/broadcast"):
        Thread(target=broadcast_msg, args=(bot, update)).start()

    # print("welcome Admin")


############
# services #
############

# callback handler for fly button.
def button(bot: Bot, update: Update) -> None:
    query = update.callback_query
    if query.data == 'Our Vision':
        bot.send_message(chat_id=query.message.chat_id, text="""
VISION
To establish GVAIET as the premier Institute, in calculating all desire for constant achievements and pursuit of perfection, while emphasizing building in a strength, intellect and character to meet all the challenges with courage and fortitude, yet tempered by empathy for the environment and weaker section of society.

""", parse_mode='Markdown')
    elif query.data == 'Our Mission':
        bot.send_message(chat_id=query.message.chat_id, text="""
MISSION
To establish GVAIET as the premier Institute, in calculating all desire for constant achievements and pursuit of perfection, while emphasizing building in a strength, intellect and character to meet all the challenges with courage and fortitude, yet tempered by empathy for the environment and weaker section of society
""")
    elif query.data == 'Trustees':
        bot.send_message(chat_id=query.message.chat_id, text="""
OUR TRUSTEES

""")
    elif query.data == 'Our Support':
        bot.send_message(chat_id=query.message.chat_id, text="""
OUR SUPPORT
""")
    elif query.data == 'Institutes':
        bot.send_message(chat_id=query.message.chat_id, text="""
Polytechnic | G.V.Acharya Polytechnic

COURSE    INTAKE    DURATION
Computer Engineering    60    03 Years

Civil Engineering    120*    03 Years

Electronics & Telecommunication    60    03 Years

Information Technology    60    03 Years

Mechanical Engineering    120    03 Years


Engineering | G.V.Acharya.Institute of Engineering & Technology


COURSE    INTAKE    DURATION

Computer Engineering    60    03 Years

Civil Engineering    60    04 Years

Electronics & Telecommunication    60    04 Years

Mechanical Engineering    60    04 Years

Mechanical Engineering (Second Shift)    60    04 Years


MBA | S.A.V. Acharya Institute of Management Studies

COURSE    INTAKE    DURATION

Master of Management Studies    180    2 Years

Namrata Acharya Junior College

The College is Affiliated to Mumbai Unversity

Namrata Acharya English School

The School is affiliated to Maharashtra State Board of Secondary and Higher Secondary Education

""")


# chat bot
def chat_bot(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="Now You're Talking To Our ChatBot.", reply_markup=reply_markup1)


# Give details About Acharya Institutions.
def about_acharya_institutions(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    keyboard = [[InlineKeyboardButton("Vision", callback_data='Our Vision'),
                 InlineKeyboardButton("Mission", callback_data='Our Mission')]]
    wk = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=chat_id,
                     text="The prestigious Leela Education Society was established in 2006 by Prof. Manjunath V. Acharya, his family and friends. It is a registered trust which was a culmination of sorts for the shared dreams and long-held beliefs of the Trustees as embodied in the Vision, yet a harbinger of a new beginning. The ‘society of teachers’ then started in right earnest the process of establishing their first Institution. The immense goodwill in the academic circles saw the coming together of Professors, Teachers and Students- all volunteering, chipping in and giving it their all. The dynamic leadership and team building ability of Prof. Acharya along with the tireless efforts of everyone involved has today seen the birth of the first of, as everyone believes, many institutions of the Society.\nSelect One: ", reply_markup=wk)

# Give details about Trustees.
def trustees(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    keyboard = [[InlineKeyboardButton("Trustees", callback_data='Trustees'),
                 InlineKeyboardButton("Support", callback_data='Our Support')]]
    imk = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=chat_id, text="""
Know More About Our Support Pillars: """, reply_markup=imk)


# Give details about Institutes.
def institutes(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    keyboard = [[InlineKeyboardButton("Institutes", callback_data='Institutes')]]
    imk = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=chat_id, text="""
        More About Our Institutions: """, reply_markup=imk)


# Give details about Admissions.
def admissions(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="""
        Do Visit Our Official Website & Contact Us To Get Current Details.
""")


# Give details about Contact Us.
def contact_us(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="""
        Contact Us
        
        VEERACHARYA TECHNICAL EDUCATION CAMPUS
        Opp Shelu Suburban Railway Station.
        Taluka-Karjat,Mumbai - 410101
        leelaeducationsociety@yahoo.co.in
        (+91) 9820078574 / 9322315476
        
        
        Reach Easily
        
        1. 05 Minutes Walkin from Shelu Station (Central Line)
        2. Connected to Badlapur - Karjat National Highway
        3. Bus Facility From Navi Mumbai(30-40 Minutes Travelling)
""")


# Give details about Gurukul Hostel.
def gurukul_hostel(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="""
        Cup of noodles and a movie on deck, a wall painted with memories and random books on a neat shelf, it's all about that hostel life...
        • Located at the foothills of Matheran.
        • 100% pollution free campus.
        • Quality mess and dining hall that keeps in mind hygiene and optimum dietary requirements, while also adding to the    culinary delight of our hostel inmates at a reasonable price.
""")


########################
# first message to bot #
########################

# Normal start to for students and staff.
def start(bot: Bot, update: Update):
    Thread(target=threaded_start, args=(bot, update)).start()


def threaded_start(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    name = update.message.from_user.first_name
    try:
        assert update.message.from_user.username is not None, "Username is Not present"
        username = update.message.from_user.username.lower()
    except Exception as e:
        print(e)
        username = name + str(chat_id)
    print(username)
    print(time.asctime(time.localtime(time.time())))
    details = db.check_user(chat_id)
    if not details[0]:
        result = db.add_user(chat_id, name, username)
        if not result[0]:
            print("Unable to add user", result[1])
    bot.send_message(chat_id=chat_id, text="""This is Acharya Bot.
/start - Subscribe to Our Bot.
/About_Acharya_Institutions - About Us,Our Vision & Mission.
/Trustees - Our Support.
/Institutes - Brief About Our Institutes.
/Admissions - Details About Admissions.
/Contact_Us - Get In Touch.
/Gurukul_Hostel - Our Hostel Facility.
/Chat_bot - Details About Our Chat Bot.

### Developer Zone ###
Bot Created by Shubham Dumbre(SD) - Shivam Gupta(pyshivam).
Contact us 
SD:- 9820286399
pyshivam:- 8424951219
T h a n k Y o u !
""", reply_markup=reply_markup)


# Kick Start to bot.
def main():
    updater = Updater('682793295:AAG2OMqee_GlDQKlOOZKFmwhPIgFWmTqzBU')

    # if admin message the show admin's control panel menu.
    updater.dispatcher.add_handler(CommandHandler("cp", admin_start, filters=Filters.user(username='pyshivam')))

    # Normal Start
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("About_Acharya_Institutions", about_acharya_institutions))
    updater.dispatcher.add_handler(CommandHandler("Trustees", trustees))
    updater.dispatcher.add_handler(CommandHandler("Institutes", institutes))
    updater.dispatcher.add_handler(CommandHandler("Admissions", admissions))
    updater.dispatcher.add_handler(CommandHandler("Contact_Us", contact_us))
    updater.dispatcher.add_handler(CommandHandler("Gurukul_Hostel", gurukul_hostel))
    updater.dispatcher.add_handler(CommandHandler("Chat_bot", chat_bot))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(MessageHandler(Filters.chat(chat_id=619236446), admin))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, chat_bot))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    # Connection  to DataBase
    db = DataBase()

    # Kicking start to Program.
    main()

#682793295:AAG2OMqee_GlDQKlOOZKFmwhPIgFWmTqzBU
