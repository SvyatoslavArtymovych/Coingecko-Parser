from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot_token, chat_id

bot = TeleBot(bot_token)


template = """<code>№ {0}
Name: {1}
Date: {2}
</code>
"""


def send_message(no, name, date, link):
    link_kb = InlineKeyboardMarkup()
    skin_link = InlineKeyboardButton(text='Link', url=link)
    link_kb.add(skin_link)

    bot.send_message(chat_id,
                     template.format(no, name, date),
                     parse_mode='html',
                     disable_web_page_preview=True,
                     reply_markup=link_kb)
